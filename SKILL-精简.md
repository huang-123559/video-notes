---
name: video-notes
description: "Summarize video content into structured Chinese Markdown notes. Use this skill whenever the user provides an MP4 video file (.mp4) and asks to generate notes, summarize, take notes, extract key points, or create a study guide from the video. Even if they just say 'help me take notes on this video' or mention summarizing a video file, trigger this skill."
---

# Video Notes

Generate structured Chinese Markdown notes from MP4 video files.

## Workflow

### Step 1: Extract Audio and Transcribe

Run the bundled transcription script to extract audio from the MP4 and transcribe it:

```bash
python <skill-path>/scripts/transcribe.py "<video_file_path>"
```

The script will:
1. Check if `ffmpeg` and `whisper` are installed; if not, print installation instructions and exit
2. Extract audio from the MP4 file using ffmpeg
3. Transcribe the audio to text using Whisper
4. Output the transcribed text to stdout

**Options:**
- `--model MODEL`: Whisper model size (tiny, base, small, medium, large). Default: base
- `--language LANG`: Force a specific language (e.g., zh, en, ja). Default: auto-detect
- `--output FILE`: Save transcript to a file instead of stdout

If the transcription fails, inform the user and ask them to check the video file.

### Step 2: Analyze Content

Read through the full transcript carefully and identify ALL of the following:

1. **Main topic** — what is this video about?
2. **Key themes** — identify ALL major topics covered (typically 5-10 for a 20-min video)
3. **Sub-topics** — for each theme, identify ALL sub-points and details
4. **Logical structure** — how do the themes relate? Is it sequential (tutorial), argumentative (debate), informational (lecture), or narrative (story)?
5. **Key concepts** — identify ALL specialized terms, tools, or ideas mentioned
6. **Examples and demonstrations** — note ALL specific examples, commands, or demos shown
7. **Steps and procedures** — if it's a tutorial, capture ALL steps in order
8. **Comparisons** — any comparisons between tools, approaches, or concepts
9. **Tips and tricks** — any bonus tips, shortcuts, or best practices mentioned
10. **Core conclusions** — what are the main takeaways?

**IMPORTANT**: Be thorough and comprehensive. Do NOT skip or condense content. Every important point from the video should appear in the notes.

### Step 3: Generate Notes

Output the notes in this format. Always write in Chinese, regardless of the video's original language.

```markdown
# [视频标题或主题]

> 来源：[文件名] | 时长：[XX:XX，如可知] | 原语言：[语言]

## 概述

[3-5 句话详细概括视频的核心内容、目标受众和价值]

## 要点总结

### 1. [主题一]
- 要点 1
  - 细节 a
  - 细节 b
  - 细节 c
- 要点 2
  - 细节 a
  - 细节 b
- 要点 3
  - 具体步骤或说明

### 2. [主题二]
- 要点 1
  - 细节 a
  - 细节 b
- 要点 2
  - 细节 a
  - 细节 b

### 3. [主题三]
- 要点 1
- 要点 2
- 要点 3

[继续添加所有主题，不要遗漏...]

## 操作步骤（如适用）

如果是教程类视频，列出完整步骤：

1. **步骤一**：[描述]
   - 具体操作：[详细说明]
   - 命令/代码：`[如有]`

2. **步骤二**：[描述]
   - 具体操作：[详细说明]
   - 命令/代码：`[如有]`

[继续所有步骤...]

## 工具/资源列表

视频中提到的所有工具、资源、链接：

| 工具/资源 | 用途 | 备注 |
|---|---|---|
| [名称 1] | [用途] | [备注] |
| [名称 2] | [用途] | [备注] |

## 关键概念

视频中涉及的所有专业术语和概念：

| 概念 | 解释 |
|---|---|
| 概念 A | 详细解释 |
| 概念 B | 详细解释 |
| 概念 C | 详细解释 |

## 对比分析（如适用）

视频中提到的对比内容：

| 对比项 | 选项 A | 选项 B |
|---|---|---|
| [维度 1] | [说明] | [说明] |
| [维度 2] | [说明] | [说明] |

## 优缺点总结（如适用）

### [工具/方案 A]
**优点：**
- 优点 1
- 优点 2

**缺点：**
- 缺点 1
- 缺点 2

## 核心结论

1. [结论 1]
2. [结论 2]
3. [结论 3]
4. [结论 4]
5. [结论 5]

## 延伸思考

视频中提到的未来趋势、建议或启发：
- [启发 1]
- [启发 2]
```

### Step 4: Save to File

After generating the notes, save them to a Markdown file:

1. Use the video filename (without extension) as the output filename
2. Save to the same directory as the video file
3. Add `.md` extension

For example:
- Input: `C:\Videos\OpenCode教程.mp4`
- Output: `C:\Videos\OpenCode教程笔记.md`

Use the Write tool to save the file, then inform the user of the file path.

## Guidelines

- **Always output in Chinese** — even if the video is in English, Japanese, or any other language
- **Be faithful to the source** — summarize what was actually said, not what you think should have been said
- **Be comprehensive** — cover ALL important points, don't skip or condense content
- **Use the speaker's own terminology** — don't paraphrase technical terms unless clarification is needed
- **Group by theme, not by time** — the notes should reflect logical structure, not chronological order
- **Keep it scannable** — use bullet points, not paragraphs; the reader should be able to find information quickly
- **Don't include filler** — skip "um", "you know", repeated phrases, and off-topic tangents
- **Preserve ALL examples** — include every example, demo, and specific case mentioned
- **Include ALL commands** — if specific commands or code are shown, include them verbatim
- **Capture ALL comparisons** — any comparisons between tools or approaches should be included
- **Note ALL tips** — any bonus tips, shortcuts, or best practices should be captured

## Error Handling

- **ffmpeg or whisper not installed**: The script will output installation instructions; relay them to the user
- **Video too long (> 2 hours)**: Warn the user that notes may be very long; ask if they want a specific section summarized instead
- **Transcription quality poor**: Suggest the user try a larger Whisper model (medium or large)
- **Video has no audio**: Inform the user that the video appears to have no audio track

## Dependencies

This skill requires:
1. **ffmpeg** — for extracting audio from video files
2. **whisper** — for transcribing audio to text (two options)

### Installation

```bash
# 1. Install ffmpeg (Windows)
winget install ffmpeg
# Or download from https://ffmpeg.org/download.html and add to PATH

# 2. Install whisper (choose one)

# Option A: openai-whisper (original, requires more dependencies)
pip install openai-whisper

# Option B: faster-whisper (lighter, faster, recommended)
pip install faster-whisper
```

**Note**: If installation times out due to slow network, try:
- Using a mirror: `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple openai-whisper`
- Installing in smaller steps: first `pip install torch --index-url https://download.pytorch.org/whl/cpu`, then install whisper

## Example Usage

**User**: "帮我把这个视频整理成笔记：C:\Videos\lecture.mp4"

**Steps**:
1. Run: `python <skill-path>/scripts/transcribe.py "C:\Videos\lecture.mp4"`
2. Read the transcript output
3. Analyze content thoroughly — identify ALL themes, sub-topics, examples, steps, comparisons
4. Generate comprehensive structured Chinese Markdown notes
5. Save to: `C:\Videos\lecture笔记.md`
6. Inform user: "笔记已保存到 C:\Videos\lecture笔记.md"
