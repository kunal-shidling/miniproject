"""
Simple CLI tool for audio transcription

Usage:
    python cli_transcribe.py <audio_file> [options]

Examples:
    python cli_transcribe.py meeting.mp3
    python cli_transcribe.py interview.wav --model small --timestamps
    python cli_transcribe.py spanish.mp3 --translate
    python cli_transcribe.py lecture.m4a --output lecture.txt
"""

import argparse
import sys
from pathlib import Path
from audio_transcriber import AudioTranscriber
from text_summarizer import TextSummarizer


def main():
    parser = argparse.ArgumentParser(
        description='Transcribe audio files to text using OpenAI Whisper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli_transcribe.py meeting.mp3
  python cli_transcribe.py interview.wav --model small --timestamps
  python cli_transcribe.py spanish.mp3 --translate
  python cli_transcribe.py lecture.m4a --output lecture.txt --format json
        """
    )
    
    parser.add_argument(
        'audio_file',
        type=str,
        help='Path to the audio file to transcribe'
    )
    
    parser.add_argument(
        '-m', '--model',
        type=str,
        default='base',
        choices=['tiny', 'base', 'small', 'medium', 'large'],
        help='Whisper model to use (default: base)'
    )
    
    parser.add_argument(
        '-l', '--language',
        type=str,
        default=None,
        help='Language code (e.g., en, es, fr). Auto-detect if not specified.'
    )
    
    parser.add_argument(
        '-t', '--translate',
        action='store_true',
        help='Translate audio to English (instead of transcribing)'
    )
    
    parser.add_argument(
        '--timestamps',
        action='store_true',
        help='Include timestamps in the output'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Output file path. If not specified, prints to stdout.'
    )
    
    parser.add_argument(
        '-f', '--format',
        type=str,
        default='txt',
        choices=['txt', 'json'],
        help='Output format (default: txt)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Print detailed progress information'
    )
    
    parser.add_argument(
        '--device',
        type=str,
        default='cpu',
        choices=['cpu', 'cuda'],
        help='Device to run on (default: cpu)'
    )
    
    # Summarization options
    parser.add_argument(
        '--summarize',
        action='store_true',
        help='Summarize the transcribed text using Groq API'
    )
    
    parser.add_argument(
        '--groq-api-key',
        type=str,
        default=None,
        help='Groq API key for summarization (or set GROQ_API_KEY env variable)'
    )
    
    parser.add_argument(
        '--groq-model',
        type=str,
        default='llama-3.3-70b-versatile',
        help='Groq model to use for summarization (default: llama-3.3-70b-versatile)'
    )
    
    parser.add_argument(
        '--max-bullets',
        type=int,
        default=10,
        help='Maximum number of bullet points in summary (default: 10)'
    )
    
    parser.add_argument(
        '--structured-summary',
        action='store_true',
        help='Use structured summary format (Main Topics, Key Points, Action Items, Decisions)'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    audio_path = Path(args.audio_file)
    if not audio_path.exists():
        print(f"Error: Audio file not found: {args.audio_file}", file=sys.stderr)
        sys.exit(1)
    
    # Determine task
    task = 'translate' if args.translate else 'transcribe'
    
    try:
        # Initialize transcriber
        if args.verbose:
            print(f"Initializing Whisper model '{args.model}'...")
        
        transcriber = AudioTranscriber(model_name=args.model, device=args.device)
        
        # Transcribe
        if args.output:
            # Save to file
            output_path = transcriber.save_transcription(
                file_path=args.audio_file,
                output_path=args.output,
                task=task,
                language=args.language,
                include_timestamps=args.timestamps,
                format=args.format,
                verbose=args.verbose
            )
            print(f"\nTranscription saved to: {output_path}")
            
            # Summarize if requested and save to separate file
            if args.summarize:
                try:
                    if args.verbose:
                        print("\nGenerating summary...")
                    
                    # Read the transcribed text
                    with open(output_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    
                    summarizer = TextSummarizer(
                        api_key=args.groq_api_key,
                        model=args.groq_model
                    )
                    
                    # Generate summary
                    if args.structured_summary:
                        result = summarizer.summarize_with_structure(
                            text,
                            verbose=args.verbose
                        )
                        summary_text = result['raw']
                    else:
                        summary_text = summarizer.summarize_to_bullets(
                            text,
                            max_bullets=args.max_bullets,
                            verbose=args.verbose
                        )
                    
                    # Save summary to file
                    summary_path = Path(output_path).with_suffix('.summary.txt')
                    with open(summary_path, 'w', encoding='utf-8') as f:
                        f.write(summary_text)
                    
                    print(f"Summary saved to: {summary_path}")
                    
                    # Also print the summary
                    print("\n" + "="*70)
                    print("SUMMARY")
                    print("="*70)
                    print(summary_text)
                    print("="*70)
                
                except Exception as e:
                    print(f"\nWarning: Summarization failed: {e}", file=sys.stderr)
        
        else:
            # Print to stdout
            if args.format == 'json':
                import json
                result = transcriber.transcribe_with_details(
                    file_path=args.audio_file,
                    task=task,
                    language=args.language,
                    verbose=args.verbose
                )
                print(json.dumps(result, indent=2, ensure_ascii=False))
            
            else:
                text = transcriber.transcribe_audio(
                    file_path=args.audio_file,
                    task=task,
                    language=args.language,
                    include_timestamps=args.timestamps,
                    verbose=args.verbose
                )
                print("\n" + "="*70)
                print("TRANSCRIPTION")
                print("="*70)
                print(text)
                print("="*70)
                
                # Summarize if requested
                if args.summarize:
                    try:
                        if args.verbose:
                            print("\nGenerating summary...")
                        
                        summarizer = TextSummarizer(
                            api_key=args.groq_api_key,
                            model=args.groq_model
                        )
                        
                        if args.structured_summary:
                            result = summarizer.summarize_with_structure(
                                text,
                                verbose=args.verbose
                            )
                            print("\n" + "="*70)
                            print("STRUCTURED SUMMARY")
                            print("="*70)
                            print(result['raw'])
                            print("="*70)
                        else:
                            summary = summarizer.summarize_to_bullets(
                                text,
                                max_bullets=args.max_bullets,
                                verbose=args.verbose
                            )
                            print("\n" + "="*70)
                            print("SUMMARY")
                            print("="*70)
                            print(summary)
                            print("="*70)
                    
                    except Exception as e:
                        print(f"\nWarning: Summarization failed: {e}", file=sys.stderr)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
