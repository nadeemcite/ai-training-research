<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 11 — Research skill: data experiments (diversity, order, curriculum)](README.md) › Reading 1 / 6
<!-- /nav:top -->

# 01 · Concept — Accha research sawaal kya hota hai?

## AI researcher ka badalta kaam

Video ka sabse bada message:
> *"Right now Claude Code, Codex... AI is coding all of the experiments and it can do them autonomously. Your job as AI researcher is just to have high-level idea which experiments to do."*

> *"Just asking these questions is your job. This is what distinguishes experienced good researcher versus novice inexperienced."*

Code likhna AI kar sakta hai. Lekin **kaunsa sawaal poochna hai**, **experiment fair hai ya nahi**, aur **result ka sahi matlab kya hai**, ye judgment tumhara hai.

## Bura sawaal vs accha sawaal

| ❌ Bura | ✅ Accha |
|---|---|
| "Zyada data accha hai?" | "**Same number of updates** pe, 8 vs 88 alag program structures dekhne se **unseen structures** pe accuracy kaise badalti hai?" |
| "Order matter karta hai?" | "**Bilkul same examples**, sirf order alag: blocked vs interleaved. Held-out accuracy pe kya asar?" |
| "Curriculum kaam karta hai?" | "Pehle 100 updates 8 structures, fir 88. Ye shuru se 88 se better hai ya nahi, **same total updates** pe?" |

Acche sawaal me ye 4 cheezein hoti hain:
1. **Ek** cheez badalti hai (independent variable)
2. Baaki sab **fixed** rehta hai (controls)
3. **Kya measure** hoga, ye pehle se tay hota hai (metric)
4. **Kahan measure** hoga: aisa data jo training me nahi tha (held-out)

## Video ke 3 sawaal (is topic me)

1. **Diversity:** *"If you have less data and you repeat the data, it's going to learn faster in the beginning, but later more data will just overtake."*
2. **Order:** *"Is it better to first train on type A, then type B, then type C, or interleave them?"*
3. **Curriculum:** *"What if we first teach it repeated patterns, simple patterns, and then after teach it more diverse data?"*

## "Toy" experiments kyun?

> Video (38:41): *"MIT says you need to start from small toy examples so you can understand what's going on. It's better than doing huge experiments, complex, that you don't know what's going on."*

Repo ke data experiments ek **248,412-param** model pe hain, aur har run **~15 sec CPU** leta hai. Isliye 10 seeds × 3 conditions bhi minutes me ho jaate hain. Tez feedback loop = zyada sawaal, zyada seekhna.

> Video (44:08): *"You don't want to wait a few minutes, a few hours, because it's wasted time. You need to be practicing how to design experiments."*

---
🎬 **Video:** 01:02–04:30 (researcher ka role), 28:05–30:27 (experiments) · 📊 Slides 9–13, 49–56

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [Topic 11 — Research skill: data experiments (diversity, order, curriculum)](README.md) | 📚 [Topic 11 overview](README.md) | [02 · Definitions — Experiment design ke shabd](02-definitions.md) ➡️ |
<!-- /nav:bottom -->
