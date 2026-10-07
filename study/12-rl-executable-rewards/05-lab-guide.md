<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 12 — RL with executable rewards + verifier](README.md) › Reading 5 / 6
<!-- /nav:top -->

# 05 · Code Lab — `lab_rewards.py`

## Run (~2 sec)

```bash
uv run study/12-rl-executable-rewards/lab_rewards.py
```

Repo ka **asli verifier** (`evaluator.py`), **asli reward function** (`train_rl.reward_for`), aur **final RL run ka saved data** (`glm53-executable-rloo-diverse-001`, jisme har rollout aur uska reward hai) use hote hain.

## Expected output (aur matlab)

```
Exp 1  model ko sirf ye prompt milta hai:
       # Complete this Python function.
       # Return x plus one.
       def increment_cjaojdr(x):
       chhupe hue tests (model ko kabhi nahi dikhte): [((-3,), -2), ((0,), 1), ((7,), 8)]
```
→ RL environment (Reading 02).

```
Exp 2  jawab                status    tests  binary  case-fraction
       sahi                 passed    3/3    +1.00    +1.00
       galat (valid)        failed    0/3    +0.00    +0.00
       aadha sahi           failed    2/3    +0.00    +0.67
       invalid Python       invalid   0/3    -0.10    -0.10   (invalid syntax (<unknown>, line 4))
       import (khatarnak)   invalid   0/3    -0.10    -0.10   (disallowed syntax: Import)
       loop (mana hai)      invalid   0/3    -0.10    -0.10   (disallowed syntax: For)
```
→ Verifier (Reading 03) aur reward modes (Reading 04).

```
Exp 3  hack: return {-3: -2, 0: 1, 7: 8}[x]  -> repo verifier: passed, reward +1.0  😱
       stronger verifier (random hidden inputs): sahi -> True, hack -> False
```
→ **Is lab ka main result:** reward hacking aur uska fix (Reading 04).

```
Exp 4  asli run, group 1 (rl-double-013), temperature 0.35:
        6x  reward +0.0  'return x * x'
        5x  reward -0.1  'return x * * x'
        4x  reward +1.0  'return x * 2'
        1x  reward -0.1  'return x * * 0'
```
→ Ek prompt, 16 rollouts: exploration (Reading 02). Topic 13 me dekhoge ki in rewards se update kaise banta hai.

```
Exp 5  96 groups me se 23 me sab 16 rewards barabar the -> koi update nahi ({'sab -0.1': 22, 'sab +0.0': 1})
       training ke dauraan sahi rollouts: pehle 24 groups 23%  ->  aakhri 24 groups 46%
```
→ Sparse reward, aur RL ka asli progress (Reading 04).

## Tumhara kaam (15 min)

1. **TODO (a):** Ek apna jawab likho jo increment ke 2/3 tests pass kare (jaise `return x + 1 if x != 0 else 5`). Binary aur case-fraction reward kitna dete hain?
2. **TODO (b):** `double` family ke liye hack likho (tests: −4→−8, 0→0, 6→12). Kya repo verifier use pass karta hai?
3. **TODO (c):** Agar reward sirf "+1 sahi / 0 baaki" ho (koi −0.1 nahi) aur model shuru me 0% sahi ho, to kya RL kabhi shuru hoga? Exp 5 ke numbers se jodo.
4. **Bonus (security soch):** `evaluator.py` ki DENIED list dekho. Koi aur trick socho jo ek "galat" function ko pass karwa de. (Sirf soch ke likho, aur dekho kya `stronger_verifier` use pakadta hai.)

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [04 · Reward design, reward hacking + Real-life](04-reward-design-and-hacking.md) | 📚 [Topic 12 overview](README.md) | [06 · Recap + Quiz](06-recap-quiz.md) ➡️ |
<!-- /nav:bottom -->
