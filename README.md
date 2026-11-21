# Typography Wallpaper Generator

A Python tool that creates minimalist, high-resolution typographic wallpapers for OLED mobile devices and 4K desktop displays using organic freehand handwriting fonts on a pure black backdrop.

---

## Features

- **Mathematical Depth Engines**:
  - **Uniform Density Chaos**: Golden-Ratio Low-Discrepancy Sampling ($z_i = (0.382 + i \cdot \phi) \pmod 1$) for visual mass balance across the entire canvas.
  - **Logical Chaos**: Multi-frequency harmonic wave oscillator ($z_i$ wave formula) producing depth crests and troughs.
  - **Chaotic 3D**: Multi-tier Z-space planes, non-rigid variable tilt angles (-29° to -19°), and cast shadows.
  - **Super-Dense**: 200+ line wall-to-wall text stream.
  - **Editorial Minimal**: Negative space preservation with lockscreen widget and macOS dock safe-zones.
- **Display Optimized**: Pure `#000000` background for OLED power savings and infinite contrast.
- **Cross-Platform**: Automatic font resolution across macOS, Linux, and Windows.
- **Zero Heavy Dependencies**: Uses standard Python libraries with Pillow for imaging.

---

## Directory Structure

```
.
├── generate.py                # Master CLI runner
├── requirements.txt           # Dependencies
├── pyproject.toml             # Packaging configuration
├── data/                      # Input datasets and templates
│   ├── lyrics.example.md      # Markdown phrase format template
│   └── tracks.example.json    # JSON track schema example
├── fonts/                     # Curated open-source TrueType fonts
│   ├── README.md              # Font license documentation
│   └── *.ttf                  # Bundled handwriting fonts
├── src/
│   └── spotify_wallpaper/     # Core Python package
│       ├── config.py          # Resolutions, colors, safe-zones
│       ├── font_loader.py     # Cross-platform font resolver & cache
│       ├── lyrics.py          # Markdown phrase parser
│       ├── spotify.py         # OAuth & Web API integration
│       ├── cli.py             # CLI parser & interactive menu
│       └── renderers/         # Rendering engines
├── scripts/                   # Standalone single-style scripts
│   ├── make_uniform_density_chaos.py
│   ├── make_logical_chaos.py
│   ├── make_chaotic_3d.py
│   ├── make_english_wallpapers.py
│   ├── make_super_dense.py
│   └── make_editorial.py
└── dist/                      # Output directory (.gitkeep)
    ├── phone/                 # Mobile outputs (1290 x 2796)
    └── desktop/               # 4K outputs (3840 x 2160)
```

---

## Quickstart

### 1. Installation

```bash
git clone https://github.com/heavens7above/spotify-lyrics-wallpaper.git
cd spotify-lyrics-wallpaper
pip install -r requirements.txt
```

### 2. Rendering Wallpapers

Run the interactive selector:
```bash
python generate.py
```

Or run any style directly via CLI flags:
```bash
# Uniform-Density (Recommended)
python generate.py uniform

# Mobile only (1290 x 2796)
python generate.py uniform -d phone

# Desktop 4K only (3840 x 2160)
python generate.py chaotic -d desktop

# Render to custom destination
python generate.py uniform -o ~/Desktop/MyWallpapers

# Render all visual styles
python generate.py all
```

---

## CLI Options

| Flag | Description | Default |
| :--- | :--- | :--- |
| `style` | Style name: `uniform`, `logical`, `chaotic`, `english`, `dense`, `editorial`, `all`, `fetch`, `list` | Interactive prompt |
| `-d`, `--device` | Target device: `phone` (mobile), `desktop` (4k), `all` | `all` |
| `--no-cutout` | Skip generating lockscreen clock & badge void cutout variants | `False` |
| `-l`, `--lyrics` | Custom path to a markdown phrase file | `data/lyrics.md` |
| `-o`, `--output` | Custom destination directory for generated PNGs | `dist/` |
| `-c`, `--fetch-count` | Number of tracks to paginate during Spotify fetch | `150` |
| `-v`, `--version` | Display program version | — |

---

## Data Input Format

Place your phrases in `data/lyrics.md` using standard markdown:

```markdown
### 1. Song Title — Artist Name
> *"First phrase line / Second phrase line..."*
- **Album**: Album Title
- **Vibe**: Description
```

If no markdown file is provided, the engine automatically uses its built-in phrase pool.

---

## Spotify Integration (Optional)

To sync your listening history:
1. Register an application on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Set Redirect URI to `http://127.0.0.1:8888/callback`.
3. Copy `.env.example` to `.env.spotify` and add your client ID and secret:
   ```bash
   cp .env.example .env.spotify
   ```
4. Run the fetch command:
   ```bash
   python generate.py fetch
   ```

---

## License

This project is licensed under the [MIT License](LICENSE). Sourced fonts are licensed under the SIL Open Font License or Apache 2.0 (see [fonts/README.md](fonts/README.md)).
