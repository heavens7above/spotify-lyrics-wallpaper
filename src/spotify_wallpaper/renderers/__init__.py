"""
Wallpaper Rendering Engines
===========================
Exports all wallpaper rendering engines:
- Uniform Density (Golden-Ratio Low Discrepancy)
- Logical Chaos (Harmonic Wave Oscillator)
- Chaotic 3D Depth (Multi-tier Z-space with Variable Angles)
- Super-Dense Wall (200+ Lines)
- Editorial Minimal & Panorama (Flow & Safe-Zones)
"""

from .uniform_density import (
    render_uniform_density_canvas,
    generate_uniform_density_wallpapers,
    draw_badge,
)
from .logical_chaos import (
    render_logical_chaos_canvas,
    generate_logical_chaos_wallpapers,
)
from .chaotic_3d import (
    render_chaotic_3d_canvas,
    generate_chaotic_3d_wallpapers,
)
from .super_dense import (
    render_super_dense_canvas,
    generate_super_dense_wallpapers,
)
from .editorial import (
    render_lyric_card,
    generate_editorial_wallpapers,
)

__all__ = [
    "render_uniform_density_canvas",
    "generate_uniform_density_wallpapers",
    "draw_badge",
    "render_logical_chaos_canvas",
    "generate_logical_chaos_wallpapers",
    "render_chaotic_3d_canvas",
    "generate_chaotic_3d_wallpapers",
    "render_super_dense_canvas",
    "generate_super_dense_wallpapers",
    "render_lyric_card",
    "generate_editorial_wallpapers",
]
