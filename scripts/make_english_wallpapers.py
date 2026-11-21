#!/usr/bin/env python3
"""
Generate Pure English Chaotic 3D Wallpapers
Filters English-only tracks from curated data and renders chaotic 3D depth-field wallpapers.
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
from spotify_wallpaper.lyrics import load_lyrics, resolve_lyrics_file, BASE_ENGLISH_LYRIC_POOL

if __name__ == "__main__":
    eng_file = resolve_lyrics_file(english=True)
    eng_lyrics = load_lyrics(str(eng_file)) if eng_file else BASE_ENGLISH_LYRIC_POOL
    generate_chaotic_3d_wallpapers(
        lyrics=eng_lyrics,
        prefix="english_chaotic_3d",
    )
