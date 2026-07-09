# Genetic direction-of-effect — literature grounding

*Pass: 2026-07-09 (results-watcher run 2b). According to PubMed (retrieved via the bio-research MCP, 2026-07-09). Machine-readable version: `references.json`.*

These references replace the bare `literature_expectation` assertions behind the direction calls in `concordance_snapshot.json` with real, citable sources. Open Targets stayed rate-limited this pass, so these PubMed citations are the interim evidence base. **Modality = KO; concordant = `protective_lof`.** Funnel is unchanged (8 → 5 → 4 → 4 → **1**), but the four directional calls are now citation-backed.

## Concordant hero

**UBASH3A — `protective_lof` ✓ (the concordant call)**
- Ge Y et al., *Diabetes* 2017 — "UBASH3A Mediates Risk for Type 1 Diabetes Through Inhibition of T-Cell Receptor-Induced NF-κB Signaling." [DOI](https://doi.org/10.2337/db16-1023) (PMID 28607106). **T1D risk alleles (rs11203203, rs80054410) *increase* UBASH3A expression, suppressing NF-κB/IL-2 → therefore loss-of-function is genetically protective (`protective_lof`).** This is the direct human-genetics basis for the hero nomination.
- Mordes JP et al., *Genes (Basel)* 2021 — TCR genotype and Ubash3a determine susceptibility to rat autoimmune diabetes. [DOI](https://doi.org/10.3390/genes12060852) (PMID 34205929). In vivo support for UBASH3A as a TCR-signalling brake.

## Directional but discordant under the strict KO rule (risk_lof = LoF raises autoimmune risk)

**CBLB — `risk_lof`, genome-wide significant ✓**
- Sanna S et al., *Nat Genet* 2010 — "Variants within the immunoregulatory CBLB gene are associated with multiple sclerosis." [DOI](https://doi.org/10.1038/ng.584) (PMID 20453840). **GWAS: rs9657904, P = 1.6×10⁻¹⁰, OR = 1.40** (genome-wide significant); Cblb-null mice are EAE-prone.
- Loeser S & Penninger JM, *Semin Immunol* 2007 — Cbl-b regulates peripheral T-cell tolerance. [DOI](https://doi.org/10.1016/j.smim.2007.02.004) (PMID 17391982). Cbl-b loss → antigen-triggered autoimmunity ("key autoimmunity gene") and Cbl-b-deficient mice reject tumors (also grounds the IO rationale).

**SOCS1 — `risk_lof`, genome-wide significant ✓**
- Hadjadj J et al., *Nat Commun* 2020 — "Early-onset autoimmunity associated with SOCS1 haploinsufficiency." [DOI](https://doi.org/10.1038/s41467-020-18925-4) (PMID 33087723). Heterozygous germline LoF → dominantly inherited autoimmunity (increased STAT activation).
- Jeanpierre M et al., *J Exp Med* 2024 — PTPN2 haploinsufficiency / systemic autoimmunity. [DOI](https://doi.org/10.1084/jem.20232337) (PMID 39028869). Groups SOCS1 with PTPN2 as monogenic autoimmunity from LoF of cytokine-signalling brakes.

**TNFAIP3 (A20) — `risk_lof`, genome-wide significant ✓**
- Mele A et al., *Adv Exp Med Biol* 2014 — SNPs at the TNFAIP3/A20 locus and autoimmune/inflammatory disease. [DOI](https://doi.org/10.1007/978-1-4939-0398-6_10) (PMID 25302371). GWAS SNPs that *decrease* A20 expression / NF-κB-inhibitory function → SLE and others. Also notes A20-KO mouse multi-organ failure → supports the tumor-suppressor/safety flag.

> Why "discordant" isn't "wrong": CBLB/SOCS1/TNFAIP3 are `risk_lof` for autoimmunity — human proof they are genuine T-cell brakes whose removal amplifies immunity. That is mechanistically *supportive* of an IO-enhancing KO; it only scores "discordant" under a strict cancer-anchored (LoF-is-protective) rule. Direction must be read with the disease anchor in mind.

## No directional immune-genetics (direction = none)

**RASA2** — Carnevale J et al., *Nature* 2022 — "RASA2 ablation in T cells boosts antigen sensitivity and long-term function." [DOI](https://doi.org/10.1038/s41586-022-05126-w) (PMID 36002574). Strong functional/novelty support (genome-wide CRISPR-KO screens; ablation boosts CAR-T persistence & efficacy) but **no directional human genetics → `none`.**

**CD5** — no genome-wide-significant directional genetics citation retrieved this pass (kept out of the directional funnel). Clinical/tractability evidence (ChEMBL immunotoxins; 15 active CD5 CAR-T/CAR-NK trials) is in `CD5.json`.

**TCEB2/ELOB, ARID1A** — direction = none (housekeeping/pan-essential complex, and somatic-tumor-suppressor/developmental genetics respectively); no directional immune-GWAS applies.

## Screen lineage (the pre-registered hit list)

- Shifrut E et al., *Cell* 2018 — "Genome-wide CRISPR Screens in Primary Human T Cells Reveal Key Regulators of Immune Function." [DOI](https://doi.org/10.1016/j.cell.2018.10.024) (PMID 30449619). SLICE genome-wide LoF screens found genes that negatively tune proliferation; ablation enhanced cancer-cell killing — the basis for the expected KO hit set.

---
*⚠️ Still pre-registered expectation, not a result. When Open Targets is reachable, cross-check these directions against OT's variant-level direction-of-effect and genetic-association scores.*
