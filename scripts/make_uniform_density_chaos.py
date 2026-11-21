#!/usr/bin/env python3
"""
Generate Uniform-Density Chaotic Wallpapers
Mathematical density-regulation using Golden-Ratio Low-Discrepancy Sampling.
Outputs directly into dist/phone/ and dist/desktop/.
"""

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)
SRC_DIR = os.path.join(PROJECT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from spotify_wallpaper.renderers.uniform_density import generate_uniform_density_wallpapers

if __name__ == "__main__":
    generate_uniform_density_wallpapers()
