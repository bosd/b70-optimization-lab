import os, sys, time, torch, importlib.util
from vllm.platforms import current_platform
import vllm._custom_ops
sys.path.insert(0, '/tmp/claude-1000/-home-steve/28337632-6e4e-40d8-9fc8-81a2b28c7aa2/scratchpad')
spec = importlib.util.spec_from_file_location('hc_ops_triton_xpu', '/tmp/claude-1000/-home-steve/28337632-6e4e-40d8-9fc8-81a2b28c7aa2/scratchpad/hc_ops_triton_xpu.py'); T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
from vllm.models.qwen4_exp.amd.ops import hc as R
device = torch.device("xpu:0"); torch.xpu.set_device(device)
HC, D, RANK = 4, 2560, 320; g = torch.Generator(device=device).manual_seed(3)
res = torch.randn(1, HC*D, generator=g, device=device, dtype=torch.bfloat16); blk = torch.randn(1, D, generator=g, device=device, dtype=torch.bfloat16)
inj = torch.randn(1, HC, generator=g, device=device, dtype=torch.bfloat16); w = torch.randn(HC*D, generator=g, device=device, dtype=torch.bfloat16)*0.1
gate = torch.randn(1, HC*D, generator=g, device=device, dtype=torch.bfloat16); lora = torch.randn(1, RANK, generator=g, device=device, dtype=torch.bfloat16)
def cmp(label, a, b):
    a=a.float(); b=b.float(); print(f"{label}: bit-identical={torch.equal(a,b)} max|diff|={(a-b).abs().max().item():.3e} mismatches={(a!=b).sum().item()}/{a.numel()}")
o_r, y_r = R.hc_combine_norm(res, blk, inj, w, 1e-6, HC); o_t, y_t = T.hc_combine_norm(res, blk, inj, w, 1e-6, HC)
cmp("combine out", o_r, o_t); cmp("combine_norm y", y_r, y_t)
cmp("silu", R.hc_silu(lora, HC), T.hc_silu(lora, HC)); cmp("gate_mix", R.hc_gate_mix(res, gate, HC), T.hc_gate_mix(res, gate, HC))
def bench(label, fn, n=96):
    for _ in range(8): fn()
    torch.xpu.synchronize(); G = torch.xpu.XPUGraph(); st = torch.xpu.Stream()
    with torch.xpu.stream(st):
        for _ in range(4): fn()
        torch.xpu.synchronize()
        with torch.xpu.graph(G, stream=st):
            for _ in range(n): fn()
    torch.xpu.synchronize()
    for _ in range(3): G.replay()
    torch.xpu.synchronize(); t0=time.perf_counter()
    for _ in range(20): G.replay()
    torch.xpu.synchronize(); t1=time.perf_counter(); print(f"GRAPH {label}: {1e6*(t1-t0)/20/n:.1f} us per call ({1e3*(t1-t0)/20:.3f} ms per {n})")
for name, mod in (("torch-ref", R), ("triton-xpu", T)):
    bench(f"{name} combine_norm", lambda: mod.hc_combine_norm(res, blk, inj, w, 1e-6, HC))
    bench(f"{name} gate_mix", lambda: mod.hc_gate_mix(res, gate, HC))
    bench(f"{name} silu", lambda: mod.hc_silu(lora, HC))
