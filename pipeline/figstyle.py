"""figstyle.py — the shared BRAKEPOINT *dark* visual language for every data figure.

All four figure scripts (`figure_significance`, `figure_targets`, `figure_evidence`,
`figure_causal_map`) import this module so the whole set reads as one premium, dark,
glowing system — the same language as the animated video's ``MapScene`` and the dark
landing page (`deliverables/_remotion/src/theme.ts`).

What it provides
----------------
* ``PALETTE`` / named colour constants (near-black teal background, teal machinery,
  amber candidates, ink/body/muted text, hairlines).
* :func:`apply_rc` — one call to set every rcParam (fonts, spines, ticks, faint grid,
  dark save background).
* :func:`dark_figure` — a figure+axes with the subtle radial glow already painted and a
  transparent plotting axes so the glow shows through.
* :func:`radial_glow` — paints the teal(upper-left)/amber(upper-right) glow on any figure.
* marker helpers (:func:`marker`, :func:`bulk_cloud`) and :func:`title_block`.

Fonts
-----
Tries to register **Space Grotesk** (display/titles) and **Plus Jakarta Sans** (body).
If they are not on the system they are downloaded from the Google Fonts repo and static
weights are instantiated with fontTools. Any failure (offline, missing fontTools, …)
degrades silently to **DejaVu Sans** — this module never raises on import.
"""
from __future__ import annotations

import urllib.request
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.font_manager as fm  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

# ---------------------------------------------------------------------------
# palette  (mirrors deliverables/_remotion/src/theme.ts)
# ---------------------------------------------------------------------------
BG = "#0a1211"        # near-black teal page background
BG_PANEL = "#0c1614"  # slightly lifted panel fill (callout boxes)
INK = "#ffffff"       # titles
BODY = "#dbe7e3"      # body text
MUTED = "#8fa39d"     # subtitles / muted annotation

TEAL = "#2fd6bf"      # bright teal (accents)
TEAL_MID = "#0d9488"  # machinery / TCR marker fill
TEAL_DK = "#0b6b62"   # machinery deep / label ink
AMBER = "#f4b062"     # bright amber (accents)
AMBER_MID = "#d97a12" # candidate-brake marker fill
AMBER_DK = "#a85c08"  # candidate deep / label ink

BULK = "#6b7a76"      # faint gray bulk cloud
SPINE = "#3a4642"     # thin muted spines / ticks
HAIRLINE = (1.0, 1.0, 1.0, 0.10)  # rgba(255,255,255,0.10)
GRIDLINE = (1.0, 1.0, 1.0, 0.05)  # faint gridlines

# quadrant / band washes
AMBER_WASH = 0.06     # "enhance / positive" region
TEAL_WASH = 0.07      # "impair / negative" region
BULK_ALPHA = 0.28

PALETTE = {
    "bg": BG, "bg_panel": BG_PANEL, "ink": INK, "body": BODY, "muted": MUTED,
    "teal": TEAL, "teal_mid": TEAL_MID, "teal_dk": TEAL_DK,
    "amber": AMBER, "amber_mid": AMBER_MID, "amber_dk": AMBER_DK,
    "bulk": BULK, "spine": SPINE,
}

# ---------------------------------------------------------------------------
# fonts
# ---------------------------------------------------------------------------
_FONT_DIR = Path(__file__).resolve().parent / "_fonts"
_VAR_SOURCES = {
    "Space Grotesk":
        "https://raw.githubusercontent.com/google/fonts/main/ofl/spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf",
    "Plus Jakarta Sans":
        "https://raw.githubusercontent.com/google/fonts/main/ofl/plusjakartasans/PlusJakartaSans%5Bwght%5D.ttf",
}
# RIBBI-safe weights: 400 (Regular) + 700 (Bold) both stay under the base family
# name, so matplotlib weight matching (normal/bold) works within one family.
_WEIGHTS = (400, 700)

DISP = "DejaVu Sans"  # display family (overwritten by _ensure_fonts on success)
SANS = "DejaVu Sans"  # body family


def _download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (figstyle)"})
    with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310 (trusted host)
        data = r.read()
    dest.write_bytes(data)


def _ensure_fonts() -> tuple[str, str]:
    """Register Space Grotesk + Plus Jakarta Sans; return (display, body) family
    names. Falls back to ('DejaVu Sans', 'DejaVu Sans') on any failure."""
    installed = {f.name for f in fm.fontManager.ttflist}
    if "Space Grotesk" in installed and "Plus Jakarta Sans" in installed:
        return "Space Grotesk", "Plus Jakarta Sans"
    try:
        from fontTools.ttLib import TTFont
        from fontTools.varLib.instancer import instantiateVariableFont

        _FONT_DIR.mkdir(parents=True, exist_ok=True)
        for fam, url in _VAR_SOURCES.items():
            slug = fam.replace(" ", "")
            var_path = _FONT_DIR / f"{slug}-var.ttf"
            if not var_path.exists():
                _download(url, var_path)
            for w in _WEIGHTS:
                static_path = _FONT_DIR / f"{slug}-{w}.ttf"
                if not static_path.exists():
                    f = TTFont(str(var_path))
                    instantiateVariableFont(f, {"wght": w}, inplace=True,
                                            updateFontNames=True)
                    try:
                        f["OS/2"].usWeightClass = w
                    except Exception:
                        pass
                    f.save(str(static_path))
                    f.close()
                fm.fontManager.addfont(str(static_path))
        names = {f.name for f in fm.fontManager.ttflist}
        disp = "Space Grotesk" if "Space Grotesk" in names else "DejaVu Sans"
        body = "Plus Jakarta Sans" if "Plus Jakarta Sans" in names else "DejaVu Sans"
        return disp, body
    except Exception as exc:  # pragma: no cover - network/env dependent
        print(f"[figstyle] font setup failed ({exc!r}); using DejaVu Sans")
        return "DejaVu Sans", "DejaVu Sans"


# ---------------------------------------------------------------------------
# rcParams
# ---------------------------------------------------------------------------
def apply_rc() -> None:
    """Install the dark rcParams. Idempotent; safe to call from every script."""
    global DISP, SANS
    DISP, SANS = _ensure_fonts()
    # Use an EXPLICIT concrete-name family list (not the generic "sans-serif")
    # so matplotlib's per-glyph fallback traverses it and reaches DejaVu Sans for
    # glyphs the brand fonts lack (α, β, ⁺, …) instead of drawing a tofu box.
    plt.rcParams.update({
        "font.family": [SANS, "DejaVu Sans"],
        "font.sans-serif": [SANS, DISP, "DejaVu Sans"],
        "svg.fonttype": "none",
        "figure.facecolor": BG,
        "savefig.facecolor": BG,
        "axes.facecolor": "none",     # transparent so the glow shows through
        "axes.edgecolor": SPINE,
        "axes.labelcolor": BODY,
        "text.color": BODY,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelcolor": MUTED,
        "ytick.labelcolor": MUTED,
        "axes.linewidth": 1.0,
        "grid.color": "#ffffff",
        "grid.alpha": 0.05,
        "grid.linewidth": 0.8,
        "legend.frameon": True,
        "legend.framealpha": 0.0,
    })


# ---------------------------------------------------------------------------
# radial glow background
# ---------------------------------------------------------------------------
def _blob(res: int, cx: float, cy: float, rad: float, rgb: tuple[int, int, int],
          amax: float) -> np.ndarray:
    """RGBA image (origin='upper') with a soft radial alpha falloff centred at
    (cx, cy) in figure-fraction coords (y measured from the TOP)."""
    yy, xx = np.mgrid[0:res, 0:res] / float(res - 1)
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    a = np.clip(1.0 - d / rad, 0.0, 1.0) ** 2 * amax
    img = np.zeros((res, res, 4), dtype=float)
    img[..., 0] = rgb[0] / 255.0
    img[..., 1] = rgb[1] / 255.0
    img[..., 2] = rgb[2] / 255.0
    img[..., 3] = a
    return img


def radial_glow(fig, teal_a: float = 0.10, amber_a: float = 0.06,
                res: int = 420) -> None:
    """Paint the subtle teal(upper-left)/amber(upper-right) glow behind everything."""
    bg = fig.add_axes([0, 0, 1, 1], zorder=-100)
    bg.set_xlim(0, 1)
    bg.set_ylim(0, 1)
    bg.axis("off")
    bg.add_patch(Rectangle((0, 0), 1, 1, color=BG, zorder=-101))
    bg.imshow(_blob(res, 0.10, 0.12, 0.85, (13, 148, 136), teal_a),
              extent=[0, 1, 0, 1], origin="upper", zorder=-100,
              interpolation="bilinear", aspect="auto")
    bg.imshow(_blob(res, 0.90, 0.10, 0.80, (217, 122, 18), amber_a),
              extent=[0, 1, 0, 1], origin="upper", zorder=-100,
              interpolation="bilinear", aspect="auto")


def dark_figure(figsize: tuple[float, float], dpi: int = 200,
                glow: bool = True, teal_a: float = 0.10, amber_a: float = 0.06):
    """Return (fig, ax): a dark figure with the glow painted and a transparent,
    lightly-styled plotting axes on top."""
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    fig.patch.set_facecolor(BG)
    if glow:
        radial_glow(fig, teal_a=teal_a, amber_a=amber_a)
    ax.set_facecolor("none")
    style_axes(ax)
    return fig, ax


# ---------------------------------------------------------------------------
# axes chrome
# ---------------------------------------------------------------------------
def style_axes(ax, grid: bool = True, hide: Sequence[str] = ("top", "right")) -> None:
    """Thin muted spines/ticks + optional faint grid."""
    for s in hide:
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom", "top", "right"):
        if ax.spines[s].get_visible():
            ax.spines[s].set_color(SPINE)
            ax.spines[s].set_linewidth(1.0)
    ax.tick_params(colors=MUTED, labelsize=10.5, length=4, width=0.9)
    if grid:
        ax.grid(color="#ffffff", alpha=0.05, lw=0.8)
        ax.set_axisbelow(True)


# ---------------------------------------------------------------------------
# marker helpers
# ---------------------------------------------------------------------------
def marker(ax, xs, ys, fill: str, *, size: float = 110, mk: str = "o",
           edge: str = "white", lw: float = 2.2, zorder: int = 6, alpha: float = 1.0):
    """A filled marker with a white edge — the BRAKEPOINT signed-scatter mark."""
    return ax.scatter(xs, ys, s=size, marker=mk, c=fill, edgecolors=edge,
                      linewidths=lw, zorder=zorder, alpha=alpha)


def bulk_cloud(ax, xs, ys, *, size: float = 7, alpha: float = BULK_ALPHA,
               zorder: int = 1):
    """The faint gray bulk cloud."""
    return ax.scatter(xs, ys, s=size, c=BULK, alpha=alpha, linewidths=0,
                      zorder=zorder, rasterized=True)


def panel_box(ax, x, y, w, h, *, zorder: int = 9, alpha: float = 0.92):
    """A rounded dark panel (for callout boxes) in axes-fraction coords."""
    from matplotlib.patches import FancyBboxPatch
    box = FancyBboxPatch((x, y), w, h, transform=ax.transAxes,
                         boxstyle="round,pad=0.012,rounding_size=0.02",
                         fc=BG_PANEL, ec=HAIRLINE, lw=1.2, zorder=zorder, alpha=alpha)
    ax.add_patch(box)
    return box


# ---------------------------------------------------------------------------
# title block
# ---------------------------------------------------------------------------
def title_block(fig, title: str, subtitles: Iterable[str] = (), *,
                x: float = 0.062, y: float = 0.975, title_size: float = 18.0,
                sub_size: float = 11.0, dy: float = 0.039,
                sub_color: str = MUTED) -> None:
    """Ink-white Space-Grotesk title + muted body subtitles, top-left.

    Both use explicit family stacks ending in DejaVu Sans so any glyph the brand
    fonts lack (e.g. ⁺ in "CD4⁺") falls back cleanly instead of rendering tofu."""
    disp_stack = [DISP, SANS, "DejaVu Sans"]
    sans_stack = [SANS, "DejaVu Sans"]
    fig.text(x, y, title, fontsize=title_size, fontweight="bold", color=INK,
             va="top", family=disp_stack)
    yy = y - dy
    for s in subtitles:
        fig.text(x, yy, s, fontsize=sub_size, color=sub_color, va="top",
                 family=sans_stack)
        yy -= dy


__all__ = [
    "PALETTE", "BG", "BG_PANEL", "INK", "BODY", "MUTED", "TEAL", "TEAL_MID",
    "TEAL_DK", "AMBER", "AMBER_MID", "AMBER_DK", "BULK", "SPINE", "HAIRLINE",
    "GRIDLINE", "AMBER_WASH", "TEAL_WASH", "BULK_ALPHA", "DISP", "SANS",
    "apply_rc", "radial_glow", "dark_figure", "style_axes", "marker",
    "bulk_cloud", "panel_box", "title_block",
]
