"""
Logical Chaos 3D Depth Wallpaper Engine
Implements a deterministic multi-frequency harmonic wave oscillator:
  z(i) = 0.5 + 0.5 * [ 0.50*sin(2π*i/7.3) + 0.32*cos(2π*i/3.7 + 0.4) + 0.18*sin(2π*i/13.1 + 1.2) ]
This 'ordered chaos' creates organic crests and troughs of depth.
"""

import math
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
from .uniform_density import draw_badge


def logical_chaos_oscillator(i: int) -> float:
    """Multi-frequency incommensurate wave oscillator in [0.0, 1.0]."""
    w1 = math.sin(2.0 * math.pi * i / 7.3)
    w2 = math.cos(2.0 * math.pi * i / 3.7 + 0.4)
    w3 = math.sin(2.0 * math.pi * i / 13.1 + 1.2)
    raw = 0.50 * w1 + 0.32 * w2 + 0.18 * w3
    return max(0.0, min(1.0, (raw + 1.0) / 2.0))


def render_logical_chaos_canvas(
    width: int,
    height: int,
    lyrics: Optional[List[str]] = None,
    angle: float = -24.0,
    is_phone: bool = True,
    font_name: str = "ArchitectsDaughter.ttf",
) -> Image.Image:
    """Renders logical chaos canvas with harmonic wave depth oscillation."""
    cw = int(width * 1.7)
    ch = int(height * 1.6)

    canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    fonts = prewarm_font_range(font_name, 18, 75)
    pool = lyrics if lyrics else BASE_LYRIC_POOL
    pool_len = len(pool)

    curr_y = 20
    i = 0

    while curr_y < ch - 60:
        z = logical_chaos_oscillator(i)

        # 1. Scale modulated by equation
        sz = int(22 + 42 * (z ** 1.35))
        f = fonts.get(sz, load_font(font_name, sz))

        # 2. Luminance & tone (deep charcoal to luminous silver)
        lum = int(65 + 165 * (z ** 1.15))
        alpha = int(185 + 70 * z)
        text_color = (lum, lum, lum, alpha)

        # 3. Horizontal phase shift (smooth mathematical sway)
        x_shift = int(25 + 35 * math.cos(0.32 * i))

        # 4. Text line
        p1 = pool[i % pool_len]
        p2 = pool[(i * 3 + 1) % pool_len]
        p3 = pool[(i * 7 + 2) % pool_len]
        p4 = pool[(i * 11 + 3) % pool_len]
        if is_phone:
            line_str = f"{p1}   ·   {p2}   ·   {p3}   ·   {p4}"
        else:
            p5 = pool[(i * 13 + 4) % pool_len]
            p6 = pool[(i * 17 + 5) % pool_len]
            line_str = f"{p1}   ·   {p2}   ·   {p3}   ·   {p4}   ·   {p5}   ·   {p6}"

        # 5. Black projection shadow proportional to z-depth
        if z > 0.45:
            depth_factor = (z - 0.45) / 0.55
            off_x = int(depth_factor * 6) + 1
            off_y = int(depth_factor * 8) + 1
            s_stroke = 2 if depth_factor > 0.4 else 1

            # Cast black shadow
            draw.text(
                (x_shift + off_x, curr_y + off_y),
                line_str,
                font=f,
                fill=(0, 0, 0, 255),
                stroke_width=s_stroke,
                stroke_fill=(0, 0, 0, 255),
            )
            # Text with 1px black separation outline
            draw.text(
                (x_shift, curr_y),
                line_str,
                font=f,
                fill=text_color,
                stroke_width=1,
                stroke_fill=(0, 0, 0, 255),
            )
        elif z > 0.20:
            # Midground subtle shadow
            draw.text(
                (x_shift + 1, curr_y + 2),
                line_str,
                font=f,
                fill=(0, 0, 0, 180),
                stroke_width=1,
                stroke_fill=(0, 0, 0, 180),
            )
            draw.text((x_shift, curr_y), line_str, font=f, fill=text_color)
        else:
            # Deep background whisper text
            draw.text((x_shift, curr_y), line_str, font=f, fill=text_color)

        bbox = draw.textbbox((0, 0), line_str, font=f)
        line_h = bbox[3] - bbox[1]

        # Spacing modulated by current line height
        curr_y += max(int(line_h * 0.85), 20)
        i += 1

    rotated = canvas.rotate(angle, resample=Image.Resampling.BICUBIC, center=(cw // 2, ch // 2))

    left = (cw - width) // 2
    top = (ch - height) // 2
    cropped = rotated.crop((left, top, left + width, top + height))

    bg = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    bg.paste(cropped, (0, 0))
    return bg


def generate_logical_chaos_wallpapers(
    lyrics: Optional[List[str]] = None,
    output_phone_dir: Optional[Path] = None,
    output_desktop_dir: Optional[Path] = None,
    devices: str = "all",
    include_cutout: bool = True,
) -> Dict[str, str]:
    """Generates phone and desktop logical chaos wallpapers."""
    out_phone = Path(output_phone_dir or PHONE_DIR)
    out_desktop = Path(output_desktop_dir or DESKTOP_DIR)
    out_phone.mkdir(parents=True, exist_ok=True)
    out_desktop.mkdir(parents=True, exist_ok=True)

    pool = lyrics or load_lyrics() or BASE_LYRIC_POOL
    saved_files = {}

    if devices in ("phone", "all"):
        print("Rendering Phone Logical Chaos Wall...")
        p_wall = render_logical_chaos_canvas(PHONE_WIDTH, PHONE_HEIGHT, pool, angle=-24.0, is_phone=True)
        p1 = out_phone / "logical_chaos_wall.png"
        p_wall.convert("RGB").save(str(p1), quality=100)
        saved_files["phone_wall"] = str(p1)
        print(f"-> Saved: {p1}")

        if include_cutout:
            print("Rendering Phone Logical Chaos Cutout...")
            mask = Image.new("L", (PHONE_WIDTH, PHONE_HEIGHT), 255)
            mask_draw = ImageDraw.Draw(mask)
            void_poly = [(680, 1150), (PHONE_WIDTH, 880), (PHONE_WIDTH, 1780), (640, 1650)]
            mask_draw.polygon(void_poly, fill=0)

            p_cutout = Image.new("RGBA", (PHONE_WIDTH, PHONE_HEIGHT), (0, 0, 0, 255))
            p_cutout.paste(p_wall, (0, 0), mask=mask)
            draw_badge(p_cutout, cx=980, cy=1350, line1="SPOTIFY ON REPEAT", line2="LOGICAL CHAOS ARCHIVE")
            p2 = out_phone / "logical_chaos_cutout.png"
            p_cutout.convert("RGB").save(str(p2), quality=100)
            saved_files["phone_cutout"] = str(p2)
            print(f"-> Saved: {p2}")

    if devices in ("desktop", "all"):
        print("Rendering Desktop 4K Logical Chaos Wall...")
        d_wall = render_logical_chaos_canvas(DESKTOP_WIDTH, DESKTOP_HEIGHT, pool, angle=-22.0, is_phone=False)
        p3 = out_desktop / "logical_chaos_wall_4k.png"
        d_wall.convert("RGB").save(str(p3), quality=100)
        saved_files["desktop_wall"] = str(p3)
        print(f"-> Saved: {p3}")

        if include_cutout:
            print("Rendering Desktop 4K Logical Chaos Cutout...")
            d_mask = Image.new("L", (DESKTOP_WIDTH, DESKTOP_HEIGHT), 255)
            d_mask_draw = ImageDraw.Draw(d_mask)
            d_void_poly = [(2100, 0), (DESKTOP_WIDTH, 0), (DESKTOP_WIDTH, DESKTOP_HEIGHT), (1700, DESKTOP_HEIGHT)]
            d_mask_draw.polygon(d_void_poly, fill=0)

            d_cutout = Image.new("RGBA", (DESKTOP_WIDTH, DESKTOP_HEIGHT), (0, 0, 0, 255))
            d_cutout.paste(d_wall, (0, 0), mask=d_mask)
            draw_badge(d_cutout, cx=2900, cy=1080, line1="SPOTIFY ON REPEAT", line2="LOGICAL CHAOS ARCHIVE")
            p4 = out_desktop / "logical_chaos_cutout_4k.png"
            d_cutout.convert("RGB").save(str(p4), quality=100)
            saved_files["desktop_cutout"] = str(p4)
            print(f"-> Saved: {p4}")

    return saved_files
