import sys, torch, importlib.util
from vllm.platforms import current_platform
import vllm._custom_ops
spec = importlib.util.spec_from_file_location('hc_ops_triton_xpu', '/tmp/claude-1000/-home-steve/28337632-6e4e-40d8-9fc8-81a2b28c7aa2/scratchpad/hc_ops_triton_xpu.py'); T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
from vllm.models.qwen4_exp.amd.ops import hc as R
device = torch.device("xpu:0"); torch.xpu.set_device(device)
HC, D, RANK = 4, 2560, 320
stats = {}
def check(name, a, b):
    ok = torch.equal(a, b); s = stats.setdefault(name, [0, 0, 0.0]); s[0] += 1; s[1] += (0 if ok else 1)
    if not ok: s[2] = max(s[2], (a.float() - b.float()).abs().max().item())
for seed in range(150):
    g = torch.Generator(device=device).manual_seed(1000 + seed)
    M = [1, 2, 4, 7][seed % 4]; scale = [0.5, 1.0, 4.0, 30.0][(seed // 4) % 4]
    res = (torch.randn(M, HC*D, generator=g, device=device) * scale).to(torch.bfloat16)
    blk = (torch.randn(M, D, generator=g, device=device) * scale).to(torch.bfloat16)
    inj = (torch.randn(M, HC, generator=g, device=device) * 3).to(torch.bfloat16)
    w_shared = (torch.randn(D, generator=g, device=device) * 0.2).to(torch.bfloat16)
    w_branch = (torch.randn(HC*D, generator=g, device=device) * 0.2).to(torch.bfloat16)
    gate = (torch.randn(M, HC*D, generator=g, device=device) * 2).to(torch.bfloat16)
    lora = (torch.randn(M, RANK, generator=g, device=device) * scale).to(torch.bfloat16)
    for wn, w in (("shared", w_shared), ("branch", w_branch)):
        o_r, y_r = R.hc_combine_norm(res, blk, inj, w, 1e-6, HC); o_t, y_t = T.hc_combine_norm(res, blk, inj, w, 1e-6, HC)
        check(f"combine_norm.out[{wn}]", o_r, o_t); check(f"combine_norm.y[{wn}]", y_r, y_t)
        check(f"grouped_rmsnorm[{wn}]", R.grouped_gemma_rmsnorm(res, w, 1e-6, HC), T.grouped_gemma_rmsnorm(res, w, 1e-6, HC))
    check("silu", R.hc_silu(lora, HC), T.hc_silu(lora, HC))
    check("gate_mix", R.hc_gate_mix(res, gate, HC), T.hc_gate_mix(res, gate, HC))
    check("combine", R.hc_combine(res, blk, inj, HC), T.hc_combine(res, blk, inj, HC))
for k, (n, bad, mx) in stats.items(): print(f"{k:28s} cases={n:4d} mismatching={bad:3d} max|diff|={mx:.3e}")
