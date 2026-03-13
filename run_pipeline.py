"""
Quick start script for the meeting pipeline.
Simple interface to run the integrated system.
"""

import sys
import os

# Add paths
sys.path.insert(0, os.path.dirname(__file__))

from meeting_pipeline import MeetingPipeline
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    print("\n" + "🎯 " + "=" * 76 + " 🎯")
    print("MEETING ASSISTANT - Integrated Pipeline".center(80))
    print("🎯 " + "=" * 76 + " 🎯")
    
    print("\n📋 System Requirements:")
    print("   ✓ Camera (for face recognition)")
    print("   ✓ Microphone (for audio recording)")
    print("   ✓ MongoDB (running)")
    print("   ✓ Groq API key (in environment or .env file)")
    
    print("\n🔄 Pipeline Steps:")
    print("   1. Face Detection & Recognition")
    print("   2. Display Person Info & Last Meeting")
    print("   3. Record Conversation")
    print("   4. Transcribe Audio to Text")
    print("   5. Generate Summary")
    print("   6. Store Meeting in Database")
    
    print("\n" + "=" * 80)
    response = input("\nReady to start? (y/n): ").strip().lower()
    
    if response not in ['y', 'yes']:
        print("Exiting...")
        sys.exit(0)
    
    try:
        pipeline = MeetingPipeline()
        pipeline.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logging.error(f"Pipeline error: {e}", exc_info=True)
