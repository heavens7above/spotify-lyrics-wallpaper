#!/usr/bin/env python3
"""
Master Wallpaper Generator CLI
Unified runner for the Spotify Lyrics Aesthetic Wallpaper Generator.
"""

import sys
import os

# Add src/ to python search path
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PROJECT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from spotify_wallpaper.cli import main

if __name__ == "__main__":
    main()
