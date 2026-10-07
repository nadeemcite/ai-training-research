<!-- nav:top -->
[🏠 Course](../README.md) › **Topic 13 / 15** › ▶️ [Pehli reading shuru karo](01-concept-compare-with-siblings.md)
<!-- /nav:top -->

# Topic 13 — RLOO: advantage se update tak, aur sirf last block train karna

**Pichle topic se link:** Topic 12 me RL ka **environment** banaya: task, verifier aur reward. Har prompt pe 16 attempts aur 16 rewards milte hain. Ab sawaal ye hai: **in rewards se weights kaise badlein?** Iska jawab hai advantage, policy gradient aur RLOO, plus ek practical trick: poore model ki jagah sirf aakhri block train karna.

**Time:** ~50 min (padhai) + ~15 min (lab, optional 2.5 min RL run)

## Reading order

| File | Type | Kya milega |
|---|---|---|
| [01-concept-compare-with-siblings](01-concept-compare-with-siblings.md) | Concept | "Apne bhai-behno se behtar tha ya nahi?" — advantage ka idea |
| [02-definitions](02-definitions.md) | Definitions | Advantage, baseline, log-prob, policy gradient, RLOO, GRPO, PPO, KL |
| [03-the-rloo-update](03-the-rloo-update.md) | Practical | Repo ka update line-by-line, aur loss ka sign kyun ulta hai |
| [04-last-block-and-real-life](04-last-block-and-real-life.md) | Practical + Real-life | Sirf 2.19M params kyun, pilot history, aur cooking class analogy |
| [05-lab-guide](05-lab-guide.md) | Code | [`lab_rloo.py`](lab_rloo.py): advantage haath se, aur CPU pe asli RL run |
| [06-recap-quiz](06-recap-quiz.md) | Test | 8 sawaal |

## RL ka loop (is topic ka part **bold**)

```
prompt → 16 attempts → verifier → rewards → **advantages → log-probs → loss → update** → dobara
```

## Repo me kahan hai?

- `sources/repo/scripts/train_rl.py`: `leave_one_out` (line 34), `completion_log_probabilities` (57), RL loop (150–191), train scope (121–130)
- `sources/repo/REPORT.md` → "Reinforcement learning" aur "Pilot history"

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [06 · Recap + Quiz](../12-rl-executable-rewards/06-recap-quiz.md) | 📚 [Topic 13 overview](README.md) | [01 · Concept — "Apne bhai-behno se behtar tha ya nahi?"](01-concept-compare-with-siblings.md) ➡️ |
<!-- /nav:bottom -->
