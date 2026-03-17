"""
Setup FFmpeg PATH and launch the microphone transcriber

This script ensures FFmpeg is available before running the transcription tool.
"""

import os
import sys
import glob
from pathlib import Path


def setup_ffmpeg():
    """Find and add FFmpeg to PATH if not already available."""
    # Check if ffmpeg is already in PATH
    import shutil
    if shutil.which('ffmpeg'):
        print("✓ FFmpeg found in PATH")
        return True
    
    print("Looking for FFmpeg installation...")
    
    # Common FFmpeg installation locations on Windows
    search_paths = [
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'WinGet', 'Packages', 'Gyan.FFmpeg*'),
        os.path.join(os.environ.get('PROGRAMFILES', ''), 'ffmpeg*'),
        os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'ffmpeg*'),
    ]
    
    for search_path in search_paths:
        matches = glob.glob(search_path)
        for match in matches:
            # Look for bin directory
            bin_paths = list(Path(match).rglob('bin'))
            for bin_path in bin_paths:
                ffmpeg_exe = bin_path / 'ffmpeg.exe'
                if ffmpeg_exe.exists():
                    # Add to PATH
                    os.environ['PATH'] = str(bin_path) + os.pathsep + os.environ.get('PATH', '')
                    print(f"✓ Found FFmpeg at: {bin_path}")
                    return True
    
    print("❌ FFmpeg not found!")
    print("\nPlease install FFmpeg:")
    print("  winget install Gyan.FFmpeg")
    print("\nThen restart your terminal and try again.")
    return False


if __name__ == "__main__":
    print("="*70)
    print("🎤 Setting up Microphone Transcription Tool")
    print("="*70)
    
    if not setup_ffmpeg():
        sys.exit(1)
    
    # Import and run the main script
    from mic_transcriber import record_and_transcribe
    
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
            sys.exit(1)
        
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
        import traceback
        traceback.print_exc()
