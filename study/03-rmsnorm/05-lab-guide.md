# 05 · Code Lab — `lab_rmsnorm.py`

## Run (~3 sec)

```bash
uv run study/03-rmsnorm/lab_rmsnorm.py
```

## Expected output (aur matlab)

```
Exp 1  x = [100.0, 1.0, 2.0, -3.0]  rms = 50.03
       haath se  x / rms = [1.999, 0.02, 0.04, -0.06]
       RMSNorm(x)        = [1.999, 0.02, 0.04, -0.06]
       norm ke baad rms  = 1.000  (hamesha ~1)
```
→ Reading 02 wala haath ka calculation aur code, dono match karte hain.

```
Exp 2  RMSNorm(x * 1000) == RMSNorm(x)? True
```
→ **Scale-invariant.** Input kitna bhi bada ho, output same rehta hai.

```
Exp 3  layer                     1         12         24         48
       bina norm               1.7        682   3.54e+05   1.52e+11
       RMSNorm ke saath       1.67       5.17       6.88       9.94
```
→ **Is lab ka main result.** 48 random layers + residual:
- Bina norm: 15,200 crore (1.52 × 10¹¹) tak explode 💥
- Pre-norm ke saath: ~10 tak, slow aur controlled growth (Reading 03 ka "honest baat" wala point)

```
Exp 4  LayerNorm(v) = [-1.342, -0.447, 0.447, 1.342]  (mean hata diya)
       RMSNorm(v)   = [0.758, 0.91, 1.061, 1.213]  (sirf scale kiya)
```
→ Dono ka fark (Reading 03).

```
Exp 5  gamma=[2,1,1,0] -> [3.997, 0.02, 0.04, -0.0]  (dim 0 bada, dim 3 band)
```
→ γ ek "equalizer" hai (Reading 04).

## Tumhara kaam (15 min)

1. **TODO (a):** Exp 3 me `std=0.1` ko `0.01` kar do. Bina norm ke kya hota hai? Ab explode hua ya nahi? **Socho:** Iska matlab init (shuruaati weights ka size) bhi stability me role play karta hai. Repo `std=0.02` use karta hai.
2. **TODO (b):** `eps=0` karke `RMSNorm(4, eps=0)(torch.zeros(4))` chalao. `nan` aata hai kyunki `0 / 0`. Isliye ε hamesha hota hai.
3. **Bonus:** Exp 3 me pre-norm ki jagah **post-norm** try karo: `h = norm(h + layer(h))`. Size kaisa rehta hai? (Hint: har layer ke baad exactly ~1.)

## Repo ke asli model pe check

```bash
cd sources/repo && uv run python -c "
from glm53_flash.model import *
m = GLM53FlashFromScratch(ModelConfig())
n = [x for x in m.modules() if isinstance(x, RMSNorm)]
print(len(n), 'RMSNorms,', sum(x.weight.numel() for x in n), 'params')"
```
Expected: `25 RMSNorms, 4800 params`
