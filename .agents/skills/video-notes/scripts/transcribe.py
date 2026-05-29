#!/usr/bin/env python3
"""Extract audio from MP4 and transcribe using Whisper.

Usage:
    python transcribe.py <video_file> [--model MODEL] [--language LANG] [--output FILE] [--timestamps]

Examples:
    python transcribe.py "C:/Videos/lecture.mp4"
    python transcribe.py video.mp4 --model medium --language zh
    python transcribe.py video.mp4 --output transcript.txt
    python transcribe.py video.mp4 --timestamps --output transcript.json
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile


def check_ffmpeg():
    """Check if ffmpeg is installed and accessible."""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return True, result.stdout.split('\n')[0]
    except FileNotFoundError:
        pass
    except subprocess.TimeoutExpired:
        pass
    return False, None


def check_whisper():
    """Check which whisper implementation is available."""
    # Try faster-whisper first (lighter, faster)
    try:
        import faster_whisper
        return True, "faster-whisper", faster_whisper.__version__
    except ImportError:
        pass

    # Try original whisper
    try:
        import whisper
        return True, "whisper", whisper.__version__
    except ImportError:
        pass

    return False, None, None


def get_video_duration(video_path):
    """Get video duration using ffprobe."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "csv=p=0", video_path],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            duration = float(result.stdout.strip())
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            return f"{minutes:02d}:{seconds:02d}", duration
    except (ValueError, subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return "Unknown", 0


def extract_audio(video_path, output_path):
    """Extract audio from video using ffmpeg."""
    cmd = [
        "ffmpeg", "-i", video_path,
        "-vn",  # No video
        "-acodec", "pcm_s16le",  # PCM 16-bit
        "-ar", "16000",  # 16kHz sample rate (Whisper's expected rate)
        "-ac", "1",  # Mono
        "-y",  # Overwrite output
        output_path
    ]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=300
        )
        if result.returncode == 0:
            return True
        else:
            print(f"ffmpeg error: {result.stderr}", file=sys.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("ffmpeg timed out during audio extraction", file=sys.stderr)
        return False


def transcribe_with_faster_whisper(audio_path, model_size="base", language=None, timestamps=False):
    """Transcribe using faster-whisper."""
    from faster_whisper import WhisperModel

    print(f"Loading faster-whisper model '{model_size}'...", file=sys.stderr)
    try:
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
    except Exception as e:
        print(f"ERROR: Failed to load model: {e}", file=sys.stderr)
        return None

    print("Transcribing audio...", file=sys.stderr)
    try:
        segments, info = model.transcribe(
            audio_path,
            language=language,
            beam_size=5,
            vad_filter=True
        )

        # Collect segment data
        text_parts = []
        segments_data = []
        for segment in segments:
            text_parts.append(segment.text)
            if timestamps:
                segments_data.append({
                    "start": round(segment.start, 2),
                    "end": round(segment.end, 2),
                    "text": segment.text.strip()
                })

        if timestamps:
            return {"segments": segments_data}
        return " ".join(text_parts)
    except Exception as e:
        print(f"ERROR: Transcription failed: {e}", file=sys.stderr)
        return None


def transcribe_with_whisper(audio_path, model_size="base", language=None, timestamps=False):
    """Transcribe using original openai-whisper."""
    import whisper

    print(f"Loading Whisper model '{model_size}'...", file=sys.stderr)
    try:
        model = whisper.load_model(model_size)
    except Exception as e:
        print(f"ERROR: Failed to load Whisper model: {e}", file=sys.stderr)
        return None

    print("Transcribing audio...", file=sys.stderr)
    try:
        options = {}
        if language:
            options["language"] = language

        result = model.transcribe(audio_path, **options)
        
        if timestamps:
            segments_data = []
            for segment in result["segments"]:
                segments_data.append({
                    "start": round(segment["start"], 2),
                    "end": round(segment["end"], 2),
                    "text": segment["text"].strip()
                })
            return {"segments": segments_data}
        return result["text"]
    except Exception as e:
        print(f"ERROR: Transcription failed: {e}", file=sys.stderr)
        return None


def transcribe_audio(audio_path, model_size="base", language=None, timestamps=False):
    """Transcribe audio using available whisper implementation."""
    has_whisper, whisper_type, _ = check_whisper()

    if not has_whisper:
        print("ERROR: No whisper implementation found.", file=sys.stderr)
        print("", file=sys.stderr)
        print("Install one of:", file=sys.stderr)
        print("  pip install faster-whisper  (recommended, lighter)", file=sys.stderr)
        print("  pip install openai-whisper", file=sys.stderr)
        return None

    if whisper_type == "faster-whisper":
        return transcribe_with_faster_whisper(audio_path, model_size, language, timestamps)
    else:
        return transcribe_with_whisper(audio_path, model_size, language, timestamps)


def main():
    parser = argparse.ArgumentParser(
        description="Extract audio from MP4 and transcribe using Whisper"
    )
    parser.add_argument("video", help="Path to the MP4 video file")
    parser.add_argument("--model", default="base",
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model size (default: base)")
    parser.add_argument("--language", help="Force language (e.g., zh, en, ja)")
    parser.add_argument("--output", help="Save transcript to file instead of stdout")
    parser.add_argument("--timestamps", action="store_true",
                       help="Output segments with timestamps as JSON")
    args = parser.parse_args()

    # Validate video file
    if not os.path.isfile(args.video):
        print(f"ERROR: Video file not found: {args.video}", file=sys.stderr)
        sys.exit(1)

    if not args.video.lower().endswith('.mp4'):
        print("WARNING: File does not have .mp4 extension. Attempting anyway.", file=sys.stderr)

    # Check dependencies
    ffmpeg_ok, ffmpeg_ver = check_ffmpeg()
    has_whisper, whisper_type, whisper_ver = check_whisper()

    if not ffmpeg_ok:
        print("ERROR: ffmpeg is not installed.", file=sys.stderr)
        print("", file=sys.stderr)
        print("Install it using one of these methods:", file=sys.stderr)
        print("  Windows: winget install ffmpeg", file=sys.stderr)
        print("  Or download from: https://ffmpeg.org/download.html", file=sys.stderr)
        print("", file=sys.stderr)
        print("After installation, make sure ffmpeg is in your PATH.", file=sys.stderr)
        sys.exit(1)

    if not has_whisper:
        print("ERROR: No whisper implementation found.", file=sys.stderr)
        print("", file=sys.stderr)
        print("Install one of:", file=sys.stderr)
        print("  pip install faster-whisper  (recommended, lighter)", file=sys.stderr)
        print("  pip install openai-whisper", file=sys.stderr)
        print("", file=sys.stderr)
        print("After installation, run this script again.", file=sys.stderr)
        sys.exit(1)

    print(f"Using ffmpeg: {ffmpeg_ver}", file=sys.stderr)
    print(f"Using {whisper_type} version: {whisper_ver}", file=sys.stderr)

    # Get video info
    duration_str, duration_secs = get_video_duration(args.video)
    print(f"Video duration: {duration_str}", file=sys.stderr)

    # Extract audio to temporary file
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, "audio.wav")

        print("Extracting audio...", file=sys.stderr)
        if not extract_audio(args.video, audio_path):
            print("ERROR: Failed to extract audio from video.", file=sys.stderr)
            sys.exit(1)

        # Transcribe
        transcript = transcribe_audio(audio_path, args.model, args.language, args.timestamps)

    if transcript is None:
        print("ERROR: Transcription failed.", file=sys.stderr)
        sys.exit(1)

    # Output
    if args.output:
        if args.timestamps:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(transcript, f, ensure_ascii=False, indent=2)
        else:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(transcript)
        print(f"Transcript saved to: {args.output}", file=sys.stderr)
    else:
        if args.timestamps:
            print(json.dumps(transcript, ensure_ascii=False, indent=2))
        else:
            print(transcript)

    print("Done!", file=sys.stderr)


if __name__ == "__main__":
    main()
