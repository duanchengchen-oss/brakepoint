# REAL FINDING — Datlinger validation run (Day 3, live Claude Science output)

**This replaces the provisional expectation in `DRAFT_finding.md`. Every number here is from the real run** `outputs/ranked_perturbations.csv` (Claude Science, seed=0) or a live database query.

## The run
- **Data:** Datlinger 2017 CROP-seq, Jurkat T cells ± TCR stimulation (the planned **smoke/validation** set, GSE92872).
- **Scale:** 5,848 cells, **96 perturbations**, control = `control`, 6 technical replicates.
- **Pipeline:** load → QC → power-equalized **E-distance** + permutation E-test → viability + (modality-aware) on-target checks → transparent gated ranking. Ran end-to-end, wrote CSV + a ranked-genes figure.

## The validation (this is the point of a smoke run)
The causal-effect-size ranking **recovers the canonical TCR-signaling hierarchy** — exactly what should top a Jurkat ± TCR screen, so the method is trustworthy:
- **Proximal TCR signaling:** ZAP70 (E=22.3), LAT (E=18.4) — the core kinase/adaptor.
- **SHP phosphatases:** PTPN6/SHP-1 (E=27.5), PTPN11/SHP-2 (E=26.7).
- **TCR-induced TF program:** FOS/JUN (AP-1), NFATC1/3, NF-κB (NFKB1/2, RELA/RELB), EGR1/2/4, NR4A1, BACH2.

Top 10 by E-distance: **FOS, PTPN6, PTPN11, BACH2, ZAP70, EGR1, LAT, NFATC1, RELA, EGR2.** Modality-aware on-target behaved correctly (KO → mRNA fold-change reported but not gated; e.g. NR4A1 0.19, FOS_3 0.45 down, others up — as expected when frameshift transcripts escape NMD). No perturbation tripped the viability flag.

## Druggable standout (live database evidence)
**PTPN11 / SHP-2 — top-3 causal hit AND clinically validated.** ClinicalTrials.gov: **36 trials** for SHP2 inhibitors, incl. a **Phase 3 recruiting** (JAB-3312 + JAB-21822, KRAS-G12C NSCLC, NCT06416410, n=392) and Phase 1/2 programs (Novartis TNO155, JAB-3312, BBP-398, ET0038). SHP-2 is a **negative regulator of T-cell activation downstream of PD-1**, so loss-of-function boosting effector function is mechanistically coherent — a rare case where a top screen hit is both drugged and immuno-relevant. (Chemical matter/tractability: precedented small-molecule, allosteric.)

## Honest scope + next step
This is the **Jurkat validation run** — it proves the E2E pipeline and recovers known biology, but Jurkat is a cell line, not the disease-grade context. **Next:** rerun on **Shifrut/Marson primary human CD8⁺ T cells (GSE119450)** for the Gladstone-grade headline, then wire `concordance.py` (Open Targets `directionOnTarget`/`directionOnTrait`) to nominate a **novel, genetically-concordant** hero. PTPN11/SHP-2 becomes the *positive control that proves the screen finds real, druggable biology*.

## 100–200 word summary (submission draft, real numbers)
Using Claude Science, we built a reproducible pipeline that ranks CRISPR perturbations in T cells by **causal effect size** — power-equalized energy distance (E-distance) with a permutation test — rather than by p-value, then filters for viability and on-target effect and treats replicates correctly. On the Datlinger CROP-seq screen (5,848 Jurkat cells, 96 perturbations) it recovers the canonical TCR-signaling hierarchy end-to-end: proximal signaling (ZAP70, LAT), the SHP phosphatases (PTPN6, PTPN11), and the TCR-induced AP-1/NFAT/NF-κB/EGR transcription-factor program. The top-ranked druggable node, **PTPN11/SHP-2**, is independently validated — 36 clinical trials including a Phase 3 — and is a PD-1-proximal brake on T-cell activation, showing the ranking finds real, therapeutically relevant biology. Every artifact carries Claude Science provenance; one command reproduces the ranking from a clean clone. We next extend to primary human CD8⁺ T cells and layer human-genetics direction-of-effect concordance to nominate a novel, tractable target.

## 3-minute demo script (real-numbers version)
- **0:00–0:30** — Q: which T-cell perturbations *causally* reshape state, and which are real drug targets? We rank by causal effect size, then keep concordant human genetics.
- **0:30–1:15** — Rigor: E-distance not p (fixed a real n-bias bug in the core — now null≈0 at all n); viability gate; modality-aware on-target; replicates done right; seeds + lockfile + one-command `make hero`.
- **1:15–2:05** — Validation (live figure): on real data the ranking **re-discovers the TCR-signaling hierarchy** (ZAP70/LAT + SHP1/2 + AP-1/NFAT/NF-κB). If the method recovers known biology unsupervised, trust its novel calls.
- **2:05–2:40** — The druggable hit: **PTPN11/SHP-2**, top-3, 36 trials incl. Phase 3, a PD-1-proximal T-cell brake — the positive control. Then the novel, genetically-concordant nomination from the primary-CD8 run.
- **2:40–3:00** — Provenance (Claude Science artifacts + reviewer), OSS-licensed, reproducible. Ask = a novel, concordant, tractable target nominated end-to-end.
