#!/usr/bin/env python3
"""
Generate Super-Dense Wallpapers
Packs 200+ to 240+ lines of lyrics tightly across the screen with wall-to-wall pure text.
Outputs directly into dist/phone/ and dist/desktop/.
"""

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)
SRC_DIR = os.path.join(PROJECT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from spotify_wallpaper.renderers.super_dense import generate_super_dense_wallpapers

if __name__ == "__main__":
    generate_super_dense_wallpapers()
