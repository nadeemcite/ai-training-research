<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 10 — Pretraining loop: random weights se Python tak](README.md) › Reading 5 / 6
<!-- /nav:top -->

# 05 · Code Lab — `lab_pretrain.py`

## Run (~2 min, CPU pe)

```bash
uv run study/10-pretraining-loop/lab_pretrain.py
```

Repo ka asli **model class, data generator (`batch_for`), generation aur verifier** import hote hain. Bas model chhota hai: 2.2M params (dim 96, 4 layers), taaki CPU pe jaldi chale.

## Expected output (aur matlab)

```
Exp 1  ek pretraining example:
       # Complete this Python function.
       # Double the input.
       def double_fofienq(x):
           return x * 2

       input  ids[:6] = [1, 39, 36, 71, 115, 113]  -> '# Com' (+BOS)
       labels ids[:6] = [39, 36, 71, 115, 113, 116]  (input ka agla token)
       padding labels = -100 -> loss me gina nahi jaata. Asli target tokens: 94 / 128
```
→ Input/label shift aur padding (Reading 02).

```
Exp 2  haath se 6.3054  |  F.cross_entropy 6.3054  |  random guess ln(260) = 5.5607
```
→ Cross-entropy haath se = library se, aur `-100` wali position skip hui (Reading 02).

```
Exp 3  gradient [30.0, 40.0, 0.0] norm=50  -> clip ke baad [0.6, 0.8, 0.0] norm=1.00  (direction same, size 1)
```
→ Gradient clipping (Reading 04).

```
Exp 4  model 2,167,040 params, batch 16, 300 steps
       step   loss   dev(8)  'double' ka greedy jawab
          0      -   0/8     '::::::::::::::::::::::::::::'
         50  1.973   0/8     'x x x x x x x x x x x x x x '
        100  0.936   0/8     'return x if x = 0'
        150  0.503   3/8     'return x * 2'
        200  0.322   6/8     'return x * 2'
        250  0.305   7/8     'return x * 2'
        300  0.253   8/8     'return x * 2'
       (101s CPU pe)
```
→ **Is lab ka main result.** Random → characters → Python shape → sahi logic. "dev(8)" ka matlab hai 8 unseen function naam (har family se 1), jinhe repo ka verifier **asli me run** karke check karta hai (Topic 12).

## Tumhara kaam (20 min)

1. **TODO (a):** `lr=1e-3` ko `1e-2` aur `1e-4` karke chalao. Kab loss sabse jaldi girta hai? Kab dev score 8/8 tak nahi pahunchta?
2. **TODO (b):** `clip_grad_norm_` wali line hata do aur `lr=1e-2` rakho. Training stable rahi? Loss me spikes dikhe?
3. **TODO (c):** `pretraining_text(1)`, `(2)`, `(3)` print karo. Kitni families dikhi? Function naam kaise badalte hain?
4. **Bonus (patience chahiye, ~8 min):** Repo ka asli 25.7M model CPU pe 100 steps train karo:
   ```bash
   cd sources/repo && uv run python scripts/train_pretrain.py --output runs/my-pretrain --device cpu --steps 100 --checkpoints 100
   ```
   *(Maine ek step time kiya: ~4.5 sec/step, to 100 steps ≈ 7–8 min. `runs/` repo ke .gitignore me hai, to ye git me nahi jaayega.)*

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [04 · AdamW, gradient clipping + Real-life](04-adamw-clipping-real-life.md) | 📚 [Topic 10 overview](README.md) | [06 · Recap + Quiz](06-recap-quiz.md) ➡️ |
<!-- /nav:bottom -->
