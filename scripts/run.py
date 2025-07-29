#!/usr/bin/env python3
"""Main entry point for speech-to-text application"""

import os
import sys

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import and run the main script
from src.speech_to_text import main

if __name__ == "__main__":
    main()
