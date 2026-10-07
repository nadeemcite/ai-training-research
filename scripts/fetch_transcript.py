"""Fetch a YouTube transcript and save it as timestamped text + JSON.

Usage: uv run scripts/fetch_transcript.py <video_id_or_url> [out_dir]
"""

import json
import re
import sys
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi


def video_id(arg: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", arg)
    return m.group(1) if m else arg


def fmt(seconds: float) -> str:
    s = int(seconds)
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


def main() -> None:
    vid = video_id(sys.argv[1])
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "sources/transcript")
    out.mkdir(parents=True, exist_ok=True)

    snippets = YouTubeTranscriptApi().fetch(vid, languages=["en"]).to_raw_data()

    (out / f"{vid}.json").write_text(json.dumps(snippets, indent=2))
    lines = [f"[{fmt(s['start'])}] {s['text']}" for s in snippets]
    (out / f"{vid}.txt").write_text("\n".join(lines) + "\n")
    print(f"Saved {len(snippets)} snippets to {out}/{vid}.{{txt,json}}")


if __name__ == "__main__":
    main()
