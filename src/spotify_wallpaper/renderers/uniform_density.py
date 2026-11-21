"""
Uniform-Density Chaotic 3D Wallpaper Engine
Mathematical density-regulation using Golden-Ratio Low-Discrepancy Sampling:
  z_i = (0.382 + i * 0.6180339887) % 1.0
This equation enforces strictly homogeneous visual density across the canvas:
- ZERO high-dense or low-dense clumps/bands
- Completely uniform visual mass from top to bottom
- Continuous chaotic placement: horizontal phase jitter via sqrt(2) irrational rotation
- Balanced 3D depth field on every line
"""

import math
from pathlib import Path
from typing import List, Optional
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

PHI = (math.sqrt(5.0) - 1.0) / 2.0  # Golden ratio fraction ~ 0.618033988749895


def render_uniform_density_canvas(
    width: int,
    height: int,
    lyrics: Optional[List[str]] = None,
    angle: float = -24.0,
    is_phone: bool = True,
    font_name: str = "ArchitectsDaughter.ttf",
) -> Image.Image:
    """Renders a uniform-density chaotic canvas using low-discrepancy sampling."""
    cw = int(width * 1.7)
    ch = int(height * 1.6)

    canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    fonts = prewarm_font_range(font_name, 24, 62)
    pool = lyrics if lyrics else BASE_LYRIC_POOL
    pool_len = len(pool)

    curr_y = 20
    i = 0

    while curr_y < ch - 60:
        # 1. Low-discrepancy depth factor z in [0, 1]
        z = (0.382 + i * PHI) % 1.0

        # 2. Balanced font scale: 28pt to 48pt
        sz = int(28 + 20 * (z ** 1.05))
        f = fonts.get(sz, load_font(font_name, sz))

        # 3. Dimensional tone (charcoal to luminous silver)
        lum = int(85 + 140 * z)
        alpha = int(200 + 55 * z)
        text_color = (lum, lum, lum, alpha)

        # 4. Chaotic horizontal shift without clustering
        x_shift = int(30 + 45 * (((0.23 + i * 1.41421356) % 1.0) - 0.5))

        # 5. Continuous phrase stream
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

        # 6. Black projection shadow for foreground lines (z > 0.62)
        if z > 0.62:
            shadow_factor = (z - 0.62) / 0.38
            off_x = int(shadow_factor * 4) + 1
            off_y = int(shadow_factor * 5) + 1

            # Cast black shadow
            draw.text(
                (x_shift + off_x, curr_y + off_y),
                line_str,
                font=f,
                fill=(0, 0, 0, 255),
                stroke_width=2,
                stroke_fill=(0, 0, 0, 255),
            )
            # Text with fine 1px black separation outline
            draw.text(
                (x_shift, curr_y),
                line_str,
                font=f,
                fill=text_color,
                stroke_width=1,
                stroke_fill=(0, 0, 0, 255),
            )
        elif z > 0.32:
            # Midground text with subtle shadow
            draw.text(
                (x_shift + 1, curr_y + 2),
                line_str,
                font=f,
                fill=(0, 0, 0, 200),
                stroke_width=1,
                stroke_fill=(0, 0, 0, 200),
            )
            draw.text((x_shift, curr_y), line_str, font=f, fill=text_color)
        else:
            # Deep background whisper text
            draw.text((x_shift, curr_y), line_str, font=f, fill=text_color)

        bbox = draw.textbbox((0, 0), line_str, font=f)
        line_h = bbox[3] - bbox[1]

        # CONSTANT DENSITY CONSTRAINT:
        # Uniform vertical packing ratio rho = 0.80 ensures homogeneous density
        curr_y += max(int(line_h * 0.80), 18)
        i += 1

    rotated = canvas.rotate(angle, resample=Image.Resampling.BICUBIC, center=(cw // 2, ch // 2))

    left = (cw - width) // 2
    top = (ch - height) // 2
    cropped = rotated.crop((left, top, left + width, top + height))

    bg = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    bg.paste(cropped, (0, 0))
    return bg


def draw_badge(
    canvas: Image.Image,
    cx: int,
    cy: int,
    line1: str = "SPOTIFY ON REPEAT",
    line2: str = "UNIFORM DENSITY ARCHIVE",
):
    """Draws a clean editorial typography badge in the cutout void."""
    draw = ImageDraw.Draw(canvas)
    f1 = load_font("sans_bold", 26)
    f2 = load_font("sans_reg", 20)

    def draw_tracked(text, y, font, color, tracking=5):
        total_w = sum(
            draw.textbbox((0, 0), ch, font=font)[2] - draw.textbbox((0, 0), ch, font=font)[0] + tracking
            for ch in text
        ) - tracking
        start_x = cx - total_w // 2
        for ch in text:
            draw.text((start_x, y), ch, font=font, fill=color)
            w = draw.textbbox((0, 0), ch, font=font)[2] - draw.textbbox((0, 0), ch, font=font)[0]
            start_x += w + tracking

    draw_tracked(line1, cy - 22, f1, (225, 225, 225, 240), tracking=5)
    draw_tracked(line2, cy + 18, f2, (155, 155, 155, 200), tracking=4)


def generate_uniform_density_wallpapers(
    lyrics: Optional[List[str]] = None,
    output_phone_dir: Optional[Path] = None,
    output_desktop_dir: Optional[Path] = None,
    devices: str = "all",  # "phone", "desktop", "all"
    include_cutout: bool = True,
) -> Dict[str, str]:
    """Generates phone and desktop uniform-density wallpapers."""
    out_phone = Path(output_phone_dir or PHONE_DIR)
    out_desktop = Path(output_desktop_dir or DESKTOP_DIR)
    out_phone.mkdir(parents=True, exist_ok=True)
    out_desktop.mkdir(parents=True, exist_ok=True)

    pool = lyrics or load_lyrics() or BASE_LYRIC_POOL
    saved_files = {}

    if devices in ("phone", "all"):
        print("Rendering Phone Uniform-Density Wall...")
        p_wall = render_uniform_density_canvas(PHONE_WIDTH, PHONE_HEIGHT, pool, angle=-24.0, is_phone=True)
        p1 = out_phone / "uniform_density_wall.png"
        p_wall.convert("RGB").save(str(p1), quality=100)
        saved_files["phone_wall"] = str(p1)
        print(f"-> Saved: {p1}")

        if include_cutout:
            print("Rendering Phone Uniform-Density Cutout...")
            mask = Image.new("L", (PHONE_WIDTH, PHONE_HEIGHT), 255)
            mask_draw = ImageDraw.Draw(mask)
            void_poly = [(660, 1140), (PHONE_WIDTH, 880), (PHONE_WIDTH, 1800), (620, 1660)]
            mask_draw.polygon(void_poly, fill=0)

            p_cutout = Image.new("RGBA", (PHONE_WIDTH, PHONE_HEIGHT), (0, 0, 0, 255))
            p_cutout.paste(p_wall, (0, 0), mask=mask)
            draw_badge(p_cutout, cx=970, cy=1350, line1="SPOTIFY ON REPEAT", line2="UNIFORM DENSITY ARCHIVE")
            p2 = out_phone / "uniform_density_cutout.png"
            p_cutout.convert("RGB").save(str(p2), quality=100)
            saved_files["phone_cutout"] = str(p2)
            print(f"-> Saved: {p2}")

    if devices in ("desktop", "all"):
        print("Rendering Desktop 4K Uniform-Density Wall...")
        d_wall = render_uniform_density_canvas(DESKTOP_WIDTH, DESKTOP_HEIGHT, pool, angle=-22.0, is_phone=False)
        p3 = out_desktop / "uniform_density_wall_4k.png"
        d_wall.convert("RGB").save(str(p3), quality=100)
        saved_files["desktop_wall"] = str(p3)
        print(f"-> Saved: {p3}")

        if include_cutout:
            print("Rendering Desktop 4K Uniform-Density Cutout...")
            d_mask = Image.new("L", (DESKTOP_WIDTH, DESKTOP_HEIGHT), 255)
            d_mask_draw = ImageDraw.Draw(d_mask)
            d_void_poly = [(2100, 0), (DESKTOP_WIDTH, 0), (DESKTOP_WIDTH, DESKTOP_HEIGHT), (1700, DESKTOP_HEIGHT)]
            d_mask_draw.polygon(d_void_poly, fill=0)

            d_cutout = Image.new("RGBA", (DESKTOP_WIDTH, DESKTOP_HEIGHT), (0, 0, 0, 255))
            d_cutout.paste(d_wall, (0, 0), mask=d_mask)
            draw_badge(d_cutout, cx=2900, cy=1080, line1="SPOTIFY ON REPEAT", line2="UNIFORM DENSITY ARCHIVE")
            p4 = out_desktop / "uniform_density_cutout_4k.png"
            d_cutout.convert("RGB").save(str(p4), quality=100)
            saved_files["desktop_cutout"] = str(p4)
            print(f"-> Saved: {p4}")

    return saved_files
