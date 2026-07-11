"""direction_figure.py — the 2-axis "magnitude x sign" plot for the leaderboard.

Renders the figure described in ``direction_figure_spec.md``:

* **X = E-distance** (magnitude, from ``run_pipeline``): how large the effect is.
* **Y = signed ``direction_score``** (from ``direction.py``): cytotoxic - exhaustion
  shift vs control; ``> 0`` toward effector, ``< 0`` toward exhaustion / loss.

Points are colored by ``direction_tier`` (brake / enhancer / required-machinery /
neutral). Known genes (IL2RB, the TCR/CD3 module, CBLB) are annotated. The top-
right quadrant — high magnitude, positive direction — is the enhancement-candidate
"brake to release" zone.

This module is **import-safe**: nothing runs at import time, and matplotlib is
imported lazily inside the plotting function (and forced to the headless ``Agg``
backend) so importing the sign logic never requires a display.

IMPORTANT — the real ranked CSV does NOT yet carry a ``direction_score`` column.
``run_pipeline.py`` writes the magnitude axis only; the signed column comes from
``run_pipeline.py --direction``, which needs scanpy's ``score_genes`` and therefore
a Claude Science re-run (scanpy is absent in the Cowork sandbox). Until then,
``plot_direction_axes`` fails fast with a clear, actionable message instead of a
cryptic KeyError.
"""

from __future__ import annotations

from collections.abc import Sequence

# Tier labels + curated modules are reused from direction.py (pure-numpy, safe to
# import). A fallback keeps this file usable even if direction.py is unavailable.
try:
    from direction import (
        CYTOTOXIC_GENES,
        EXHAUSTION_GENES,
        TIER_BRAKE,
        TIER_ENHANCER,
        TIER_NEUTRAL,
        TIER_REQUIRED,
    )
except Exception:  # pragma: no cover - direction.py should normally be importable
    TIER_BRAKE, TIER_ENHANCER = "brake", "enhancer"
    TIER_REQUIRED, TIER_NEUTRAL = "required-machinery", "neutral"
    CYTOTOXIC_GENES = EXHAUSTION_GENES = ()

# Genes to call out on the plot (only annotated if present in the CSV).
HERO_GENE = "IL2RB"
# Activation-required TCR / CD3 complex + proximal signaling (positive controls;
# expected far-right, negative-Y => required-machinery).
TCR_MODULE: tuple[str, ...] = (
    "CD3D",
    "CD3E",
    "CD3G",
    "CD247",
    "ZAP70",
    "LAT",
    "LCK",
    "TRAC",
    "LCP2",
)
BRAKE_GENE = "CBLB"  # canonical therapeutic brake; expected far-right, positive-Y.

# Tier -> color (colorblind-friendly; brake highlighted as the candidate class).
TIER_COLORS: dict[str, str] = {
    TIER_BRAKE: "#2ca02c",  # green  — enhancement candidate (the prize)
    TIER_ENHANCER: "#1f77b4",  # blue   — normally promotes effector function
    TIER_REQUIRED: "#d62728",  # red    — essential machinery / positive control
    TIER_NEUTRAL: "#b0b0b0",  # gray   — no directional shift
}
DEFAULT_COLOR = "#7f7f7f"

# The pipeline writes ``e_distance``; the task/spec name it ``edistance``. Accept both.
_X_COLUMN_ALIASES: tuple[str, ...] = ("edistance", "e_distance", "e_dist")
_DIRECTION_COLUMN = "direction_score"
_TIER_COLUMN = "direction_tier"
_PERT_COLUMN = "perturbation"


class MissingDirectionColumn(ValueError):
    """Raised when the ranked CSV has no ``direction_score`` column.

    This is the *expected* state until a Claude Science ``--direction`` re-run
    regenerates the ranked CSV with the signed axis, so the message is actionable
    rather than a bare KeyError.
    """


def _resolve_x_column(columns: Sequence[str]) -> str:
    """Return whichever E-distance column name is present (``edistance``/``e_distance``)."""
    for name in _X_COLUMN_ALIASES:
        if name in columns:
            return name
    raise MissingDirectionColumn(
        "ranked CSV has no E-distance column; expected one of "
        f"{_X_COLUMN_ALIASES}, found {list(columns)}"
    )


def _annotation_genes() -> list[str]:
    """Genes worth calling out, de-duplicated, hero first."""
    ordered = [HERO_GENE, BRAKE_GENE, *TCR_MODULE]
    seen: set[str] = set()
    out: list[str] = []
    for g in ordered:
        if g not in seen:
            seen.add(g)
            out.append(g)
    return out


def plot_direction_axes(
    ranked_csv: str,
    out_png: str,
    *,
    pert_column: str = _PERT_COLUMN,
    title: str = "Perturbation effect: magnitude (E-distance) x signed direction",
    dpi: int = 150,
) -> str:
    """Scatter X = E-distance vs Y = signed ``direction_score``; save to ``out_png``.

    Parameters
    ----------
    ranked_csv:
        Path to a ranked CSV. Must contain a ``direction_score`` column and an
        E-distance column (``edistance`` or ``e_distance``). ``direction_tier`` and
        ``perturbation`` are used when present (for color + annotations).
    out_png:
        Output PNG path.

    Returns
    -------
    The ``out_png`` path (for convenience / testing).

    Raises
    ------
    MissingDirectionColumn:
        If ``direction_score`` (or an E-distance column) is absent — the honest
        signal that a Claude Science ``run_pipeline.py --direction`` re-run is still
        needed to regenerate the CSV with the signed axis.
    """
    import matplotlib

    matplotlib.use("Agg")  # headless: never needs a display
    import matplotlib.pyplot as plt
    import pandas as pd

    df = pd.read_csv(ranked_csv)

    if _DIRECTION_COLUMN not in df.columns:
        raise MissingDirectionColumn(
            f"ranked CSV {ranked_csv!r} has no {_DIRECTION_COLUMN!r} column — the "
            "signed direction axis has not been computed yet. Regenerate it with a "
            "Claude Science run: `python run_pipeline.py --direction ...` "
            "(needs scanpy.tl.score_genes; unavailable in the Cowork sandbox). "
            f"Columns present: {list(df.columns)}"
        )
    x_col = _resolve_x_column(df.columns)

    # Drop rows with no magnitude or no direction (e.g. low-cell perts => NaN).
    plot_df = df.dropna(subset=[x_col, _DIRECTION_COLUMN]).copy()

    tiers = (
        plot_df[_TIER_COLUMN].astype(str)
        if _TIER_COLUMN in plot_df.columns
        else pd.Series([TIER_NEUTRAL] * len(plot_df), index=plot_df.index)
    )
    colors = [TIER_COLORS.get(t, DEFAULT_COLOR) for t in tiers]

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.axhline(0.0, color="0.5", lw=1.0, ls="--", zorder=1)  # sign boundary
    ax.scatter(
        plot_df[x_col],
        plot_df[_DIRECTION_COLUMN],
        c=colors,
        s=42,
        alpha=0.85,
        edgecolors="white",
        linewidths=0.5,
        zorder=3,
    )

    # Annotate the known call-out genes that are actually in the table.
    if pert_column in plot_df.columns:
        by_pert = {
            str(p): (float(x), float(y))
            for p, x, y in zip(
                plot_df[pert_column], plot_df[x_col], plot_df[_DIRECTION_COLUMN]
            )
        }
        for gene in _annotation_genes():
            if gene in by_pert:
                gx, gy = by_pert[gene]
                weight = "bold" if gene in (HERO_GENE, BRAKE_GENE) else "normal"
                ax.annotate(
                    gene,
                    (gx, gy),
                    textcoords="offset points",
                    xytext=(6, 5),
                    fontsize=9,
                    fontweight=weight,
                    zorder=4,
                )

    # Quadrant guide: top-right is the enhancement-candidate zone.
    xmax = float(plot_df[x_col].max()) if len(plot_df) else 1.0
    ymax = float(plot_df[_DIRECTION_COLUMN].abs().max()) or 1.0
    ax.text(
        0.98 * xmax,
        0.92 * ymax,
        "high-magnitude + positive direction\n= candidate BRAKE to enhance",
        ha="right",
        va="top",
        fontsize=8,
        color=TIER_COLORS[TIER_BRAKE],
        style="italic",
    )
    ax.text(
        0.98 * xmax,
        -0.92 * ymax,
        "high-magnitude + negative direction\n= activation-required machinery",
        ha="right",
        va="bottom",
        fontsize=8,
        color=TIER_COLORS[TIER_REQUIRED],
        style="italic",
    )

    ax.set_xlabel("E-distance (effect magnitude, power-equalized)")
    ax.set_ylabel("signed direction_score  (cytotoxic - exhaustion, vs control)")
    ax.set_title(title)

    # Legend from the tier colors (only tiers that appear, plus a stable order).
    from matplotlib.lines import Line2D

    present = [t for t in TIER_COLORS if t in set(tiers)]
    handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            linestyle="",
            markersize=8,
            markerfacecolor=TIER_COLORS[t],
            markeredgecolor="white",
            label=t,
        )
        for t in present
    ]
    if handles:
        ax.legend(handles=handles, title="tier", loc="best", fontsize=8, framealpha=0.9)

    fig.tight_layout()
    fig.savefig(out_png, dpi=dpi)
    plt.close(fig)
    return out_png


def _selftest() -> None:
    """Synthetic self-test: exercise the plotting path with matplotlib only.

    Builds a fake ranked DataFrame (with a ``direction_score`` column) covering all
    four tiers + the call-out genes, writes it to a temp CSV, renders a PNG to
    ``/tmp``, and asserts the PNG is non-empty. Also asserts the graceful-failure
    path fires when ``direction_score`` is absent.
    """
    import os
    import tempfile

    import numpy as np
    import pandas as pd

    rng = np.random.default_rng(0)

    # A realistic-ish mix: annotated genes at sensible quadrants + random filler.
    rows = [
        # (perturbation, e_distance, direction_score, direction_tier)
        (BRAKE_GENE, 58.0, 1.7, TIER_BRAKE),  # far-right, +Y  (the prize)
        (HERO_GENE, 44.0, 0.9, TIER_BRAKE),  # hero, enhancement zone
        ("ZAP70", 73.0, -1.9, TIER_REQUIRED),  # far-right, -Y  (machinery)
        ("CD3E", 66.0, -1.6, TIER_REQUIRED),
        ("LCP2", 40.0, -1.1, TIER_ENHANCER),  # negative but viable
        ("SOCS1", 30.0, 0.6, TIER_BRAKE),
        ("FILLER1", 12.0, 0.02, TIER_NEUTRAL),  # low-mag neutral
        ("FILLER2", 9.0, -0.03, TIER_NEUTRAL),
    ]
    # Add random filler perturbations to make the scatter look populated.
    for i in range(20):
        e = float(rng.uniform(2, 50))
        d = float(rng.normal(0, 0.5))
        tier = (
            TIER_NEUTRAL
            if abs(d) <= 0.05
            else TIER_BRAKE
            if d > 0
            else TIER_ENHANCER
        )
        rows.append((f"G{i:02d}", e, d, tier))

    df = pd.DataFrame(
        rows, columns=[_PERT_COLUMN, "e_distance", _DIRECTION_COLUMN, _TIER_COLUMN]
    )

    tmpdir = tempfile.gettempdir()
    csv_path = os.path.join(tmpdir, "direction_axes_selftest.csv")
    png_path = os.path.join(tmpdir, "direction_axes_selftest.png")
    df.to_csv(csv_path, index=False)

    out = plot_direction_axes(csv_path, png_path)
    assert out == png_path
    assert os.path.exists(png_path) and os.path.getsize(png_path) > 0, "PNG not written"
    print(f"[selftest] wrote {png_path} ({os.path.getsize(png_path)} bytes)")

    # Graceful-failure path: a CSV with no direction_score must raise clearly.
    bad_csv = os.path.join(tmpdir, "direction_axes_selftest_nodir.csv")
    df.drop(columns=[_DIRECTION_COLUMN]).to_csv(bad_csv, index=False)
    try:
        plot_direction_axes(bad_csv, os.path.join(tmpdir, "should_not_exist.png"))
    except MissingDirectionColumn as exc:
        print(f"[selftest] graceful failure OK: {type(exc).__name__}")
    else:  # pragma: no cover
        raise AssertionError("expected MissingDirectionColumn on CSV without direction_score")

    print("SELFTEST PASSED  (2-axis figure renders; missing-column path fails gracefully)")


if __name__ == "__main__":
    _selftest()
