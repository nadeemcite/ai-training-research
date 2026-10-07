<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 11 — Research skill: data experiments (diversity, order, curriculum)](README.md) › Reading 3 / 6
<!-- /nav:top -->

# 03 · Practical — Repo ke 3 asli experiments

Setup (teeno me same): 248k-param mini GLM, 200 updates, batch 24, LR 8e-4, **10 paired seeds**, aur metric held-out 32 structures pe target-byte accuracy.

Lab Exp 3 me ye saare numbers repo ke `results.json` se **khud dobara nikaale** gaye hain:

| Sawaal | A → B (mean) | Fark | p | B jeeta |
|---|---|---:|---:|---:|
| Diversity: 8 repeated → 88 diverse | 57.0% → 60.2% | **+3.2** | 0.0137 | 9/10 |
| Order: blocked → interleaved | 50.5% → 60.2% | **+9.7** | 0.0020 | 10/10 |
| Curriculum: diverse → 8-then-88 | 60.2% → 59.6% | −0.6 | 0.2148 | 1/10 |

## Experiment 1: Data diversity 📊

**Sawaal:** Same updates pe, 8 structures baar-baar dekhna vs 88 alag structures?

| Updates | 8 repeated | 88 diverse | Fark | p |
|---:|---:|---:|---:|---:|
| 50 | 27.8% | 25.9% | −1.9 | 0.21 |
| 100 | 43.5% | 45.7% | +2.2 | 0.12 |
| 200 | 57.0% | 60.2% | **+3.2** | **0.014** |

**Seekh:** Diversity ka fayda **turant nahi** dikhta. Kam training me repeated data jaldi "yaad" ho jaata hai, aur zyada training ke baad diverse data aage nikal jaata hai.
> Video: *"Diversity is not useful if you do just a few steps, but then at 200 steps it becomes more and more useful."*

Report ka conclusion: *"A larger corpus is not automatically better when the training budget is too small to absorb it."*

## Experiment 2: Order (blocked vs interleaved) 🔀

**Sawaal:** **Bilkul same 4,800 examples**, sirf order alag:
```
blocked:     A A A A B B B B C C C C ...
interleaved: A B C A B C A B C A B C ...
```

**Result:** Interleaved **+9.7 points**, aur **10/10 seeds** me better. Ye teeno me sabse strong result hai.

**Seekh:** Same data, sirf order badalne se itna fark pada. Blocked me model aakhri block pe hi focus karta hai.
> Video: *"If you train it like this, then as it starts to learn C, it's going to start forgetting A and B. So it's better to interleave them."*

## Experiment 3: Curriculum (pehle aasaan, fir mushkil) 📈

**Sawaal:** Pehle 100 updates sirf 8 structures, fir 100 updates 88 structures. Kya ye shuru se 88 se better hai?

| Condition | Accuracy |
|---|---:|
| 8 repeated (poore 200) | 57.0% |
| **Curriculum** 8 → 88 | 59.6% |
| Diverse 88 shuru se | 60.2% |

**Result:** Curriculum ne sirf-8 ko haraya, lekin shuru-se-diverse ko **nahi**. −0.6 ka fark p = 0.21 pe significant nahi hai.

> Video: *"Curriculum did not make substantial progress as opposed to just training on the complex data from the start. Maybe this complex data was also too simple. So I need to think carefully about my experiment setup."*

## Ek chhupa hua sach: exact accuracy 0% 😬

Teeno experiments me **exact-expression accuracy har condition me 0%** rahi. Model ne poora expression ek baar bhi bilkul sahi nahi likha. Ye sirf partial byte-level learning hai.

Isliye results ka matlab hai "kis condition me model **thoda zyada** seekha", ye nahi ki "kaunsi condition se model **kaam karne laga**". Ye report ke "Limits" section me imaandaari se likha hai.

## Live run ka ek nuance (lab Exp 5)

Lab me blocked vs interleaved khud chalaoge (3 seeds). Blocked ke numbers repo ke saved results se **exact match** karte hain (seed 11: 43.2%). Interleaved thoda alag aata hai (59.3% vs 58.1%), kyunki repo report "interleaved" ke liye diversity experiment ka "88 diverse" arm reuse karta hai, jo thoda alag code path hai. Fark chhota hai aur conclusion same hai, lekin aisi details padhna bhi research ka hissa hai.

---
📄 `artifacts/experiments/pretraining-*-summary/REPORT.md` · 🎬 Video 28:05–30:27 · 📊 Slides 49–56

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [02 · Definitions — Experiment design ke shabd](02-definitions.md) | 📚 [Topic 11 overview](README.md) | [04 · Imaandaar conclusions + Real-life](04-honest-conclusions-real-life.md) ➡️ |
<!-- /nav:bottom -->
