"""
Cross-Platform Font Resolver and Cache
Safely loads bundled handwriting fonts and system sans fonts across macOS, Linux, and Windows.
"""

import os
import sys
from pathlib import Path
from PIL import ImageFont
from .config import FONTS_DIR

_FONT_CACHE = {}

# System font candidate locations
SYSTEM_FONT_CANDIDATES_BOLD = [
    # macOS
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    # Linux
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    # Windows
    "C:\\Windows\\Fonts\\arialbd.ttf",
    "C:\\Windows\\Fonts\\segoeui.ttf",
]

SYSTEM_FONT_CANDIDATES_REGULAR = [
    # macOS
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    # Linux
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/TTF/DejaVuSans.ttf",
    # Windows
    "C:\\Windows\\Fonts\\arial.ttf",
    "C:\\Windows\\Fonts\\segoeui.ttf",
]


def get_bundled_font_path(font_name: str) -> str:
    """Returns absolute path to a bundled font in fonts/ directory."""
    path = FONTS_DIR / font_name
    if path.is_file():
        return str(path)
    # Check if font_name needs .ttf extension
    if not font_name.endswith(".ttf"):
        path_ttf = FONTS_DIR / f"{font_name}.ttf"
        if path_ttf.is_file():
            return str(path_ttf)
    # Fallback to first available ttf in fonts dir
    for f in FONTS_DIR.glob("*.ttf"):
        return str(f)
    return ""


def get_sans_font_path(bold: bool = True) -> str:
    """Finds an available system sans-serif font across platforms, or falls back to bundled font."""
    candidates = SYSTEM_FONT_CANDIDATES_BOLD if bold else SYSTEM_FONT_CANDIDATES_REGULAR
    for p in candidates:
        if os.path.isfile(p):
            return p

    # Fallback to bundled font if system font not found
    fallback = get_bundled_font_path("ArchitectsDaughter.ttf")
    if fallback:
        return fallback

    return ""


def load_font(font_identifier: str, size: int) -> ImageFont.FreeTypeFont:
    """
    Load a font with memory caching.
    font_identifier can be a filename in fonts/, an absolute path, or 'sans_bold' / 'sans_reg'.
    """
    cache_key = (font_identifier, size)
    if cache_key in _FONT_CACHE:
        return _FONT_CACHE[cache_key]

    resolved_path = None
    if font_identifier == "sans_bold":
        resolved_path = get_sans_font_path(bold=True)
    elif font_identifier in ("sans_reg", "sans_regular"):
        resolved_path = get_sans_font_path(bold=False)
    elif os.path.isabs(font_identifier) and os.path.isfile(font_identifier):
        resolved_path = font_identifier
    else:
        resolved_path = get_bundled_font_path(font_identifier)

    font = None
    if resolved_path and os.path.isfile(resolved_path):
        try:
            font = ImageFont.truetype(resolved_path, size)
        except Exception:
            font = None

    if font is None:
        # Ultimate fallback
        try:
            default_font_path = get_bundled_font_path("ArchitectsDaughter.ttf")
            font = ImageFont.truetype(default_font_path, size)
        except Exception:
            font = ImageFont.load_default()

    _FONT_CACHE[cache_key] = font
    return font


def prewarm_font_range(font_name: str, min_size: int, max_size: int) -> dict:
    """Pre-caches a dictionary of font sizes for rapid access in render loops."""
    return {sz: load_font(font_name, sz) for sz in range(min_size, max_size + 1)}
