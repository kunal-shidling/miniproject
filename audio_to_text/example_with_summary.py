"""
Quick Example: Transcribe Audio with AI Summary

This script demonstrates the complete workflow:
1. Transcribe an audio file
2. Generate a bullet-point summary using Groq API

Usage:
    python example_with_summary.py <audio_file>
"""

import os
import sys
from audio_transcriber import AudioTranscriber
from text_summarizer import TextSummarizer


def main():
    if len(sys.argv) < 2:
        print("Usage: python example_with_summary.py <audio_file>")
        print("\nMake sure to set GROQ_API_KEY environment variable:")
        print("  PowerShell: $env:GROQ_API_KEY = 'your-api-key'")
        print("  CMD: set GROQ_API_KEY=your-api-key")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    
    # Check if Groq API key is set
    if not os.getenv('GROQ_API_KEY'):
        print("Error: GROQ_API_KEY environment variable not set!")
        print("\nGet your API key from: https://console.groq.com/keys")
        print("\nThen set it:")
        print("  PowerShell: $env:GROQ_API_KEY = 'your-api-key'")
        print("  CMD: set GROQ_API_KEY=your-api-key")
        sys.exit(1)
    
    print("="*70)
    print("AUDIO TRANSCRIPTION WITH AI SUMMARY")
    print("="*70)
    
    # Step 1: Transcribe audio
    print("\n[1/2] Transcribing audio...")
    print(f"File: {audio_file}")
    
    try:
        transcriber = AudioTranscriber(model_name='base', device='cpu')
        text = transcriber.transcribe_audio(audio_file, verbose=True)
        
        print("\n" + "-"*70)
        print("TRANSCRIPTION:")
        print("-"*70)
        print(text[:500] + "..." if len(text) > 500 else text)
        print("-"*70)
        print(f"Full transcription length: {len(text)} characters")
        
    except Exception as e:
        print(f"Error during transcription: {e}")
        sys.exit(1)
    
    # Step 2: Generate summary
    print("\n[2/2] Generating AI summary...")
    
    try:
        summarizer = TextSummarizer(model='llama-3.3-70b-versatile')
        
        # Option 1: Standard bullet points
        print("\n📋 Generating bullet-point summary...")
        summary = summarizer.summarize_to_bullets(
            text,
            max_bullets=10,
            verbose=True
        )
        
        print("\n" + "="*70)
        print("SUMMARY (Bullet Points)")
        print("="*70)
        print(summary)
        print("="*70)
        
        # Option 2: Structured summary
        print("\n📊 Generating structured summary...")
        structured = summarizer.summarize_with_structure(text, verbose=True)
        
        print("\n" + "="*70)
        print("STRUCTURED SUMMARY")
        print("="*70)
        print(structured['raw'])
        print("="*70)
        
        print("\n✅ Complete! Your audio has been transcribed and summarized.")
        
    except Exception as e:
        print(f"Error during summarization: {e}")
        print("\nNote: Make sure your GROQ_API_KEY is valid.")
        sys.exit(1)


if __name__ == "__main__":
    main()
