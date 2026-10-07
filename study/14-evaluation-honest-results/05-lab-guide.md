<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 14 — Evaluation: sahi naapna, imaandaari se bolna](README.md) › Reading 5 / 6
<!-- /nav:top -->

# 05 · Code Lab — `lab_evaluation.py`

## Run (~3 sec)

```bash
uv run study/14-evaluation-honest-results/lab_evaluation.py
```

Repo ke asli **confirmation receipts** (har task ka before/after model output aur verifier result) aur asli analysis functions (`mcnemar_exact`, `paired_bootstrap`) use hote hain. Kuch train nahi hota, sirf **saved results ka imaandaar analysis** hai.

## Expected output (aur matlab)

```
Exp 1  greedy pass@1 (confirm, 3 RL families): before 0/24  ->  after 16/24
       increment  0/8 -> 8/8
       double     0/8 -> 8/8
       even       0/8 -> 0/8
```
→ Main result (Reading 03).

```
Exp 2  paired: 16 tasks gained, 0 lost  ->  exact p = 0.0000305   (= 2 / 2^16 = 0.0000305)
       paired bootstrap 95% interval for the gain: [+45.8%, +83.3%]
```
→ McNemar aur bootstrap (Reading 02). REPORT ka p exact match karta hai.

```
Exp 3  sampled (temperature 0.35, 8 samples/task), sab 8 families, 64 tasks:
       before pass@1 = 24.6%
       before pass@8 = 39.1%
       after  pass@1 = 35.4%
       after  pass@8 = 53.1%
       (receipt summary: pass@8 before 39.1%, after 53.1%)
```
→ pass@k estimator (Reading 02). Hamara function receipt se match karta hai.

```
Exp 4  per-family sampled exact rate (8 tasks x 8 samples):
       RL double        4/64 -> 45/64  ↑
       RL even          3/64 ->  3/64  —
       RL increment     6/64 -> 40/64  ↑
          absolute      0/64 ->  0/64  —
          list_sum     61/64 -> 56/64  ↓
          nonnegative   0/64 ->  0/64  —
          reverse       0/64 ->  0/64  —
          square       52/64 -> 37/64  ↓
```
→ Interference (Reading 04).

```
Exp 5  screen (1 seed, dev tasks solved /20): binary 5, partial reward 5, ..., group size 4 8, group size 16 6
       confirm (3 fresh seeds, 40 tasks):
         seed 31415: group 8 = 12/40, group 4 = 13/40  (+1)
         seed 27182: group 8 = 14/40, group 4 = 13/40  (-1)
         seed 16180: group 8 = 11/40, group 4 = 8/40  (-3)
       mean: group 8 = 12.3, group 4 = 11.3  ->  screen ka 'winner' confirm me haar gaya
```
→ Replication failure (Reading 04). *(Ye numbers slides 72–73 se hain. Raw variant runs repo me commit nahi hue.)*

## Tumhara kaam (10 min)

1. **TODO (a):** `pass_at_k(8, 1, 8)` aur `pass_at_k(8, 1, 1)` nikaalo. Ek sahi sample, do alag numbers. Kyun?
2. **TODO (b):** 10 gains aur 6 losses pe McNemar p kya hoga? (`mcnemar_exact([True]*6 + [False]*10, [False]*6 + [True]*10)`)
3. **TODO (c):** `square` 52 → 37 ka girna noise hai ya asli? Ise kaise test karoge? (Hint: confirm receipts me per-task data hai, to paired comparison karo.)

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [04 · Interference, replication + Real-life](04-interference-replication-real-life.md) | 📚 [Topic 14 overview](README.md) | [06 · Recap + Quiz](06-recap-quiz.md) ➡️ |
<!-- /nav:bottom -->
