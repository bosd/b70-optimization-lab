"""Offline graph-replay timing of one hyper-connection mix (Qwen3.8 Flash-Next: HC=4, D=2560, lora 320, merged down N=336) at M=1 on one B70."""
import os, time, torch, torch.nn.functional as F
from vllm.platforms import current_platform
import vllm._custom_ops
from vllm.models.qwen4_exp.amd.ops.hc import hc_combine_norm, hc_silu, hc_gate_mix
device = torch.device("xpu:0"); torch.xpu.set_device(device)
M = int(os.getenv("Q38_BENCH_M", "1")); HC, D, R, PAD = 4, 2560, 320, 12; NDOWN = R + HC + PAD
g = torch.Generator(device=device).manual_seed(1)
NMIX = 96  # two mixes per layer, 48 layers
W_down = [torch.randn(NDOWN, HC * D, generator=g, device=device, dtype=torch.bfloat16) * 0.02 for _ in range(NMIX)]
W_up = [torch.randn(HC * D, R, generator=g, device=device, dtype=torch.bfloat16) * 0.02 for _ in range(NMIX)]
norm_w = torch.randn(HC * D, generator=g, device=device, dtype=torch.bfloat16) * 0.1
residual = torch.randn(M, HC * D, generator=g, device=device, dtype=torch.bfloat16)
block_out = torch.randn(M, D, generator=g, device=device, dtype=torch.bfloat16)
inj = torch.randn(M, HC, generator=g, device=device, dtype=torch.bfloat16)
def full_mix(i):
    hs, xn = hc_combine_norm(residual, block_out, inj, norm_w, 1e-6, HC)
    dj = F.linear(xn, W_down[i]); lora, injection, _ = dj.split([R, HC, PAD], dim=-1)
    lora = hc_silu(lora, HC); gate = F.linear(lora, W_up[i]); return hc_gate_mix(xn, gate, HC)
def gemms_only(i):
    dj = F.linear(residual, W_down[i]); return F.linear(dj[:, :R], W_up[i])
def glue_only(i):
    hs, xn = hc_combine_norm(residual, block_out, inj, norm_w, 1e-6, HC)
    lora = hc_silu(xn[:, :R], HC); return hc_gate_mix(xn, residual, HC)
def bench(label, fn):
    for i in range(8): fn(i)
    torch.xpu.synchronize()
    G = torch.xpu.XPUGraph(); stream = torch.xpu.Stream()
    with torch.xpu.stream(stream):
        for i in range(4): fn(i)
        torch.xpu.synchronize()
        with torch.xpu.graph(G, stream=stream):
            for i in range(NMIX): fn(i)
    torch.xpu.synchronize()
    for _ in range(3): G.replay()
    torch.xpu.synchronize(); t0 = time.perf_counter(); reps = 20
    for _ in range(reps): G.replay()
    torch.xpu.synchronize(); t1 = time.perf_counter()
    per = 1e3 * (t1 - t0) / reps
    print(f"GRAPH {label} M={M}: {per:.3f} ms per step of {NMIX} mixes = {1e3*per/NMIX:.1f} us per mix", flush=True)
bytes_per_mix = (W_down[0].numel() + W_up[0].numel()) * 2
print(f"weights per mix {bytes_per_mix/2**20:.2f} MiB; per step {NMIX*bytes_per_mix/2**30:.2f} GiB -> {NMIX*bytes_per_mix/500e9*1e3:.2f} ms at 500 GB/s")
bench("full mix (combine_norm + down + silu + up + gate_mix)", full_mix)
bench("gemms only (down + up)", gemms_only)
bench("glue only (combine_norm + silu + gate_mix)", glue_only)
def cn_only(i):
    return hc_combine_norm(residual, block_out, inj, norm_w, 1e-6, HC)
def silu_only(i):
    return hc_silu(residual[:, :R], HC)
def gm_only(i):
    return hc_gate_mix(residual, residual, HC)
def torch_ref_glue(i):
    from vllm.models.qwen4_exp.amd.ops.hc import _hc_combine_norm_torch, _hc_silu_torch, _hc_gate_mix_torch
    hs, xn = _hc_combine_norm_torch(residual, block_out, inj, norm_w, 1e-6, HC)
    lora = _hc_silu_torch(xn[:, :R], HC); return _hc_gate_mix_torch(xn, residual, HC)
bench("combine_norm only", cn_only)
bench("silu only", silu_only)
bench("gate_mix only", gm_only)
bench("torch reference glue (eager ops captured)", torch_ref_glue)
