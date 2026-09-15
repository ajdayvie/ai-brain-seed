#!/usr/bin/env python3
"""
render-digest.py — turn an audio-digest markdown file into a pre-rendered MP3.

Used by the `audio-digest` skill. Reads a digest file from `<vault>/digests/`,
strips everything that is filing metadata rather than script, and renders the
spoken body with edge-tts (Microsoft neural voices; free, no API key, needs a
network connection).

Usage:
    python render-digest.py <path-to-digest.md> [--voice NAME] [--rate PCT] [--dry-run]

Prints one line of JSON to stdout:
    {"ok": true, "audio": "...mp3", "seconds": 271.4, "words": 780, "wpm": 172}

Exit codes: 0 ok, 1 bad input, 2 render failed (network/edge-tts).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# Warm, conversational, closest of the free voices to an explaining colleague.
DEFAULT_VOICE = "en-US-AndrewMultilingualNeural"

# Negative rate slows delivery. Digests are explanatory, not news reads:
# -8% lands near 170 wpm, which is a pace you can follow while driving.
DEFAULT_RATE = "-8%"

FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.DOTALL)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def strip_to_script(raw: str) -> tuple[str, str]:
    """Return (title, spoken_body). Everything not meant for the ear is removed."""
    body = FRONTMATTER.sub("", raw, count=1)
    body = HTML_COMMENT.sub("", body)

    title = ""
    lines = body.splitlines()
    out: list[str] = []
    for line in lines:
        if not title and line.startswith("# "):
            title = line[2:].strip()
            continue
        # A digest body should carry no headings at all. If one slipped in,
        # speak its text rather than dropping the content on the floor.
        if line.startswith("#"):
            out.append(line.lstrip("#").strip())
            continue
        out.append(line)

    text = "\n".join(out)

    # Defensive cleanup. By spec the body is plain spoken prose, but a stray
    # link or emphasis marker must never be read aloud as punctuation noise.
    text = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", text)   # [[page|label]]
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)              # [[page]]
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)         # [text](url)
    text = re.sub(r"`{1,3}([^`]*)`{1,3}", r"\1", text)           # code spans
    text = re.sub(r"(\*\*|__|\*|_)", "", text)                   # emphasis
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.M)         # bullets
    text = re.sub(r"^\s*>\s?", "", text, flags=re.M)             # quotes
    text = re.sub(r"[‘’]", "'", text)
    text = re.sub(r"[“”]", '"', text)
    text = re.sub(r"[—–]", ", ", text)                 # dashes -> a beat
    text = re.sub(r"[^\x00-\x7F]+", " ", text)                   # emoji, symbols
    text = re.sub(r"\n{3,}", "\n\n", text)

    return title, text.strip()


def duration_seconds(path: Path) -> float | None:
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(path)],
            capture_output=True, text=True, timeout=60,
        )
        return round(float(r.stdout.strip()), 1)
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("digest", type=Path)
    ap.add_argument("--voice", default=DEFAULT_VOICE)
    ap.add_argument("--rate", default=DEFAULT_RATE)
    ap.add_argument("--dry-run", action="store_true",
                    help="print the spoken text and exit; render nothing")
    args = ap.parse_args()

    if not args.digest.is_file():
        print(json.dumps({"ok": False, "error": f"no such file: {args.digest}"}))
        return 1

    title, script = strip_to_script(args.digest.read_text(encoding="utf-8"))
    if not script:
        print(json.dumps({"ok": False, "error": "no spoken body found"}))
        return 1

    # The title is spoken first so the file identifies itself when scrubbed to
    # from a car stereo, where no filename is visible.
    spoken = f"{title}.\n\n{script}" if title else script
    words = len(spoken.split())

    if args.dry_run:
        print(spoken)
        return 0

    audio = args.digest.with_suffix(".mp3")

    # edge-tts 7.x wants a file, not stdin. A sidecar next to the digest also
    # keeps the exact spoken text auditable when a render sounds wrong.
    txt = args.digest.with_suffix(".speech.txt")
    txt.write_text(spoken, encoding="utf-8")

    cmd = [sys.executable, "-m", "edge_tts",
           "--voice", args.voice, f"--rate={args.rate}",
           "-f", str(txt), "--write-media", str(audio)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=900)
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"ok": False, "error": f"edge-tts failed to start: {e}"}))
        return 2
    finally:
        txt.unlink(missing_ok=True)

    if proc.returncode != 0 or not audio.is_file():
        print(json.dumps({"ok": False, "error": (proc.stderr or "render failed")[-400:]}))
        return 2

    secs = duration_seconds(audio)
    print(json.dumps({
        "ok": True,
        "audio": str(audio),
        "seconds": secs,
        "words": words,
        "wpm": round(words / (secs / 60)) if secs else None,
        "voice": args.voice,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
