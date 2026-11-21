"""
Master Command-Line Interface for Spotify Lyrics Wallpaper Generator
=====================================================================
Features:
- Dual-mode: Interactive guided wizard or direct CLI flags & subcommands
- ANSI color styling with automatic non-TTY degradation
- Flexible device targeting (phone, desktop, all, mobile, 4k, pc)
- Custom output paths, custom lyrics files, custom fonts, and seeds
- Post-render summary report with dimensions, file sizes, and elapsed time
- Graceful KeyboardInterrupt handling (no raw tracebacks)
"""

import sys
import os
import time
import argparse
from pathlib import Path
from typing import List, Optional, Dict

from .config import PHONE_DIR, DESKTOP_DIR, DIST_DIR, FONTS_DIR
from .lyrics import load_lyrics, BASE_ENGLISH_LYRIC_POOL, resolve_lyrics_file
from .renderers import (
    generate_uniform_density_wallpapers,
    generate_logical_chaos_wallpapers,
    generate_chaotic_3d_wallpapers,
    generate_super_dense_wallpapers,
    generate_editorial_wallpapers,
)
from .spotify import run_spotify_pipeline

VERSION = "1.0.0"

# ANSI Terminal Colors
USE_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")

def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text

def green(text: str) -> str: return _c("32;1", text)
def cyan(text: str) -> str: return _c("36;1", text)
def yellow(text: str) -> str: return _c("33;1", text)
def red(text: str) -> str: return _c("31;1", text)
def dim(text: str) -> str: return _c("2;37", text)
def bold(text: str) -> str: return _c("1", text)

DEVICE_ALIASES = {
    "phone": "phone",
    "mobile": "phone",
    "iphone": "phone",
    "android": "phone",
    "desktop": "desktop",
    "pc": "desktop",
    "mac": "desktop",
    "4k": "desktop",
    "all": "all",
    "both": "all",
}

STYLE_DESCRIPTIONS = {
    "uniform": "Uniform Density Chaos (Golden-Ratio low-discrepancy sampling, perfectly homogeneous)",
    "logical": "Logical Chaos (Harmonic wave oscillation depth field equation)",
    "chaotic": "Full Chaotic 3D (Multi-angle variable tilts with bold cast shadows)",
    "english": "English-Only Chaotic 3D (Refined for English tracks and phrase streams)",
    "dense": "Super-Dense Wall (200+ lines packed tightly wall-to-wall)",
    "editorial": "Minimal Editorial Flow (Generous negative space with lockscreen widget safe-zones)",
    "all": "Render all 6 visual wallpaper styles in sequence",
}


def print_banner():
    banner = f"""
{cyan("╔═════════════════════════════════════════════════════════════════╗")}
{cyan("║")}          {bold("SPOTIFY LYRICS AESTHETIC WALLPAPER GENERATOR")}           {cyan("║")}
{cyan("║")}       {dim("Minimalist Organic Typography for OLED & 4K Displays")}      {cyan("║")}
{cyan("╚═════════════════════════════════════════════════════════════════╝")}
"""
    print(banner)


def format_file_size(num_bytes: int) -> str:
    """Format bytes into human-readable string (KB/MB)."""
    if num_bytes >= 1024 * 1024:
        return f"{num_bytes / (1024 * 1024):.2f} MB"
    elif num_bytes >= 1024:
        return f"{num_bytes / 1024:.1f} KB"
    return f"{num_bytes} B"


def print_summary_table(results: Dict[str, str], elapsed: float):
    """Prints a clean ASCII summary table of generated wallpaper files."""
    if not results:
        return

    print("\n" + bold("=" * 65))
    print(bold(f"  GENERATION SUMMARY  ") + dim(f"(Completed in {elapsed:.2f}s)"))
    print("=" * 65)

    for key, file_path in results.items():
        if os.path.isfile(file_path):
            size_str = format_file_size(os.path.getsize(file_path))
            rel_path = os.path.relpath(file_path, os.getcwd())
            print(f"  {green('✔')}  {bold(key):<18} : {rel_path} {dim(f'[{size_str}]')}")

    print("=" * 65 + "\n")


def interactive_menu() -> str:
    print_banner()

    lyrics_file = resolve_lyrics_file()
    if lyrics_file:
        print(dim(f"  Source dataset : {lyrics_file}"))
    else:
        print(dim("  Source dataset : Built-in aesthetic phrase pool"))

    print("\n" + bold("Available Wallpaper Styles:"))
    for i, (k, desc) in enumerate(STYLE_DESCRIPTIONS.items(), 1):
        print(f"  {cyan(str(i))}. {bold(k):<10} - {desc}")
    print(f"  {cyan('8')}. {bold('fetch'):<10} - Authenticate with Spotify Web API to sync top tracks")
    print("=" * 65)

    try:
        choice = input(bold("Enter choice (1-8 or name) [default: 1]: ")).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print(yellow("\nOperation cancelled by user."))
        sys.exit(0)

    mapping = {
        "1": "uniform",
        "2": "logical",
        "3": "chaotic",
        "4": "english",
        "5": "dense",
        "6": "editorial",
        "7": "all",
        "8": "fetch",
    }
    return mapping.get(choice, choice or "uniform")


def resolve_device_target(device_input: str) -> str:
    normalized = device_input.lower().strip()
    return DEVICE_ALIASES.get(normalized, "all")


def run_style(
    style: str,
    devices: str = "all",
    lyrics_path: Optional[str] = None,
    include_cutout: bool = True,
    output_dir: Optional[str] = None,
) -> Dict[str, str]:
    lyrics = load_lyrics(lyrics_path) if lyrics_path else None
    all_saved = {}

    phone_out = Path(output_dir) / "phone" if output_dir else PHONE_DIR
    desk_out = Path(output_dir) / "desktop" if output_dir else DESKTOP_DIR

    start_time = time.time()

    if style in ("uniform", "homogenous", "constant"):
        print(cyan("\n>>> Rendering Uniform-Density Chaos Wallpapers..."))
        saved = generate_uniform_density_wallpapers(
            lyrics=lyrics,
            output_phone_dir=phone_out,
            output_desktop_dir=desk_out,
            devices=devices,
            include_cutout=include_cutout,
        )
        all_saved.update(saved)

    elif style in ("logical", "chaos", "equation"):
        print(cyan("\n>>> Rendering Logical Chaos Wallpapers..."))
        saved = generate_logical_chaos_wallpapers(
            lyrics=lyrics,
            output_phone_dir=phone_out,
            output_desktop_dir=desk_out,
            devices=devices,
            include_cutout=include_cutout,
        )
        all_saved.update(saved)

    elif style in ("chaotic", "3d"):
        print(cyan("\n>>> Rendering Chaotic 3D Depth Wallpapers..."))
        saved = generate_chaotic_3d_wallpapers(
            lyrics=lyrics,
            output_phone_dir=phone_out,
            output_desktop_dir=desk_out,
            devices=devices,
            include_cutout=include_cutout,
            prefix="chaotic_3d",
        )
        all_saved.update(saved)

    elif style in ("english", "eng"):
        print(cyan("\n>>> Rendering English-Only Chaotic 3D Wallpapers..."))
        eng_file = resolve_lyrics_file(lyrics_path, english=True)
        eng_lyrics = load_lyrics(str(eng_file)) if eng_file else BASE_ENGLISH_LYRIC_POOL
        saved = generate_chaotic_3d_wallpapers(
            lyrics=eng_lyrics,
            output_phone_dir=phone_out,
            output_desktop_dir=desk_out,
            devices=devices,
            include_cutout=include_cutout,
            prefix="english_chaotic_3d",
        )
        all_saved.update(saved)

    elif style in ("dense", "superdense"):
        print(cyan("\n>>> Rendering Super-Dense (200+ Lines) Wallpapers..."))
        saved = generate_super_dense_wallpapers(
            lyrics=lyrics,
            output_phone_dir=phone_out,
            output_desktop_dir=desk_out,
            devices=devices,
        )
        all_saved.update(saved)

    elif style in ("editorial", "minimal"):
        print(cyan("\n>>> Rendering Minimal Editorial Flow Wallpapers..."))
        saved = generate_editorial_wallpapers(
            output_phone_dir=phone_out,
            output_desktop_dir=desk_out,
            devices=devices,
        )
        all_saved.update(saved)

    elif style == "all":
        print("\n" + bold("=" * 65))
        print(bold("          RENDERING ALL 6 WALLPAPER STYLES             "))
        print("=" * 65)

        print(cyan("\n>>> [1/6] Uniform-Density Chaos Wallpapers..."))
        all_saved.update(generate_uniform_density_wallpapers(lyrics=lyrics, output_phone_dir=phone_out, output_desktop_dir=desk_out, devices=devices, include_cutout=include_cutout))

        print(cyan("\n>>> [2/6] Logical Chaos Wallpapers..."))
        all_saved.update(generate_logical_chaos_wallpapers(lyrics=lyrics, output_phone_dir=phone_out, output_desktop_dir=desk_out, devices=devices, include_cutout=include_cutout))

        print(cyan("\n>>> [3/6] Chaotic 3D Depth Wallpapers..."))
        all_saved.update(generate_chaotic_3d_wallpapers(lyrics=lyrics, output_phone_dir=phone_out, output_desktop_dir=desk_out, devices=devices, include_cutout=include_cutout, prefix="chaotic_3d"))

        print(cyan("\n>>> [4/6] English Chaotic 3D Wallpapers..."))
        eng_file = resolve_lyrics_file(lyrics_path, english=True)
        eng_lyrics = load_lyrics(str(eng_file)) if eng_file else BASE_ENGLISH_LYRIC_POOL
        all_saved.update(generate_chaotic_3d_wallpapers(lyrics=eng_lyrics, output_phone_dir=phone_out, output_desktop_dir=desk_out, devices=devices, include_cutout=include_cutout, prefix="english_chaotic_3d"))

        print(cyan("\n>>> [5/6] Super-Dense Wallpapers..."))
        all_saved.update(generate_super_dense_wallpapers(lyrics=lyrics, output_phone_dir=phone_out, output_desktop_dir=desk_out, devices=devices))

        print(cyan("\n>>> [6/6] Minimal Editorial Flow Wallpapers..."))
        all_saved.update(generate_editorial_wallpapers(output_phone_dir=phone_out, output_desktop_dir=desk_out, devices=devices))

    else:
        print(red(f"Error: Unknown style '{style}'."))
        print(f"Choose from: {', '.join(STYLE_DESCRIPTIONS.keys())}")
        sys.exit(1)

    elapsed = time.time() - start_time
    print_summary_table(all_saved, elapsed)
    return all_saved


def main():
    parser = argparse.ArgumentParser(
        prog="spotify-wallpaper",
        description="Spotify Lyrics Aesthetic Wallpaper Generator for OLED Mobile & 4K Desktop Displays",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate.py                            # Interactive style selector
  python generate.py uniform                    # Render recommended Uniform Density style
  python generate.py uniform --device phone     # Render mobile only (1290x2796)
  python generate.py chaotic --device desktop   # Render 4K desktop only (3840x2160)
  python generate.py all                        # Generate complete wallpaper collection
  python generate.py fetch --fetch-count 200    # Authenticate and pull 200 tracks from Spotify
  python generate.py list                       # Display all visual style descriptions
        """,
    )

    parser.add_argument(
        "style",
        nargs="?",
        default=None,
        help="Style name: uniform, logical, chaotic, english, dense, editorial, all, fetch, or list",
    )
    parser.add_argument(
        "-d", "--device",
        default="all",
        help="Target device: phone (mobile/iphone), desktop (4k/pc), or all [default: all]",
    )
    parser.add_argument(
        "--no-cutout",
        action="store_true",
        help="Skip generating lockscreen clock & badge void cutout variants",
    )
    parser.add_argument(
        "-l", "--lyrics",
        default=None,
        metavar="PATH",
        help="Custom path to a curated lyrics markdown file",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        metavar="DIR",
        help="Custom destination directory for generated wallpaper PNGs",
    )
    parser.add_argument(
        "-c", "--fetch-count",
        type=int,
        default=150,
        metavar="N",
        help="Number of Spotify tracks to paginate during fetch [default: 150]",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )

    args = parser.parse_args()

    style = args.style
    if not style:
        try:
            style = interactive_menu()
        except (KeyboardInterrupt, EOFError):
            print(yellow("\nExiting."))
            sys.exit(0)

    # Normalize device alias
    target_device = resolve_device_target(args.device)

    # Handle informational commands
    if style in ("list", "list-styles", "styles"):
        print_banner()
        print(bold("Available Visual Styles:"))
        for name, desc in STYLE_DESCRIPTIONS.items():
            print(f"  • {cyan(name):<12} : {desc}")
        print(f"  • {cyan('fetch'):<12} : Authenticates with Spotify and fetches top tracks & saved songs")
        return

    # Handle Spotify fetching
    if style in ("fetch", "spotify", "auth"):
        print_banner()
        print(cyan("Starting Spotify Web API OAuth Pipeline..."))
        try:
            run_spotify_pipeline(fetch_count=args.fetch_count)
        except KeyboardInterrupt:
            print(yellow("\nSpotify fetch cancelled by user."))
        except Exception as e:
            print(red(f"\n[ERROR] Spotify fetch failed: {e}"))
            sys.exit(1)
        return

    # Execute wallpaper rendering
    try:
        run_style(
            style=style,
            devices=target_device,
            lyrics_path=args.lyrics,
            include_cutout=not args.no_cutout,
            output_dir=args.output,
        )
    except KeyboardInterrupt:
        print(yellow("\nRendering aborted by user."))
        sys.exit(130)
    except Exception as e:
        print(red(f"\n[ERROR] Rendering encountered an error: {e}"))
        sys.exit(1)


if __name__ == "__main__":
    main()
