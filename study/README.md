# 🎓 GLM-5.3-Flash Classroom — AI Research seekho, chhote steps me

> [!NOTE]
> **🗣️ Language: Hinglish (Hindi in Roman script + English technical terms), not English.**
> The notes are written for Hindi/Urdu speakers. If you're looking for English material, please use the [original video](https://www.youtube.com/watch?v=-gfgQfw2g_E) and [repo](https://github.com/vukrosic/glm-5.3-flash-from-scratch) instead.

**Main source:** [Build & Train GLM-5.3-Flash From Scratch](https://www.youtube.com/watch?v=-gfgQfw2g_E) by **Vuk Rosić** ([@vukrosic](https://www.youtube.com/@vukrosic)), published free by **[freeCodeCamp.org](https://www.freecodecamp.org)** 🙏 (full credits in the [root README](../README.md))
**Code:** `sources/repo/` (submodule) · **Transcript:** `sources/transcript/` · **Video:** `sources/video/` (download separately, see root README)
**Slides vs transcript check:** `sources/SLIDES_VS_TRANSCRIPT.md`

<!-- nav:start -->
▶️ **Shuru karo:** [Topic 01 — Tokens aur Tokenizer](01-tokens-aur-tokenizer/README.md)
<!-- /nav:start -->

## Is classroom ka rule

- Har file **1–2 page** ki hai. Ek baar me ek hi file padho.
- Har topic me same pattern hai:
  1. **Concept** — idea kya hai, analogy ke saath
  2. **Definitions** — exact words ka matlab
  3. **Practical knowledge** — real models me ye kaise use hota hai
  4. **Real-life example**
  5. **Code lab** — khud run karo, khud todo
  6. **Recap + Quiz** — khud ko test karo
- Har reading ke end me `🎬 Video:` timestamp diya hai, us part ko video me dekh lo.

## Kaise run karein

```bash
uv sync                                                   # ek baar
uv run study/01-tokens-aur-tokenizer/lab_tokenizer.py
uv run study/02-embeddings-aur-output-head/lab_embeddings.py
uv run study/03-rmsnorm/lab_rmsnorm.py
uv run study/04-rope-position/lab_rope.py
uv run study/05-attention-aur-linear-attention/lab_linear_attention.py
uv run study/06-sparse-attention-aur-hybrid-rhythm/lab_sparse_attention.py
uv run study/07-mixture-of-experts/lab_moe.py
uv run study/08-hyper-connections/lab_hyper_connections.py
uv run study/09-vision-image-to-tokens/lab_vision.py
uv run study/10-pretraining-loop/lab_pretrain.py                 # ~2 min
uv run study/11-research-data-experiments/lab_experiments.py     # --run se khud experiment (~90 sec)
uv run study/12-rl-executable-rewards/lab_rewards.py
uv run study/13-rloo-advantage-last-block/lab_rloo.py            # --run se CPU pe RL (~2.5 min)
uv run study/14-evaluation-honest-results/lab_evaluation.py
uv run study/15-capstone-full-glm-training/glm53_full.py --stages pretrain,rl,eval,vision   # ~5 min
```

## Syllabus (✅ ready · ⏳ review ke baad)

| # | Topic | Video | Status |
|---|---|---|---|
| 01 | [Tokens aur Tokenizer (BPE vs Byte)](01-tokens-aur-tokenizer/) | 05:00–07:00 | ✅ |
| 02 | [Embeddings, Output Head aur Weight Tying](02-embeddings-aur-output-head/) | 07:00–08:30, 10:47–14:30 | ✅ |
| 03 | [RMSNorm: numbers ko control me rakhna](03-rmsnorm/) | 14:27 | ✅ |
| 04 | [RoPE: position ka pata kaise chalta hai](04-rope-position/) | 15:10 | ✅ |
| 05 | [Attention basics → Linear attention (running memory)](05-attention-aur-linear-attention/) | 16:00–19:00 | ✅ |
| 06 | [Sparse attention + the 3:1 hybrid rhythm](06-sparse-attention-aur-hybrid-rhythm/) | 18:38 | ✅ |
| 07 | [Mixture of Experts (router, top-k, shared expert)](07-mixture-of-experts/) | 20:00 | ✅ |
| 08 | [Hyper-connections (4 residual streams)](08-hyper-connections/) | 11:30, 21:30 | ✅ |
| 09 | [Vision: image → 16 tokens](09-vision-image-to-tokens/) | 23:07 | ✅ |
| 10 | [Pretraining loop: cross-entropy, AdamW, grad clipping](10-pretraining-loop/) | 26:14 | ✅ |
| 11 | [Research skill: data diversity, ordering, curriculum](11-research-data-experiments/) | 28:26 | ✅ |
| 12 | [RL with executable rewards + verifier](12-rl-executable-rewards/) | 30:30 | ✅ |
| 13 | [RLOO / advantage, last-block training](13-rloo-advantage-last-block/) | 36:59 | ✅ |
| 14 | [Evaluation: train/dev/confirm, pass@k, seeds, significance](14-evaluation-honest-results/) | 38:00–44:00 | ✅ |
| 15 | [🎓 Capstone: poora GLM-5.3 pipeline ek file me](15-capstone-full-glm-training/) | sab | ✅ |

> 🎉 Saare 15 topics ready hain. Format, length, Hinglish ka level ya labs me kuch change chahiye to batao.
