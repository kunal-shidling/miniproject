# API Reference - Meeting Pipeline

## Core Classes

### MeetingPipeline

Main controller class that orchestrates the entire meeting workflow.

```python
from meeting_pipeline import MeetingPipeline
```

#### Constructor

```python
MeetingPipeline()
```

Initializes all components (camera, face detection, database, audio, etc.)

**Raises:**
- `Exception`: If component initialization fails

#### Methods

##### `capture_and_recognize_face()`

Captures face from camera and identifies the person.

**Returns:**
- `Tuple[Optional[str], Optional[str], Optional[str], bool]`
  - `person_id`: Database ID of the person
  - `person_name`: Name of the person
  - `image_path`: Path to captured image
  - `is_new_person`: True if newly registered, False if existing

**Usage:**
```python
person_id, name, img_path, is_new = pipeline.capture_and_recognize_face()
```

##### `display_person_info(person_id, person_name, image_path, is_new)`

Displays person information and last meeting summary.

**Parameters:**
- `person_id` (str): Person's database ID
- `person_name` (str): Person's name
- `image_path` (str): Path to person's image
- `is_new` (bool): Whether this is a new registration

**Usage:**
```python
pipeline.display_person_info(person_id, "John Doe", "image.jpg", False)
```

##### `record_and_process_meeting(person_id, person_name, image_path)`

Records conversation, transcribes, summarizes, and stores in database.

**Parameters:**
- `person_id` (str): Person's database ID
- `person_name` (str): Person's name
- `image_path` (str): Path to person's image

**Returns:**
- `bool`: True if successful, False otherwise

**Usage:**
```python
success = pipeline.record_and_process_meeting(person_id, "John", "img.jpg")
```

##### `run()`

Executes the complete pipeline workflow.

**Usage:**
```python
pipeline.run()
```

##### `cleanup()`

Releases resources (camera, database connections).

**Usage:**
```python
pipeline.cleanup()
```

---

## Database Module

### FaceDatabase

MongoDB interface for storing face embeddings and meetings.

```python
from opencv.database import FaceDatabase
```

#### Constructor

```python
FaceDatabase(uri: str = config.MONGODB_URI)
```

**Parameters:**
- `uri` (str): MongoDB connection URI

#### Connection Methods

##### `connect()`

Establishes connection to MongoDB.

**Returns:**
- `bool`: True if successful, False otherwise

**Usage:**
```python
db = FaceDatabase()
if db.connect():
    print("Connected")
```

##### `disconnect()`

Closes MongoDB connection.

**Usage:**
```python
db.disconnect()
```

##### `is_connected()`

Checks connection status.

**Returns:**
- `bool`: True if connected

#### Embedding Methods

##### `store_embedding(name, embedding, check_duplicates=True)`

Stores face embedding in database.

**Parameters:**
- `name` (str): Person's name
- `embedding` (np.ndarray): 512-dimensional face embedding
- `check_duplicates` (bool): Whether to check for duplicates

**Returns:**
- `bool`: True if stored successfully

**Usage:**
```python
success = db.store_embedding("John Doe", embedding)
```

##### `get_embedding_by_name(name)`

Retrieves embedding by person's name.

**Parameters:**
- `name` (str): Person's name

**Returns:**
- `np.ndarray`: Face embedding or None

**Usage:**
```python
embedding = db.get_embedding_by_name("John Doe")
```

##### `get_all_embeddings()`

Retrieves all stored embeddings.

**Returns:**
- `List[Dict]`: List of records with name and embedding

**Usage:**
```python
all_records = db.get_all_embeddings()
```

##### `delete_embedding(name)`

Deletes embedding by name.

**Parameters:**
- `name` (str): Person's name

**Returns:**
- `bool`: True if deleted

#### Meeting Methods

##### `store_meeting(person_id, person_name, transcript, summary, audio_path=None, image_path=None)`

Stores a meeting record.

**Parameters:**
- `person_id` (str): Person's database ID
- `person_name` (str): Person's name
- `transcript` (str): Full transcript
- `summary` (str): Meeting summary
- `audio_path` (str, optional): Path to audio file
- `image_path` (str, optional): Path to image file

**Returns:**
- `str`: Meeting ID or None

**Usage:**
```python
meeting_id = db.store_meeting(
    person_id="123",
    person_name="John",
    transcript="Meeting transcript...",
    summary="Key points..."
)
```

##### `get_last_meeting(person_id)`

Gets most recent meeting for a person.

**Parameters:**
- `person_id` (str): Person's database ID

**Returns:**
- `Dict`: Meeting record or None

**Usage:**
```python
last_meeting = db.get_last_meeting(person_id)
if last_meeting:
    print(last_meeting['summary'])
```

##### `get_all_meetings(person_id)`

Gets all meetings for a person (newest first).

**Parameters:**
- `person_id` (str): Person's database ID

**Returns:**
- `List[Dict]`: List of meeting records

**Usage:**
```python
meetings = db.get_all_meetings(person_id)
for meeting in meetings:
    print(meeting['timestamp'], meeting['summary'])
```

##### `get_person_by_name(name)`

Gets complete person record by name.

**Parameters:**
- `name` (str): Person's name

**Returns:**
- `Dict`: Person record including _id

**Usage:**
```python
person = db.get_person_by_name("John Doe")
person_id = str(person['_id'])
```

##### `update_person_image(person_id, image_path)`

Updates stored image path for a person.

**Parameters:**
- `person_id` (str): Person's database ID
- `image_path` (str): New image path

**Returns:**
- `bool`: True if updated

---

## Audio Module

### MicrophoneTranscriber

Records and transcribes audio from microphone.

```python
from audio_to_text.mic_transcriber import MicrophoneTranscriber
```

#### Constructor

```python
MicrophoneTranscriber(
    model_name='base',
    device='cpu',
    sample_rate=16000,
    channels=1
)
```

**Parameters:**
- `model_name` (str): Whisper model ('tiny', 'base', 'small', 'medium', 'large')
- `device` (str): 'cpu' or 'cuda'
- `sample_rate` (int): Audio sample rate in Hz
- `channels` (int): Number of channels (1=mono, 2=stereo)

#### Methods

##### `record_audio(duration=None, device_id=None, show_progress=True)`

Records audio from microphone.

**Parameters:**
- `duration` (int, optional): Duration in seconds. None for manual stop
- `device_id` (int, optional): Microphone device ID
- `show_progress` (bool): Show recording progress

**Returns:**
- `np.ndarray`: Recorded audio data

**Usage:**
```python
transcriber = MicrophoneTranscriber()
audio = transcriber.record_audio(duration=10)
```

##### `save_audio(audio_data, file_path)`

Saves audio data to WAV file.

**Parameters:**
- `audio_data` (np.ndarray): Audio data
- `file_path` (str): Output file path

**Usage:**
```python
transcriber.save_audio(audio, "recording.wav")
```

##### `list_microphones()`

Lists available microphone devices.

**Usage:**
```python
transcriber.list_microphones()
```

---

### AudioTranscriber

Transcribes audio files to text using Whisper.

```python
from audio_to_text.audio_transcriber import AudioTranscriber
```

#### Constructor

```python
AudioTranscriber(model_name='base', device='cpu')
```

#### Methods

##### `transcribe(file_path, task='transcribe', language=None, verbose=True)`

Transcribes audio file to text.

**Parameters:**
- `file_path` (str): Path to audio file
- `task` (str): 'transcribe' or 'translate'
- `language` (str, optional): Source language code
- `verbose` (bool): Show progress

**Returns:**
- `Dict`: Result containing 'text', 'segments', 'language'

**Usage:**
```python
transcriber = AudioTranscriber(model_name='base')
result = transcriber.transcribe("audio.wav")
text = result['text']
```

---

### TextSummarizer

Summarizes text using Groq API.

```python
from audio_to_text.text_summarizer import TextSummarizer
```

#### Constructor

```python
TextSummarizer(api_key=None, model='llama-3.3-70b-versatile')
```

**Parameters:**
- `api_key` (str, optional): Groq API key (reads from env if not provided)
- `model` (str): Model name

#### Methods

##### `summarize_to_bullets(text, max_bullets=10, focus=None, verbose=False)`

Generates bullet-point summary.

**Parameters:**
- `text` (str): Text to summarize
- `max_bullets` (int): Maximum bullet points
- `focus` (str, optional): Focus area
- `verbose` (bool): Show progress

**Returns:**
- `str`: Bullet-point summary

**Usage:**
```python
summarizer = TextSummarizer()
summary = summarizer.summarize_to_bullets(
    text="Long transcript...",
    max_bullets=5,
    focus="action items"
)
```

---

## Face Recognition Module

### Camera

Camera interface for capturing frames.

```python
from opencv.camera import Camera
```

#### Methods

##### `read()`

Reads a frame from camera.

**Returns:**
- `np.ndarray`: Camera frame or None

##### `close()`

Releases camera resources.

---

### FaceDetector

Detects faces using MTCNN.

```python
from opencv.detector import FaceDetector
```

#### Methods

##### `detect_faces(image)`

Detects all faces in image.

**Returns:**
- `Tuple[List, List]`: (bounding_boxes, confidences)

##### `detect_and_extract_largest_face(image_path)`

Detects and extracts the largest face.

**Returns:**
- `Tuple[bool, np.ndarray, Dict]`: (success, face_image, info)

---

### FaceEmbedder

Generates face embeddings using FaceNet.

```python
from opencv.embedder import FaceEmbedder
```

#### Methods

##### `generate_embedding(face_image)`

Generates 512-dimensional embedding.

**Parameters:**
- `face_image` (np.ndarray): Face image

**Returns:**
- `np.ndarray`: Face embedding

---

### FaceRecognizer

Matches faces against database.

```python
from opencv.recognizer import FaceRecognizer
```

#### Methods

##### `find_best_match(query_embedding)`

Finds best matching person.

**Returns:**
- `Tuple[str, float, List]`: (name, similarity, all_matches)

---

## Configuration

### pipeline_config.py

```python
# Audio settings
WHISPER_MODEL = 'base'
SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1

# Groq settings
GROQ_MODEL = 'llama-3.3-70b-versatile'
MAX_SUMMARY_BULLETS = 10

# Face recognition
RECOGNITION_THRESHOLD = 0.85
```

### opencv/config.py

```python
# Camera
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Face detection
RECOGNITION_THRESHOLD = 0.85
DUPLICATE_THRESHOLD = 0.98

# Database
MONGODB_URI = "mongodb://localhost:27017/"
MONGODB_DATABASE = "meeting_assistant"
MONGODB_COLLECTION = "face_embeddings"
```

---

## Data Structures

### Person Record

```python
{
    '_id': ObjectId,
    'name': str,
    'embedding': [float],  # 512 dimensions
    'date': datetime,
    'image_path': str,
    'updated_at': datetime
}
```

### Meeting Record

```python
{
    '_id': ObjectId,
    'person_id': str,
    'person_name': str,
    'timestamp': datetime,
    'transcript': str,
    'summary': str,
    'audio_path': str,
    'image_path': str
}
```

---

## Error Handling

All methods include error handling and logging. Common exceptions:

- `ConnectionFailure`: MongoDB connection issues
- `FileNotFoundError`: Missing audio/image files
- `ValueError`: Invalid parameters
- `RuntimeError`: Component initialization failures

---

## Best Practices

1. Always call `cleanup()` after pipeline execution
2. Check return values before proceeding
3. Handle keyboard interrupts gracefully
4. Use context managers when possible
5. Validate inputs before database operations
6. Monitor disk space for audio/image storage
7. Regularly backup MongoDB database
8. Use appropriate model sizes for your hardware

---

## Examples

See [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for comprehensive usage examples.
