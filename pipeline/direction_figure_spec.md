# Direction-of-Effect Figure Spec — the 2-axis "magnitude × sign" plot

**Status:** spec + guarded plotting code (`direction_figure.py`). The real figure
needs a ranked CSV that carries a `direction_score` column, which requires a
Claude Science scanpy re-run of `run_pipeline.py --direction` (scanpy is absent
in the Cowork sandbox, so the current `outputs*/ranked_perturbations.csv` files
have the magnitude axis only — no `direction_score` yet).

## Why this figure exists

The E-distance leaderboard ranks perturbations by **magnitude only**: how far a
knockout moves cells away from control in the embedding. Magnitude cannot tell
apart two very different biological stories that both land "far from control":

- an **activation-required** gene (CD3D/E/G, ZAP70, LAT, LCK): knockout *cripples*
  the cell — a large but therapeutically *wrong-way* effect (a positive control),
- a therapeutic **brake** (CBLB, PDCD1/CTLA4 axis): knockout *enhances* effector
  function — a large effect in the *desired* direction (an enhancement candidate).

`direction.py` adds the missing **sign**: a per-cell cytotoxic-minus-exhaustion
`score_genes` axis, aggregated per (perturbation × donor), giving a signed
`direction_score` and a `tier`. This figure puts magnitude and sign on one plot
so a reader can separate "big" from "big *and* useful" at a glance.

## Axes

| axis | quantity | source column | meaning |
|------|----------|---------------|---------|
| **X** | E-distance (magnitude) | `edistance` / `e_distance` | how large the perturbation effect is (power-equalized) |
| **Y** | signed `direction_score` | `direction_score` | cytotoxic − exhaustion shift vs control; `>0` = toward effector, `<0` = toward exhaustion/loss-of-function |

- X is strictly positive (a distance). Y is signed and centered on 0.
- Draw a horizontal reference line at **y = 0** (the sign boundary).
- Optionally draw a light vertical reference at the significance/median E-distance.

## Point encoding

- **Color = `direction_tier`** (from `direction.py`):
  - `brake` — positive direction, viable → **enhancement candidate** (highlight color)
  - `enhancer` — negative direction, viable → normally promotes effector function
  - `required-machinery` — negative direction, NOT viable → essential machinery (positive control)
  - `neutral` — `|direction_score| <= tau` → no directional shift
- **Size** may encode `-log10(e_qval)` or `n_cells` (optional; magnitude is already X).
- Marker for **donor sign-agreement**: outline/filled for `direction_sign_agreement == True`
  vs hollow when donors disagree (softens the n=2 donor caveat visually).

## Annotated genes (call-outs)

- **IL2RB** — the hero gene (genome-scale CD4 arm); label prominently.
- **TCR / CD3 module** — CD3D, CD3E, CD3G, CD247, ZAP70, LAT, LCK, TRAC (activation-
  required positive controls); expected far-right, negative-Y → `required-machinery`.
- **CBLB** — the canonical therapeutic brake; expected far-right, positive-Y → `brake`.

## Quadrant reading (top-right is the prize)

```
            Y = direction_score
                    ^  toward EFFECTOR (cytotoxic)
                    |
  low-mag,          |         HIGH-magnitude + POSITIVE direction
  positive          |         = candidate BRAKE to ENHANCE  <-- IL2RB / CBLB target zone
  (weak effector    |         (big effect, in the therapeutic direction)
   nudge)           |
--------------------+--------------------------> X = E-distance (magnitude)
                    |
  low-mag,          |         HIGH-magnitude + NEGATIVE direction
  negative          |         = ACTIVATION-REQUIRED machinery / toxic KO
  (weak loss)       |         (big effect, wrong-way; positive controls: CD3, ZAP70)
                    |  toward EXHAUSTION / loss-of-function
```

- **Top-right (high X, +Y):** the target zone — large effect in the effector-
  enhancing direction. Brakes to release (IL2RB rewiring, CBLB) live here.
- **Bottom-right (high X, −Y):** large effect but wrong-way — activation-required
  machinery / toxic knockouts. These validate the axis (they *should* be big and
  negative) but are not enhancement targets.
- **Left half (low X):** small effects regardless of sign — deprioritized.

## Implementation

`direction_figure.py :: plot_direction_axes(ranked_csv, out_png)`:

- reads the ranked CSV, scatters **X = E-distance**, **Y = `direction_score`**,
- accepts either `edistance` or `e_distance` as the X column (the pipeline writes
  `e_distance`; the spec/task name it `edistance`),
- colors points by `direction_tier` when present (else a single neutral color),
- annotates the known genes above when present in the CSV,
- **does not run on import**, and **fails with a clear message** if the CSV has no
  `direction_score` column (the honest signal that a Claude Science re-run is still
  needed). A synthetic `__main__` self-test exercises the plotting path with
  matplotlib's Agg backend and writes a PNG to `/tmp`.
