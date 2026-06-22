#!/usr/bin/env python3
"""Train a small EAGLE-1 draft body from Qwen 3.6 target hidden-state samples.

This intentionally exports the same minimal checkpoint layout produced by
create-qwen36-eagle1-smoke-checkpoint.py: draft body only, no embed_tokens and
no lm_head. vLLM shares those target modules at serve time.
"""

from __future__ import annotations

import argparse
import glob
import json
import math
import os
import shutil
from dataclasses import asdict, dataclass
from typing import Any

import torch
import torch.nn as nn
import torch.nn.functional as F
from safetensors.torch import load_file, save_file
from torch.utils.data import DataLoader, Dataset


@dataclass
class DraftShape:
    hidden_size: int = 2048
    intermediate_size: int = 4096
    num_hidden_layers: int = 1
    num_attention_heads: int = 16
    num_key_value_heads: int = 2
    head_dim: int = 128
    vocab_size: int = 248320
    max_position_embeddings: int = 262144
    rope_theta: float = 10000000.0
    rms_norm_eps: float = 1e-6


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset-dir",
        required=True,
        action="append",
        help="Dataset directory. May be passed multiple times.",
    )
    parser.add_argument("--target-model", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--init-checkpoint", default="")
    parser.add_argument("--num-layers", type=int, default=1)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--max-len", type=int, default=256)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--train-dtype", default="float32",
                        choices=("float32", "bfloat16"))
    parser.add_argument("--export-dtype", default="bfloat16",
                        choices=("float32", "float16", "bfloat16"))
    parser.add_argument("--feature-loss-weight", type=float, default=1.0)
    parser.add_argument("--token-loss-weight", type=float, default=0.1)
    parser.add_argument("--grad-clip", type=float, default=1.0)
    parser.add_argument("--log-every", type=int, default=1)
    parser.add_argument("--shuffle-seed", type=int, default=0)
    return parser.parse_args()


def dtype_from_name(name: str) -> torch.dtype:
    return {
        "float32": torch.float32,
        "float16": torch.float16,
        "bfloat16": torch.bfloat16,
    }[name]


def choose_device(name: str) -> torch.device:
    if name != "auto":
        return torch.device(name)
    if hasattr(torch, "xpu") and torch.xpu.is_available():
        return torch.device("xpu:0")
    if torch.cuda.is_available():
        return torch.device("cuda:0")
    return torch.device("cpu")


def torch_load(path: str) -> dict[str, Any]:
    try:
        return torch.load(path, map_location="cpu", weights_only=False)
    except TypeError:
        return torch.load(path, map_location="cpu")


class EagleDataset(Dataset):
    def __init__(self, dataset_dirs: list[str], max_len: int) -> None:
        self.paths: list[str] = []
        for dataset_dir in dataset_dirs:
            self.paths.extend(sorted(glob.glob(os.path.join(dataset_dir, "*.pt"))))
        if not self.paths:
            raise FileNotFoundError(f"No .pt samples found in {dataset_dirs}")
        self.max_len = max_len

    def __len__(self) -> int:
        return len(self.paths)

    def __getitem__(self, index: int) -> dict[str, torch.Tensor]:
        data = torch_load(self.paths[index])
        hidden = data["hidden_state"][: self.max_len].to(torch.float32)
        input_ids = data["input_ids"][: self.max_len].to(torch.long)
        if "positions" in data:
            positions = data["positions"][: self.max_len].to(torch.long)
        else:
            positions = torch.arange(hidden.shape[0], dtype=torch.long)
        loss_mask = data["loss_mask"][: self.max_len].to(torch.float32)
        if "sampled_next_token_ids" in data:
            next_ids = data["sampled_next_token_ids"][: self.max_len].to(torch.long)
        else:
            next_ids = torch.empty_like(input_ids)
            next_ids[:-1] = input_ids[1:]
            next_ids[-1] = 0

        target = torch.zeros_like(hidden)
        target[:-1] = hidden[1:]
        draft_input_ids = next_ids.clone()
        target_token_ids = torch.zeros_like(input_ids)
        target_token_ids[:-1] = next_ids[1:]
        loss_mask = loss_mask.clone()
        if loss_mask.numel():
            loss_mask[-1] = 0
        return {
            "hidden": hidden,
            "draft_input_ids": draft_input_ids,
            "positions": positions,
            "target": target,
            "target_token_ids": target_token_ids,
            "loss_mask": loss_mask,
        }


def collate(samples: list[dict[str, torch.Tensor]]) -> dict[str, torch.Tensor]:
    max_len = max(s["hidden"].shape[0] for s in samples)
    hidden_size = samples[0]["hidden"].shape[-1]
    batch = {
        "hidden": torch.zeros(len(samples), max_len, hidden_size, dtype=torch.float32),
        "draft_input_ids": torch.zeros(len(samples), max_len, dtype=torch.long),
        "positions": torch.zeros(len(samples), max_len, dtype=torch.long),
        "target": torch.zeros(len(samples), max_len, hidden_size, dtype=torch.float32),
        "target_token_ids": torch.zeros(len(samples), max_len, dtype=torch.long),
        "loss_mask": torch.zeros(len(samples), max_len, dtype=torch.float32),
    }
    for i, sample in enumerate(samples):
        n = sample["hidden"].shape[0]
        for key in batch:
            batch[key][i, :n] = sample[key]
    return batch


class RMSNorm(nn.Module):
    def __init__(self, hidden_size: int, eps: float) -> None:
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.eps = eps

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        variance = x.pow(2).mean(dim=-1, keepdim=True)
        return self.weight * x * torch.rsqrt(variance + self.eps)


def fused_add_rms_norm(
    x: torch.Tensor,
    residual: torch.Tensor,
    norm: RMSNorm,
) -> tuple[torch.Tensor, torch.Tensor]:
    residual = (x.to(torch.float32) + residual.to(torch.float32)).to(x.dtype)
    return norm(residual), residual


def apply_neox_rope(x: torch.Tensor, cos: torch.Tensor,
                    sin: torch.Tensor) -> torch.Tensor:
    x1, x2 = torch.chunk(x, 2, dim=-1)
    return torch.cat((x1 * cos - x2 * sin, x2 * cos + x1 * sin), dim=-1)


class EagleDraftLayer(nn.Module):
    def __init__(
        self,
        shape: DraftShape,
        disable_input_layernorm: bool,
    ) -> None:
        super().__init__()
        self.shape = shape
        self.disable_input_layernorm = disable_input_layernorm
        h = shape.hidden_size
        i = shape.intermediate_size
        self.input_layernorm = (
            nn.Identity() if disable_input_layernorm
            else RMSNorm(h, shape.rms_norm_eps)
        )
        self.q_proj = nn.Linear(h, shape.num_attention_heads * shape.head_dim,
                                bias=False)
        self.k_proj = nn.Linear(h, shape.num_key_value_heads * shape.head_dim,
                                bias=False)
        self.v_proj = nn.Linear(h, shape.num_key_value_heads * shape.head_dim,
                                bias=False)
        self.o_proj = nn.Linear(shape.num_attention_heads * shape.head_dim, h,
                                bias=False)
        self.post_attention_layernorm = RMSNorm(h, shape.rms_norm_eps)
        self.gate_proj = nn.Linear(h, i, bias=False)
        self.up_proj = nn.Linear(h, i, bias=False)
        self.down_proj = nn.Linear(i, h, bias=False)

        inv_freq = 1.0 / (
            shape.rope_theta
            ** (torch.arange(0, shape.head_dim, 2, dtype=torch.float32) /
                shape.head_dim)
        )
        self.register_buffer("inv_freq", inv_freq, persistent=False)

    def _apply_rope(
        self,
        q: torch.Tensor,
        k: torch.Tensor,
        positions: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        if positions.dim() == 1:
            positions = positions.unsqueeze(0)
        freqs = positions.to(torch.float32).unsqueeze(-1) * self.inv_freq.to(
            positions.device).view(1, 1, -1)
        cos = freqs.cos().unsqueeze(1)
        sin = freqs.sin().unsqueeze(1)
        cos = cos.to(q.dtype)
        sin = sin.to(q.dtype)
        return apply_neox_rope(q, cos, sin), apply_neox_rope(k, cos, sin)

    def forward(
        self,
        hidden: torch.Tensor,
        residual: torch.Tensor | None,
        positions: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        bsz, seq_len, _ = hidden.shape
        if positions is None:
            positions = torch.arange(seq_len, device=hidden.device,
                                     dtype=torch.long).expand(bsz, seq_len)
        else:
            positions = positions.to(device=hidden.device, dtype=torch.long)
        if residual is None:
            residual = hidden
            x = self.input_layernorm(hidden)
        else:
            if isinstance(self.input_layernorm, nn.Identity):
                residual = hidden + residual
                x = hidden
            else:
                x, residual = fused_add_rms_norm(
                    hidden, residual, self.input_layernorm)

        q = self.q_proj(x).view(
            bsz, seq_len, self.shape.num_attention_heads, self.shape.head_dim)
        k = self.k_proj(x).view(
            bsz, seq_len, self.shape.num_key_value_heads, self.shape.head_dim)
        v = self.v_proj(x).view(
            bsz, seq_len, self.shape.num_key_value_heads, self.shape.head_dim)
        q = q.transpose(1, 2)
        k = k.transpose(1, 2)
        v = v.transpose(1, 2)
        q, k = self._apply_rope(q, k, positions)
        if self.shape.num_key_value_heads != self.shape.num_attention_heads:
            repeat = self.shape.num_attention_heads // self.shape.num_key_value_heads
            k = k.repeat_interleave(repeat, dim=1)
            v = v.repeat_interleave(repeat, dim=1)
        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(
            self.shape.head_dim)
        mask = torch.triu(
            torch.ones(seq_len, seq_len, device=x.device, dtype=torch.bool),
            diagonal=1,
        )
        scores = scores.masked_fill(mask, float("-inf"))
        attn = torch.softmax(scores, dim=-1)
        x = torch.matmul(attn, v).transpose(1, 2).contiguous().view(
            bsz, seq_len, self.shape.num_attention_heads * self.shape.head_dim)
        x = self.o_proj(x)
        x, residual = fused_add_rms_norm(
            x, residual, self.post_attention_layernorm)
        x = self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x))
        return x, residual


class Eagle1Draft(nn.Module):
    def __init__(
        self,
        shape: DraftShape,
        embed_weight: torch.Tensor,
        lm_head_weight: torch.Tensor,
    ) -> None:
        super().__init__()
        self.shape = shape
        h = shape.hidden_size
        self.register_buffer("embed_weight", embed_weight, persistent=False)
        self.register_buffer("lm_head_weight", lm_head_weight, persistent=False)
        self.fc = nn.Linear(2 * h, h, bias=False)
        self.layers = nn.ModuleList(
            EagleDraftLayer(shape, disable_input_layernorm=(i == 0))
            for i in range(shape.num_hidden_layers)
        )

    def forward(
        self,
        hidden: torch.Tensor,
        draft_input_ids: torch.Tensor,
        positions: torch.Tensor | None = None,
    ) -> torch.Tensor:
        embeds = F.embedding(draft_input_ids, self.embed_weight).to(hidden.dtype)
        x = self.fc(torch.cat([embeds, hidden], dim=-1))
        residual = None
        for layer in self.layers:
            x, residual = layer(x, residual, positions)
        return x + residual

    def logits(self, hidden: torch.Tensor) -> torch.Tensor:
        return F.linear(hidden, self.lm_head_weight)

    def export_state(self, dtype: torch.dtype) -> dict[str, torch.Tensor]:
        state = {
            "fc.weight": self.fc.weight.detach().cpu().to(dtype),
        }
        for i, layer in enumerate(self.layers):
            prefix = f"layers.{i}"
            if not layer.disable_input_layernorm:
                state[f"{prefix}.input_layernorm.weight"] = (
                    layer.input_layernorm.weight.detach().cpu().to(dtype)
                )
            state.update({
                f"{prefix}.self_attn.q_proj.weight":
                    layer.q_proj.weight.detach().cpu().to(dtype),
                f"{prefix}.self_attn.k_proj.weight":
                    layer.k_proj.weight.detach().cpu().to(dtype),
                f"{prefix}.self_attn.v_proj.weight":
                    layer.v_proj.weight.detach().cpu().to(dtype),
                f"{prefix}.self_attn.o_proj.weight":
                    layer.o_proj.weight.detach().cpu().to(dtype),
                f"{prefix}.post_attention_layernorm.weight":
                    layer.post_attention_layernorm.weight.detach().cpu().to(dtype),
                f"{prefix}.mlp.gate_proj.weight":
                    layer.gate_proj.weight.detach().cpu().to(dtype),
                f"{prefix}.mlp.up_proj.weight":
                    layer.up_proj.weight.detach().cpu().to(dtype),
                f"{prefix}.mlp.down_proj.weight":
                    layer.down_proj.weight.detach().cpu().to(dtype),
            })
        return state


def load_target_shared_weights(target_model: str) -> tuple[torch.Tensor, torch.Tensor]:
    index_path = os.path.join(target_model, "model.safetensors.index.json")
    with open(index_path, "r", encoding="utf-8") as f:
        index = json.load(f)
    weight_map = index["weight_map"]
    embed_name = "model.language_model.embed_tokens.weight"
    head_name = "lm_head.weight"
    shard_names = {weight_map[embed_name], weight_map[head_name]}
    loaded: dict[str, torch.Tensor] = {}
    for shard in shard_names:
        tensors = load_file(os.path.join(target_model, shard), device="cpu")
        for name in (embed_name, head_name):
            if name in tensors:
                loaded[name] = tensors[name]
    return loaded[embed_name], loaded[head_name]


def write_config(out_dir: str, shape: DraftShape, export_dtype: str) -> None:
    config = {
        "architectures": ["LlamaForCausalLM"],
        "model_type": "llama",
        "vocab_size": shape.vocab_size,
        "hidden_size": shape.hidden_size,
        "intermediate_size": shape.intermediate_size,
        "num_hidden_layers": shape.num_hidden_layers,
        "num_attention_heads": shape.num_attention_heads,
        "num_key_value_heads": shape.num_key_value_heads,
        "head_dim": shape.head_dim,
        "hidden_act": "silu",
        "max_position_embeddings": shape.max_position_embeddings,
        "rms_norm_eps": shape.rms_norm_eps,
        "rope_theta": shape.rope_theta,
        "attention_bias": False,
        "attention_dropout": 0.0,
        "tie_word_embeddings": False,
        "bos_token_id": 248044,
        "eos_token_id": 248044,
        "pad_token_id": None,
        "torch_dtype": export_dtype,
        "dtype": export_dtype,
        "draft_vocab_size": shape.vocab_size,
    }
    generation_config = {
        "bos_token_id": 248044,
        "eos_token_id": 248044,
        "pad_token_id": None,
    }
    with open(os.path.join(out_dir, "config.json"), "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, sort_keys=True)
        f.write("\n")
    with open(
        os.path.join(out_dir, "generation_config.json"),
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(generation_config, f, indent=2, sort_keys=True)
        f.write("\n")


def load_init(model: Eagle1Draft, init_dir: str) -> None:
    if not init_dir:
        return
    path = os.path.join(init_dir, "model.safetensors")
    if not os.path.exists(path):
        return
    weights = load_file(path, device="cpu")
    with torch.no_grad():
        mapping: dict[str, torch.nn.Parameter] = {
            "fc.weight": model.fc.weight,
        }
        for i, layer in enumerate(model.layers):
            prefix = f"layers.{i}"
            if not layer.disable_input_layernorm:
                mapping[f"{prefix}.input_layernorm.weight"] = (
                    layer.input_layernorm.weight)
            mapping.update({
                f"{prefix}.self_attn.q_proj.weight": layer.q_proj.weight,
                f"{prefix}.self_attn.k_proj.weight": layer.k_proj.weight,
                f"{prefix}.self_attn.v_proj.weight": layer.v_proj.weight,
                f"{prefix}.self_attn.o_proj.weight": layer.o_proj.weight,
                f"{prefix}.post_attention_layernorm.weight":
                    layer.post_attention_layernorm.weight,
                f"{prefix}.mlp.gate_proj.weight": layer.gate_proj.weight,
                f"{prefix}.mlp.up_proj.weight": layer.up_proj.weight,
                f"{prefix}.mlp.down_proj.weight": layer.down_proj.weight,
            })
        for name, param in mapping.items():
            if name in weights:
                param.copy_(weights[name].to(param.dtype))


def main() -> int:
    args = parse_args()
    shape = DraftShape()
    if args.num_layers < 1:
        raise ValueError("--num-layers must be at least 1")
    shape.num_hidden_layers = args.num_layers
    device = choose_device(args.device)
    train_dtype = dtype_from_name(args.train_dtype)
    export_dtype = dtype_from_name(args.export_dtype)

    os.makedirs(args.out_dir, exist_ok=True)
    embed_weight, lm_head_weight = load_target_shared_weights(args.target_model)
    embed_weight = embed_weight.to(device=device, dtype=train_dtype)
    lm_head_weight = lm_head_weight.to(device=device, dtype=train_dtype)

    model = Eagle1Draft(shape, embed_weight, lm_head_weight).to(
        device=device, dtype=train_dtype)
    load_init(model, args.init_checkpoint)
    model.train()

    dataset = EagleDataset(args.dataset_dir, args.max_len)
    generator = torch.Generator()
    generator.manual_seed(args.shuffle_seed)
    loader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        shuffle=True,
        collate_fn=collate,
        generator=generator,
    )
    optim = torch.optim.AdamW(model.parameters(), lr=args.lr)
    metrics: list[dict[str, float | int]] = []

    step = 0
    for epoch in range(args.epochs):
        for batch in loader:
            step += 1
            hidden = batch["hidden"].to(device=device, dtype=train_dtype)
            draft_input_ids = batch["draft_input_ids"].to(device=device)
            positions = batch["positions"].to(device=device)
            target = batch["target"].to(device=device, dtype=train_dtype)
            target_token_ids = batch["target_token_ids"].to(device=device)
            loss_mask = batch["loss_mask"].to(device=device, dtype=train_dtype)

            pred = model(hidden, draft_input_ids, positions)
            mask = loss_mask > 0
            feature_loss = F.smooth_l1_loss(pred[mask], target[mask])
            target_ids = target_token_ids[mask]
            logits = model.logits(pred[mask])
            token_loss = F.cross_entropy(logits.float(), target_ids)
            loss = (
                args.feature_loss_weight * feature_loss
                + args.token_loss_weight * token_loss
            )

            optim.zero_grad(set_to_none=True)
            loss.backward()
            if args.grad_clip > 0:
                torch.nn.utils.clip_grad_norm_(model.parameters(), args.grad_clip)
            optim.step()

            with torch.no_grad():
                acc1 = (logits.argmax(dim=-1) == target_ids).float().mean()
                top3 = logits.topk(3, dim=-1).indices
                acc3 = (top3 == target_ids[:, None]).any(dim=-1).float().mean()
            row = {
                "epoch": epoch + 1,
                "step": step,
                "loss": float(loss.detach().cpu()),
                "feature_loss": float(feature_loss.detach().cpu()),
                "token_loss": float(token_loss.detach().cpu()),
                "top1": float(acc1.detach().cpu()),
                "top3": float(acc3.detach().cpu()),
                "tokens": int(mask.sum().detach().cpu()),
            }
            metrics.append(row)
            if args.log_every and step % args.log_every == 0:
                print(json.dumps(row, sort_keys=True), flush=True)

    save_file(model.export_state(export_dtype),
              os.path.join(args.out_dir, "model.safetensors"))
    write_config(args.out_dir, shape, args.export_dtype)
    summary = {
        "dataset_dir": args.dataset_dir,
        "dataset_samples": len(dataset),
        "target_model": args.target_model,
        "init_checkpoint": args.init_checkpoint,
        "out_dir": args.out_dir,
        "device": str(device),
        "train_dtype": args.train_dtype,
        "export_dtype": args.export_dtype,
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "lr": args.lr,
        "max_len": args.max_len,
        "num_layers": args.num_layers,
        "shuffle_seed": args.shuffle_seed,
        "shape": asdict(shape),
        "final_metrics": metrics[-1] if metrics else {},
    }
    with open(os.path.join(args.out_dir, "training_metrics.json"), "w",
              encoding="utf-8") as f:
        json.dump({"summary": summary, "steps": metrics}, f, indent=2,
                  sort_keys=True)
        f.write("\n")
    with open(os.path.join(args.out_dir, "summary.json"), "w",
              encoding="utf-8") as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")
    src_script = os.path.abspath(__file__)
    try:
        shutil.copy2(src_script, os.path.join(args.out_dir, os.path.basename(src_script)))
    except OSError:
        pass
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
