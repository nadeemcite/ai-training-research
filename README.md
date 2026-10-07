# ai-training-research

A personal AI-research classroom built around Vuk Rosić's
[Build & Train GLM-5.3-Flash From Scratch](https://www.youtube.com/watch?v=-gfgQfw2g_E).
It has short Hinglish readings and a runnable CPU code lab for each concept.

**Start here → [`study/README.md`](study/README.md)**

```
sources/
  repo/         git submodule → github.com/vukrosic/glm-5.3-flash-from-scratch (pinned at 96d9c7c)
  transcript/   timestamped transcript (.txt) + raw snippets (.json)
  video/        (not committed) downloaded video, see below
  SLIDES_VS_TRANSCRIPT.md   which slide deck matches the video, and the gaps between them
scripts/
  fetch_transcript.py       uv run scripts/fetch_transcript.py <url> [out_dir]
study/          chapters 01–07: tokens → embeddings → RMSNorm → RoPE → linear/sparse attention → MoE
```

## Setup

```bash
git clone --recurse-submodules git@github.com:nadeemcite/ai-training-research.git
cd ai-training-research
uv sync
uv run study/01-tokens-aur-tokenizer/lab_tokenizer.py
```

Already cloned without submodules? Run `git submodule update --init`.

## Download the video (optional, not committed)

```bash
uv run yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "sources/video/%(title)s [%(id)s].%(ext)s" "https://www.youtube.com/watch?v=-gfgQfw2g_E"
```
