import os, torch
from vllm.config import VllmConfig, set_current_vllm_config
from vllm.model_executor.layers.layernorm import RMSNorm
dev, dtype, hidden, eps = "xpu", torch.float16, 4096, 1e-6
with set_current_vllm_config(VllmConfig()):
    norm = RMSNorm(hidden, eps=eps).to(dev).to(dtype)
torch.manual_seed(0)
with torch.no_grad():
    norm.weight.copy_(torch.randn(hidden, device=dev, dtype=dtype) * 0.02 + 1.0)
w = norm.weight.data

def rms_torch(x, acc):
    xa = x.to(acc)
    return (xa * torch.rsqrt(xa.pow(2).mean(-1, keepdim=True) + eps) * w.to(acc)).to(x.dtype)

print(f"{'rows':>5} {'exact rows':>12} {'max |diff|':>12} {'max ulp':>9}")
for m in (1, 16, 64, 128):
    tot_exact = 0; tot = 0; mx = 0.0; mulp = 0
    for sd in range(5):
        torch.manual_seed(sd)
        x = torch.randn(m, hidden, device=dev, dtype=dtype)
        with torch.no_grad():
            a = norm(x.clone()); b = rms_torch(x, torch.float16)
        d = (a.float() - b.float()).abs()
        mx = max(mx, float(d.max()))
        ai = a.view(torch.int16).to(torch.int32); bi = b.view(torch.int16).to(torch.int32)
        mulp = max(mulp, int((ai - bi).abs().max()))
        tot_exact += int((a.view(torch.int16) == b.view(torch.int16)).all(dim=-1).sum()); tot += m
    print(f"{m:>5} {tot_exact:>5}/{tot:<6} {mx:>12.3e} {mulp:>9}")
