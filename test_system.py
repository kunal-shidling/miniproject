"""
Test script to verify all components are working.
Run this before using the full pipeline.
"""

import sys
import os

print("=" * 80)
print("MEETING PIPELINE - SYSTEM TEST")
print("=" * 80)

test_results = []

# Test 1: Python version
print("\n[1/10] Testing Python version...")
try:
    import sys
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro}")
        test_results.append(("Python Version", True))
    else:
        print(f"   ✗ Python {version.major}.{version.minor}.{version.micro} (need 3.8+)")
        test_results.append(("Python Version", False))
except Exception as e:
    print(f"   ✗ Error: {e}")
    test_results.append(("Python Version", False))

# Test 2: OpenCV
print("\n[2/10] Testing OpenCV...")
try:
    import cv2
    print(f"   ✓ OpenCV {cv2.__version__}")
    test_results.append(("OpenCV", True))
except ImportError:
    print("   ✗ OpenCV not installed")
    print("   Run: pip install opencv-python opencv-contrib-python")
    test_results.append(("OpenCV", False))

# Test 3: PyTorch
print("\n[3/10] Testing PyTorch...")
try:
    import torch
    print(f"   ✓ PyTorch {torch.__version__}")
    if torch.cuda.is_available():
        print(f"   ✓ CUDA available: {torch.cuda.get_device_name(0)}")
    else:
        print("   ℹ CUDA not available (CPU only)")
    test_results.append(("PyTorch", True))
except ImportError:
    print("   ✗ PyTorch not installed")
    print("   Run: pip install torch torchvision")
    test_results.append(("PyTorch", False))

# Test 4: MTCNN
print("\n[4/10] Testing MTCNN...")
try:
    from mtcnn import MTCNN
    print("   ✓ MTCNN available")
    test_results.append(("MTCNN", True))
except ImportError:
    print("   ✗ MTCNN not installed")
    print("   Run: pip install mtcnn")
    test_results.append(("MTCNN", False))

# Test 5: FaceNet
print("\n[5/10] Testing FaceNet...")
try:
    from facenet_pytorch import InceptionResnetV1
    print("   ✓ FaceNet (facenet-pytorch) available")
    test_results.append(("FaceNet", True))
except ImportError:
    print("   ✗ FaceNet not installed")
    print("   Run: pip install facenet-pytorch")
    test_results.append(("FaceNet", False))

# Test 6: Whisper
print("\n[6/10] Testing Whisper...")
try:
    import whisper
    print("   ✓ OpenAI Whisper available")
    test_results.append(("Whisper", True))
except ImportError:
    print("   ✗ Whisper not installed")
    print("   Run: pip install openai-whisper")
    test_results.append(("Whisper", False))

# Test 7: Sounddevice
print("\n[7/10] Testing Sounddevice...")
try:
    import sounddevice as sd
    print("   ✓ Sounddevice available")
    test_results.append(("Sounddevice", True))
except ImportError:
    print("   ✗ Sounddevice not installed")
    print("   Run: pip install sounddevice")
    test_results.append(("Sounddevice", False))

# Test 8: Groq
print("\n[8/10] Testing Groq...")
try:
    from groq import Groq
    print("   ✓ Groq SDK available")
    test_results.append(("Groq SDK", True))
except ImportError:
    print("   ✗ Groq not installed")
    print("   Run: pip install groq")
    test_results.append(("Groq SDK", False))

# Test 9: MongoDB
print("\n[9/10] Testing MongoDB...")
try:
    from pymongo import MongoClient
    print("   ✓ PyMongo available")
    test_results.append(("PyMongo", True))
except ImportError:
    print("   ✗ PyMongo not installed")
    print("   Run: pip install pymongo")
    test_results.append(("PyMongo", False))

# Test 10: Environment variables
print("\n[10/10] Testing Environment Variables...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    groq_key = os.getenv('GROQ_API_KEY')
    if groq_key:
        masked_key = groq_key[:8] + "..." + groq_key[-4:]
        print(f"   ✓ GROQ_API_KEY found: {masked_key}")
        test_results.append(("GROQ API Key", True))
    else:
        print("   ✗ GROQ_API_KEY not found")
        print("   Create .env file with: GROQ_API_KEY=your_key_here")
        test_results.append(("GROQ API Key", False))
except Exception as e:
    print(f"   ✗ Error: {e}")
    test_results.append(("GROQ API Key", False))

# Summary
print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)

passed = sum(1 for _, result in test_results if result)
total = len(test_results)

for test_name, result in test_results:
    status = "✓ PASS" if result else "✗ FAIL"
    print(f"{status:10} - {test_name}")

print("=" * 80)
print(f"Result: {passed}/{total} tests passed")
print("=" * 80)

if passed == total:
    print("\n🎉 All tests passed! You're ready to run the pipeline.")
    print("   Run: python run_pipeline.py")
else:
    print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
    print("   Install missing packages with: pip install -r requirements.txt")

# Optional: Test camera
print("\n" + "=" * 80)
response = input("Would you like to test the camera? (y/n): ").strip().lower()
if response in ['y', 'yes']:
    try:
        print("\nTesting camera... (Press 'q' to close)")
        import cv2
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("✗ Could not open camera")
        else:
            print("✓ Camera opened successfully")
            print("  Showing camera feed...")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                cv2.putText(frame, "Camera Test - Press 'q' to quit", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow("Camera Test", frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            print("✓ Camera test complete")
    except Exception as e:
        print(f"✗ Camera test failed: {e}")

# Optional: Test microphone
print("\n" + "=" * 80)
response = input("Would you like to test the microphone? (y/n): ").strip().lower()
if response in ['y', 'yes']:
    try:
        import sounddevice as sd
        import numpy as np
        
        print("\nAvailable microphones:")
        devices = sd.query_devices()
        for idx, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                print(f"  [{idx}] {device['name']}")
        
        print("\nRecording 3 seconds... Speak now!")
        duration = 3
        sample_rate = 16000
        
        recording = sd.rec(int(duration * sample_rate), 
                          samplerate=sample_rate, 
                          channels=1, 
                          dtype='float32')
        sd.wait()
        
        # Check if audio was captured
        if recording.max() > 0.01:
            print("✓ Microphone working! Audio captured.")
        else:
            print("⚠️  Very quiet or no audio detected. Check microphone settings.")
            
    except Exception as e:
        print(f"✗ Microphone test failed: {e}")

print("\n" + "=" * 80)
print("Testing complete!")
print("=" * 80)
