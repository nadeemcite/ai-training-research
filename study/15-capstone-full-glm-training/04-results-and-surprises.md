<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 15 — Capstone: poora GLM-5.3-Flash ek file me 🎓](README.md) › Reading 4 / 6
<!-- /nav:top -->

# 04 · Results — hamara asli run, aur rasta me mile surprises

## Final run (default settings, Mac CPU, ~3.7 min)

```
model tiny: 2,167,328 params, ~840,224 active/token
STAGE pretrain (200 steps)      loss 5.530 → 0.303      balance ~1.02 (perfect = 1.0)
STAGE rl (48 groups × 16)       exact rollouts during RL: 82/192 → 458/768 total
STAGE eval (confirm, ek baar)
  RL families greedy pass@1: 2/12 -> 8/12   (gains 6, losses 0, McNemar p = 0.0312)
  all 8 families sampled pass@1 73.4% -> 81.2%,  pass@8 90.6% -> 96.9%
    RL increment    4/32 -> 25/32 ↑        square       32/32 -> 31/32 ↓
    RL double      16/32 -> 32/32 ↑        absolute     32/32 -> 24/32 ↓
    RL even         8/32 ->  8/32 —        list_sum     32/32 -> 24/32 ↓
                                           nonnegative, reverse: 32/32 -> 32/32 —
STAGE vision: held-out digits 0/200 -> 141/200
```

Ye run do baar chalaya gaya, aur dono baar **bilkul same** numbers aaye.

## Vuk ke repo ke result se tulna

| | Repo (25.7M, GPU) | Hamara capstone (2.2M, CPU) |
|---|---|---|
| RL families | increment, double, even | same |
| increment / double | ↑↑ | ↑↑ (double 32/32!) |
| even | flat | **flat** (8/32 → 8/32) |
| Untrained families | square, list_sum ↓ | absolute, list_sum ↓ |
| Greedy, paired | 16 gains / 0 losses, p = 0.00003 | 6 gains / 0 losses, p = 0.031 |

**Pattern same hai:** trained families sudhri, `even` phir se nahi hili, aur doosri families me interference dikha. 12 tasks pe p = 0.031 (24 pe chhota hota). Topic 14 ka "kam tasks = kam statistical power" yahin dikhta hai.

## Surprise 1: pretraining kitni ho, ye sabse bada knob nikla

Same code, sirf `--pretrain-steps` badla (1 seed each):

| Pretrain steps | RL ke dauraan sahi rollouts | Greedy (RL families) |
|---:|---:|---|
| 120 | 154/768 | 0/12 → 4/12 |
| **200** | **458/768** | **2/12 → 8/12** |

120 steps pe model itna kamzor tha ki RL ke paas badhane ko kam "sahi" attempts the (Topic 12 ka sparse reward). Isliye default **200** kiya gaya. Ye Topic 15 Reading 05 ka research sawaal #5 hai, aur pehli jhalak yahin mil gayi.

**RL learning rate** bhi try kiya (120-step checkpoint pe): 1e-4 → greedy +4, 3e-5 → +4, 1e-5 → +0. Bahut chhota lr = kuch nahi seekha (repo ke pilot #2 jaisa).

## Surprise 2: FIX-08 ka pehla signal (sirf anecdote!)

120 pretrain steps, ek hi seed:

| | Pretrain loss @120 | RL sahi rollouts | Greedy |
|---|---:|---:|---|
| Repo-style (identity do baar) | 0.851 | 34/768 | 0/12 → 2/12 |
| FIX-08 (identity ek baar) | 0.665 | 154/768 | 0/12 → 4/12 |

Fixed version aage dikhta hai, lekin **ye 1 seed hai**, to ye ek anecdote hai, discovery nahi (Topic 14). Ise 5+ seeds pe confirm karna roadmap ka sawaal #1 hai.

## Surprise 3: maine khud ek bug likha (aur pakda) 🐛

Capstone ka pehla version before/after eval ke liye model weights save/restore karta tha:
```python
after_state = model.state_dict()          # ❌ ye COPY nahi, sirf live tensors ke references hain
model.load_state_dict(before_state)       # ab after_state bhi "before" weights dikhata hai!
model.load_state_dict(after_state)        # model kabhi "after" pe wapas nahi aaya
```
Eval numbers sahi the (after-eval restore se pehle hua tha), lekin **saved `model.pt` asal me pre-RL weights tha**. Pakda kaise? RL ke baad ke outputs dekhe, to wo ajeeb tarah se pretraining jaise lag rahe the.

**Fix:** `{k: v.detach().clone() for k, v in model.state_dict().items()}`

> Topic 07, 08, 12 me repo ke bugs mile, aur yahan khud ka. Video ka line har jagah sach hai: *"maybe it's a bug in my code or bug that AI generated."* Isliye **outputs khud padho**, sirf numbers mat dekho.

## Kya claim kar sakte hain?

✅ Ek file, ~4 min, CPU: random weights → Python likhna → RL se trained families pe sudhaar (paired p = 0.031) → images se digits padhna.
❌ Ye "GLM-5.3 reproduce kiya" nahi hai, aur 1 seed pe kisi fix ke "behtar" hone ka claim bhi nahi hai.

---
📄 `runs/capstone/receipt.json` (tumhare run ka poora record)

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [03 · Kaise chalayein](03-run-it.md) | 📚 [Topic 15 overview](README.md) | [05 · Research roadmap — ab kya karein?](05-research-roadmap.md) ➡️ |
<!-- /nav:bottom -->
