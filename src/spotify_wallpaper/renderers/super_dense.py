"""
Super-Dense (200+ Line) Wallpaper Engine
Packs 200 to 240+ lines of lyrics tightly across the screen:
- Wall-to-wall pure text
- Continuous horizontal phrase chaining
- Interleaved chaotic lines (mysterious from afar, readable up close)
"""

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
from ..font_loader import load_font, prewarm_font_range
from ..lyrics import BASE_LYRIC_POOL, load_lyrics


def render_super_dense_canvas(
    width: int,
    height: int,
    lyrics: Optional[List[str]] = None,
    angle: float = -24.0,
    line_spacing_factor: float = 0.82,
    font_sizes: Optional[List[int]] = None,
    seed: int = 42,
    font_name: str = "ArchitectsDaughter.ttf",
) -> Image.Image:
    """Renders a super-dense wallpaper canvas packed with 200+ lines of lyrics."""
    random.seed(seed)
    pool = lyrics if lyrics else BASE_LYRIC_POOL
    pool_len = len(pool)

    cw = int(width * 1.7)
    ch = int(height * 1.6)

    canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    sizes = font_sizes or [22, 26, 32, 24, 28, 38, 20, 30]
    fonts = {sz: load_font(font_name, sz) for sz in sizes}

    curr_y = 10
    line_idx = 0

    while curr_y < ch - 30:
        sz = sizes[line_idx % len(sizes)]
        font = fonts[sz]

        # Horizontal phrase chain
        p1 = pool[line_idx % pool_len]
        p2 = pool[(line_idx * 3 + 1) % pool_len]
        p3 = pool[(line_idx * 7 + 2) % pool_len]
        p4 = pool[(line_idx * 11 + 3) % pool_len]
        p5 = pool[(line_idx * 13 + 4) % pool_len]
        line_text = f"{p1}   ·   {p2}   ·   {p3}   ·   {p4}   ·   {p5}"

        # Tone variation
        lum = random.randint(140, 235)
        alpha = random.randint(190, 255)
        color = (lum, lum, lum, alpha)

        x_shift = random.randint(-40, 40)
        draw.text((x_shift, curr_y), line_text, font=font, fill=color)

        bbox = draw.textbbox((0, 0), line_text, font=font)
        lh = bbox[3] - bbox[1]
        curr_y += max(int(lh * line_spacing_factor), 12)
        line_idx += 1

    rotated = canvas.rotate(angle, resample=Image.Resampling.BICUBIC, center=(cw // 2, ch // 2))

    left = (cw - width) // 2
    top = (ch - height) // 2
    cropped = rotated.crop((left, top, left + width, top + height))

    bg = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    bg.paste(cropped, (0, 0))
    return bg


def generate_super_dense_wallpapers(
    lyrics: Optional[List[str]] = None,
    output_phone_dir: Optional[Path] = None,
    output_desktop_dir: Optional[Path] = None,
    devices: str = "all",
) -> Dict[str, str]:
    """Generates phone and desktop super-dense wallpapers."""
    out_phone = Path(output_phone_dir or PHONE_DIR)
    out_desktop = Path(output_desktop_dir or DESKTOP_DIR)
    out_phone.mkdir(parents=True, exist_ok=True)
    out_desktop.mkdir(parents=True, exist_ok=True)

    pool = lyrics or load_lyrics() or BASE_LYRIC_POOL
    saved_files = {}

    if devices in ("phone", "all"):
        print("Rendering Phone Super-Dense Wall (Tightly Packed - 200 lines)...")
        p_dense = render_super_dense_canvas(PHONE_WIDTH, PHONE_HEIGHT, pool, angle=-24, line_spacing_factor=0.82, seed=42)
        p1 = out_phone / "super_dense_wall.png"
        p_dense.convert("RGB").save(str(p1), quality=100)
        saved_files["phone_dense"] = str(p1)
        print(f"-> Saved: {p1}")

        print("Rendering Phone Dense Tapestry (Interleaved Chaos - 239 lines)...")
        p_tapestry = render_super_dense_canvas(
            PHONE_WIDTH, PHONE_HEIGHT, pool, angle=-24, line_spacing_factor=0.73,
            font_sizes=[24, 36, 48, 28, 40, 22, 44, 32, 50], seed=77
        )
        p2 = out_phone / "dense_tapestry.png"
        p_tapestry.convert("RGB").save(str(p2), quality=100)
        saved_files["phone_tapestry"] = str(p2)
        print(f"-> Saved: {p2}")

    if devices in ("desktop", "all"):
        print("Rendering Desktop 4K Super-Dense Wall (3840x2160 - 244 lines)...")
        d_dense = render_super_dense_canvas(DESKTOP_WIDTH, DESKTOP_HEIGHT, pool, angle=-22, line_spacing_factor=0.82, seed=88)
        p3 = out_desktop / "super_dense_wall_4k.png"
        d_dense.convert("RGB").save(str(p3), quality=100)
        saved_files["desktop_dense"] = str(p3)
        print(f"-> Saved: {p3}")

    return saved_files
