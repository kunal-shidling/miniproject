# Quick Reference - Audio Transcription with AI Summary

## 🚀 Most Common Commands

### 1. Simple Transcription with Summary
```powershell
python cli_transcribe.py meeting.mp3 --summarize
```
**Output**: Prints transcription + bullet-point summary to console

### 2. Save to File with Summary
```powershell
python cli_transcribe.py interview.wav -o interview.txt --summarize
```
**Output**: 
- `interview.txt` - Full transcription
- `interview.summary.txt` - Bullet points

### 3. Structured Summary (Best for Meetings)
```powershell
python cli_transcribe.py meeting.mp3 --summarize --structured-summary
```
**Output**: Summary with sections:
- Main Topics
- Key Points  
- Action Items
- Decisions

### 4. Quick Summary (5 bullets)
```powershell
python cli_transcribe.py talk.mp3 --summarize --max-bullets 5
```

### 5. Better Quality Transcription
```powershell
python cli_transcribe.py audio.mp3 --model small --summarize
```

## ⚙️ Setup (One-Time)

### Install Dependencies
```powershell
pip install -r requirements.txt
```

### Get & Set Groq API Key
1. Get key: https://console.groq.com/keys
2. Set it:
```powershell
$env:GROQ_API_KEY = "your-api-key-here"
```

Or run setup script:
```powershell
.\setup_groq.ps1
```

## 📝 Summary Options

| Flag | Description | Example |
|------|-------------|---------|
| `--summarize` | Enable summarization | Required for summaries |
| `--structured-summary` | Use structured format | Better for meetings |
| `--max-bullets 5` | Set bullet count | Quick overviews |
| `--groq-model` | Choose model | Different quality/speed |

## 🎯 Whisper Models (Speed vs Quality)

| Model | Speed | Quality | Use Case |
|-------|-------|---------|----------|
| `tiny` | ⚡⚡⚡ | ⭐ | Quick tests |
| `base` | ⚡⚡ | ⭐⭐ | Default, balanced |
| `small` | ⚡ | ⭐⭐⭐ | Good quality |
| `medium` | 🐌 | ⭐⭐⭐⭐ | High quality |
| `large` | 🐌🐌 | ⭐⭐⭐⭐⭐ | Best quality |

Usage:
```powershell
python cli_transcribe.py audio.mp3 --model small --summarize
```

## 🔍 Example Outputs

### Standard Bullet Points
```
• Main topic discussed in the conversation
• Important decision that was made  
• Key action item identified
• Notable conclusion reached
```

### Structured Summary
```
MAIN TOPICS:
• Primary discussion subject
• Secondary topic covered

KEY POINTS:
• Important detail mentioned
• Significant data point

ACTION ITEMS:
• Task to be completed
• Follow-up required

DECISIONS:
• Decision made about X
• Agreement reached on Y
```

## 💡 Pro Tips

1. **For meetings/interviews**: Use `--structured-summary`
2. **For quick overview**: Use `--max-bullets 5`
3. **For better accuracy**: Use `--model small` or `--model medium`
4. **Save everything**: Use `-o filename.txt` to save both transcription and summary

## 🐛 Troubleshooting

### "Groq API key not found"
```powershell
$env:GROQ_API_KEY = "your-key-here"
```

### "Module 'groq' not found"
```powershell
pip install groq
```

### Transcription too slow
```powershell
python cli_transcribe.py audio.mp3 --model tiny --summarize
```

## 📖 Full Documentation

- **Complete Guide**: [SUMMARIZATION_GUIDE.md](SUMMARIZATION_GUIDE.md)
- **Main README**: [README.md](README.md)

## 🎓 Batch Processing Multiple Files

```powershell
# Process all MP3 files in current directory
Get-ChildItem *.mp3 | ForEach-Object {
    python cli_transcribe.py $_.Name -o "$($_.BaseName).txt" --summarize
}
```

---

**Need help? Check SUMMARIZATION_GUIDE.md for detailed examples!**
