<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 13 — RLOO: advantage se update tak, aur sirf last block train karna](README.md) › Reading 3 / 6
<!-- /nav:top -->

# 03 · Practical — Repo ka RLOO update, line by line

Slide 68 "The RLOO update":

```python
generations = generate_group(model, task, group_size=16)          # 1. 16 attempts (sampling, temp 0.35)
rewards = [reward_for(task, g) for g in generations]              # 2. verifier → +1 / 0 / −0.1
advantages = leave_one_out(rewards)                               # 3. tulna

log_probs = completion_log_probabilities(model, generations)      # 4. har attempt ka log P
loss = -(advantages * log_probs).mean()                           # 5. policy gradient loss

loss.backward()                                                   # 6. gradient
optimizer.step()                                                  # 7. update
```

> Slide: *"No reference completion is shown during RL."* Model ko kabhi `return x * 2` dikhaya nahi gaya. Usne khud likha aur reward mila.

## `leave_one_out`, 3 lines

```python
def leave_one_out(rewards):
    total = sum(rewards)
    return [reward - (total - reward) / (len(rewards) - 1) for reward in rewards]
```

`(total − reward) / (n − 1)` = baaki sab ka mean, ek hi pass me.

## Loss me minus sign kyun?

Hum chahte hain ki **achhe attempts ki probability badhe**, yaani `advantage × log_prob` **maximize** ho. Lekin optimizers loss ko **minimize** karte hain, isliye minus laga dete hain:

```
minimize  −(adv × logp)   ≡   maximize  adv × logp
```

- `adv > 0`: logp badhana loss ghatata hai → attempt **zyada** likely ✅
- `adv < 0`: logp ghatana loss ghatata hai → attempt **kam** likely ✅

Lab Exp 4 (3 attempts, advantages `[+0.9, −0.3, −0.6]`):
```
gradient step direction [+0.3, −0.1, −0.2]   ← positive = probability badhegi
```

## Repo ke safety checks

```python
spread = max(rewards) - min(rewards)
updated = spread > 1e-8 and all(generation["token_ids"] for generation in generations)
if updated:
    ...
    if not torch.isfinite(objective): raise FloatingPointError
    clip_grad_norm_(trainable_parameters, 1.0)
```

- **Spread zero** → skip (advantages sab 0 hain, to compute waste mat karo)
- **Khaali attempt** → skip (log-prob undefined hai)
- **NaN** → turant ruko
- **Gradient clipping** → Topic 10 wala hi

## Kya missing hai? (honest)

REPORT ka "Limitations": *"The RL update has no explicit KL penalty; interference was observed."*

Real systems (PPO, GRPO) aksar ek **KL penalty** lagate hain jo model ko pretrained version se zyada door jaane nahi deta. Iske bina RL trained families pe focus karta hai aur doosri families bigaad sakta hai. Topic 14 me `square` aur `list_sum` ka girna dekhoge.

---
📁 `train_rl.py` lines 150–191 · 📊 Slide 68 · 🎬 Video 36:59–37:37

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [02 · Definitions — Advantage, log-prob, policy gradient](02-definitions.md) | 📚 [Topic 13 overview](README.md) | [04 · Sirf last block train karo, pilot history + Real-life](04-last-block-and-real-life.md) ➡️ |
<!-- /nav:bottom -->
