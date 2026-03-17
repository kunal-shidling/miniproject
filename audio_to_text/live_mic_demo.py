"""
Live Microphone Transcription Demo

This script demonstrates how to use the microphone transcription feature
to capture live audio and convert it to text.
"""

from mic_transcriber import MicrophoneTranscriber, record_and_transcribe
import sys


def demo_1_quick_transcribe():
    """Demo 1: Quick 10-second transcription"""
    print("\n" + "="*70)
    print("Demo 1: Quick 10-Second Transcription (Translate to English)")
    print("="*70)
    
    try:
        text = record_and_transcribe(duration=10, translate_to_english=True)
        
        print("\n" + "="*70)
        print("📝 TRANSCRIPTION RESULT:")
        print("="*70)
        print(text)
        print("="*70)
    
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_2_custom_duration():
    """Demo 2: Custom duration recording"""
    print("\n" + "="*70)
    print("Demo 2: Custom Duration Recording")
    print("="*70)
    
    duration = 15  # Change this to your desired duration
    
    try:
        mic = MicrophoneTranscriber(model_name='base')
        
        print(f"Recording for {duration} seconds...")
        text = mic.transcribe_from_mic(
            duration=duration,
            task='translate',  # Translate to English
            verbose=True
        )
        
        print("\n" + "="*70)
        print("📝 TRANSCRIPTION RESULT:")
        print("="*70)
        print(text)
        print("="*70)
    
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_3_manual_stop():
    """Demo 3: Record until user presses Ctrl+C"""
    print("\n" + "="*70)
    print("Demo 3: Manual Stop Recording (Press Ctrl+C to stop)")
    print("="*70)
    
    try:
        mic = MicrophoneTranscriber(model_name='base')
        
        text = mic.transcribe_from_mic(
            duration=None,  # No duration = manual stop
            task='translate',
            verbose=True
        )
        
        print("\n" + "="*70)
        print("📝 TRANSCRIPTION RESULT:")
        print("="*70)
        print(text)
        print("="*70)
    
    except KeyboardInterrupt:
        print("\n⚠️  Recording cancelled")
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_4_save_audio():
    """Demo 4: Save the recorded audio file"""
    print("\n" + "="*70)
    print("Demo 4: Record and Save Audio File")
    print("="*70)
    
    try:
        text = record_and_transcribe(
            duration=10,
            translate_to_english=True,
            save_audio=True  # This will save the audio file
        )
        
        print("\n" + "="*70)
        print("📝 TRANSCRIPTION RESULT:")
        print("="*70)
        print(text)
        print("="*70)
    
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_5_transcribe_original_language():
    """Demo 5: Transcribe in original language (not translate)"""
    print("\n" + "="*70)
    print("Demo 5: Transcribe in Original Language")
    print("="*70)
    
    try:
        mic = MicrophoneTranscriber(model_name='base')
        
        text = mic.transcribe_from_mic(
            duration=10,
            task='transcribe',  # Keep original language
            language='en',  # Specify language if known
            verbose=True
        )
        
        print("\n" + "="*70)
        print("📝 TRANSCRIPTION RESULT:")
        print("="*70)
        print(text)
        print("="*70)
    
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_6_list_microphones():
    """Demo 6: List available microphones"""
    print("\n" + "="*70)
    print("Demo 6: List Available Microphones")
    print("="*70)
    
    try:
        mic = MicrophoneTranscriber()
        mic.list_microphones()
    
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_7_specific_microphone():
    """Demo 7: Use a specific microphone"""
    print("\n" + "="*70)
    print("Demo 7: Use Specific Microphone")
    print("="*70)
    
    try:
        mic = MicrophoneTranscriber(model_name='base')
        
        # First, list available microphones
        mic.list_microphones()
        
        print("\nEnter the device ID from the list above (or press Enter for default):")
        device_input = input("Device ID: ").strip()
        
        device_id = int(device_input) if device_input else None
        
        text = mic.transcribe_from_mic(
            duration=10,
            device_id=device_id,
            task='translate',
            verbose=True
        )
        
        print("\n" + "="*70)
        print("📝 TRANSCRIPTION RESULT:")
        print("="*70)
        print(text)
        print("="*70)
    
    except Exception as e:
        print(f"❌ Error: {e}")


def interactive_menu():
    """Interactive menu for selecting demos"""
    while True:
        print("\n" + "="*70)
        print("🎤 Live Microphone Transcription - Interactive Demo")
        print("="*70)
        print("\nSelect a demo:")
        print("  1. Quick 10-second transcription (translate to English)")
        print("  2. Custom duration recording")
        print("  3. Manual stop recording (Ctrl+C to stop)")
        print("  4. Record and save audio file")
        print("  5. Transcribe in original language")
        print("  6. List available microphones")
        print("  7. Use specific microphone")
        print("  0. Exit")
        print("="*70)
        
        choice = input("\nEnter your choice (0-7): ").strip()
        
        if choice == '1':
            demo_1_quick_transcribe()
        elif choice == '2':
            demo_2_custom_duration()
        elif choice == '3':
            demo_3_manual_stop()
        elif choice == '4':
            demo_4_save_audio()
        elif choice == '5':
            demo_5_transcribe_original_language()
        elif choice == '6':
            demo_6_list_microphones()
        elif choice == '7':
            demo_7_specific_microphone()
        elif choice == '0':
            print("\n👋 Goodbye!")
            break
        else:
            print("\n⚠️  Invalid choice. Please select 0-7.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line argument provided
        demo_choice = sys.argv[1]
        
        demos = {
            '1': demo_1_quick_transcribe,
            '2': demo_2_custom_duration,
            '3': demo_3_manual_stop,
            '4': demo_4_save_audio,
            '5': demo_5_transcribe_original_language,
            '6': demo_6_list_microphones,
            '7': demo_7_specific_microphone
        }
        
        if demo_choice in demos:
            demos[demo_choice]()
        else:
            print(f"Invalid demo number: {demo_choice}")
            print("Usage: python live_mic_demo.py [1-7]")
    else:
        # Interactive mode
        interactive_menu()
