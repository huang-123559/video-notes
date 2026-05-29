# AGENTS.md

## What this repo is

An OpenCode skill that converts MP4 videos into structured Chinese Markdown notes. No application code, no build system, no tests — just a skill definition and two Python helper scripts.

## Key files

- `.agents/skills/video-notes/SKILL.md` — the skill definition; contains the full workflow, output template, and guidelines. **Read this before doing anything.**
- `.agents/skills/video-notes/scripts/transcribe.py` — extracts audio via ffmpeg, transcribes via Whisper
- `.agents/skills/video-notes/scripts/screenshot.py` — captures JPEG screenshots at timestamps using ffmpeg
- `transcript.txt` — a sample/test transcript (not an input artifact)

## External dependencies (not installable via pip alone)

- **ffmpeg** must be on PATH. Install: `winget install ffmpeg`
- **Whisper** (one of):
  - `pip install faster-whisper` (recommended)
  - `pip install openai-whisper`

If pip times out, use Tsinghua mirror: `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple faster-whisper`

## Running the scripts

```bash
# Transcribe (stdout)
python .agents/skills/video-notes/scripts/transcribe.py "<video.mp4>"

# Transcribe with timestamps (JSON output, needed for screenshots)
python .agents/skills/video-notes/scripts/transcribe.py "<video.mp4>" --timestamps --output transcript.json

# Screenshots from timestamps
python .agents/skills/video-notes/scripts/screenshot.py "<video.mp4>" --json transcript.json --output screenshots/
```

Script options: `--model {tiny,base,small,medium,large}`, `--language {zh,en,ja}`, `--output FILE`, `--timestamps`

## Conventions

- **All notes output in Chinese**, regardless of video language.
- Notes are saved as `<video_name>笔记.md` in the same directory as the video.
- Screenshots go in a `screenshots/` folder next to the notes.
- Screenshot filenames: `{prefix}_{NNN}_{MM-SS}.jpg`
- The skill's `<skill-path>` placeholder in SKILL.md resolves to `.agents/skills/video-notes/scripts/` at runtime.
