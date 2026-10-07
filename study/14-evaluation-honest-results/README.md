<!-- nav:top -->
[🏠 Course](../README.md) › **Topic 14 / 15** › ▶️ [Pehli reading shuru karo](01-concept-train-dev-confirm.md)
<!-- /nav:top -->

# Topic 14 — Evaluation: sahi naapna, imaandaari se bolna

**Pichle topics se link:** Topic 13 me RL ne model ko badla. Lekin "badla" ka matlab "behtar hua" nahi hai. Kya ye sach me behtar hai? Kahan behtar hai? Kahan bura hua? Kya ye luck tha? Ye topic **evaluation** ke baare me hai, jo research ka sabse aakhri aur sabse zaroori kadam hai.

> Video (33:20): *"Of course you will always need to see how you are measuring your results."*

**Time:** ~50 min (padhai) + ~10 min (lab)

## Reading order

| File | Type | Kya milega |
|---|---|---|
| [01-concept-train-dev-confirm](01-concept-train-dev-confirm.md) | Concept | Teen splits, aur confirmation set "ek hi baar kyun" |
| [02-definitions](02-definitions.md) | Definitions | Greedy, pass@1, pass@k, McNemar, bootstrap, interference, replication |
| [03-the-main-result](03-the-main-result.md) | Practical | 0/24 → 16/24: p-value, interval, aur kya ye claim hai, kya nahi |
| [04-interference-replication-real-life](04-interference-replication-real-life.md) | Practical + Real-life | Jo bigda, jo replicate nahi hua, aur cricket trial analogy |
| [05-lab-guide](05-lab-guide.md) | Code | [`lab_evaluation.py`](lab_evaluation.py): saved receipts se saare numbers khud nikaalo |
| [06-recap-quiz](06-recap-quiz.md) | Test | 8 sawaal |

## Repo me kahan hai?

- `sources/repo/artifacts/receipts/runs/confirm-*.json`: har confirm task ka before/after output
- `sources/repo/scripts/analyze_rl_variants.py`: McNemar, bootstrap, Holm correction
- `sources/repo/REPORT.md` → "Confirmation results", "Limitations"
- Slides 69–76 (variant screen aur replication)

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [06 · Recap + Quiz](../13-rloo-advantage-last-block/06-recap-quiz.md) | 📚 [Topic 14 overview](README.md) | [01 · Concept — Train, Dev, Confirm: teen alag kamre](01-concept-train-dev-confirm.md) ➡️ |
<!-- /nav:bottom -->
