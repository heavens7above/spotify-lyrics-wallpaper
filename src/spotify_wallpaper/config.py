"""
Configuration & Environment Constants
"""

import os
from pathlib import Path

# Paths
MODULE_DIR = Path(__file__).resolve().parent
SRC_DIR = MODULE_DIR.parent
PROJECT_DIR = SRC_DIR.parent

FONTS_DIR = PROJECT_DIR / "fonts"
DATA_DIR = PROJECT_DIR / "data"
DIST_DIR = PROJECT_DIR / "dist"
PHONE_DIR = DIST_DIR / "phone"
DESKTOP_DIR = DIST_DIR / "desktop"
ASSETS_DIR = PROJECT_DIR / "assets"

# Credentials & Input Files
ENV_FILE = PROJECT_DIR / ".env.spotify"
ENV_ALT_FILE = PROJECT_DIR / ".env"

DEFAULT_LYRICS_FILE = DATA_DIR / "lyrics.md"
FALLBACK_LYRICS_FILE = PROJECT_DIR / "lyrics.md"

DEFAULT_ENGLISH_LYRICS_FILE = DATA_DIR / "lyrics_english.md"
FALLBACK_ENGLISH_LYRICS_FILE = PROJECT_DIR / "lyrics_english.md"

DEFAULT_TRACKS_FILE = DATA_DIR / "spotify_top_tracks.json"
FALLBACK_TRACKS_FILE = PROJECT_DIR / "spotify_top_tracks.json"

DEFAULT_ENGLISH_TRACKS_FILE = DATA_DIR / "spotify_english_tracks.json"
FALLBACK_ENGLISH_TRACKS_FILE = PROJECT_DIR / "spotify_english_tracks.json"

# Resolutions
PHONE_WIDTH = 1290
PHONE_HEIGHT = 2796

DESKTOP_WIDTH = 3840
DESKTOP_HEIGHT = 2160

# Palette (OLED True Black Base)
COLOR_BG = (0, 0, 0, 255)
COLOR_BG_TRANSPARENT = (0, 0, 0, 0)
COLOR_WHITE = (255, 255, 255, 255)
COLOR_OFF_WHITE = (248, 249, 250, 255)
COLOR_FOREGROUND_SILVER = (220, 220, 220, 240)
COLOR_MIDGROUND_ASH = (145, 145, 145, 200)
COLOR_BACKGROUND_CHARCOAL = (75, 75, 75, 175)

# Ensure output directories exist
os.makedirs(PHONE_DIR, exist_ok=True)
os.makedirs(DESKTOP_DIR, exist_ok=True)
