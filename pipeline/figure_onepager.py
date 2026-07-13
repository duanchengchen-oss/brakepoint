"""figure_onepager.py — the BRAKEPOINT one-pager summary poster (DARK premium style).

A tall portrait poster that composites the already-regenerated DARK sub-figures
(`target_matrix.png` — the convergent-evidence centerpiece — and
`donor_consistency.png` — the donor scatter) and wraps them in the shared
BRAKEPOINT visual language from :mod:`figstyle` (near-black teal background,
teal/amber palette, Space Grotesk / Plus Jakarta Sans with DejaVu fallback,
subtle radial glow).

We do NOT re-plot any data here: the panels are the exact standalone figures, so
the poster stays in lock-step with the rest of the figure set. Everything else is
type + honest framing that mirrors the live landing page (`deliverables/index.html`)
and the written summary (`deliverables/summary.md`).

Run:  python3 figure_onepager.py
Outputs: ../deliverables/figures/brakepoint_onepager.{png,svg}
"""
from __future__ import annotations

from pathlib import Path

from matplotlib.patches import FancyBboxPatch

import figstyle

# ---------------------------------------------------------------------------
# canvas
# ---------------------------------------------------------------------------
W_IN, H_IN, DPI = 16.0, 26.4, 200          # -> 3200 x 5280 px portrait poster
ASPECT = W_IN / H_IN                        # inches width / height

XL, XR = 0.045, 0.955                       # content left / right (figure frac)
CW = XR - XL


def _stacks():
    disp = [figstyle.DISP, figstyle.SANS, "DejaVu Sans"]
    sans = [figstyle.SANS, "DejaVu Sans"]
    return disp, sans


# ---------------------------------------------------------------------------
# helpers (all coords are "T from top" in figure fraction; y_mpl = 1 - T)
# ---------------------------------------------------------------------------
def _card(ax, x, T_top, w, h, *, fill=figstyle.BG_PANEL, ec=figstyle.HAIRLINE,
          lw=1.4, radius=0.010, z=2):
    """Rounded card on the given (data 0..1) axes; T_top is distance from top."""
    b = 1.0 - T_top - h
    box = FancyBboxPatch(
        (x, b), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        fc=fill, ec=ec, lw=lw, zorder=z, mutation_aspect=ASPECT,
    )
    ax.add_patch(box)


def _text(ax, x, T, s, size, color, family, *, weight="normal", ha="left",
          va="top", z=25, alpha=1.0, spacing=1.05):
    return ax.text(x, 1.0 - T, s, fontsize=size, color=color, family=family,
                   fontweight=weight, ha=ha, va=va, zorder=z, alpha=alpha,
                   linespacing=spacing)


def _rich(fig, ax, x, T, segments, size, family, *, weight="normal", va="top", z=25):
    """Left-aligned run of coloured (text, colour) segments, measured with the
    Agg renderer so the words butt up cleanly regardless of font."""
    r = fig.canvas.get_renderer()
    Wpx = fig.get_size_inches()[0] * fig.dpi
    cur = x
    y = 1.0 - T
    for text, color in segments:
        t = ax.text(cur, y, text, fontsize=size, color=color, family=family,
                    fontweight=weight, ha="left", va=va, zorder=z)
        cur += t.get_window_extent(renderer=r).width / Wpx
    return cur


def _place_image(fig, back_ax, path, x, T_top, w, *, z=6, pad=0.006,
                 card_fill=figstyle.BG):
    """Composite a sub-figure PNG at (x, T_top) with width `w`; height is derived
    to preserve the image's aspect ratio (no distortion). A hairline card frames
    it. Returns the bottom edge (T from top) of the framed card."""
    img = figstyle.plt.imread(str(path))
    ih, iw = img.shape[0], img.shape[1]
    h = w * ASPECT * (ih / iw)              # frac height that preserves aspect
    _card(back_ax, x - pad, T_top - pad, w + 2 * pad, h + 2 * pad,
          fill=card_fill, z=3)
    b = 1.0 - T_top - h
    imax = fig.add_axes([x, b, w, h], zorder=z)
    imax.imshow(img, aspect="auto", interpolation="lanczos")
    imax.axis("off")
    return T_top + h + pad


def _dot(ax, x, T, color, *, size=90, z=26):
    ax.scatter([x], [1.0 - T], s=size, c=color, edgecolors="white",
               linewidths=1.4, zorder=z)


# ---------------------------------------------------------------------------
# build
# ---------------------------------------------------------------------------
def build(out_png: str, out_svg: str) -> None:
    figstyle.apply_rc()
    disp, sans = _stacks()

    fig = figstyle.plt.figure(figsize=(W_IN, H_IN), dpi=DPI)
    fig.patch.set_facecolor(figstyle.BG)
    figstyle.radial_glow(fig, teal_a=0.13, amber_a=0.09)

    # back layer (cards, dividers) below composited images
    back = fig.add_axes([0, 0, 1, 1], zorder=2)
    back.set_xlim(0, 1); back.set_ylim(0, 1); back.axis("off")
    # front layer (all type) above everything
    front = fig.add_axes([0, 0, 1, 1], zorder=25)
    front.set_xlim(0, 1); front.set_ylim(0, 1); front.axis("off")

    figs_dir = Path(out_png).resolve().parent

    # ---- header / eyebrow -------------------------------------------------
    _rich(fig, front, XL, 0.020,
          [("B R A K E P O I N T", figstyle.TEAL),
           ("   ·   Built with Claude · Life Sciences (research track)", figstyle.MUTED)],
          15.5, disp, weight="bold")
    _text(front, XR, 0.020, "Public CD4⁺ T-cell CRISPRi screen · Marson + Pritchard",
          15.5, figstyle.MUTED, sans, ha="right")

    # ---- hero headline ----------------------------------------------------
    hl_size, hl_dt, hl0 = 52, 0.0290, 0.055
    _rich(fig, front, XL, hl0,
          [("A genome-scale ", figstyle.INK),
           ("discovery", figstyle.AMBER)],
          hl_size, disp, weight="bold")
    _rich(fig, front, XL, hl0 + hl_dt,
          [("engine", figstyle.AMBER),
           (" for next-generation", figstyle.INK)],
          hl_size, disp, weight="bold")
    _text(front, XL, hl0 + 2 * hl_dt, "cancer-immunotherapy targets.",
          hl_size, figstyle.INK, disp, weight="bold")

    # brake-metaphor subline
    _rich(fig, front, XL, hl0 + 3 * hl_dt + 0.008,
          [("Immunotherapy works by cutting the ", figstyle.BODY),
           ("brakes", figstyle.AMBER),
           (" off a T cell — Brakepoint hunts the rest.", figstyle.BODY)],
          19.5, sans)

    # ---- sub-lead (bold sell) ---------------------------------------------
    lead_T, lead_dt, ls = 0.180, 0.0145, 15.5
    _rich(fig, front, XL, lead_T,
          [("Brakepoint reads ", figstyle.BODY),
           ("2.6M", figstyle.INK),
           (" human T cells and ", figstyle.BODY),
           ("12,449", figstyle.INK),
           (" gene shutoffs as one experiment.", figstyle.BODY)], ls, sans)
    _text(front, XL, lead_T + lead_dt,
          "It scores each shutoff by impact and direction — a stronger or weaker T cell —",
          ls, figstyle.BODY, sans)
    _text(front, XL, lead_T + 2 * lead_dt,
          "splitting real drug targets from the machinery a cell needs to survive.",
          ls, figstyle.BODY, sans)
    _rich(fig, front, XL, lead_T + 3 * lead_dt,
          [("With zero prior hints it rediscovered ", figstyle.BODY),
           ("CBLB", figstyle.AMBER),
           (" — then surfaced four more candidates.", figstyle.BODY)], ls, sans)

    # ---- stat tiles -------------------------------------------------------
    tiles = [
        ("2.6M", "single human T cells, read at once", figstyle.INK),
        ("12,449", "gene shutoffs across the genome", figstyle.INK),
        ("CBLB", "rediscovered blind, from raw data", figstyle.AMBER),
    ]
    tile_T, tile_h, tgap = 0.252, 0.056, 0.018
    tile_w = (CW - 2 * tgap) / 3.0
    for i, (num, lab, ncol) in enumerate(tiles):
        tx = XL + i * (tile_w + tgap)
        _card(back, tx, tile_T, tile_w, tile_h, z=3)
        _text(front, tx + 0.016, tile_T + 0.011, num, 34, ncol, disp, weight="bold")
        _text(front, tx + 0.016, tile_T + tile_h - 0.010, lab, 13.5,
              figstyle.MUTED, sans, va="bottom", spacing=1.15)

    # ---- centerpiece: convergent-evidence matrix --------------------------
    mat_bot = _place_image(fig, back, figs_dir / "target_matrix.png",
                           XL, 0.330, CW, z=6)

    # ---- bottom row: CBLB lead panel (left) + donor scatter (right) -------
    row_T = mat_bot + 0.026
    donor_w = 0.395
    donor_x = XR - donor_w
    donor_bot = _place_image(fig, back, figs_dir / "donor_consistency.png",
                             donor_x, row_T, donor_w, z=6)

    lead_x, lead_w = XL, (donor_x - 0.028) - XL
    lead_h = donor_bot - row_T
    _card(back, lead_x, row_T, lead_w, lead_h, z=3)
    px, py = lead_x + 0.020, row_T + 0.020
    _text(front, px, py, "THE PROOF · CBLB", 13, figstyle.AMBER, disp,
          weight="bold")
    _text(front, px, py + 0.024, "Found blind. Now in the clinic.", 24,
          figstyle.INK, disp, weight="bold")
    bullets = [
        (figstyle.TEAL, "Surfaced from the raw genome-scale",
         "ranking — with zero prior hints."),
        (figstyle.TEAL, "Pharma is already in the clinic here:",
         "NX-1607 (Ph1), HST-1011 (Ph1/2)."),
        (figstyle.AMBER, "Release this E3-ligase brake and",
         "the T cell fights harder."),
    ]
    by = py + 0.070
    for col, l1, l2 in bullets:
        _dot(front, px + 0.006, by + 0.004, col, size=95)
        _text(front, px + 0.022, by, l1, 14.5, figstyle.BODY, sans)
        _text(front, px + 0.022, by + 0.0165, l2, 14.5, figstyle.BODY, sans)
        by += 0.050

    # ---- payoff / sell footer band ----------------------------------------
    foot_T = donor_bot + 0.022
    foot_h = 0.980 - foot_T
    _card(back, XL, foot_T, CW, foot_h, fill=figstyle.BG_PANEL, z=3)
    fx, fy = XL + 0.022, foot_T + 0.014
    _text(front, fx, fy, "THE PAYOFF · AN AI-NATIVE DISCOVERY BLUEPRINT", 13,
          figstyle.TEAL, disp, weight="bold")

    col2_x = XL + CW * 0.500
    row0 = fy + 0.020
    row_dt = 0.014
    # confident sell chips — 2 left + 2 right (one forward line, right/bottom)
    left_items = [
        (figstyle.TEAL, [("Five candidates: ", figstyle.BODY),
                         ("CBLB", figstyle.AMBER),
                         (", CD5, DGKA, SMAD3, UBASH3A.", figstyle.BODY)]),
        (figstyle.TEAL, [("One week, one person · NVIDIA DGX Spark · Claude Science.",
                          figstyle.BODY)]),
    ]
    right_items = [
        (figstyle.TEAL, [("Reproducible from one command — caught its own math bug.",
                          figstyle.BODY)]),
        (figstyle.AMBER, [("Candidate targets — ready to test, not finished drugs.",
                           figstyle.BODY)]),
    ]

    def _footcol(items, x0):
        for i, (col, segs) in enumerate(items):
            yy = row0 + i * row_dt
            _dot(front, x0 + 0.006, yy + 0.004, col, size=80)
            _rich(fig, front, x0 + 0.022, yy, segs, 13.5, sans)

    _footcol(left_items, fx)
    _footcol(right_items, col2_x)

    # data credit + author / contact (full-width)
    cred_y = row0 + 2 * row_dt + 0.002
    _text(front, fx, cred_y,
          "Data: public Marson lab (Gladstone) + Pritchard lab (Stanford) CRISPRi "
          "screen · bioRxiv 10.64898/2025.12.23.696273",
          12.5, figstyle.MUTED, sans)
    _rich(fig, front, fx, cred_y + 0.0145,
          [("Chengchen (Sam) Duan", figstyle.INK),
           ("   ·   duanchengchen@gmail.com   ·   github.com/duanchengchen-oss",
            figstyle.MUTED)], 13.5, sans)

    fig.savefig(out_png, dpi=DPI, facecolor=figstyle.BG)
    fig.savefig(out_svg, facecolor=figstyle.BG)
    figstyle.plt.close(fig)
    print("wrote", out_png, "+", out_svg)


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--png", default="../deliverables/figures/brakepoint_onepager.png")
    ap.add_argument("--svg", default="../deliverables/figures/brakepoint_onepager.svg")
    a = ap.parse_args()
    build(a.png, a.svg)
