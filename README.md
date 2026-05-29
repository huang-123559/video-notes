# Video Notes

[English](#english) | [中文](#中文)

---

## 中文

将 MP4 视频内容自动整理成结构化的中文 Markdown 笔记。

### 功能特点

- 自动从 MP4 视频中提取音频
- 使用 Whisper 进行语音转文字
- 智能分析内容并生成结构化笔记
- 支持中英日等多种语言的视频
- 输出格式化的中文 Markdown 笔记
- 支持自动截取关键帧截图
- 提供精简版和完整版两种 SKILL 模板

### 前置要求

1. **ffmpeg** - 用于从视频中提取音频
2. **whisper** - 用于语音转文字（二选一）
   - `faster-whisper`（推荐，更轻量快速）
   - `openai-whisper`（原版）

### 安装

```bash
# 安装 ffmpeg (Windows)
winget install ffmpeg
# 或从 https://ffmpeg.org/download.html 下载并添加到 PATH

# 安装 whisper（二选一）

# 选项 A: faster-whisper（推荐）
pip install faster-whisper

# 选项 B: openai-whisper
pip install openai-whisper
```

**注意**：如果安装超时，可以使用镜像源：
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple faster-whisper
```

### 使用方法

在 opencode 中使用此 skill：

```
帮我把这个视频整理成笔记：C:\Videos\lecture.mp4
```

或者：
```
Summarize this video into Chinese notes: C:\Videos\lecture.mp4
```

脚本会自动：
1. 提取视频音频
2. 转录为文字
3. 生成结构化中文笔记
4. 保存为 Markdown 文件

### 转录脚本选项

```bash
python scripts/transcribe.py <video_file> [options]

# 选项：
#   --model MODEL      Whisper 模型大小 (tiny, base, small, medium, large)，默认 base
#   --language LANG    强制指定语言 (如 zh, en, ja)，默认自动检测
#   --output FILE      保存转录文本到文件而非标准输出
#   --timestamps       输出带时间戳的 JSON 格式（用于截图）
```

### 截图脚本选项

```bash
python scripts/screenshot.py <video_file> [options]

# 选项：
#   --times TIME [TIME ...]  指定截图时间点（秒或 MM:SS 格式）
#   --json FILE              使用 transcribe.py 生成的 JSON 文件自动截图
#   --output DIR             输出目录（默认：screenshots）
#   --prefix NAME            文件名前缀（默认：screenshot）
```

### 笔记输出格式

生成的笔记包含以下部分：
- **概述** - 视频核心内容概括
- **命令速查表** - 视频中出现的所有命令和操作
- **快捷键** - 视频中提到的所有快捷键
- **要点总结** - 按主题分组的详细要点（含截图）
- **操作步骤** - 教程类视频的完整步骤
- **常见问题与解决** - 视频中提到的常见问题
- **最佳实践** - 视频中提到的最佳实践
- **工具/资源列表** - 视频中提到的工具和资源
- **关键概念** - 专业术语解释
- **对比分析** - 工具或方案对比
- **核心结论** - 主要收获
- **延伸思考** - 未来趋势和启发

---

## English

Automatically generate structured Chinese Markdown notes from MP4 video content.

### Features

- Extract audio from MP4 videos automatically
- Speech-to-text using Whisper
- Intelligent content analysis and structured note generation
- Support for videos in multiple languages (Chinese, English, Japanese, etc.)
- Formatted Chinese Markdown output
- Automatic key frame screenshot capture
- Both simplified and full SKILL templates available

### Prerequisites

1. **ffmpeg** - for extracting audio from video
2. **whisper** - for speech-to-text (choose one)
   - `faster-whisper` (recommended, lighter and faster)
   - `openai-whisper` (original)

### Installation

```bash
# Install ffmpeg (Windows)
winget install ffmpeg
# Or download from https://ffmpeg.org/download.html and add to PATH

# Install whisper (choose one)

# Option A: faster-whisper (recommended)
pip install faster-whisper

# Option B: openai-whisper
pip install openai-whisper
```

### Usage

Use this skill in opencode:

```
帮我把这个视频整理成笔记：C:\Videos\lecture.mp4
```

Or:
```
Summarize this video into Chinese notes: C:\Videos\lecture.mp4
```

The script will automatically:
1. Extract audio from video
2. Transcribe to text
3. Generate structured Chinese notes
4. Save as Markdown file

### Transcribe Script Options

```bash
python scripts/transcribe.py <video_file> [options]

# Options:
#   --model MODEL      Whisper model size (tiny, base, small, medium, large), default: base
#   --language LANG    Force language (e.g., zh, en, ja), default: auto-detect
#   --output FILE      Save transcript to file instead of stdout
#   --timestamps       Output JSON with timestamps (for screenshots)
```

### Screenshot Script Options

```bash
python scripts/screenshot.py <video_file> [options]

# Options:
#   --times TIME [TIME ...]  Timestamps to capture (seconds or MM:SS format)
#   --json FILE              Use JSON from transcribe.py for auto-capture
#   --output DIR             Output directory (default: screenshots)
#   --prefix NAME            Filename prefix (default: screenshot)
```

### Note Output Format

Generated notes include:
- **Overview** - Core content summary
- **Command Reference** - All commands and operations from the video
- **Keyboard Shortcuts** - All keyboard shortcuts mentioned
- **Key Points** - Detailed points grouped by topic (with screenshots)
- **Steps** - Complete tutorial steps (if applicable)
- **Common Issues & Solutions** - Common problems mentioned
- **Best Practices** - Best practices from the video
- **Tools/Resources** - Tools and resources mentioned
- **Key Concepts** - Technical term explanations
- **Comparisons** - Tool or approach comparisons
- **Conclusions** - Main takeaways
- **Further Thinking** - Future trends and insights

---

## 项目结构 / Project Structure

```
video-notes/
├── .agents/
│   └── skills/
│       └── video-notes/
│           ├── SKILL.md          # 完整版 SKILL 定义
│           ├── scripts/
│           │   ├── transcribe.py # 转录脚本
│           │   └── screenshot.py # 截图脚本
│           └── evals/
│               └── evals.json    # 评估文件
├── SKILL-精简.md                 # 精简版 SKILL 定义
├── AGENTS.md                     # OpenCode 代理配置
├── README.md                     # 本文件
└── LICENSE                       # MIT 许可证
```

---

## License

MIT License - see [LICENSE](LICENSE) for details.
