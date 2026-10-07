"""Lab 3 — RMSNorm: numbers ko control me rakhna.

Run:  uv run study/03-rmsnorm/lab_rmsnorm.py
"""

import torch
import torch.nn as nn

torch.manual_seed(0)


class RMSNorm(nn.Module):
    """Same logic as sources/repo/glm53_flash/model.py (copied for study)."""

    def __init__(self, dim: int, eps: float = 1e-6):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(dim))  # gamma: seekhne wala scale
        self.eps = eps

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        scale = torch.rsqrt(x.float().pow(2).mean(-1, keepdim=True) + self.eps)
        return (x.float() * scale).to(x.dtype) * self.weight


# --- Experiment 1: haath se RMSNorm ------------------------------------------
x = torch.tensor([100.0, 1.0, 2.0, -3.0])
rms = x.pow(2).mean().sqrt()
print(f"Exp 1  x = {x.tolist()}  rms = {rms:.2f}")
print(f"       haath se  x / rms = {[round(v, 3) for v in (x / rms).tolist()]}")
print(f"       RMSNorm(x)        = {[round(v, 3) for v in RMSNorm(4)(x).tolist()]}")
y = RMSNorm(4)(x)
print(f"       norm ke baad rms  = {y.pow(2).mean().sqrt():.3f}  (hamesha ~1)")

# --- Experiment 2: scale-invariance — x ko 1000 se multiply karo -------------
print("Exp 2  RMSNorm(x * 1000) == RMSNorm(x)?",
      torch.allclose(RMSNorm(4)(x * 1000), RMSNorm(4)(x), atol=1e-5))

# --- Experiment 3: 48 layers ka deep stack — norm ke bina vs saath -----------
# Har layer ek random Linear hai. Real model me bhi 12 blocks x (attention + MoE) hain.
DIM, DEPTH = 192, 48
layers = [nn.Linear(DIM, DIM, bias=False) for _ in range(DEPTH)]
for layer in layers:
    nn.init.normal_(layer.weight, std=0.1)  # thoda bada init -> explode hoga
norms = [RMSNorm(DIM) for _ in range(DEPTH)]


def run(use_norm: bool) -> list[float]:
    h = torch.randn(1, DIM)
    sizes = []
    with torch.no_grad():
        for layer, norm in zip(layers, norms):
            update = layer(norm(h) if use_norm else h)
            h = h + update  # residual connection (pre-norm style)
            sizes.append(h.pow(2).mean().sqrt().item())
    return sizes


plain, normed = run(False), run(True)
print(f"Exp 3  {'layer':<17}", "  ".join(f"{i:>9}" for i in (1, 12, 24, 48)))
print(f"       {'bina norm':<17}", "  ".join(f"{plain[i - 1]:>9.3g}" for i in (1, 12, 24, 48)))
print(f"       {'RMSNorm ke saath':<17}", "  ".join(f"{normed[i - 1]:>9.3g}" for i in (1, 12, 24, 48)))

# --- Experiment 4: RMSNorm vs LayerNorm --------------------------------------
v = torch.tensor([5.0, 6.0, 7.0, 8.0])
ln = nn.LayerNorm(4, elementwise_affine=False)
print(f"Exp 4  LayerNorm(v) = {[round(a, 3) for a in ln(v).tolist()]}  (mean hata diya)")
print(f"       RMSNorm(v)   = {[round(a, 3) for a in RMSNorm(4)(v).tolist()]}  (sirf scale kiya)")

# --- Experiment 5: gamma (weight) kya karta hai ------------------------------
n = RMSNorm(4)
with torch.no_grad():
    n.weight.copy_(torch.tensor([2.0, 1.0, 1.0, 0.0]))
print(f"Exp 5  gamma=[2,1,1,0] -> {[round(a, 3) for a in n(x).tolist()]}  (dim 0 bada, dim 3 band)")

# TODO (tumhara kaam):
#  a) Exp 3 me std=0.1 ko 0.01 kar do. Ab bina norm ke kya hota hai? Kya ab bhi explode hota hai?
#  b) eps=0 karke RMSNorm(torch.zeros(4)) chalao. Kya aata hai aur eps kyun zaroori hai?
