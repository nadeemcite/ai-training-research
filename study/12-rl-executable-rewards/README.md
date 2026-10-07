<!-- nav:top -->
[🏠 Course](../README.md) › **Topic 12 / 15** › ▶️ [Pehli reading shuru karo](01-concept-imitation-vs-reward.md)
<!-- /nav:top -->

# Topic 12 — RL with executable rewards + verifier

**Pichle topics se link:** Topic 10 me pretraining ne model ko "Python jaisa dikhne wala" code likhna sikhaya. Lekin chhota model aksar `return x * * 0 0` jaisa code likhta tha, jo dikhta sahi hai par chalta nahi. **Reinforcement Learning (RL)** me model khud jawab likhta hai, hum use **asli me run karke** check karte hain, aur sahi jawab ko reward dete hain. Is topic me RL ka **environment** banana seekhoge: verifier aur reward. Update ka math (RLOO / advantage) Topic 13 me hai.

**Time:** ~50 min (padhai) + ~15 min (lab)

## Reading order

| File | Type | Kya milega |
|---|---|---|
| [01-concept-imitation-vs-reward](01-concept-imitation-vs-reward.md) | Concept | Pretraining (nakal) vs RL (koshish + inaam) |
| [02-definitions](02-definitions.md) | Definitions | Policy, environment, rollout, reward, verifier, group, temperature |
| [03-verifier-sandbox](03-verifier-sandbox.md) | Practical | Repo ka verifier: model ka code **safely** kaise chalayein |
| [04-reward-design-and-hacking](04-reward-design-and-hacking.md) | Practical + Real-life | Reward kaise design karein, **reward hacking** (repo me mila ek asli hole), driving test analogy |
| [05-lab-guide](05-lab-guide.md) | Code | [`lab_rewards.py`](lab_rewards.py): verifier todo, hack karo, asli RL run ka data dekho |
| [06-recap-quiz](06-recap-quiz.md) | Test | 8 sawaal |

## RL ka loop (is topic ka part **bold** hai)

```
prompt → model 16 jawab likhta hai → **verifier chalata hai** → **reward** → update (Topic 13) → dobara
```

## Repo me kahan hai?

- `sources/repo/glm53_flash/evaluator.py`: verifier (sandbox + tests)
- `sources/repo/scripts/train_rl.py`: `reward_for`, RL loop
- `sources/repo/glm53_flash/tasks.py`: tasks, hidden test cases, splits
- `sources/repo/REPORT.md`: RL results aur "pilot history"

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [06 · Recap + Quiz](../11-research-data-experiments/06-recap-quiz.md) | 📚 [Topic 12 overview](README.md) | [01 · Concept — Nakal (pretraining) vs Koshish + Inaam (RL)](01-concept-imitation-vs-reward.md) ➡️ |
<!-- /nav:bottom -->
