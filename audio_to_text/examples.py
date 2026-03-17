"""
Example usage script for the Audio Transcription Module

This script demonstrates various ways to use the audio_transcriber module
for converting audio files to text using OpenAI Whisper.
"""

from audio_transcriber import AudioTranscriber, transcribe_audio
import os


def example_1_simple_transcription():
    """Example 1: Simple transcription using the convenience function"""
    print("\n" + "="*70)
    print("Example 1: Simple Transcription")
    print("="*70)
    
    # Replace with your audio file path
    audio_file = "sample_audio.mp3"
    
    if not os.path.exists(audio_file):
        print(f"⚠️  Audio file '{audio_file}' not found. Skipping example.")
        return
    
    try:
        # Simple one-line transcription
        text = transcribe_audio(audio_file, model='base')
        print(f"\n📝 Transcription:\n{text}")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_2_class_based_transcription():
    """Example 2: Using the AudioTranscriber class for more control"""
    print("\n" + "="*70)
    print("Example 2: Class-Based Transcription with Timestamps")
    print("="*70)
    
    audio_file = "sample_audio.mp3"
    
    if not os.path.exists(audio_file):
        print(f"⚠️  Audio file '{audio_file}' not found. Skipping example.")
        return
    
    try:
        # Initialize transcriber with base model
        transcriber = AudioTranscriber(model_name='base', device='cpu')
        
        # Transcribe with timestamps
        text = transcriber.transcribe_audio(
            file_path=audio_file,
            task='transcribe',
            include_timestamps=True,
            verbose=True
        )
        
        print(f"\n📝 Transcription with Timestamps:\n{text}")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_3_translation_to_english():
    """Example 3: Translate audio from any language to English"""
    print("\n" + "="*70)
    print("Example 3: Translation to English")
    print("="*70)
    
    audio_file = "spanish_audio.mp3"
    
    if not os.path.exists(audio_file):
        print(f"⚠️  Audio file '{audio_file}' not found. Skipping example.")
        return
    
    try:
        transcriber = AudioTranscriber(model_name='base')
        
        # Translate to English (works for any language)
        english_text = transcriber.transcribe_audio(
            file_path=audio_file,
            task='translate',  # 'translate' converts to English
            verbose=True
        )
        
        print(f"\n🌍 English Translation:\n{english_text}")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_4_detailed_transcription():
    """Example 4: Get detailed transcription with segments and metadata"""
    print("\n" + "="*70)
    print("Example 4: Detailed Transcription with Segments")
    print("="*70)
    
    audio_file = "sample_audio.mp3"
    
    if not os.path.exists(audio_file):
        print(f"⚠️  Audio file '{audio_file}' not found. Skipping example.")
        return
    
    try:
        transcriber = AudioTranscriber(model_name='base')
        
        # Get detailed results
        result = transcriber.transcribe_with_details(
            file_path=audio_file,
            task='transcribe',
            verbose=True
        )
        
        print(f"\n📊 Detailed Results:")
        print(f"Language: {result['language']}")
        print(f"Duration: {result['duration']:.2f} seconds")
        print(f"\nFull Text:\n{result['text']}")
        print(f"\nSegments ({len(result['segments'])}):")
        
        for i, segment in enumerate(result['segments'][:3], 1):  # Show first 3
            print(f"\n  Segment {i}:")
            print(f"    Time: {segment['start_formatted']} → {segment['end_formatted']}")
            print(f"    Text: {segment['text']}")
        
        if len(result['segments']) > 3:
            print(f"\n  ... and {len(result['segments']) - 3} more segments")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def example_5_save_to_file():
    """Example 5: Save transcription to file (txt and JSON formats)"""
    print("\n" + "="*70)
    print("Example 5: Save Transcription to File")
    print("="*70)
    
    audio_file = "sample_audio.mp3"
    
    if not os.path.exists(audio_file):
        print(f"⚠️  Audio file '{audio_file}' not found. Skipping example.")
        return
    
    try:
        transcriber = AudioTranscriber(model_name='base')
        
        # Save as plain text
        txt_output = transcriber.save_transcription(
            file_path=audio_file,
            output_path="transcription.txt",
            format='txt',
            include_timestamps=False,
            verbose=True
        )
        print(f"\n✅ Text saved to: {txt_output}")
        
        # Save as JSON with detailed information
        json_output = transcriber.save_transcription(
            file_path=audio_file,
            output_path="transcription.json",
            format='json',
            verbose=True
        )
        print(f"✅ JSON saved to: {json_output}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def example_6_specify_language():
    """Example 6: Manually specify the language"""
    print("\n" + "="*70)
    print("Example 6: Transcription with Specified Language")
    print("="*70)
    
    audio_file = "sample_audio.mp3"
    
    if not os.path.exists(audio_file):
        print(f"⚠️  Audio file '{audio_file}' not found. Skipping example.")
        return
    
    try:
        transcriber = AudioTranscriber(model_name='base')
        
        # Specify language explicitly (can improve accuracy and speed)
        # Common language codes: 'en', 'es', 'fr', 'de', 'it', 'pt', 'ja', 'ko', 'zh'
        text = transcriber.transcribe_audio(
            file_path=audio_file,
            task='transcribe',
            language='en',  # Specify English
            verbose=True
        )
        
        print(f"\n📝 Transcription (English):\n{text}")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_7_different_models():
    """Example 7: Compare different model sizes"""
    print("\n" + "="*70)
    print("Example 7: Using Different Model Sizes")
    print("="*70)
    
    audio_file = "sample_audio.mp3"
    
    if not os.path.exists(audio_file):
        print(f"⚠️  Audio file '{audio_file}' not found. Skipping example.")
        return
    
    print("\nModel sizes (speed vs accuracy trade-off):")
    print("  - tiny: Fastest, lowest accuracy")
    print("  - base: Good balance (recommended)")
    print("  - small: Better accuracy, slower")
    print("  - medium: High accuracy, much slower")
    print("  - large: Best accuracy, slowest\n")
    
    try:
        # Using tiny model for speed
        print("Using 'tiny' model (fastest)...")
        transcriber_tiny = AudioTranscriber(model_name='tiny')
        text_tiny = transcriber_tiny.transcribe_audio(audio_file)
        print(f"Result: {text_tiny[:100]}...")
        
        # Using base model for balance
        print("\nUsing 'base' model (balanced)...")
        transcriber_base = AudioTranscriber(model_name='base')
        text_base = transcriber_base.transcribe_audio(audio_file)
        print(f"Result: {text_base[:100]}...")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def example_8_batch_processing():
    """Example 8: Process multiple audio files"""
    print("\n" + "="*70)
    print("Example 8: Batch Processing Multiple Files")
    print("="*70)
    
    # List of audio files to process
    audio_files = ["file1.mp3", "file2.wav", "file3.m4a"]
    
    # Initialize transcriber once for efficiency
    transcriber = AudioTranscriber(model_name='base')
    
    for audio_file in audio_files:
        if not os.path.exists(audio_file):
            print(f"⚠️  Skipping '{audio_file}' (not found)")
            continue
        
        try:
            print(f"\n📁 Processing: {audio_file}")
            text = transcriber.transcribe_audio(audio_file, verbose=False)
            
            # Save to corresponding text file
            output_file = os.path.splitext(audio_file)[0] + ".txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            print(f"✅ Saved to: {output_file}")
            print(f"Preview: {text[:100]}...")
        
        except Exception as e:
            print(f"❌ Error processing {audio_file}: {e}")


def example_9_error_handling():
    """Example 9: Proper error handling"""
    print("\n" + "="*70)
    print("Example 9: Error Handling Examples")
    print("="*70)
    
    transcriber = AudioTranscriber(model_name='base')
    
    # Test 1: File not found
    print("\nTest 1: File not found")
    try:
        transcriber.transcribe_audio("nonexistent_file.mp3")
    except FileNotFoundError as e:
        print(f"✅ Caught expected error: {e}")
    
    # Test 2: Unsupported format
    print("\nTest 2: Unsupported format")
    try:
        # Create a dummy file with wrong extension
        with open("test.xyz", 'w') as f:
            f.write("dummy")
        transcriber.transcribe_audio("test.xyz")
    except ValueError as e:
        print(f"✅ Caught expected error: {e}")
    finally:
        if os.path.exists("test.xyz"):
            os.remove("test.xyz")
    
    # Test 3: Invalid task
    print("\nTest 3: Invalid task")
    try:
        transcriber.transcribe_audio("sample.mp3", task='invalid_task')
    except ValueError as e:
        print(f"✅ Caught expected error: {e}")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("🎙️  Audio Transcription Module - Examples")
    print("="*70)
    print("\nThis script demonstrates various features of the audio transcriber.")
    print("Note: Some examples require audio files to be present.")
    
    # Run examples
    example_1_simple_transcription()
    example_2_class_based_transcription()
    example_3_translation_to_english()
    example_4_detailed_transcription()
    example_5_save_to_file()
    example_6_specify_language()
    example_7_different_models()
    example_8_batch_processing()
    example_9_error_handling()
    
    print("\n" + "="*70)
    print("✅ Examples completed!")
    print("="*70)


if __name__ == "__main__":
    main()
