"""
Meeting History Viewer
View stored meetings and person information from the database.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'opencv'))

from opencv.database import FaceDatabase
import logging

logging.basicConfig(level=logging.ERROR)


def print_header(text, char="=", width=80):
    """Print a formatted header."""
    print("\n" + char * width)
    print(text.center(width))
    print(char * width)


def print_section(text, char="-", width=80):
    """Print a section divider."""
    print("\n" + char * width)
    print(text)
    print(char * width)


def view_all_people(db):
    """Display all registered people."""
    print_header("REGISTERED PEOPLE")
    
    people = db.get_all_embeddings()
    
    if not people:
        print("\nNo people registered yet.")
        return []
    
    print(f"\nTotal People: {len(people)}\n")
    
    for i, person in enumerate(people, 1):
        person_id = str(person.get('_id', ''))
        name = person.get('name', 'Unknown')
        date = person.get('date', 'N/A')
        
        # Count meetings
        meetings = db.get_all_meetings(person_id)
        meeting_count = len(meetings)
        
        print(f"{i}. {name}")
        print(f"   ID: {person_id}")
        print(f"   Registered: {date}")
        print(f"   Meetings: {meeting_count}")
        print()
    
    return people


def view_person_meetings(db, person):
    """Display all meetings for a specific person."""
    person_id = str(person.get('_id', ''))
    name = person.get('name', 'Unknown')
    
    print_header(f"MEETINGS FOR: {name}")
    
    meetings = db.get_all_meetings(person_id)
    
    if not meetings:
        print(f"\nNo meetings recorded for {name} yet.")
        return
    
    print(f"\nTotal Meetings: {len(meetings)}\n")
    
    for i, meeting in enumerate(meetings, 1):
        timestamp = meeting['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"\n{'=' * 80}")
        print(f"Meeting {i} - {timestamp}")
        print('=' * 80)
        
        print(f"\n📝 SUMMARY:")
        print(meeting['summary'])
        
        print(f"\n📄 TRANSCRIPT:")
        transcript = meeting['transcript']
        if len(transcript) > 300:
            print(transcript[:300] + "...")
            print(f"\n[Full transcript: {len(transcript)} characters]")
        else:
            print(transcript)
        
        if meeting.get('audio_path'):
            print(f"\n🎵 Audio: {meeting['audio_path']}")
        
        if meeting.get('image_path'):
            print(f"📷 Image: {meeting['image_path']}")
        
        print('=' * 80)


def export_to_file(db, filename="meeting_export.txt"):
    """Export all data to a text file."""
    print_header("EXPORTING DATA")
    
    people = db.get_all_embeddings()
    
    if not people:
        print("\nNo data to export.")
        return
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("MEETING HISTORY EXPORT\n")
        f.write("=" * 80 + "\n\n")
        
        for person in people:
            person_id = str(person['_id'])
            name = person['name']
            
            f.write(f"\n\n{'=' * 80}\n")
            f.write(f"PERSON: {name}\n")
            f.write(f"ID: {person_id}\n")
            f.write('=' * 80 + "\n")
            
            meetings = db.get_all_meetings(person_id)
            f.write(f"\nTotal Meetings: {len(meetings)}\n")
            
            for i, meeting in enumerate(meetings, 1):
                timestamp = meeting['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                
                f.write(f"\n{'-' * 80}\n")
                f.write(f"Meeting {i} - {timestamp}\n")
                f.write('-' * 80 + "\n")
                
                f.write(f"\nSUMMARY:\n{meeting['summary']}\n")
                f.write(f"\nTRANSCRIPT:\n{meeting['transcript']}\n")
                
                if meeting.get('audio_path'):
                    f.write(f"\nAudio: {meeting['audio_path']}\n")
                if meeting.get('image_path'):
                    f.write(f"Image: {meeting['image_path']}\n")
    
    print(f"\n✓ Data exported to: {filename}")


def search_meetings(db, keyword):
    """Search meetings by keyword."""
    print_header(f"SEARCH RESULTS: '{keyword}'")
    
    people = db.get_all_embeddings()
    results = []
    
    for person in people:
        person_id = str(person['_id'])
        meetings = db.get_all_meetings(person_id)
        
        for meeting in meetings:
            if keyword.lower() in meeting['transcript'].lower() or \
               keyword.lower() in meeting['summary'].lower():
                results.append({
                    'person': person['name'],
                    'timestamp': meeting['timestamp'],
                    'summary': meeting['summary']
                })
    
    if not results:
        print(f"\nNo meetings found containing '{keyword}'")
        return
    
    print(f"\nFound {len(results)} meeting(s):\n")
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['person']} - {result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   {result['summary'][:200]}...")


def main_menu():
    """Display main menu and handle user input."""
    db = FaceDatabase()
    
    print_header("MEETING HISTORY VIEWER", "=", 80)
    print("\nConnecting to database...")
    
    if not db.connect():
        print("\n❌ Failed to connect to database")
        print("\nMake sure:")
        print("  1. MongoDB is running")
        print("  2. Connection string is correct in opencv/config.py")
        return
    
    print("✓ Connected to database")
    
    while True:
        print("\n" + "=" * 80)
        print("MAIN MENU")
        print("=" * 80)
        print("\n1. View all people")
        print("2. View person's meetings")
        print("3. Search meetings")
        print("4. Export all data")
        print("5. Database statistics")
        print("6. Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == '1':
            people = view_all_people(db)
            
        elif choice == '2':
            people = db.get_all_embeddings()
            if not people:
                print("\nNo people registered yet.")
                continue
            
            print("\nAvailable people:")
            for i, person in enumerate(people, 1):
                print(f"{i}. {person['name']}")
            
            try:
                person_choice = int(input("\nEnter person number: ")) - 1
                if 0 <= person_choice < len(people):
                    view_person_meetings(db, people[person_choice])
                else:
                    print("Invalid choice")
            except ValueError:
                print("Invalid input")
        
        elif choice == '3':
            keyword = input("\nEnter search keyword: ").strip()
            if keyword:
                search_meetings(db, keyword)
        
        elif choice == '4':
            filename = input("\nEnter filename (default: meeting_export.txt): ").strip()
            if not filename:
                filename = "meeting_export.txt"
            export_to_file(db, filename)
        
        elif choice == '5':
            print_header("DATABASE STATISTICS")
            
            people = db.get_all_embeddings()
            total_people = len(people)
            total_meetings = 0
            
            for person in people:
                meetings = db.get_all_meetings(str(person['_id']))
                total_meetings += len(meetings)
            
            print(f"\nTotal People: {total_people}")
            print(f"Total Meetings: {total_meetings}")
            if total_people > 0:
                print(f"Average Meetings per Person: {total_meetings / total_people:.1f}")
        
        elif choice == '6':
            print("\nExiting...")
            break
        
        else:
            print("\nInvalid choice. Please enter 1-6.")
    
    db.disconnect()
    print("\n✓ Disconnected from database")
    print("=" * 80)


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
