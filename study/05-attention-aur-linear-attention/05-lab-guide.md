<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 05 — Attention basics → Linear attention](README.md) › Reading 5 / 6
<!-- /nav:top -->

# 05 · Code Lab — `lab_linear_attention.py`

## Run (~3 sec)

```bash
uv run study/05-attention-aur-linear-attention/lab_linear_attention.py
```

## Lab me teen functions hain

| Function | Kya hai |
|---|---|
| `softmax_attention` | Classic causal attention. `[T×T]` matrix banata hai |
| `linear_attention_parallel` | **Repo jaisa** cumsum version |
| `linear_attention_recurrent` | Token-by-token loop with fixed `S`, aur optional `decay` |

## Expected output (aur matlab)

```
Exp 1  causal attention weights (row = query token, col = key token):
       1.00  0.00  0.00  0.00  0.00
       0.81  0.19  0.00  0.00  0.00
       ...
```
→ Upar-right triangle 0 hai (causal mask), aur har row ka sum 1 hai (Reading 01).

```
Exp 2  parallel == recurrent?  True
```
→ Training (cumsum) aur generation (loop), ek hi math (Reading 03).

```
Exp 3  context T   softmax scores T*T     linear state d*d
             192               36,864             1,024
       1,000,000    1,000,000,000,000             1,024
```
→ T² vs fixed state (Reading 02).

```
Exp 4  pairs  softmax-recall  linear-recall
           4           100%            50%
          16           100%            19%
          64           100%             2%
```
→ Compression ki keemat (Reading 04).

```
Exp 5  decay=0.8, 32 pairs, kaunse wapas mile? (0 = sabse purana, 31 = sabse naya)
       ······························✓✓
```
→ Decay se recency bias (Reading 04).

```
Exp 6  pairs  raw outer-product memory recall (no phi)
           4           100%
          16           100%
          64            83%
```
→ Asli bottleneck φ = elu+1 hai (Reading 04).

## Tumhara kaam (25 min)

1. **TODO (a):** `d = 128` kar do. Exp 4 (linear) aur Exp 6 (raw) me se kiska recall sudhra?
   *(Maine check kiya: Exp 6 ka 64-pair recall 100% ho jaata hai, lekin Exp 4 lagbhag same rehta hai. Socho kyun. Hint: bada d raw memory ko zyada "slots" deta hai, lekin elu+1 ke positive keys phir bhi overlap karte hain.)*
2. **TODO (b):** Exp 5 me `decay = 0.95` aur `0.5` try karo. Kitne recent pairs yaad rehte hain? Decay "kitna lamba yaad rakhna hai" ka knob kyun hai?
3. **Socho:** Agar linear attention itna weak hai recall me, to GLM-5.3 isse 75% layers me kyun use karta hai? (Hint: Reading 03 ki cost table + Topic 06.)

## Repo ke asli layer pe check

```bash
cd sources/repo && uv run python -c "
import torch; from glm53_flash.model import LinearAttention, ModelConfig
la = LinearAttention(ModelConfig()); x = torch.randn(1, 20, 192)
y1 = la(x); y2 = la(torch.cat([x, torch.randn(1, 5, 192)], 1))[:, :20]
print('causal (future se past nahi badla):', torch.allclose(y1, y2, atol=1e-5))"
```
Expected: `causal (future se past nahi badla): True`

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [04 · Trade-off — Compressed memory ki keemat](04-tradeoff-real-life.md) | 📚 [Topic 05 overview](README.md) | [06 · Recap + Quiz](06-recap-quiz.md) ➡️ |
<!-- /nav:bottom -->
