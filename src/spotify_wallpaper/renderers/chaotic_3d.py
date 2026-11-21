"""
Chaotic 3D Depth Wallpaper Engine
- Multi-tier Z-space planes (deep charcoal, mid ash-silver, near light silver)
- Variable angles (-29° to -19°) breaking rigid parallel lines
- Black projection shadows (+7, +9) and occlusion contours
- High aesthetic contrast for OLED displays
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
from ..font_loader import load_font, prewarm_font_range
from ..lyrics import BASE_LYRIC_POOL, load_lyrics
from .uniform_density import draw_badge


def render_chaotic_3d_canvas(
    width: int,
    height: int,
    lyrics: Optional[List[str]] = None,
    seed: int = 42,
    font_name: str = "ArchitectsDaughter.ttf",
) -> Image.Image:
    """Renders a multi-tier chaotic 3D depth canvas with variable angles and shadow projections."""
    random.seed(seed)
    pool = lyrics if lyrics else BASE_LYRIC_POOL
    pool_len = len(pool)

    # 1. Background layer (Z = -2)
    cw, ch = int(width * 1.8), int(height * 1.7)
    bg_canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(bg_canvas)

    font_bg_sizes = [20, 24, 28, 22, 26]
    fonts_bg = {sz: load_font(font_name, sz) for sz in font_bg_sizes}

    y = 20
    idx = 0
    while y < ch - 40:
        sz = random.choice(font_bg_sizes)
        f = fonts_bg[sz]
        p1 = pool[idx % pool_len]
        p2 = pool[(idx * 3 + 1) % pool_len]
        p3 = pool[(idx * 5 + 2) % pool_len]
        p4 = pool[(idx * 7 + 3) % pool_len]
        p5 = pool[(idx * 11 + 4) % pool_len]
        line = f"{p1}   ·   {p2}   ·   {p3}   ·   {p4}   ·   {p5}"

        grey = random.randint(48, 80)
        alpha = random.randint(160, 215)
        bg_draw.text((random.randint(10, 50), y), line, font=f, fill=(grey, grey, grey, alpha))

        bbox = bg_draw.textbbox((0, 0), line, font=f)
        y += int((bbox[3] - bbox[1]) * random.uniform(0.70, 0.88))
        idx += 1

    rotated_bg = bg_canvas.rotate(-24, resample=Image.Resampling.BICUBIC, center=(cw // 2, ch // 2))
    left = (cw - width) // 2
    top = (ch - height) // 2
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    canvas.paste(rotated_bg.crop((left, top, left + width, top + height)), (0, 0))

    # 2. Midground & Foreground floating phrases (Z = -1 to +2)
    sizes_mid = [32, 36, 42, 46]
    sizes_fore = [52, 60, 70, 80]

    fonts_mid = {sz: load_font(font_name, sz) for sz in sizes_mid}
    fonts_fore = {sz: load_font(font_name, sz) for sz in sizes_fore}

    def render_phrase_strip(text, font, color, shadow_offset, shadow_stroke, angle):
        dummy = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
        d_draw = ImageDraw.Draw(dummy)
        bbox = d_draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0] + 50
        th = bbox[3] - bbox[1] + 35

        pad_x = abs(shadow_offset[0]) + shadow_stroke + 25
        pad_y = abs(shadow_offset[1]) + shadow_stroke + 25
        strip = Image.new("RGBA", (int(tw + pad_x * 2), int(th + pad_y * 2)), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(strip)

        tx, ty = pad_x, pad_y

        # Deep black projection shadow
        sx = tx + shadow_offset[0]
        sy = ty + shadow_offset[1]
        s_draw.text(
            (sx, sy),
            text,
            font=font,
            fill=(0, 0, 0, 255),
            stroke_width=shadow_stroke,
            stroke_fill=(0, 0, 0, 255),
        )

        # Main text with black contour outline
        s_draw.text(
            (tx, ty),
            text,
            font=font,
            fill=color,
            stroke_width=2,
            stroke_fill=(0, 0, 0, 255),
        )

        return strip.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)

    curr_y = -120
    while curr_y < height + 180:
        is_foreground = random.random() < 0.40

        if is_foreground:
            sz = random.choice(sizes_fore)
            font = fonts_fore[sz]
            lum = random.randint(215, 245)
            color = (lum, lum, lum, 255)
            shadow_offset = (random.randint(6, 10), random.randint(7, 12))
            shadow_stroke = 3
            angle = random.uniform(-27.0, -21.0)
            step_y = int(sz * random.uniform(1.15, 1.45))
        else:
            sz = random.choice(sizes_mid)
            font = fonts_mid[sz]
            lum = random.randint(125, 175)
            color = (lum, lum, lum, 230)
            shadow_offset = (random.randint(3, 5), random.randint(4, 6))
            shadow_stroke = 2
            angle = random.uniform(-29.0, -19.0)
            step_y = int(sz * random.uniform(0.95, 1.25))

        p_idx = random.randint(0, pool_len - 1)
        p1 = pool[p_idx]
        p2 = pool[(p_idx + 3) % pool_len]
        p3 = pool[(p_idx + 7) % pool_len]
        text_line = f"{p1}   ·   {p2}   ·   {p3}"

        strip = render_phrase_strip(text_line, font, color, shadow_offset, shadow_stroke, angle)

        pos_x = random.randint(-250, 40)
        pos_y = curr_y + random.randint(-15, 15)

        canvas.paste(strip, (pos_x, pos_y), mask=strip)
        curr_y += max(step_y, 45)

    return canvas


def generate_chaotic_3d_wallpapers(
    lyrics: Optional[List[str]] = None,
    output_phone_dir: Optional[Path] = None,
    output_desktop_dir: Optional[Path] = None,
    devices: str = "all",
    include_cutout: bool = True,
    prefix: str = "chaotic_3d",
) -> Dict[str, str]:
    """Generates phone and desktop chaotic 3D wallpapers."""
    out_phone = Path(output_phone_dir or PHONE_DIR)
    out_desktop = Path(output_desktop_dir or DESKTOP_DIR)
    out_phone.mkdir(parents=True, exist_ok=True)
    out_desktop.mkdir(parents=True, exist_ok=True)

    pool = lyrics or load_lyrics() or BASE_LYRIC_POOL
    saved_files = {}

    if devices in ("phone", "all"):
        print(f"Rendering Phone {prefix} Wall...")
        p_wall = render_chaotic_3d_canvas(PHONE_WIDTH, PHONE_HEIGHT, pool, seed=333)
        p1 = out_phone / f"{prefix}_wall.png"
        p_wall.convert("RGB").save(str(p1), quality=100)
        saved_files["phone_wall"] = str(p1)
        print(f"-> Saved: {p1}")

        if include_cutout:
            print(f"Rendering Phone {prefix} Cutout...")
            mask = Image.new("L", (PHONE_WIDTH, PHONE_HEIGHT), 255)
            mask_draw = ImageDraw.Draw(mask)
            void_poly = [(660, 1140), (PHONE_WIDTH, 880), (PHONE_WIDTH, 1800), (620, 1660)]
            mask_draw.polygon(void_poly, fill=0)

            p_cutout = Image.new("RGBA", (PHONE_WIDTH, PHONE_HEIGHT), (0, 0, 0, 255))
            p_cutout.paste(p_wall, (0, 0), mask=mask)
            draw_badge(p_cutout, cx=970, cy=1350, line1="SPOTIFY ON REPEAT", line2="CHAOTIC 3D ARCHIVE")
            p2 = out_phone / f"{prefix}_cutout.png"
            p_cutout.convert("RGB").save(str(p2), quality=100)
            saved_files["phone_cutout"] = str(p2)
            print(f"-> Saved: {p2}")

    if devices in ("desktop", "all"):
        print(f"Rendering Desktop 4K {prefix} Wall...")
        d_wall = render_chaotic_3d_canvas(DESKTOP_WIDTH, DESKTOP_HEIGHT, pool, seed=777)
        p3 = out_desktop / f"{prefix}_wall_4k.png"
        d_wall.convert("RGB").save(str(p3), quality=100)
        saved_files["desktop_wall"] = str(p3)
        print(f"-> Saved: {p3}")

        if include_cutout:
            print(f"Rendering Desktop 4K {prefix} Cutout...")
            d_mask = Image.new("L", (DESKTOP_WIDTH, DESKTOP_HEIGHT), 255)
            d_mask_draw = ImageDraw.Draw(d_mask)
            d_void_poly = [(2100, 0), (DESKTOP_WIDTH, 0), (DESKTOP_WIDTH, DESKTOP_HEIGHT), (1700, DESKTOP_HEIGHT)]
            d_mask_draw.polygon(d_void_poly, fill=0)

            d_cutout = Image.new("RGBA", (DESKTOP_WIDTH, DESKTOP_HEIGHT), (0, 0, 0, 255))
            d_cutout.paste(d_wall, (0, 0), mask=d_mask)
            draw_badge(d_cutout, cx=2900, cy=1080, line1="SPOTIFY ON REPEAT", line2="CHAOTIC 3D ARCHIVE")
            p4 = out_desktop / f"{prefix}_cutout_4k.png"
            d_cutout.convert("RGB").save(str(p4), quality=100)
            saved_files["desktop_cutout"] = str(p4)
            print(f"-> Saved: {p4}")

    return saved_files
