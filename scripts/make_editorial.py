#!/usr/bin/env python3
"""
Generate Minimal Editorial Flow Wallpapers
Generates clean spacing wallpapers honoring mobile lockscreen clock safe-zones
and desktop 3-column panoramic landscape.
Outputs directly into dist/phone/ and dist/desktop/.
"""

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)
SRC_DIR = os.path.join(PROJECT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from spotify_wallpaper.renderers.editorial import generate_editorial_wallpapers

if __name__ == "__main__":
    generate_editorial_wallpapers()
