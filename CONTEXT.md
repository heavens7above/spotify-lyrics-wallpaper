# Technical Specifications & Design Architecture

## 1. Visual Philosophy
- **Contrast**: Pure `#000000` base for OLED displays.
- **Color Temperature**: Off-white (`#F8F9FA`), ash silver (`#8A8A8A`), and deep charcoal (`#454545`).
- **Typography**: Organic freehand script with variable scales and angular jitter (-29° to -19°).

---

## 2. Canvas & Safe Zones

### Phone (1290 × 2796)
- **Top Safe Zone (0 - 680px)**: Reserved for lockscreen digital clock and system widgets.
- **Reading Zone (680 - 2400px)**: High-density typographic scatter.
- **Bottom Safe Zone (2400 - 2796px)**: Preserved for camera and flashlight controls.

### Desktop 4K (3840 × 2160)
- **Top Safe Zone (0 - 80px)**: Preserved for menu bar.
- **Bottom Safe Zone (2000 - 2160px)**: Preserved for system dock.
- **Layout**: 3-column panoramic flow or balanced diagonal scatter.

---

## 3. Mathematical Depth Engines

### Low-Discrepancy Sampling (Uniform Density)
Uses golden-ratio quasi-random sequence:
$$z_i = (0.382 + i \cdot \phi) \pmod 1$$
where $\phi = \frac{\sqrt{5} - 1}{2} \approx 0.6180339887$.

### Harmonic Wave Oscillator (Logical Chaos)
Uses multi-frequency wave combination:
$$z(i) = 0.5 + 0.5 \cdot \left[ 0.50 \sin\left(\frac{2\pi i}{7.3}\right) + 0.32 \cos\left(\frac{2\pi i}{3.7} + 0.4\right) + 0.18 \sin\left(\frac{2\pi i}{13.1} + 1.2\right) \right]$$
