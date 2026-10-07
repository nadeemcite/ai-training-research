<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 03 — RMSNorm: numbers ko control me rakhna](README.md) › Reading 2 / 6
<!-- /nav:top -->

# 02 · Definitions — RMS, epsilon, gamma

## Definitions

| Term | Matlab |
|---|---|
| **RMS (Root Mean Square)** | Vector ka "typical size": har number ka square lo, average lo, fir square root lo |
| **Normalize** | Vector ko uske RMS se divide karo, taaki naya RMS = 1 ho |
| **ε (epsilon)** | Bahut chhota number (`1e-6`). Agar vector zero ho to divide-by-zero se bachata hai |
| **γ (gamma) / weight** | Har dimension ka ek **seekhne wala** scale. Shuru me sab 1 hote hain |
| **Scale-invariant** | Input ko 1000× karo, output wahi rahega |

## Formula

```
RMS(x) = sqrt( (x₁² + x₂² + ... + x_d²) / d )

RMSNorm(x) = ( x / sqrt(mean(x²) + ε) ) × γ
```

## Haath se ek example (lab Exp 1)

`x = [100, 1, 2, -3]`

| Step | Calculation | Result |
|---|---|---|
| 1. Squares | 10000, 1, 4, 9 | |
| 2. Mean | 10014 / 4 | 2503.5 |
| 3. Square root | √2503.5 | **50.03** |
| 4. Divide | x / 50.03 | `[1.999, 0.02, 0.04, -0.06]` |
| 5. × γ (sab 1) | koi change nahi | `[1.999, 0.02, 0.04, -0.06]` |

Check karo: naye vector ka RMS = **1.000** ✅

## Repo ka code (poora)

```python
class RMSNorm(nn.Module):
    def __init__(self, dim, eps=1e-6):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(dim))   # γ
        self.eps = eps

    def forward(self, x):
        scale = torch.rsqrt(x.float().pow(2).mean(-1, keepdim=True) + self.eps)
        return (x.float() * scale).to(x.dtype) * self.weight
```

Line by line:
- `x.pow(2).mean(-1)`: squares ka mean, last dimension (192) pe
- `torch.rsqrt(...)`: **r**eciprocal **sqrt** = `1 / sqrt(...)`. Divide se multiply sasta hai
- `x.float()`: calculation hamesha float32 me hoti hai, chahe model bfloat16 me chal raha ho. Isse precision bachti hai
- `* self.weight`: γ lagao

## γ kyun chahiye?

Agar har vector ka RMS zabardasti 1 kar diya, to model ki aazaadi chhin jaati hai. γ ke through model seekh sakta hai ki "dimension 5 important hai, use 3× bada rakho" aur "dimension 90 bekaar hai, use 0 kar do". Lab Exp 5 me ye dikhta hai.

Params: har RMSNorm me sirf **192** (ek γ per dimension).

---
📁 `model.py` lines 33–41

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [01 · Concept — Numbers ko "explode" hone se bachana](01-concept.md) | 📚 [Topic 03 overview](README.md) | [03 · Practical — Pre-norm, aur LayerNorm se fark](03-practical-pre-norm.md) ➡️ |
<!-- /nav:bottom -->
