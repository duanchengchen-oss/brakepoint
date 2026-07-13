# narration_v3 — rationale (F5-TTS input vs. on-screen captions)

Two files, 11 lines each, one per scene:

- **`narration_v3.txt`** — the text fed to F5-TTS. Gene/acronym names are respelled and
  numbers are written as words, so the model says them right at ~1.5x speed.
- **`captions_v3.txt`** — the display text for on-screen captions. Proper spelling
  (CBLB, CD4, DGKA, 2.6 million, 97%, CAR-T). Phrasing/punctuation is identical to the
  narration so the captions track the audio; only spelling/number format differs.

Read each line aloud at speed to check cadence: F5 breathes at commas, semicolons,
colons, periods, and em dashes (—). Em dashes = the longest in-sentence pause. I kept
those for emphasis and used commas for breath, but avoided over-comma'd, choppy lines.

---

## CBLB respelling — 3 candidates to A/B on F5 (ranked)

Known failure: raw `CBLB` (and space/dot letter forms) slurred to **"CBLOB" / "C.B.LowB"**
at 1.5x — F5 merged the four capitals into a pseudo-word and turned the second-to-last
letter into "Low". The fix is to stop the model from *reading letters* and make it *say
words*.

1. **`see bee ell bee`**  ← **top pick, used in `narration_v3.txt`.**
   Full phonetic spelling: four unambiguous English words, nothing to merge into "CBLOB",
   no "Low". This is the most robust across TTS engines. Minor risk: it can sound a hair
   spelled-out/deliberate, but at 1.5x it tightens up and that beats a slur. (Use "ell",
   not "el" — "ell" reads as the letter L; "el" can drift Spanish.)
2. **`C-B-L-B`**
   Hyphen-joined single letters. Hyphens force letter-by-letter separation more reliably
   than spaces or dots. Risk: some models voice the hyphen as "dash" or ignore it and
   slur anyway.
3. **`C.B.L.B.`**
   Period-separated letters (each period = micro-pause). Included for completeness, ranked
   last because it is closest to the form that already produced "C.B.LowB".

Avoid the bare space form **`C B L B`** — that is the documented-bad baseline (→ "CBLOB").

If the human confirms "see bee ell bee" wins, note it reads correctly in all three scenes
it appears (8, 9, 11) — keep it identical everywhere for consistency.

## Other genes/acronyms (respellings used in narration_v3.txt)

- **DGKA / DGKα → `D G K alpha`** (scenes 8, 9, 10). Spelled letters + the word "alpha".
- **UBASH3A → `you-bash three A`** (scene 8). "you-bash" reads as a word, digit spelled out,
  trailing letter "A" → "ay".
- **CD4 → `C D four`** (scene 3); **CD5 → `C D five`** (scenes 8, 9, 10).
- **CAR-T → `car T`** (scene 2) → "car tee". Caption keeps "CAR-T".
- **SMAD3 → `smad three`** (scene 8). Failure was **"Smen3"** — caused by the attached digit
  and the capitalized token. Lowercasing to a plain word ("smad") + detaching the number
  ("three") fixes both. **Backup if F5 lengthens the vowel to "smaid": `smadd three`** (the
  double-d cues a short "a" as in "mad").
- **T cell / T-cell activation → `T cell` / `T cell activation`** in narration (hyphen dropped
  so F5 doesn't hesitate); captions keep "T-cell activation".

**Consistency caveat for the human:** CBLB uses full phonetic words while DGKA/CD4/CD5 use
spaced single letters (per the agreed convention). If the spaced forms *also* slur at 1.5x
in testing, apply the same phonetic treatment — `dee jee kay alpha`, `see dee four`,
`see dee five` — for a uniform, slur-proof read.

**Watch item (not flagged in QA, left as-is):** `CRISPR-interference` relies on F5 saying
"crisper". If it ever spells C-R-I-S-P-R, respell to `crisper interference` in scene 3.

## Numbers (narration = words, captions = numerals)

- `2.6 million` → spoken **"two point six million"** (scene 3).
- `97%` → spoken **"ninety-seven percent"** (scene 4).
- "twelve thousand" / "eleven thousand" / "two million" / "seven" kept as words in both
  files (they already read cleanly and match the spoken cadence; captions follow the
  existing player house style from gen_vtt.py).

---

## Per-scene notes

**1 · Title/hook** — Unchanged text. Em dash after "T cell" sets up the "but they help only
a minority" turn; comma before "genome-wide" gives the closing breath. Reads clean at speed.

**2 · Thesis** — 断句 fix. The original ran two "which…" clauses through a single em dash
("which genes are the brakes — which knockdowns push…"), which spoken becomes one long
run-on. Split into two distinct questions with a colon + "And" so F5 lands a clear
question intonation on each: "…across the genome: which genes are the brakes? And which
knockdowns push…?" CAR-T → "car T" in narration.

**3 · The screen** — Colon after "screen" opens the list; commas segment it for natural
pacing. "two point six million" and "C D four" respelled. Kept the honest "Two donors, out
of an intended four." beat as its own short sentence.

**4 · The trap** — Added a comma after "two million cells" for a breath before the payoff
("that breaks down: over ninety-seven percent…"). "ninety-seven percent" spelled out.

**5 · Discovery engine** — Unchanged. The colon before "direction" and the em dash after it
("direction — toward the effector program, or away") are the two emphasis beats; left intact.

**6 · Explore live — MANDATORY FIX (12k → 11k).** Reworded to explain the drop instead of
letting an unexplained "eleven thousand" contradict scenes 3–4's "twelve thousand":
**"Every one of the eleven thousand that passed our testing threshold is here to explore."**
(12,449 profiled → 11,438 passed testing.) Also dropped the redundant "knockdowns tested" so
the subject isn't a mouthful before the em dash.

**7 · Why it's different** — Unchanged. Three short parallel sentences (DE / genetics / us)
already pace well; kept the em dashes as the contrast beats.

**8 · Shortlist** — The five-gene list is the pronunciation-critical line. Commas between each
respelled name force F5 to separate them (no run-together), and the em dash before "each
scored" gives a pause into the evidence clause. Gene list unchanged: CBLB, CD5, DGKA, SMAD3,
UBASH3A.

**9 · The lead — MANDATORY FIX (cut donor stutter).** Ends at **"CD5 and DGKA come next."** —
the original "— and both hold up across donors" was immediately repeated by scene 10's "CD5
and DGKA hold up in both", a stutter. Scene 10 now owns the donor point. Narration drops the
hyphen in "T-cell" → "T cell activation".

**10 · Reported honestly — MANDATORY FIX (honesty → strength).** Kept the honest caveat but
corrected its interpretation: the non-significant enrichment is a **power limit at two donors,
not a null result** — "Known brakes aren't significantly enriched — but that's a two-donor
power limit, not a null result." Semicolon after "hold up in both" and the em dash before
"but that's" give the two internal pauses. ~19s spoken (original 17.6s); scene 9 shrank to
compensate, so overall pacing holds.

**11 · Close — MANDATORY FIXES (reproducibility wording + validation framing).**
- "every number reproducible from one command" → **"Every figure regenerates from cached
  outputs with one command"** (honest: genome-scale rerun needs a GPU; figures come from
  cached outputs).
- Added the validation beat that pairs with scene 10's caveat: **"a target the industry
  already drugs, so recovering it validates our method."** Recovering a known, druggable brake
  (CBLB) is the positive control that the ranking works — without overclaiming the null.
- Kept the self-caught-bug credibility beat and the call to action. Runs ~20s; acceptable for
  the payoff/close, and balanced by the shorter scene 9.

*(Optimized directly for English cadence rather than via codex — the line-level phrasing
judgment was the point of the task.)*
