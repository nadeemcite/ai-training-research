<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 13 — RLOO: advantage se update tak, aur sirf last block train karna](README.md) › Reading 5 / 6
<!-- /nav:top -->

# 05 · Code Lab — `lab_rloo.py`

## Run

```bash
uv run study/13-rloo-advantage-last-block/lab_rloo.py          # ~3 sec
uv run study/13-rloo-advantage-last-block/lab_rloo.py --run    # + ~2.5 min: CPU pe pretrain → RL
```

Repo ke asli `leave_one_out`, `completion_log_probabilities`, `reward_for`, `generate_group` aur final run ka receipt use hote hain.

## Expected output (aur matlab)

```
Exp 1  rewards      [1.0, 0.0, -0.1, 1.0]
       attempt 0: +1.0 - mean[0.0, -0.1, 1.0] = +1.0 - +0.300 = +0.700
       attempt 1: +0.0 - mean[1.0, -0.1, 1.0] = +0.0 - +0.633 = -0.633
       attempt 2: -0.1 - mean[1.0, 0.0, 1.0] = -0.1 - +0.667 = -0.767
       attempt 3: +1.0 - mean[1.0, 0.0, -0.1] = +1.0 - +0.300 = +0.700
       advantages ka sum = +0.000  (hamesha ~0: kuch upar, kuch neeche)
Exp 2  rewards [1.0, 1.0, 1.0, 1.0] -> advantages [0.0, 0.0, 0.0, 0.0]
Exp 2  rewards [-0.1, -0.1, -0.1, -0.1] -> advantages [0.0, 0.0, 0.0, 0.0]
```
→ Advantage (Reading 01).

```
Exp 3  asli group 1 (rl-double-013), 16 rewards: [-0.1, 0.0, 1.0] values
       reward +1.0:  RLOO advantage +0.840   GRPO advantage +1.669
       reward +0.0:  RLOO advantage -0.227   GRPO advantage -0.450
       reward -0.1:  RLOO advantage -0.333   GRPO advantage -0.662
       (saved receipt ka advantage bhi: +0.840 for +1.0)
```
→ RLOO vs GRPO (Reading 02).

```
Exp 4  advantages [+0.9, -0.3, -0.6] -> gradient step direction [0.3, -0.1, -0.2]
       (positive = us attempt ki probability badhegi)
```
→ Loss ka sign (Reading 03).

```
Exp 5  last block + final norm + tied embedding/head: 2,190,152 / 25,730,592 = 8.5%  (repo receipt: 2,190,152)
```
→ Train scope (Reading 04).

`--run` ke saath (asli output; tumhare numbers thode alag ho sakte hain):
```
Exp 6  pretraining 120 steps (46s). Dev sampled exact: 3/96
       RL group 16: updates 14, sahi rollouts ab tak 34/256  (43s)
       RL group 32: updates 30, sahi rollouts ab tak 70/512  (85s)
       RL group 48: updates 43, sahi rollouts ab tak 121/768  (126s)
       RL ke baad dev sampled exact: 25/96
```
→ **Is lab ka main result:** RL ne CPU pe 2 min me sahi attempts ~8× badha diye.

## Tumhara kaam (15 min)

1. **TODO (a):** Exp 1 me rewards `[1, 1, 1, 0]` karo. Akele 0 wale ka advantage kitna negative hai? Ye "sabse zyada seekhne layak" attempt kyun hai?
2. **TODO (b):** Exp 3 me RLOO aur GRPO advantages ka ratio nikaalo. Kya har reward pe same hai?
3. **TODO (c):** Exp 6 me RL lr `1e-4` ko `1e-3` aur `1e-5` karo. Reading 04 ki pilot history se compare karo.
4. **Bonus:** Exp 6 me train scope "sirf last block" (embedding hata ke) karo. Kya RL ab bhi kaam karta hai? (Pilot #3 yaad karo.)

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [04 · Sirf last block train karo, pilot history + Real-life](04-last-block-and-real-life.md) | 📚 [Topic 13 overview](README.md) | [06 · Recap + Quiz](06-recap-quiz.md) ➡️ |
<!-- /nav:bottom -->
