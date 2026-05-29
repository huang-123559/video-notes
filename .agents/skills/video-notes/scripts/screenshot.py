#!/usr/bin/env python3
"""Capture screenshots from video at specified timestamps.

Usage:
    python screenshot.py <video_file> --times TIME [TIME ...] [--output DIR] [--prefix NAME]
    python screenshot.py <video_file> --json FILE [--output DIR]

Examples:
    python screenshot.py video.mp4 --times 12.5 45.0 120.0
    python screenshot.py video.mp4 --times 0:12 1:30 2:00 --output screenshots/
    python screenshot.py video.mp4 --json transcript.json --output screenshots/
"""

import argparse
import json
import os
import subprocess
import sys


def check_ffmpeg():
    """Check if ffmpeg is installed and accessible."""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return False


def parse_time(time_str):
    """Parse time string to seconds. Supports formats: SS.s, MM:SS, HH:MM:SS."""
    try:
        # Try direct float conversion
        return float(time_str)
    except ValueError:
        pass

    # Try MM:SS or HH:MM:SS format
    parts = time_str.split(':')
    try:
        if len(parts) == 2:
            minutes, seconds = parts
            return int(minutes) * 60 + float(seconds)
        elif len(parts) == 3:
            hours, minutes, seconds = parts
            return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    except ValueError:
        pass

    raise ValueError(f"Invalid time format: {time_str}")


def format_timestamp(seconds):
    """Format seconds to readable timestamp for filename."""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}-{secs:02d}"


def capture_screenshot(video_path, time_seconds, output_path):
    """Capture a single screenshot from video at specified time."""
    cmd = [
        "ffmpeg",
        "-ss", str(time_seconds),
        "-i", video_path,
        "-frames:v", "1",
        "-q:v", "2",  # High quality JPEG
        "-y",  # Overwrite output
        output_path
    ]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return True
        else:
            print(f"ffmpeg error at {time_seconds}s: {result.stderr}", file=sys.stderr)
            return False
    except subprocess.TimeoutExpired:
        print(f"ffmpeg timed out capturing at {time_seconds}s", file=sys.stderr)
        return False


def load_segments_from_json(json_path):
    """Load segments from JSON file (output of transcribe.py --timestamps)."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, dict) and "segments" in data:
        return data["segments"]
    elif isinstance(data, list):
        return data
    else:
        print("ERROR: Invalid JSON format. Expected {segments: [...]} or [...]", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Capture screenshots from video at specified timestamps"
    )
    parser.add_argument("video", help="Path to the MP4 video file")
    parser.add_argument("--times", nargs="+",
                       help="Timestamps to capture (seconds or MM:SS format)")
    parser.add_argument("--json",
                       help="JSON file with segments from transcribe.py --timestamps")
    parser.add_argument("--output", "-o", default="screenshots",
                       help="Output directory for screenshots (default: screenshots)")
    parser.add_argument("--prefix", "-p", default="screenshot",
                       help="Filename prefix (default: screenshot)")
    args = parser.parse_args()

    # Validate inputs
    if not os.path.isfile(args.video):
        print(f"ERROR: Video file not found: {args.video}", file=sys.stderr)
        sys.exit(1)

    if not args.times and not args.json:
        print("ERROR: Must specify either --times or --json", file=sys.stderr)
        sys.exit(1)

    # Check ffmpeg
    if not check_ffmpeg():
        print("ERROR: ffmpeg is not installed.", file=sys.stderr)
        print("Install: winget install ffmpeg", file=sys.stderr)
        sys.exit(1)

    # Collect timestamps
    timestamps = []
    if args.json:
        segments = load_segments_from_json(args.json)
        for seg in segments:
            if "start" in seg:
                timestamps.append({
                    "time": seg["start"],
                    "text": seg.get("text", "")[:50]  # First 50 chars for label
                })
    else:
        for t in args.times:
            timestamps.append({
                "time": parse_time(t),
                "text": ""
            })

    # Create output directory
    os.makedirs(args.output, exist_ok=True)

    # Capture screenshots
    results = []
    for i, ts in enumerate(timestamps):
        time_sec = ts["time"]
        timestamp_str = format_timestamp(time_sec)
        filename = f"{args.prefix}_{i+1:03d}_{timestamp_str}.jpg"
        output_path = os.path.join(args.output, filename)

        print(f"Capturing {i+1}/{len(timestamps)} at {timestamp_str}...", file=sys.stderr)
        if capture_screenshot(args.video, time_sec, output_path):
            results.append({
                "time": time_sec,
                "file": output_path,
                "text": ts["text"]
            })
        else:
            print(f"WARNING: Failed to capture at {timestamp_str}", file=sys.stderr)

    # Output results as JSON
    print(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\nCaptured {len(results)}/{len(timestamps)} screenshots to {args.output}/", file=sys.stderr)


if __name__ == "__main__":
    main()
