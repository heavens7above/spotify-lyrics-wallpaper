#!/usr/bin/env python3
"""
Generate Chaotic 3D Depth Wallpapers
Multi-tier Z-space planes, variable angles (-29° to -19°), and black projection shadows.
Outputs directly into dist/phone/ and dist/desktop/.
"""

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)
SRC_DIR = os.path.join(PROJECT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from spotify_wallpaper.renderers.chaotic_3d import generate_chaotic_3d_wallpapers

if __name__ == "__main__":
    generate_chaotic_3d_wallpapers()
