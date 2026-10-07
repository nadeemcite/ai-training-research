<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 13 — RLOO: advantage se update tak, aur sirf last block train karna](README.md) › Reading 2 / 6
<!-- /nav:top -->

# 02 · Definitions — Advantage, log-prob, policy gradient

| Term | Matlab | Repo me |
|---|---|---|
| **Policy** | Model jo action (tokens) chunta hai | GLM model |
| **Baseline** | Ek "expected" reward jisse tulna hoti hai | baaki 15 attempts ka mean |
| **Advantage** | `reward − baseline`: expectation se kitna behtar/bura | `leave_one_out(rewards)` |
| **Log-probability** | `log P(attempt | prompt)`: model ke hisaab se is attempt ke aane ka (log) chance | `completion_log_probabilities` |
| **Policy gradient (REINFORCE)** | Advantage × log-prob ka gradient. Achhe attempts ki probability badhao, bure ki ghatao | `loss = −(adv × logp).mean()` |
| **RLOO** | REINFORCE + leave-one-out baseline | repo ka algorithm |
| **GRPO** | Group mean baseline + std se normalize (+ PPO-style clipping, KL) | DeepSeek ka |
| **PPO** | Purana standard: critic model + clipped update | — |
| **On-policy** | Sirf abhi wale model ke attempts se seekho | haan |
| **KL penalty** | Model ko original se zyada door jaane se rokne wala extra loss | **repo me nahi** |
| **Train scope** | Kaunse parameters update hote hain | last block + final norm + tied head |

## Log-probability ek attempt ka

Attempt = tokens `[t₁, t₂, ..., tₙ]`. Model har position pe probability deta hai:
```
log P(attempt) = log p(t₁) + log p(t₂ | t₁) + ... + log p(tₙ | ...)
```

Repo isse **length se divide** karta hai (per-token average), taaki lambe jawab automatically zyada heavy na ho jaayein:
```python
return (token_log_probabilities * mask).sum(dim=1) / lengths
```

**Efficiency trick:** Saare 16 attempts ka log-prob **ek hi model call** me nikalta hai (padding + mask). REPORT: *"all 16 completion log-probabilities required one model call rather than 16."*

## RLOO vs GRPO, asli numbers (lab Exp 3)

Group 1 (`rl-double-013`) ke 16 rewards (4× +1, 6× 0, 6× −0.1):

| Reward | RLOO advantage | GRPO advantage |
|---:|---:|---:|
| +1.0 | **+0.840** | +1.669 |
| 0.0 | −0.227 | −0.450 |
| −0.1 | −0.333 | −0.662 |

Order aur sign **same** hai. GRPO bas std se scale karta hai, jisse har group ke advantages ka size ek jaisa ho jaata hai. Lab ka +0.840 repo ke saved receipt se **exact match** karta hai.

---
📁 `train_rl.py` lines 34–36, 57–79 · 🎬 Video 36:59–37:37

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [01 · Concept — "Apne bhai-behno se behtar tha ya nahi?"](01-concept-compare-with-siblings.md) | 📚 [Topic 13 overview](README.md) | [03 · Practical — Repo ka RLOO update, line by line](03-the-rloo-update.md) ➡️ |
<!-- /nav:bottom -->
