# Quick Setup Guide

## 1. Install Python Dependencies

```powershell
# From project root (d:\miniproject)
pip install -r requirements.txt
```

## 2. Set Up Groq API Key

Create a file named `.env` in the project root:

```
GROQ_API_KEY=your_key_here
```

Get your free key from: https://console.groq.com/keys

## 3. Configure MongoDB

Edit `opencv/config.py` line 45:

```python
# For MongoDB Atlas (recommended)
MONGODB_URI = "mongodb+srv://username:password@cluster.mongodb.net/"

# OR for local MongoDB
MONGODB_URI = "mongodb://localhost:27017/"
```

## 4. Test Individual Components

### Test Camera
```powershell
cd opencv
python camera.py
```

### Test Face Detection
```powershell
cd opencv
python detector.py
```

### Test Database Connection
```powershell
cd opencv
python database.py
```

### Test Microphone
```powershell
cd audio_to_text
python mic_transcriber.py
```

### Test Whisper Transcription
```powershell
cd audio_to_text
python audio_transcriber.py
```

### Test Groq Summarization
```powershell
cd audio_to_text
python text_summarizer.py
```

## 5. Run the Integrated Pipeline

```powershell
cd d:\miniproject
python run_pipeline.py
```

## Common Issues

### Issue: "No module named 'opencv'"
**Solution:** Add paths or install opencv-python
```powershell
pip install opencv-python opencv-contrib-python
```

### Issue: "Failed to connect to MongoDB"
**Solution:** Check MongoDB is running or Atlas credentials are correct

### Issue: "GROQ_API_KEY not found"
**Solution:** Create `.env` file with your API key

### Issue: "Camera not found"
**Solution:** Update `CAMERA_INDEX` in `opencv/config.py`

### Issue: "Microphone not working"
**Solution:** Check permissions and default device settings

## Directory Structure After Setup

```
miniproject/
├── .env                          # Your API keys (create this)
├── meeting_pipeline.py
├── run_pipeline.py
├── README.md
├── QUICKSTART.md                 # This file
├── requirements.txt
├── opencv/
├── audio_to_text/
└── meeting_data/                 # Created automatically
    ├── images/
    ├── audio/
    └── transcripts/
```

## Next Steps

1. Run `python run_pipeline.py`
2. Follow on-screen instructions
3. Press 'c' to capture your face
4. Record a short conversation
5. View your meeting summary!

## Need Help?

Refer to the full [README.md](README.md) for detailed documentation.
