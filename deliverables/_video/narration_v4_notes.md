# narration_v4 — prosody / 断句 pass for F5-TTS

Goal of v4 over v3: stop F5-TTS from mis-pausing. F5 inserts an unnatural
micro-pause at **hyphens** (and can clip hyphenated compounds), and makes a
**hard stop at em dashes (—)**. v4 removes every spoken hyphen and every em dash
from the F5 INPUT, and reworks the one trailing fragment F5 stumbled on
("…the rest, genome-wide."). Meaning, facts, honest framing, and per-line length
(~13–19 s spoken) are unchanged.

## Files
- **`narration_v4.txt`** — F5 INPUT. De-hyphenated compounds, no em dashes, gene
  respellings that already work kept verbatim.
- **`captions_v4.txt`** — DISPLAY text. Same wording/sentence structure as
  narration (so captions track the audio), but proper spelling: gene symbols
  (CBLB/CD4/CD5/DGKA/SMAD3/UBASH3A), CAR-T, 2.6 million, 97%, and hyphens
  restored in written compounds (genome-wide sense, genome-scale,
  CRISPR-interference, off-switch, T-cell, early-phase, two-donor).

## Global rules applied
- **Zero em dashes** anywhere in the F5 input. Each "—" became a period (clean
  full stop) or a comma (light breath), whichever read more naturally. Chose a
  hard cutover to zero (not "1–2 kept") because the user is actively hearing F5
  mis-pause; a period at a real pause is just as strong and carries no dash risk.
- **Zero spoken hyphens** except the one intentional pronunciation aid
  **"you-bash three A"** (UBASH3A) — explicitly retained per the brief; its hyphen
  is a within-word syllable cue, not a compound break.
- **Gene/number respellings unchanged:** see bee ell bee (CBLB), C D four (CD4),
  C D five (CD5), D G K alpha (DGKA), smad three (SMAD3), you-bash three A
  (UBASH3A), car T (CAR-T); "twelve thousand", "two point six million", "two
  million", "eleven thousand", "seven", "ninety seven" stay words in narration.
- **No new claims added.** (Codex's draft inserted "We generated no data
  ourselves." and a spoken "p equal to 0.70"; both were dropped — they are
  content additions beyond a prosody pass and change length. v3 already carries
  the honesty via "chosen using prior evidence", "two donor power limit, not a
  null result", "hypothesis to test, not a finished answer".)

---

## Per-line changes

**1 · Hook.**
- De-hyphenation / re-flow: the trailing fragment **"So we went looking for the
  rest, genome-wide."** → **"So we went looking for the rest of them, right
  across the genome."** No spoken "genome-wide" hyphen, and it now reads as a full
  clause instead of an afterthought.
- Em dash removed: "on a T cell — but they help…" → comma. Reads as one connected
  contrast instead of a hard stop.

**2 · Thesis.**
- Em dash removed: "beyond checkpoint therapy — they also throttle…" → split into
  two short sentences ("…therapy. They also throttle engineered car T.").
- Colon softened to a comma: v3 "So across the genome: which genes are the
  brakes?" → **"So across the genome, which genes are the brakes?"** Kept the two
  distinct questions (question intonation on each) from v3's design.
- "car T" kept.

**3 · The screen.**
- De-hyphenated **"genome-scale" → "genome scale"** and **"CRISPR-interference" →
  "CRISPR interference"** (both were spoken hyphens).
- Kept the list-introducing colon after "screen" (a natural "namely" pause, not a
  hyphen/dash — F5 handles it) and the punchy honest beat "Two donors, out of an
  intended four."

**4 · The trap.**
- De-hyphenated **"ninety-seven" → "ninety seven"** (caption keeps 97%).
- Em dash removed: "rank by significance — but at two million cells, that breaks
  down:" → comma + period: **"…rank by significance, but at two million cells,
  that breaks down. Over ninety seven percent…"** The colon also became a period
  so the payoff stands as its own sentence.

**5 · Discovery engine.**
- Two em dashes removed. v3 had "wrong genes — the biggest hits…" and "direction —
  toward the effector program, or away." → **"…wrong genes. The biggest hits are
  the cell's own signaling machinery. So we add what a magnitude ranking leaves
  out. Direction. Does the knockdown push toward the effector program, or away?"**
- The single most dramatic beat (the "direction" reveal) is preserved as a
  one-word sentence **"Direction."** — F5 pauses cleanly at the period, giving the
  same emphasis the old em dash intended, with no dash artifact. The follow-up is
  now a proper question instead of a dangling appositive.

**6 · Explore live.**
- Em dash removed: "…here to explore — search any gene…" → period:
  **"…here to explore. Search any gene, hover any point…"**
- Kept contractions ("isn't", "It's") and the "eleven thousand that passed our
  testing threshold" fix from v3 (consistency with 12k profiled → 11k passed).

**7 · Why it's different.**
- Two em dashes removed: "finds correlations — not what to drug" → comma; "which
  way it pushes — then weigh it…" → comma. Both are light breaths now, keeping the
  three-beat contrast (DE / genetics / us) without hard stops.

**8 · Shortlist.**
- Reworded **"five prior-informed candidates"** (spoken hyphen) → **"five
  candidates chosen using prior evidence"** — no hyphen, and it makes the honest
  "prior-informed, not de-novo" point explicit.
- Em dash removed after the gene list: "…you-bash three A — each scored…" →
  period: **"…you-bash three A. Each scored across seven lines of evidence…"**
- Gene list + separating commas unchanged (forces F5 to segment each respelled
  name). "you-bash three A" hyphen deliberately kept.

**9 · The lead.**
- De-hyphenated **"off-switch" → "off switch"** and **"early-phase" → "early
  phase"** (both spoken hyphens; captions restore them, plus adjectival "T-cell").
- No em dashes in this line. Ends on "C D five and D G K alpha come next." (v3's
  donor-stutter fix retained).

**10 · Reported honestly.**
- De-hyphenated **"two-donor" → "two donor"** (caption restores "two-donor").
- Em dash removed: "aren't significantly enriched — but that's a two-donor power
  limit, not a null result." → comma: **"…aren't significantly enriched, but
  that's a two donor power limit, not a null result."**
- Semicolon after "hold up in both" split into a period for a cleaner three-beat
  cadence ("…hold up in both. The other three ride on one donor."). Honest
  power-limit framing and "hypothesis to test, not a finished answer" kept intact.

**11 · Close.**
- Em dash removed: "led by see bee ell bee — a target the industry already drugs…"
  → period: **"…led by see bee ell bee. It's a target the industry already drugs,
  so recovering it validates our method."**
- Reproducibility wording, self-caught-bug beat, call to action, and "Built with
  Claude Science." all unchanged.

---

## Consistency note carried forward from v3
If the spaced letter forms (C D four / C D five / D G K alpha) ever slur at speed,
apply the same full-phonetic treatment used for CBLB (see dee four / see dee five /
dee jee kay alpha). CRISPR still relies on F5 saying "crisper"; if it spells the
letters, respell to "crisper interference" in line 3. Neither was changed here —
this pass was strictly prosody (hyphens + em dashes + one fragment).
