"""
Editorial Minimal & Panorama Wallpaper Engine
Focuses on clean spacing, organic handwritten curves, and dedicated safe zones
for mobile lockscreen widgets and desktop dock/menu bars.
"""

import os
import random
from pathlib import Path
from typing import List, Optional, Dict
from PIL import Image, ImageFont, ImageDraw

from ..config import (
    PHONE_WIDTH,
    PHONE_HEIGHT,
    DESKTOP_WIDTH,
    DESKTOP_HEIGHT,
    PHONE_DIR,
    DESKTOP_DIR,
)
from ..font_loader import load_font
from ..lyrics import load_structured_tracks

DEFAULT_TRACKS_FALLBACK = [
    {
        "title": "Minimalist Composition",
        "artist": "Design Studio",
        "quote": "Organic freehand monoline script / High contrast OLED true black canvas...",
        "album": "Typography Vol. 1",
        "lines": ["Organic freehand monoline script", "High contrast OLED true black canvas..."]
    },
    {
        "title": "Harmonic Resonance",
        "artist": "Waveform Lab",
        "quote": "Deterministic wave oscillation field / Golden ratio low discrepancy distribution...",
        "album": "Parametric Design",
        "lines": ["Deterministic wave oscillation field", "Golden ratio low discrepancy distribution..."]
    },
    {
        "title": "Spatial Dynamics",
        "artist": "Vector Systems",
        "quote": "Multi tier depth field projection shadow / Homogeneous visual density packing...",
        "album": "Spatial Audio",
        "lines": ["Multi tier depth field projection shadow", "Homogeneous visual density packing..."]
    },
]


def render_lyric_card(
    track: Dict,
    font_main: ImageFont.FreeTypeFont,
    font_credit: ImageFont.FreeTypeFont,
    max_width: int = 900,
    angle: float = 0.0,
    ink_color=(245, 245, 245, 245),
    credit_color=(140, 140, 140, 180),
) -> Image.Image:
    """Renders a single lyric card with organic rotation and artist credit."""
    lines = track.get("lines", [])
    if not lines and track.get("quote"):
        lines = [l.strip() for l in track["quote"].split("/") if l.strip()]

    dummy = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(dummy)

    line_boxes = [d.textbbox((0, 0), line, font=font_main) for line in lines]
    max_line_w = max((b[2] - b[0] for b in line_boxes), default=200)
    line_h = max((b[3] - b[1] for b in line_boxes), default=40)

    credit_str = f"— {track.get('title', '')} · {track.get('artist', '')}"
    c_box = d.textbbox((0, 0), credit_str, font=font_credit)
    credit_w = c_box[2] - c_box[0]
    credit_h = c_box[3] - c_box[1]

    card_w = int(max(max_line_w, credit_w) + 80)
    card_h = int(len(lines) * (line_h + 12) + credit_h + 35)

    card = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card)

    y_offset = 10
    for line in lines:
        cdraw.text((15, y_offset), line, font=font_main, fill=ink_color)
        y_offset += line_h + 12

    cdraw.text((25, y_offset + 6), credit_str, font=font_credit, fill=credit_color)

    if abs(angle) > 0.05:
        card = card.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)

    return card


def generate_editorial_wallpapers(
    tracks: Optional[List[Dict]] = None,
    output_phone_dir: Optional[Path] = None,
    output_desktop_dir: Optional[Path] = None,
    devices: str = "all",
) -> Dict[str, str]:
    """Generates phone editorial minimal flow and desktop 4K panorama wallpapers."""
    out_phone = Path(output_phone_dir or PHONE_DIR)
    out_desktop = Path(output_desktop_dir or DESKTOP_DIR)
    out_phone.mkdir(parents=True, exist_ok=True)
    out_desktop.mkdir(parents=True, exist_ok=True)

    track_list = tracks or load_structured_tracks() or DEFAULT_TRACKS_FALLBACK
    saved_files = {}

    font_main_phone = load_font("Caveat.ttf", 44)
    font_credit_phone = load_font("IndieFlower.ttf", 24)

    if devices in ("phone", "all"):
        print("Rendering Phone Minimal Editorial Flow...")
        bg_phone = Image.new("RGBA", (PHONE_WIDTH, PHONE_HEIGHT), (0, 0, 0, 255))
        safe_top = 680
        safe_bottom = 2400
        y = safe_top + 40
        random.seed(42)

        for i, t in enumerate(track_list[:13]):
            angle = random.uniform(-2.5, 2.5)
            alpha = random.randint(220, 255) if i < 5 else random.randint(180, 230)
            ink = (248, 248, 248, alpha)
            credit_ink = (140, 140, 140, int(alpha * 0.75))

            card = render_lyric_card(
                t, font_main_phone, font_credit_phone,
                max_width=980, angle=angle, ink_color=ink, credit_color=credit_ink
            )

            if i % 3 == 0:
                x = 80
            elif i % 3 == 1:
                x = (PHONE_WIDTH - card.width) // 2
            else:
                x = PHONE_WIDTH - card.width - 80

            x = max(40, min(x, PHONE_WIDTH - card.width - 40))
            if y + card.height > safe_bottom:
                break

            bg_phone.alpha_composite(card, (int(x), int(y)))
            y += card.height + 25

        p1 = out_phone / "editorial_minimal.png"
        bg_phone.convert("RGB").save(str(p1), quality=100)
        saved_files["phone_editorial"] = str(p1)
        print(f"-> Saved: {p1}")

    if devices in ("desktop", "all"):
        print("Rendering Desktop 4K Panorama (3-Column Flow)...")
        bg_desk = Image.new("RGBA", (DESKTOP_WIDTH, DESKTOP_HEIGHT), (0, 0, 0, 255))
        font_main_desk = load_font("Caveat.ttf", 46)
        font_credit_desk = load_font("IndieFlower.ttf", 26)

        col_width = 1100
        col_gap = 120
        left_margin = (DESKTOP_WIDTH - (3 * col_width + 2 * col_gap)) // 2
        columns_x = [
            left_margin,
            left_margin + col_width + col_gap,
            left_margin + 2 * (col_width + col_gap)
        ]

        safe_top = 160
        safe_bottom = 2000
        col_y = [safe_top + random.randint(0, 40) for _ in range(3)]
        random.seed(88)

        for i, t in enumerate(track_list[:36]):
            col_idx = col_y.index(min(col_y))
            angle = random.uniform(-2.5, 2.5)
            alpha = random.randint(190, 255)
            ink = (245, 245, 245, alpha)
            credit_ink = (135, 135, 135, int(alpha * 0.7))

            card = render_lyric_card(
                t, font_main_desk, font_credit_desk,
                max_width=col_width - 60, angle=angle, ink_color=ink, credit_color=credit_ink
            )

            if col_y[col_idx] + card.height > safe_bottom:
                continue

            x = columns_x[col_idx] + random.randint(-20, 20)
            bg_desk.alpha_composite(card, (int(x), int(col_y[col_idx])))
            col_y[col_idx] += card.height + random.randint(30, 50)

        p2 = out_desktop / "panorama_3column_4k.png"
        bg_desk.convert("RGB").save(str(p2), quality=100)
        saved_files["desktop_panorama"] = str(p2)
        print(f"-> Saved: {p2}")

    return saved_files
