<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 04 — RoPE: model ko position kaise pata chalti hai](README.md) › Reading 5 / 6
<!-- /nav:top -->

# 05 · Code Lab — `lab_rope.py`

## Run (~3 sec)

```bash
uv run study/04-rope-position/lab_rope.py
```

## Expected output (aur matlab)

```
Exp 1  pos 0: [1, 0] -> [+1.000, +0.000]   length = 1.000
Exp 1  pos 1: [1, 0] -> [+0.540, +0.841]   length = 1.000
Exp 1  pos 2: [1, 0] -> [-0.416, +0.909]   length = 1.000
Exp 1  pos 3: [1, 0] -> [-0.990, +0.141]   length = 1.000
```
→ Same vector, har position pe aur zyada ghooma. Length same rahi (Reading 02).

```
Exp 2  rotation ke baad lengths same? True
```
→ 50 random 32-dim vectors pe bhi length nahi badli.

```
Exp 3  query pos    5, key pos    3 (doori 2) -> score +0.1496
Exp 3  query pos  105, key pos  103 (doori 2) -> score +0.1496
Exp 3  query pos 1005, key pos 1003 (doori 2) -> score +0.1495
Exp 3  query pos    5, key pos    1 (doori 4) -> score -2.3298
```
→ **Is lab ka main result.** Score sirf doori pe depend karta hai (Reading 03).

```
Exp 4  pair 0  : har token pe 1.0000 rad  (second ki sui, tez)
       pair 8  : har token pe 0.0100 rad
       pair 15 : har token pe 0.000178 rad  (ghante ki sui, dheemi)
       pair 15 ko ek chakkar (2pi) lagane me ~35,333 tokens
```
→ Frequencies (Reading 02, 04).

```
Exp 5  rope=False  shuffle ke baad bhi output same? True
Exp 5  rope=True   shuffle ke baad bhi output same? False
```
→ **Order-blindness ka proof.** Bina RoPE ke pehle 5 tokens shuffle karne se kuch nahi badla, yaani `x - 1` = `1 - x`. RoPE ke saath order matter karta hai ✅ (Reading 01)

## Tumhara kaam (20 min)

1. **TODO (a):** `score(50, 0)`, `score(250, 200)` aur `score(50, 49)` print karo. Pehle do same kyun hain?
2. **TODO (b):** Exp 4 me base `10000` ko `500000` kar do. Pair 15 ka chakkar ab kitne tokens ka hai? Lambe context (128k) ke liye ye kyun better hai?
3. **Socho:** Exp 1 me pos 7 (≈ 2π + 0.72) aur pos 1 kaafi paas-paas dikhenge, kyunki pair 0 ghoom ke wapas aa gaya. Model phir bhi position 1 aur 7 me fark kaise karta hai? (Hint: baaki 15 pairs.)

## Repo ke asli function pe check

```bash
cd sources/repo && uv run python -c "
import torch; from glm53_flash.model import apply_rope
q = torch.randn(1, 10, 6, 32); rq, rk = apply_rope(q, q)
print('shape same:', rq.shape == q.shape, '| pos 0 unchanged:', torch.allclose(rq[:, 0], q[:, 0]))"
```
Expected: `shape same: True | pos 0 unchanged: True` (position 0 pe angle 0 hai, to koi rotation nahi)

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [04 · Released GLM ka twist (NoPE) + Real-life](04-glm-nope-and-real-life.md) | 📚 [Topic 04 overview](README.md) | [06 · Recap + Quiz](06-recap-quiz.md) ➡️ |
<!-- /nav:bottom -->
