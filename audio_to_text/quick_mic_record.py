"""
Simple script to record audio from microphone and transcribe to English text

This is a quick-start script for the microphone transcription feature.
"""

from mic_transcriber import record_and_transcribe

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🎤 Live Microphone to English Text Converter")
    print("="*70)
    print("\nThis will record audio from your microphone and translate it to English.")
    print("\nOptions:")
    print("1. Quick 10-second recording")
    print("2. Custom duration")
    print("3. Press Ctrl+C to stop manually")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    try:
        if choice == '1':
            print("\n🎤 Recording for 10 seconds...")
            text = record_and_transcribe(duration=10, translate_to_english=True)
        
        elif choice == '2':
            duration = int(input("Enter duration in seconds: "))
            print(f"\n🎤 Recording for {duration} seconds...")
            text = record_and_transcribe(duration=duration, translate_to_english=True)
        
        elif choice == '3':
            print("\n🎤 Recording... Press Ctrl+C when done speaking")
            text = record_and_transcribe(duration=None, translate_to_english=True)
        
        else:
            print("Invalid option!")
            exit(1)
        
        # Display result
        print("\n" + "="*70)
        print("✅ ENGLISH TRANSCRIPTION:")
        print("="*70)
        print(text)
        print("="*70)
        
        # Ask if user wants to save
        save = input("\nSave to file? (y/n): ").strip().lower()
        if save == 'y':
            filename = input("Enter filename (default: transcription.txt): ").strip()
            if not filename:
                filename = "transcription.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
            
            print(f"✅ Saved to {filename}")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Recording cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
