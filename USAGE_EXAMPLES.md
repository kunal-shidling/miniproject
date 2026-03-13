# Meeting Pipeline - Usage Examples

## Example 1: Basic Usage

```python
# Run the complete pipeline
from meeting_pipeline import MeetingPipeline

pipeline = MeetingPipeline()
pipeline.run()
pipeline.cleanup()
```

## Example 2: Custom Workflow

```python
from meeting_pipeline import MeetingPipeline

# Initialize
pipeline = MeetingPipeline()

try:
    # Step 1: Face recognition
    person_id, name, img_path, is_new = pipeline.capture_and_recognize_face()
    
    if person_id:
        print(f"Identified: {name}")
        
        # Step 2: Show info
        pipeline.display_person_info(person_id, name, img_path, is_new)
        
        # Step 3: Record meeting
        success = pipeline.record_and_process_meeting(person_id, name, img_path)
        
        if success:
            print("Meeting recorded successfully!")
    
finally:
    pipeline.cleanup()
```

## Example 3: Access Meeting History

```python
from opencv.database import FaceDatabase

# Connect to database
db = FaceDatabase()
db.connect()

# Get person
person = db.get_person_by_name("John Doe")
if person:
    person_id = str(person['_id'])
    
    # Get all meetings
    meetings = db.get_all_meetings(person_id)
    
    print(f"Total meetings: {len(meetings)}")
    for i, meeting in enumerate(meetings, 1):
        print(f"\nMeeting {i}:")
        print(f"Date: {meeting['timestamp']}")
        print(f"Summary:\n{meeting['summary']}")

# Cleanup
db.disconnect()
```

## Example 4: Query Last Meeting

```python
from opencv.database import FaceDatabase

db = FaceDatabase()
db.connect()

# Get person
person = db.get_person_by_name("Jane Smith")
if person:
    person_id = str(person['_id'])
    
    # Get last meeting
    last_meeting = db.get_last_meeting(person_id)
    
    if last_meeting:
        print("Last Meeting:")
        print(f"Date: {last_meeting['timestamp']}")
        print(f"Transcript: {last_meeting['transcript'][:200]}...")
        print(f"Summary: {last_meeting['summary']}")
    else:
        print("No previous meetings")

db.disconnect()
```

## Example 5: Manual Audio Processing

```python
from audio_to_text.mic_transcriber import MicrophoneTranscriber
from audio_to_text.text_summarizer import TextSummarizer

# Initialize
transcriber = MicrophoneTranscriber(model_name='base')
summarizer = TextSummarizer()

# Record
print("Recording for 10 seconds...")
audio_data = transcriber.record_audio(duration=10)

# Save
audio_path = "test_recording.wav"
transcriber.save_audio(audio_data, audio_path)

# Transcribe
result = transcriber.transcriber.transcribe(audio_path)
transcript = result['text']
print(f"\nTranscript:\n{transcript}")

# Summarize
summary = summarizer.summarize_to_bullets(transcript, max_bullets=5)
print(f"\nSummary:\n{summary}")
```

## Example 6: Face Recognition Only

```python
from opencv.camera import Camera
from opencv.detector import FaceDetector
from opencv.embedder import FaceEmbedder
from opencv.database import FaceDatabase
from opencv.recognizer import FaceRecognizer
import cv2

# Initialize components
camera = Camera()
detector = FaceDetector()
embedder = FaceEmbedder()
database = FaceDatabase()
database.connect()
recognizer = FaceRecognizer(database)

# Capture frame
frame = camera.read()
cv2.imwrite("temp_capture.jpg", frame)

# Process
success, face_img, info = detector.detect_and_extract_largest_face("temp_capture.jpg")

if success:
    # Generate embedding
    embedding = embedder.generate_embedding(face_img)
    
    # Recognize
    name, similarity, matches = recognizer.find_best_match(embedding)
    
    if name and similarity >= 0.85:
        print(f"Recognized: {name} ({similarity:.2%})")
    else:
        print("Unknown person")

# Cleanup
camera.close()
database.disconnect()
```

## Example 7: Batch Process Multiple Recordings

```python
from audio_to_text.audio_transcriber import AudioTranscriber
from audio_to_text.text_summarizer import TextSummarizer
from pathlib import Path

# Initialize
transcriber = AudioTranscriber(model_name='base')
summarizer = TextSummarizer()

# Process all audio files in a directory
audio_dir = Path("meeting_data/audio")
results = []

for audio_file in audio_dir.glob("*.wav"):
    print(f"\nProcessing: {audio_file.name}")
    
    # Transcribe
    result = transcriber.transcribe(str(audio_file))
    transcript = result['text']
    
    # Summarize
    summary = summarizer.summarize_to_bullets(transcript)
    
    results.append({
        'file': audio_file.name,
        'transcript': transcript,
        'summary': summary
    })
    
    print(f"✓ Processed: {audio_file.name}")

# Save results
for r in results:
    print(f"\n{r['file']}:")
    print(r['summary'])
```

## Example 8: Register Multiple People

```python
from opencv.camera import Camera
from opencv.detector import FaceDetector
from opencv.embedder import FaceEmbedder
from opencv.database import FaceDatabase
import cv2

# Initialize
camera = Camera()
detector = FaceDetector()
embedder = FaceEmbedder()
database = FaceDatabase()
database.connect()

names = ["Alice", "Bob", "Charlie"]

for name in names:
    print(f"\nRegistering: {name}")
    print("Position yourself and press 'c'")
    
    while True:
        frame = camera.read()
        cv2.imshow("Capture", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('c'):
            # Save and process
            img_path = f"temp_{name}.jpg"
            cv2.imwrite(img_path, frame)
            
            # Extract face and generate embedding
            success, face, _ = detector.detect_and_extract_largest_face(img_path)
            if success:
                embedding = embedder.generate_embedding(face)
                if database.store_embedding(name, embedding):
                    print(f"✓ {name} registered")
                    break
            
cv2.destroyAllWindows()
camera.close()
database.disconnect()
```

## Example 9: Export Meeting Data

```python
from opencv.database import FaceDatabase
import json
from datetime import datetime

db = FaceDatabase()
db.connect()

# Get all people
people = db.get_all_embeddings()

export_data = []

for person in people:
    person_id = str(person['_id'])
    meetings = db.get_all_meetings(person_id)
    
    export_data.append({
        'name': person['name'],
        'total_meetings': len(meetings),
        'meetings': [
            {
                'date': m['timestamp'].isoformat(),
                'summary': m['summary']
            } for m in meetings
        ]
    })

# Save to JSON
with open('meeting_export.json', 'w') as f:
    json.dump(export_data, f, indent=2)

print(f"Exported data for {len(people)} people")
db.disconnect()
```

## Example 10: Search Meetings by Keywords

```python
from opencv.database import FaceDatabase

db = FaceDatabase()
db.connect()

# Search for meetings containing specific keywords
keyword = "budget"
results = []

# Get all people
people = db.get_all_embeddings()

for person in people:
    person_id = str(person['_id'])
    meetings = db.get_all_meetings(person_id)
    
    for meeting in meetings:
        if keyword.lower() in meeting['transcript'].lower():
            results.append({
                'person': person['name'],
                'date': meeting['timestamp'],
                'summary': meeting['summary']
            })

print(f"Found {len(results)} meetings mentioning '{keyword}':")
for r in results:
    print(f"\n{r['person']} - {r['date']}")
    print(r['summary'])

db.disconnect()
```

## Command Line Quick Start

```bash
# Run full pipeline
python run_pipeline.py

# Test system
python test_system.py

# Test individual components
cd opencv
python main.py

cd audio_to_text
python mic_transcriber.py
```

## Environment Variables

Create `.env` file:

```bash
GROQ_API_KEY=your_api_key_here
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=meeting_assistant
WHISPER_MODEL=base
GROQ_MODEL=llama-3.3-70b-versatile
```

## Tips

1. **Camera Quality**: Use good lighting for better face recognition
2. **Microphone**: Use external mic for better audio quality
3. **Processing Speed**: Use GPU for faster transcription (set WHISPER_DEVICE='cuda')
4. **Storage**: Monitor disk space for audio/video storage
5. **Privacy**: Always get consent before recording
6. **Backup**: Regularly backup MongoDB database
7. **Testing**: Test with known faces before production use
8. **Accuracy**: Fine-tune thresholds in config files

## Troubleshooting

### Low Recognition Accuracy
- Adjust `RECOGNITION_THRESHOLD` in opencv/config.py
- Ensure good lighting conditions
- Register faces from multiple angles

### Poor Transcription Quality
- Use larger Whisper model ('medium' or 'large')
- Improve microphone placement
- Reduce background noise

### Slow Processing
- Use smaller Whisper model ('tiny' or 'base')
- Enable GPU acceleration
- Process shorter audio segments

### Database Issues
- Check MongoDB connection string
- Verify network access (for Atlas)
- Check disk space
