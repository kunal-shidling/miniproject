"""
Utility functions for the meeting pipeline.
"""

import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


def create_directories(base_dir: Path):
    """
    Create necessary directories for the pipeline.
    
    Args:
        base_dir: Base directory path
    """
    directories = [
        base_dir / "images",
        base_dir / "audio",
        base_dir / "transcripts"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Directory created/verified: {directory}")


def generate_filename(person_name: str, file_type: str, extension: str) -> str:
    """
    Generate a timestamped filename.
    
    Args:
        person_name: Name of the person
        file_type: Type of file (e.g., 'meeting', 'transcript')
        extension: File extension (e.g., 'wav', 'txt')
        
    Returns:
        str: Generated filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = person_name.replace(' ', '_').replace('/', '_').replace('\\', '_')
    return f"{file_type}_{safe_name}_{timestamp}.{extension}"


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        str: Formatted duration (e.g., "2m 30s")
    """
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    
    if mins > 0:
        return f"{mins}m {secs}s"
    else:
        return f"{secs}s"


def truncate_text(text: str, max_length: int = 500) -> str:
    """
    Truncate text to specified length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def validate_file_exists(file_path: str) -> bool:
    """
    Check if a file exists.
    
    Args:
        file_path: Path to file
        
    Returns:
        bool: True if exists, False otherwise
    """
    return os.path.exists(file_path) and os.path.isfile(file_path)


def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes.
    
    Args:
        file_path: Path to file
        
    Returns:
        float: File size in MB
    """
    if not validate_file_exists(file_path):
        return 0.0
    
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)


def print_section_header(title: str, width: int = 80):
    """
    Print a formatted section header.
    
    Args:
        title: Section title
        width: Width of the header
    """
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)


def print_info_box(title: str, content: dict, width: int = 80):
    """
    Print formatted information box.
    
    Args:
        title: Box title
        content: Dictionary of key-value pairs to display
        width: Width of the box
    """
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)
    
    for key, value in content.items():
        print(f"{key}: {value}")
    
    print("=" * width)


def safe_input(prompt: str, default: str = "") -> str:
    """
    Safe input with default value.
    
    Args:
        prompt: Input prompt
        default: Default value if input is empty
        
    Returns:
        str: User input or default
    """
    try:
        user_input = input(prompt).strip()
        return user_input if user_input else default
    except (KeyboardInterrupt, EOFError):
        return default


def confirm_action(prompt: str, default: bool = False) -> bool:
    """
    Ask user for confirmation.
    
    Args:
        prompt: Confirmation prompt
        default: Default response if user just presses Enter
        
    Returns:
        bool: True if confirmed, False otherwise
    """
    default_text = "[Y/n]" if default else "[y/N]"
    response = safe_input(f"{prompt} {default_text}: ", "").lower()
    
    if not response:
        return default
    
    return response in ['y', 'yes']
