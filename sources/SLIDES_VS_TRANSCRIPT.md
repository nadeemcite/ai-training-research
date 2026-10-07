# Slides vs Transcript — match check

Video: `-gfgQfw2g_E` · Repo commit: `96d9c7c` (2026-08-28)

## Short answer

**`slides/slides.html` (76 slides) matches the video. `slides/slides.md` (37 slides) does not, because it is an older, shorter draft.**

| File | Slides | Matches video? |
|---|---:|---|
| `repo/slides/slides.html` | 76 | ✅ Yes. Same topics in the same order, and every spoken section has a slide |
| `repo/slides/slides.md` | 37 | ⚠️ Partly. Covers only the architecture and RL core. It has no vision, RMSNorm/RoPE, or data experiments, and no RL variant screen |

To view the real deck: `cd sources/repo && python slides/serve_slides.py --port 8765` → http://127.0.0.1:8765/slides.html

## Section-by-section mapping (video → slides.html)

| Video time | What is said | slides.html # |
|---|---|---|
| 00:00–04:30 | Intro, the AI-researcher job, asking research questions | 1–14 |
| 05:00–07:00 | BPE vs byte tokens, the 260-token vocab | 15–16 |
| 07:00–08:30 | Embeddings → transformer → probability over the vocab | 17, 25 |
| 08:30–10:00 | GLM-5.3 parts: hybrid attention, MoE, hyper-connections, tied weights | 26 |
| 10:00–10:45 | 320B vs 25.7M spec table, 0/24 → 16/24 | 6–7 |
| 10:47–14:30 | Forward pass code: embedding, 4 streams, output head, weight tying | 27–28, 41 |
| 14:30–15:40 | RMSNorm, RoPE, NoPE + sparse indexer | 29–31 |
| 15:40–20:00 | Linear attention memory, the 3:1 rhythm, sparse attention | 32–36 |
| 20:00–22:30 | MoE (8 of 288 → 2 of 8 + shared), config, hybrid block | 37–40 |
| 22:28–23:00 | Weight tying (repeated) | 41 |
| 23:00–26:00 | Vision: 32×32 image → 16 tokens | 18–23 ⚠️ (comes *earlier* in the deck than in the talk) |
| 26:00–28:00 | Pretraining step, AdamW, before/after generation | 43–48 |
| 28:00–30:30 | Data diversity, ordering, curriculum experiments | 49–56 |
| 30:30–38:00 | RL: executable reward, verifier, 16 rollouts, RLOO advantage, last-block update | 57–68 |
| 38:00–40:30 | Confirmation split, per-family gains/regressions | 69–71 |
| 40:30–44:24 | RL variant screen (group size, temperature, reward shape), seeds, conclusions | 72–76 |

## Mismatches / things to note

1. **Order:** In the deck, vision (slides 18–23) comes before the architecture. In the video it is explained after weight tying.
2. **Spoken "4% → 45%"** is the *dev sampled-rollout rate* (4/96 = 4.2% → 44/96 = 45.8%, `REPORT.md`). The "0/24 → 16/24" figure is a different metric: greedy pass@1 on the *confirmation* split. Keep the two numbers separate.
3. **`slides.md` references missing assets:** `glm53-official-architecture.png`, `rl-progress.png`, `confirmation-results.png`, and `token-generation-before-after.mp4`. The repo has `pretraining-before-after.mp4` instead.
4. **Transcript ASR errors:** "GLM 5.3 flesh" means Flash. "Drupal AI" is most likely Zhipu AI (Z.ai), the company behind GLM. "deep six" means DeepSeek. "bite dense" means ByteDance. "BP tokenizers" means BPE. "cloud code" means Claude Code. "KDA" is Kimi Delta Attention.
5. **The spoken claim "nope = no positional encoding in main attention, RoPE only in indexer"** describes the *released* GLM model. The teaching model applies RoPE in its own attention for simplicity (said at 15:30, slide 31).
6. **Token IDs check:** slide "Code becomes tokens" shows `d e f ␠ x :` → `104 105 106 36 124 62`. This is correct: UTF-8 byte + offset 4 (`tokenizer.py`).
