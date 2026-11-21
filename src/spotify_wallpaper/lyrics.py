"""
Typography Phrase Pools & Text Utilities
Provides modular phrases and loaders for wallpaper generation.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional
from .config import (
    DEFAULT_LYRICS_FILE,
    FALLBACK_LYRICS_FILE,
    DEFAULT_ENGLISH_LYRICS_FILE,
    FALLBACK_ENGLISH_LYRICS_FILE,
)

# Original abstract & poetic typography phrases for aesthetic rendering
BASE_LYRIC_POOL = [
    "ORGANIC FREEHAND MONOLINE SCRIPT",
    "MINIMALIST NEGATIVE SPACE RATIO 0.80",
    "HIGH CONTRAST OLED TRUE BLACK CANVAS",
    "GOLDEN RATIO LOW DISCREPANCY DISTRIBUTION",
    "HARMONIC FREQUENCY RESONANCE PATTERN",
    "MULTI TIER DEPTH FIELD PROJECTION SHADOW",
    "CONTINUOUS UNBROKEN HORIZONTAL TEXT STREAM",
    "PARAMETRIC DESIGN EXPERIMENTATION ARCHIVE",
    "DETERMINISTIC WAVE OSCILLATION FIELD",
    "TYPOGRAPHIC GEOMETRY ROTATIONAL MATRIX",
    "HOMOGENEOUS VISUAL DENSITY PACKING",
    "INCOMMENSURATE PHASE ANGLE OSCILLATOR",
]

BASE_POOL = BASE_LYRIC_POOL
BASE_ENGLISH_LYRIC_POOL = BASE_LYRIC_POOL


def resolve_lyrics_file(custom_path: Optional[str] = None, english: bool = False) -> Optional[Path]:
    """Resolves lyrics file from custom path, data/ directory, or project root."""
    if custom_path:
        p = Path(custom_path)
        if p.is_file():
            return p
    candidates = (
        [DEFAULT_ENGLISH_LYRICS_FILE, FALLBACK_ENGLISH_LYRICS_FILE]
        if english
        else [DEFAULT_LYRICS_FILE, FALLBACK_LYRICS_FILE, DEFAULT_LYRICS_FILE.parent / "lyrics.example.md"]
    )
    for p in candidates:
        if p.is_file():
            return p
    return None


def load_lyrics(lyrics_path: Optional[str] = None) -> List[str]:
    """Parses markdown file and extracts uppercase phrase fragments."""
    file_path = resolve_lyrics_file(lyrics_path)
    if not file_path or not file_path.is_file():
        return list(BASE_LYRIC_POOL)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"###\s+\d+\.\s+(.*?)\s+—\s+(.*?)\n>\s+\*\"(.*?)\"\*"
    matches = re.findall(pattern, content)

    lyric_lines = []
    for title, artist, quote in matches:
        phrases = quote.replace("...", "").split(" / ")
        for p in phrases:
            cleaned = p.strip().upper()
            cleaned = re.sub(r'[",*]', '', cleaned)
            if len(cleaned) > 3:
                lyric_lines.append(cleaned)

    return lyric_lines if lyric_lines else list(BASE_LYRIC_POOL)


def load_structured_tracks(lyrics_path: Optional[str] = None) -> List[Dict]:
    """Loads tracks as structured dictionaries."""
    file_path = resolve_lyrics_file(lyrics_path)
    if not file_path or not file_path.is_file():
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"###\s+\d+\.\s+(.*?)\s+—\s+(.*?)\n>\s+\*\"(.*?)\"\*\n-\s+\*\*Album\*\*:\s+(.*?)\n-\s+\*\*Vibe\*\*:\s+(.*?)(?=\n###|\Z)"
    matches = re.findall(pattern, content, re.DOTALL)

    tracks = []
    for title, artist, quote, album, vibe in matches:
        raw_lines = [l.strip() for l in quote.replace("...", "").split(" / ") if l.strip()]
        tracks.append({
            "title": title.strip(),
            "artist": artist.strip(),
            "quote": quote.strip(),
            "album": album.strip(),
            "vibe": vibe.strip(),
            "lines": raw_lines,
        })
    return tracks
