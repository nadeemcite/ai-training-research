<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 15 — Capstone: poora GLM-5.3-Flash ek file me 🎓](README.md) › Reading 5 / 6
<!-- /nav:top -->

# 05 · Research roadmap — ab kya karein?

> Video (43:22): *"I encourage you to just go talk to Codex or Claude Code. You can tell it which kind of experiments can I do here, and don't be so concerned about scaling. I just want you to learn how to do some experiments, how to learn scientific thinking, how to measure properly, how to conclude properly."*

Course khatam hua, lekin **research ab shuru** hoti hai. Neeche 10 sawaal hain jo tum capstone file se **CPU pe** kar sakte ho. Har ek ke liye Topic 11 ka format follow karo: sawaal → ek variable → controls → metric → seeds → imaandaar conclusion.

## Architecture (Topics 03–08)

| # | Sawaal | Kya badlo | Kya naapo |
|---:|---|---|---|
| 1 | Kya FIX-08 (identity once) pretraining behtar karta hai? | `HybridBlock.forward` me `x + a + m` vs `a + m` | Held-out loss, dev pass@1, 5 seeds |
| 2 | 3:1 rhythm ki jagah 1:1 ya sab linear? | `(i + 1) % 4` → `% 2`, ya `sparse=False` | Pretraining loss, aur lambi-doori tasks |
| 3 | Linear attention me decay se kya hota hai? | `S = γS + kvᵀ` (cumsum ki jagah loop) | Loss, aur Topic 05 ka recall test |
| 4 | Top-1 vs top-2 vs top-4 experts, same compute pe? | `top_k` | Loss per FLOP |

## Data (Topics 10–11)

| # | Sawaal | Kya badlo | Kya naapo |
|---:|---|---|---|
| 5 | Kitni pretraining ke baad RL sabse zyada fayda deta hai? | `--pretrain-steps 80 / 120 / 200 / 400` | RL ka gain (after − before), per family |
| 6 | Kya ek family ko pretraining se hata do to RL use "naya" sikha sakta hai? | `pretrain_batch` me ek family skip karo | Us family pe RL ke baad pass@k |

## RL (Topics 12–14)

| # | Sawaal | Kya badlo | Kya naapo |
|---:|---|---|---|
| 7 | Interference kaise kam karein? | Ek **KL penalty** add karo: `loss += β × KL(policy ‖ pretrained)` | Trained families ka gain vs untrained ka loss |
| 8 | Random hidden tests (FIX-12) se kya RL slow hota hai? | `verify(..., n_random=0)` vs `8` | Training curve, final pass@1 |
| 9 | RLOO vs GRPO normalization? | `leave_one_out` vs `(r − mean) / std` | Stability, dev curve |
| 10 | `even` kyun fail hota hai? | `--rl-families even` akele | Failed outputs padho (Topic 14 Reading 03) |

## Kaam karne ka tareeka

1. **Ek sawaal chuno.** Hypothesis likho, result se **pehle**.
2. AI assistant se code badlwao (Claude Code, Codex). Video ka point: *"AI can do all of these experiments by itself."* Tumhara kaam sawaal aur judgment hai.
3. **3+ seeds** chalao, har ek ka alag `--out` folder rakho.
4. Receipts compare karo (Topic 11 ka `paired_sign_flip`).
5. Imaandaar conclusion likho: kya measure hua, kya nahi.
6. **Share karo.** Video (43:48): *"Keep posting your experiments every day or every week on social media. Consistency is more important than intensity."*

## Aur seekhne ke liye

- **Vuk Rosić** ka YouTube aur unki research community (root README me links)
- **freeCodeCamp** pe aur free courses
- Papers jo is course me aaye: ViT, RoPE, RMSNorm, Switch Transformer (MoE), Hyper-Connections / mHC, DeepSeek-V3.2 (DSA), DeepSeekMath (GRPO), Codex (pass@k)

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [04 · Results — hamara asli run, aur rasta me mile surprises](04-results-and-surprises.md) | 📚 [Topic 15 overview](README.md) | [06 · Final recap — poora course, ek page me](06-final-recap.md) ➡️ |
<!-- /nav:bottom -->
