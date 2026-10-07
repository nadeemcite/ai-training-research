# ai-training-research

A personal AI-research classroom built around one excellent free course. It has short readings and a runnable CPU code lab for each concept.

> [!IMPORTANT]
> **🗣️ Language: the study notes are in Hinglish, not English.**
>
> Hinglish is Hindi written in the Roman (English) alphabet and mixed with English technical words. Here is a real sentence from the notes:
>
> *"Har layer se pehle vector ka size 1 kar do. Vector ki **direction** (pattern/meaning) wahi rehti hai, sirf uska overall **size** fix ho jaata hai."*
>
> **If you can read that comfortably, you're in the right place. 🎉** If not, the notes probably won't work well for you. Please don't spend time on them; go straight to the original English course instead:
> - 📺 [The video](https://www.youtube.com/watch?v=-gfgQfw2g_E) (English, by Vuk Rosić on freeCodeCamp)
> - 💻 [The original code, slides and reports](https://github.com/vukrosic/glm-5.3-flash-from-scratch) (English)
>
> What *is* language-independent here: the **code labs** (`study/*/lab_*.py`) are plain Python with English code. Only their comments and printed labels are in Hinglish. The [`SLIDES_VS_TRANSCRIPT.md`](sources/SLIDES_VS_TRANSCRIPT.md) analysis and this README are in English.

**Start here → [`study/README.md`](study/README.md)** *(Hinglish)* · **Full pipeline in one file → [`glm53_full.py`](study/15-capstone-full-glm-training/glm53_full.py)**

---

## 🙏 The course this is built on

[![Build & Train a GLM-5.3-Flash Model From Scratch with Python](https://img.youtube.com/vi/-gfgQfw2g_E/maxresdefault.jpg)](https://www.youtube.com/watch?v=-gfgQfw2g_E)

### ▶️ [Build & Train a GLM-5.3-Flash Model From Scratch with Python](https://www.youtube.com/watch?v=-gfgQfw2g_E)

**Created by [Vuk Rosić](https://www.youtube.com/@vukrosic)** · **Published by [freeCodeCamp.org](https://www.youtube.com/@freecodecamp)** · 44 min · October 2026

Everything in this repo exists because of this video. Please **watch it first, and watch it on YouTube**. Views, likes and comments on the original are what keep free education like this coming.

## ❤️ Credits & gratitude

### Vuk Rosić: creator, teacher, researcher

This whole classroom stands on Vuk's work. He built a working 25.7M-parameter GLM-5.3-Flash from scratch: hybrid linear + sparse attention, mixture of experts, hyper-connections, vision, pretraining and RL. He trained it on a single machine, measured every claim honestly, and then **gave all of it away for free**: the code, the slides, the experiments and the reports.

Even more valuable than the code is his message: an AI researcher's real job is **asking good questions and designing honest experiments**. He shows that you don't need a GPU cluster to learn this. You can do real research on a CPU. That idea shaped how every chapter here is written: each one ends with a research question, not just a quiz.

Thank you, Vuk. 🙏

- 📺 YouTube: [@vukrosic](https://www.youtube.com/@vukrosic)
- 💻 Code: [github.com/vukrosic/glm-5.3-flash-from-scratch](https://github.com/vukrosic/glm-5.3-flash-from-scratch) (MIT License, © 2026 Vuk Rosic)
- 🖥️ Slides: [slides.html](https://github.com/vukrosic/glm-5.3-flash-from-scratch/blob/main/slides/slides.html)
- 🧪 His AI research community: [Become an AI Researcher in 90 days](https://www.skool.com/become-ai-researcher-2669/about)

### freeCodeCamp.org: for making this free for everyone

freeCodeCamp is a **nonprofit** that has published thousands of hours of full-length courses for free, with no paywall and no ads in the middle of a lesson. Courses like this one would usually sit behind an expensive bootcamp. freeCodeCamp puts them in front of anyone with an internet connection, including learners like me studying in Hinglish on a laptop.

Thank you, freeCodeCamp, for publishing this course and for everything you do for learners around the world. 🙏

- 📺 YouTube: [@freecodecamp](https://www.youtube.com/@freecodecamp)
- 🌐 Learn to code for free: [freecodecamp.org](https://www.freecodecamp.org)
- 📰 Articles: [freecodecamp.org/news](https://freecodecamp.org/news)
- 💝 **If this helped you, consider supporting them:** [freecodecamp.org/donate](https://www.freecodecamp.org/donate)

### Also thanks to

- **[Z.ai](https://z.ai/blog/glm-5.3-flash)** for designing and openly describing GLM-5.3-Flash, the model this course rebuilds in miniature.
- The researchers whose ideas appear in these notes: RMSNorm, RoPE, linear attention / KDA, DeepSeek Sparse Attention, mixture of experts, and DeepSeek / ByteDance hyper-connections. Each chapter names the work it draws on.

### A note on this repo

This is an **unofficial, personal study companion**, not affiliated with or endorsed by Vuk Rosić, freeCodeCamp or Z.ai. Any mistakes in the notes are mine, not theirs. The upstream code is included unchanged as a git submodule under its MIT license. The transcript is included only as a study aid. **If any creator would like something changed or removed, please [open an issue](https://github.com/nadeemcite/ai-training-research/issues) and I'll do it right away.**

---

## Video chapters → study chapters

| Video | Topic (from the official chapter list) | Study chapter |
|---|---|---|
| [00:00](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=0s) | Introduction & What We're Building | — |
| [01:02](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=62s) | Modern AI Researcher Role & Asking Research Questions | [11 · Data experiments](study/11-research-data-experiments/) |
| [04:50](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=290s) | Tokenization: Byte-Level Vocabulary | [01 · Tokens](study/01-tokens-aur-tokenizer/) |
| [07:01](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=421s) | Embeddings & Transformer Forward Pass | [02 · Embeddings](study/02-embeddings-aur-output-head/) |
| [08:53](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=533s) | GLM-5.3 Architecture Overview & Model Specifications | — |
| [10:25](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=625s) | Code Walkthrough: Embeddings & Token Representation | [02 · Embeddings](study/02-embeddings-aur-output-head/) |
| [11:56](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=716s) | Manifold Constrained Hyperconnections | [08 · Hyper-connections](study/08-hyper-connections/) |
| [13:27](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=807s) | Output Projection & Weight Tying | [02 · Embeddings](study/02-embeddings-aur-output-head/) |
| [14:27](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=867s) | RMSNorm & Normalization Layers | [03 · RMSNorm](study/03-rmsnorm/) |
| [15:10](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=910s) | Positional Encodings (RoPE vs. NoPE) & Sparse Attention Indexer | [04 · RoPE](study/04-rope-position/) |
| [18:30](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=1110s) | Linear Attention vs. Sparse Attention | [05 · Linear](study/05-attention-aur-linear-attention/), [06 · Sparse](study/06-sparse-attention-aur-hybrid-rhythm/) |
| [20:46](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=1246s) | Mixture of Experts & Shared Experts | [07 · MoE](study/07-mixture-of-experts/) |
| [23:06](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=1386s) | Adding Vision: Patch Embeddings & 2D RoPE | [09 · Vision](study/09-vision-image-to-tokens/) |
| [26:14](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=1574s) | Pre-Training Pipeline, Loss & AdamW | [10 · Pretraining](study/10-pretraining-loop/) |
| [28:05](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=1685s) | Pre-Training Experiments: Diversity, Interleaving, Curriculum | [11 · Data experiments](study/11-research-data-experiments/) |
| [30:27](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=1827s) | Post-Training & Reinforcement Learning Setup | [12 · RL rewards](study/12-rl-executable-rewards/) |
| [34:44](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=2084s) | Reward Functions & GRPO | [12 · RL rewards](study/12-rl-executable-rewards/), [13 · RLOO](study/13-rloo-advantage-last-block/) |
| [37:37](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=2257s) | Parameter-Efficient RL Updates & Freezing Layers | [13 · RLOO](study/13-rloo-advantage-last-block/) |
| [39:35](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=2375s) | Evaluating RL Results: Task Gains & Regression Risks | [14 · Evaluation](study/14-evaluation-honest-results/) |
| [40:47](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=2447s) | RL Hyperparameter Experiments: Group Size, Temperature & Seeds | [14 · Evaluation](study/14-evaluation-honest-results/) |
| [43:03](https://www.youtube.com/watch?v=-gfgQfw2g_E&t=2583s) | Summary & Advice for Aspiring AI Researchers | [15 · Capstone](study/15-capstone-full-glm-training/) |

---

## Repo layout

```
sources/
  repo/         git submodule → github.com/vukrosic/glm-5.3-flash-from-scratch (pinned at 96d9c7c)
  transcript/   timestamped transcript (.txt) + raw snippets (.json)
  video/        (not committed) downloaded video, see below
  SLIDES_VS_TRANSCRIPT.md   which slide deck matches the video, and the gaps between them
scripts/
  fetch_transcript.py       uv run scripts/fetch_transcript.py <url> [out_dir]
  build_nav.py              uv run scripts/build_nav.py   (re-run after adding a chapter or reading)
study/          (Hinglish) chapters 01–15: architecture → vision → pretraining → research → RL → evaluation → capstone
```

## Setup

```bash
git clone --recurse-submodules git@github.com:nadeemcite/ai-training-research.git
cd ai-training-research
uv sync
uv run study/01-tokens-aur-tokenizer/lab_tokenizer.py
```

Already cloned without submodules? Run `git submodule update --init`.

## Download the video for offline study (optional, not committed)

Please watch on [YouTube](https://www.youtube.com/watch?v=-gfgQfw2g_E) first, because that supports the creators. For personal offline viewing:

```bash
uv run yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "sources/video/%(title)s [%(id)s].%(ext)s" "https://www.youtube.com/watch?v=-gfgQfw2g_E"
```
