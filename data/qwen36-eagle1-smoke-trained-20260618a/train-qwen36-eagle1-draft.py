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
    num_attention_heads: int = 16
    num_key_value_heads: int = 2
    head_dim: int = 128
    vocab_size: int = 248320
    max_position_embeddings: int = 262144
    rope_theta: float = 10000000.0
    rms_norm_eps: float = 1e-6


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-dir", required=True)
    parser.add_argument("--target-model", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--init-checkpoint", default="")
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
    def __init__(self, dataset_dir: str, max_len: int) -> None:
        self.paths = sorted(glob.glob(os.path.join(dataset_dir, "*.pt")))
        if not self.paths:
            raise FileNotFoundError(f"No .pt samples found in {dataset_dir}")
        self.max_len = max_len

    def __len__(self) -> int:
        return len(self.paths)

    def __getitem__(self, index: int) -> dict[str, torch.Tensor]:
        data = torch_load(self.paths[index])
        hidden = data["hidden_state"][: self.max_len].to(torch.float32)
        input_ids = data["input_ids"][: self.max_len].to(torch.long)
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
        loss_mask = loss_mask.clone()
        if loss_mask.numel():
            loss_mask[-1] = 0
        return {
            "hidden": hidden,
            "draft_input_ids": draft_input_ids,
            "target": target,
            "loss_mask": loss_mask,
        }


def collate(samples: list[dict[str, torch.Tensor]]) -> dict[str, torch.Tensor]:
    max_len = max(s["hidden"].shape[0] for s in samples)
    hidden_size = samples[0]["hidden"].shape[-1]
    batch = {
        "hidden": torch.zeros(len(samples), max_len, hidden_size, dtype=torch.float32),
        "draft_input_ids": torch.zeros(len(samples), max_len, dtype=torch.long),
        "target": torch.zeros(len(samples), max_len, hidden_size, dtype=torch.float32),
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


def rotate_half(x: torch.Tensor) -> torch.Tensor:
    x1 = x[..., ::2]
    x2 = x[..., 1::2]
    out = torch.empty_like(x)
    out[..., ::2] = -x2
    out[..., 1::2] = x1
    return out


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
        i = shape.intermediate_size
        self.register_buffer("embed_weight", embed_weight, persistent=False)
        self.register_buffer("lm_head_weight", lm_head_weight, persistent=False)
        self.fc = nn.Linear(2 * h, h, bias=False)
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
        freqs = torch.einsum("t,d->td", positions.to(torch.float32),
                             self.inv_freq.to(positions.device))
        cos = freqs.cos().repeat_interleave(2, dim=-1)[None, None, :, :]
        sin = freqs.sin().repeat_interleave(2, dim=-1)[None, None, :, :]
        cos = cos.to(q.dtype)
        sin = sin.to(q.dtype)
        return (q * cos + rotate_half(q) * sin,
                k * cos + rotate_half(k) * sin)

    def forward(
        self,
        hidden: torch.Tensor,
        draft_input_ids: torch.Tensor,
    ) -> torch.Tensor:
        bsz, seq_len, _ = hidden.shape
        embeds = F.embedding(draft_input_ids, self.embed_weight).to(hidden.dtype)
        x = self.fc(torch.cat([embeds, hidden], dim=-1))
        residual = x

        q = self.q_proj(x).view(
            bsz, seq_len, self.shape.num_attention_heads, self.shape.head_dim)
        k = self.k_proj(x).view(
            bsz, seq_len, self.shape.num_key_value_heads, self.shape.head_dim)
        v = self.v_proj(x).view(
            bsz, seq_len, self.shape.num_key_value_heads, self.shape.head_dim)
        q = q.transpose(1, 2)
        k = k.transpose(1, 2)
        v = v.transpose(1, 2)
        positions = torch.arange(seq_len, device=x.device, dtype=torch.long)
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
        residual = residual + x
        x = self.post_attention_layernorm(residual)
        x = self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x))
        return x + residual

    def logits(self, hidden: torch.Tensor) -> torch.Tensor:
        return F.linear(hidden, self.lm_head_weight)

    def export_state(self, dtype: torch.dtype) -> dict[str, torch.Tensor]:
        return {
            "fc.weight": self.fc.weight.detach().cpu().to(dtype),
            "layers.0.self_attn.q_proj.weight":
                self.q_proj.weight.detach().cpu().to(dtype),
            "layers.0.self_attn.k_proj.weight":
                self.k_proj.weight.detach().cpu().to(dtype),
            "layers.0.self_attn.v_proj.weight":
                self.v_proj.weight.detach().cpu().to(dtype),
            "layers.0.self_attn.o_proj.weight":
                self.o_proj.weight.detach().cpu().to(dtype),
            "layers.0.post_attention_layernorm.weight":
                self.post_attention_layernorm.weight.detach().cpu().to(dtype),
            "layers.0.mlp.gate_proj.weight":
                self.gate_proj.weight.detach().cpu().to(dtype),
            "layers.0.mlp.up_proj.weight":
                self.up_proj.weight.detach().cpu().to(dtype),
            "layers.0.mlp.down_proj.weight":
                self.down_proj.weight.detach().cpu().to(dtype),
        }


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
        "num_hidden_layers": 1,
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
        mapping = {
            "fc.weight": model.fc.weight,
            "layers.0.self_attn.q_proj.weight": model.q_proj.weight,
            "layers.0.self_attn.k_proj.weight": model.k_proj.weight,
            "layers.0.self_attn.v_proj.weight": model.v_proj.weight,
            "layers.0.self_attn.o_proj.weight": model.o_proj.weight,
            "layers.0.post_attention_layernorm.weight":
                model.post_attention_layernorm.weight,
            "layers.0.mlp.gate_proj.weight": model.gate_proj.weight,
            "layers.0.mlp.up_proj.weight": model.up_proj.weight,
            "layers.0.mlp.down_proj.weight": model.down_proj.weight,
        }
        for name, param in mapping.items():
            if name in weights:
                param.copy_(weights[name].to(param.dtype))


def main() -> int:
    args = parse_args()
    shape = DraftShape()
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
    loader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        shuffle=True,
        collate_fn=collate,
    )
    optim = torch.optim.AdamW(model.parameters(), lr=args.lr)
    metrics: list[dict[str, float | int]] = []

    step = 0
    for epoch in range(args.epochs):
        for batch in loader:
            step += 1
            hidden = batch["hidden"].to(device=device, dtype=train_dtype)
            draft_input_ids = batch["draft_input_ids"].to(device=device)
            target = batch["target"].to(device=device, dtype=train_dtype)
            loss_mask = batch["loss_mask"].to(device=device, dtype=train_dtype)

            pred = model(hidden, draft_input_ids)
            mask = loss_mask > 0
            feature_loss = F.smooth_l1_loss(pred[mask], target[mask])
            with torch.no_grad():
                target_logits = model.logits(target[mask])
                target_ids = target_logits.argmax(dim=-1)
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
