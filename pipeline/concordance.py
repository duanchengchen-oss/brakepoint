"""
concordance.py — direction-of-effect concordance funnel (the scored differentiator).

Given a ranked perturbation table (from run_pipeline) and human-genetics evidence per
gene (Open Targets), decide whether each perturbation's causal direction AGREES with the
disease-risk direction, and report the honest coverage FUNNEL — few gene-disease pairs
carry a usable directional call, so reporting the funnel (not a cherry-picked hit) is the
point (npj Drug Discovery 2025).

Evidence acquisition is pluggable and reproducible:
  - if a snapshot JSON (gene -> evidence) exists, use it (pin on Day 1);
  - else the caller passes an `evidence_fn(gene)` that hits the Open Targets MCP.
The scoring/funnel LOGIC below is pure-Python and unit-tested (`python concordance.py`).

Modality logic:
  KO / CRISPRi  -> loss-of-function is therapeutic -> a PROTECTIVE-LoF allele is concordant
  CRISPRa       -> gain-of-function is therapeutic -> a RISK-LoF allele is concordant
"""
from __future__ import annotations
import json, pathlib
from dataclasses import dataclass, asdict, field
from typing import Callable, Optional, List


def concordance_call(modality: str, genetic_direction: Optional[str]) -> str:
    """'concordant' | 'discordant' | 'no_direction'.
    genetic_direction in {'protective_lof', 'risk_lof', None}."""
    if genetic_direction is None:
        return "no_direction"
    if modality in ("KO", "CRISPRi"):
        return "concordant" if genetic_direction == "protective_lof" else "discordant"
    if modality == "CRISPRa":
        return "concordant" if genetic_direction == "risk_lof" else "discordant"
    return "no_direction"


@dataclass
class GeneEvidence:
    gene: str
    any_gwas: bool = False
    genome_wide_sig: bool = False
    direction: Optional[str] = None            # 'protective_lof' | 'risk_lof' | None


def build_funnel(genes: List[str], evidence_fn: Callable[[str], GeneEvidence], modality="KO"):
    """Return (per_gene_rows, funnel_counts). The funnel is the honest coverage story."""
    rows = []
    funnel = dict(genes=0, any_gwas=0, genome_wide_sig=0, directional=0, concordant=0)
    for g in genes:
        ev = evidence_fn(g)
        funnel["genes"] += 1
        funnel["any_gwas"] += int(ev.any_gwas)
        funnel["genome_wide_sig"] += int(ev.genome_wide_sig)
        call = concordance_call(modality, ev.direction if ev.genome_wide_sig else None)
        funnel["directional"] += int(call != "no_direction")
        funnel["concordant"] += int(call == "concordant")
        rows.append(dict(gene=g, any_gwas=ev.any_gwas, genome_wide_sig=ev.genome_wide_sig,
                         direction=ev.direction, concordance=call))
    return rows, funnel


def load_snapshot(path) -> Optional[dict]:
    p = pathlib.Path(path)
    if not p.exists():
        return None
    return {g: GeneEvidence(gene=g, **v) for g, v in json.loads(p.read_text()).items()}


def _smoke():
    snap = {
        "SOCS1": dict(any_gwas=True, genome_wide_sig=True, direction="protective_lof"),  # concordant KO
        "RISKY": dict(any_gwas=True, genome_wide_sig=True, direction="risk_lof"),         # discordant KO
        "NODIR": dict(any_gwas=True, genome_wide_sig=True, direction=None),               # sig but no direction
        "NONE":  dict(any_gwas=False, genome_wide_sig=False, direction=None),             # no genetics
    }
    ev = {g: GeneEvidence(gene=g, **v) for g, v in snap.items()}
    rows, funnel = build_funnel(list(ev), lambda g: ev[g], modality="KO")
    for r in rows:
        print(f"  {r['gene']:6s} -> {r['concordance']}")
    print("funnel:", funnel)
    assert funnel == dict(genes=4, any_gwas=3, genome_wide_sig=3, directional=2, concordant=1)
    assert [r["concordance"] for r in rows] == ["concordant", "discordant", "no_direction", "no_direction"]
    print("CONCORDANCE SMOKE PASSED")


if __name__ == "__main__":
    _smoke()
