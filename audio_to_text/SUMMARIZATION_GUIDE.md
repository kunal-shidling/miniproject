# Audio Transcription with AI Summarization

Complete guide for transcribing audio and generating bullet-point summaries using Groq API.

## 🚀 Quick Setup

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Get Your Groq API Key

1. Visit https://console.groq.com/keys
2. Create a free account
3. Generate an API key
4. Set it as an environment variable:

**Windows PowerShell:**
```powershell
$env:GROQ_API_KEY = "your-api-key-here"
```

**Windows CMD:**
```cmd
set GROQ_API_KEY=your-api-key-here
```

**Permanent (Windows):**
```powershell
[System.Environment]::SetEnvironmentVariable('GROQ_API_KEY', 'your-api-key-here', 'User')
```

## 📝 Usage Examples

### Basic Transcription with Summary

Transcribe audio and get a bullet-point summary:

```powershell
python cli_transcribe.py meeting.mp3 --summarize
```

### Save to File with Summary

```powershell
python cli_transcribe.py interview.wav --output interview.txt --summarize
```

This creates two files:
- `interview.txt` - Full transcription
- `interview.summary.txt` - Bullet-point summary

### Structured Summary

Get a detailed summary with sections (Main Topics, Key Points, Action Items, Decisions):

```powershell
python cli_transcribe.py meeting.mp3 --summarize --structured-summary
```

### Custom Number of Bullet Points

```powershell
python cli_transcribe.py lecture.m4a --summarize --max-bullets 5
```

### Specify Groq Model

```powershell
python cli_transcribe.py talk.mp3 --summarize --groq-model llama-3.1-70b-versatile
```

### Complete Example with All Options

```powershell
python cli_transcribe.py meeting.mp3 `
  --model small `
  --output meeting.txt `
  --summarize `
  --structured-summary `
  --groq-model llama-3.3-70b-versatile `
  --verbose
```

## 🎯 Command-Line Arguments

### Transcription Options

| Argument | Description | Default |
|----------|-------------|---------|
| `audio_file` | Path to audio file (required) | - |
| `-m, --model` | Whisper model (tiny/base/small/medium/large) | base |
| `-l, --language` | Language code (e.g., en, es, fr) | auto-detect |
| `-t, --translate` | Translate to English | False |
| `--timestamps` | Include timestamps | False |
| `-o, --output` | Output file path | stdout |
| `-f, --format` | Output format (txt/json) | txt |
| `--device` | Device (cpu/cuda) | cpu |
| `-v, --verbose` | Verbose output | False |

### Summarization Options

| Argument | Description | Default |
|----------|-------------|---------|
| `--summarize` | Enable summarization | False |
| `--groq-api-key` | Groq API key | $GROQ_API_KEY |
| `--groq-model` | Groq model to use | llama-3.3-70b-versatile |
| `--max-bullets` | Max bullet points | 10 |
| `--structured-summary` | Use structured format | False |

## 📊 Summary Formats

### Standard Bullet Points

Simple, concise bullet points highlighting key information:

```
• Main topic discussed in the conversation
• Important decision that was made
• Key action item for follow-up
• Notable insight or conclusion
```

### Structured Summary

Organized summary with multiple sections:

```
MAIN TOPICS:
• Primary subject discussed
• Secondary topic covered

KEY POINTS:
• Important fact or detail
• Notable statistic or information
• Significant insight

ACTION ITEMS:
• Task to complete
• Follow-up required

DECISIONS:
• Decision made during conversation
• Conclusion reached
```

## 🔧 Available Groq Models

- **llama-3.3-70b-versatile** (Default) - Best balance of speed and quality
- **llama-3.1-70b-versatile** - High-quality summaries
- **mixtral-8x7b-32768** - Good for longer texts
- **gemma2-9b-it** - Faster, lightweight option

## 💡 Tips & Best Practices

### 1. Choose the Right Whisper Model

- **tiny** - Fastest, lowest quality (demo/testing)
- **base** - Good balance (default)
- **small** - Better accuracy, slower
- **medium/large** - Best quality, much slower

### 2. Optimize Summarization

- Use `--max-bullets 5-7` for quick overviews
- Use `--structured-summary` for meetings and interviews
- For long conversations (>30 min), use `small` or `medium` Whisper model

### 3. Batch Processing

Create a script to process multiple files:

```powershell
$files = Get-ChildItem *.mp3
foreach ($file in $files) {
    python cli_transcribe.py $file.Name --output "$($file.BaseName).txt" --summarize
}
```

## 🐛 Troubleshooting

### "Groq API key not found"

Make sure you've set the environment variable:
```powershell
$env:GROQ_API_KEY = "your-api-key-here"
```

Or pass it directly:
```powershell
python cli_transcribe.py audio.mp3 --summarize --groq-api-key "your-api-key-here"
```

### "Module 'groq' not found"

Install the Groq library:
```powershell
pip install groq
```

### Slow Transcription

- Use a smaller Whisper model: `--model tiny` or `--model base`
- If you have a GPU: `--device cuda`

### Summary Too Long/Short

Adjust the number of bullet points:
```powershell
--max-bullets 5  # Shorter
--max-bullets 15 # Longer
```

## 📖 Example Workflow

Complete workflow for processing a meeting recording:

```powershell
# 1. Transcribe with summary
python cli_transcribe.py meeting_2026-03-03.mp3 `
  --model small `
  --output meeting.txt `
  --summarize `
  --structured-summary `
  --verbose

# This creates:
# - meeting.txt (full transcription)
# - meeting.summary.txt (structured summary)

# 2. Review the summary
Get-Content meeting.summary.txt

# 3. Archive
Move-Item meeting.* .\archive\2026-03\
```

## 🎓 Advanced Usage

### Using as Python Module

```python
from audio_transcriber import AudioTranscriber
from text_summarizer import TextSummarizer

# Transcribe
transcriber = AudioTranscriber(model_name='base')
text = transcriber.transcribe_audio('meeting.mp3')

# Summarize
summarizer = TextSummarizer(api_key='your-api-key')
summary = summarizer.summarize_to_bullets(text, max_bullets=10)

print(summary)
```

### Standalone Text Summarization

You can also summarize existing text files:

```powershell
python text_summarizer.py transcript.txt --verbose
```

## 📞 Support

- **Groq API Issues**: https://console.groq.com/docs
- **Whisper Issues**: https://github.com/openai/whisper

## ✨ Features

✅ Multiple audio format support (MP3, WAV, M4A, FLAC, OGG, etc.)  
✅ Automatic language detection  
✅ Translation to English  
✅ Timestamp extraction  
✅ AI-powered summarization  
✅ Structured summary format  
✅ Customizable bullet point count  
✅ Multiple Groq models supported  
✅ Batch processing support  
✅ File output and console output  

---

**Happy transcribing! 🎙️➡️📝➡️✨**
