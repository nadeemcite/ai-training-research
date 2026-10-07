# 05 · Code Lab — `lab_moe.py`

## Run (~12 sec, CPU pe)

```bash
uv run study/07-mixture-of-experts/lab_moe.py
```

## Expected output (aur matlab)

```
Exp 1  token -> chune gaye experts (weights)
       token 0: E2 (0.57), E3 (0.43)  + shared
       token 1: E6 (0.55), E3 (0.45)  + shared
       ...
       output shape (1, 5, 192) = input shape  ✓
```
→ Router har token ke liye alag 2 experts chunta hai (Reading 02).

```
Exp 2  usage = [0.2, 0.1, 0.2, 0.1, 0.2, 0.1, 0.1, 0.0]  sum = 1.0
```
→ 5 tokens × 2 slots = 10 slots. E8 ko koi nahi mila, aur sum = 1 (repo test yahi check karta hai).

```
Exp 3  ek expert = 221,184 params
       ek MoE layer: total 1,990,656  |  har token ke liye active 663,552  (33%)
       12 layers:    total 23,887,872  |  active 7,962,624
       GLM-5.3 (8 of 288 + shared) me ek token ~3.1% experts use karta hai
```
→ Total vs active (Reading 03).

```
Exp 4  balanced usage  -> balance loss 0.000
       collapsed (sirf E1, E2) -> balance loss 0.375
```
→ Repo ka formula (Reading 04).

```
Exp 5  balance_weight=0.0  seed=1  usage=[0.1, 0.15, 0.08, 0.08, 0.23, 0.08, 0.19, 0.08]  min=0.08  max=0.23
Exp 5  balance_weight=0.0  seed=2  usage=[0.19, 0.19, 0.11, 0.09, 0.12, 0.09, 0.12, 0.09]  min=0.09  max=0.19
Exp 5  balance_weight=1.0  seed=1  usage=[0.13, 0.14, 0.11, 0.1, 0.15, 0.11, 0.15, 0.12]  min=0.10  max=0.15
Exp 5  balance_weight=1.0  seed=2  usage=[0.15, 0.14, 0.13, 0.11, 0.12, 0.11, 0.13, 0.11]  min=0.11  max=0.15
```
→ Default setting (`3 * mu`) me imbalance **mild** hai (max 0.23 vs ideal 0.125), aur balance loss ise even kar deta hai. Dono seeds pe same trend hai.

**Honest note:** Maine pehle sirf thoda bias add karke collapse dikhane ki koshish ki thi, lekin wo nahi hua. Toy setups me collapse hamesha apne aap nahi hota. Isliye TODO (b) me common direction ko strong karoge, aur tab asli collapse dikhega.

## Tumhara kaam (25 min)

1. **TODO (a):** `TOP_K = 1` aur `TOP_K = 4` karke Exp 3 dekho. Active % kaise badla? Quality vs cost ka trade-off socho.
2. **TODO (b):** Exp 5 me `3 * mu` ko `8 * mu` kar do (dono jagah: `data` aur `target`). Bina balance loss ke kitne experts **dead (0.00)** hue? Balance loss ke saath? *(Maine chala ke dekha: bina balance ke 2 seeds pe 2–3 experts 0% pe, aur balance ke saath sab ~12%.)*
3. **TODO (c):** Repo ka test chalao:
   ```bash
   cd sources/repo && uv run python -m pytest tests/test_lab.py -k usage -q
   ```
4. **Bug hunt:** Reading 04 ka bug khud verify karo:
   ```bash
   cd sources/repo && uv run python -c "
   import torch; from glm53_flash.model import *
   m = GLM53FlashFromScratch(ModelConfig()); _, usage = m(torch.randint(4, 260, (2, 32)))
   print('usage.requires_grad =', usage.requires_grad)"
   ```
   Expected: `False`. Ab socho: fix kaise karoge? (Hint: `SparseMoE.forward` me `torch.softmax(logits, -1).mean(0)` bhi return karo.)
