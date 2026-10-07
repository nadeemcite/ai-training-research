<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 14 — Evaluation: sahi naapna, imaandaari se bolna](README.md) › Reading 2 / 6
<!-- /nav:top -->

# 02 · Definitions — Evaluation ke shabd

| Term | Matlab |
|---|---|
| **Greedy decoding** | Har step pe sabse probable token. Same prompt pe hamesha same output |
| **pass@1 (greedy)** | Ek koshish (greedy) me sahi hua? Tasks ka fraction |
| **pass@k** | k sampled koshishon me se **kam se kam ek** sahi? |
| **Exact rollout rate** | Saare sampled attempts me se kitne sahi |
| **Paired evaluation** | Before aur after, **same tasks** pe |
| **McNemar test** | Paired yes/no data ka test: sirf "badle hue" tasks (gains vs losses) gine jaate hain |
| **Bootstrap interval** | Tasks ko random dobara chun-chun ke (resample) gain ka range nikaalna |
| **Interference** | Ek cheez sikhane se doosri cheez bigad jaana |
| **Replication** | Naye seeds pe dobara chala ke dekhna ki result tikta hai ya nahi |
| **Holm correction** | Bahut saare tests ek saath karo to p-values ko adjust karna (luck se "jeet" kam pakdo) |

## pass@1 vs pass@k

> Video (32:51): *"Pass at one means you just give it one try and then judge if it's correct or incorrect. If you have pass at eight, it means you are giving it eight tries and if any one of eight is correct, you take it as correctly answered."*

**Unbiased estimator** (Codex paper, 2021): n samples me se c sahi hain, to:
```
pass@k = 1 − C(n−c, k) / C(n, k)
```
"k random samples me **ek bhi** sahi na aane ka chance", 1 me se ghatao.

| n | c (sahi) | pass@1 | pass@8 |
|---:|---:|---:|---:|
| 8 | 0 | 0% | 0% |
| 8 | 1 | 12.5% | **100%** |
| 8 | 4 | 50% | 100% |

Ek hi sahi sample pass@8 ko 100% bana deta hai! Isliye pass@k "model **kar sakta** hai" naapta hai, aur pass@1 "model **reliably karta** hai".

## McNemar: sirf badle hue tasks gino

24 tasks, before/after:

| | After ✅ | After ❌ |
|---|---:|---:|
| **Before ✅** | 0 | 0 |
| **Before ❌** | **16 (gains)** | 8 |

Jo tasks dono me same rahe, wo kuch nahi batate. Sirf **16 gains vs 0 losses** matter karte hain. Agar RL ka koi asar na hota, to har badla hua task 50-50 chance se gain ya loss hota. 16/16 gains ka chance hai `2 × (1/2)^16` = **0.0000305**.

## Bootstrap interval

Tasks ko 20,000 baar random resample karo aur har baar gain nikaalo. Beech ke 95% values = interval. Lab me (greedy pass@1 gain): **[+45.8%, +83.3%]**. REPORT ka [+25.0, +53.1] **sampled** exact rate ke liye hai, jo ek alag metric hai.

---
📁 `scripts/analyze_rl_variants.py` (`mcnemar_exact`, `paired_bootstrap`, `holm`) · 🎬 Video 32:51–33:50

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [01 · Concept — Train, Dev, Confirm: teen alag kamre](01-concept-train-dev-confirm.md) | 📚 [Topic 14 overview](README.md) | [03 · Practical — Main result: 0/24 → 16/24](03-the-main-result.md) ➡️ |
<!-- /nav:bottom -->
