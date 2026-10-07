<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 11 — Research skill: data experiments (diversity, order, curriculum)](README.md) › Reading 5 / 6
<!-- /nav:top -->

# 05 · Code Lab — `lab_experiments.py`

## Run

```bash
uv run study/11-research-data-experiments/lab_experiments.py          # ~5 sec: saved results ka analysis
uv run study/11-research-data-experiments/lab_experiments.py --run    # + ~90 sec: khud experiment
```

Repo ke **asli experiment functions** (`train_condition`, `render_example`, `static_items`) aur **asli 10-seed saved results** use hote hain.

## Expected output (aur matlab)

```
Exp 1  kul 120 program structures -> train 88, held-out 32 (kabhi train nahi hue)
       [train   ] ('add', 'add', 'abs'): Task: start with x. Increase it by 5. Add 4. Make the result nonnegative.  ⏎  Python: abs(((x + 5) + 4))
       [held-out] ('neg', 'neg', 'add'): Task: start with x. Negate it. Negate it. Increase it by 4.  ⏎  Python: ((-(-x)) + 4)
```
→ Data aur held-out split (Reading 02).

```
Exp 2  blocked     order: A A A A B B B B C C C C
Exp 2  interleaved order: A B C A B C A B C A B C
```
→ Same examples, sirf order alag (Reading 03).

```
Exp 3  sawaal (200 updates, 10 paired seeds)            A -> B mean    diff     p      B jeeta
       Diversity: 8 repeated -> 88 diverse?         57.0% -> 60.2%   +3.2  0.0137  9/10
       Order: blocked -> interleaved?               50.5% -> 60.2%   +9.7  0.0020  10/10
       Curriculum: diverse -> 8-to-88 curriculum?   60.2% -> 59.6%   -0.6  0.2148  1/10
```
→ **Repo ke report ke teeno p-values exact reproduce hue** (0.0137, 0.001953, 0.2148). Ye tumhare 10-line `paired_sign_flip` function se nikle hain.

```
Exp 4  seeds   sabse chhota possible p (sab seeds ek hi direction me)
           1   1.0000   <- 0.05 ke neeche aa hi nahi sakta!
           3   0.2500   <- 0.05 ke neeche aa hi nahi sakta!
           5   0.0625   <- 0.05 ke neeche aa hi nahi sakta!
           6   0.0312
          10   0.0020
```
→ Reading 02 ki table.

```
Exp 5  blocked vs interleaved, 3 seeds x 200 updates (CPU, ~90s)...
       seed 11: blocked 43.2%  interleaved 59.3%
       seed 22: blocked 54.5%  interleaved 61.0%
       seed 33: blocked 50.4%  interleaved 61.4%
       mean diff +11.2 points, interleaved jeeta 3/3, p = 0.25
```
→ **3/3 jeet, bada fark (+11 points), phir bhi p = 0.25.** Kyunki 3 seeds pe isse chhota p possible hi nahi hai (Exp 4).

## Tumhara kaam (20 min)

1. **TODO (a):** Curriculum result pe ek line ka imaandaar conclusion likho. Kya "curriculum bekaar hai" kehna sahi hai?
2. **TODO (b):** Exp 5 ka paradox apne shabdon me samjhao: 3/3 jeet aur p = 0.25.
3. **TODO (c):** Repo report kehta hai "long homogeneous blocks **likely** create recency bias or forgetting". Forgetting ko **directly measure** karne ka experiment design karo. (Hint: har 20 updates pe, *pehle block wale* structures pe accuracy track karo.)
4. **Bonus:** Exp 5 me seeds `(11, 22, 33)` ko `(11, 22, 33, 44, 55, 66)` karo (~3 min). Ab p kitna aaya?

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [04 · Imaandaar conclusions + Real-life](04-honest-conclusions-real-life.md) | 📚 [Topic 11 overview](README.md) | [06 · Recap + Quiz](06-recap-quiz.md) ➡️ |
<!-- /nav:bottom -->
