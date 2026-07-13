# Task: build 6 Remotion scene components (Remotion 4.0.290, React 19, TypeScript)

You are completing a motion-graphics video. The framework, timeline, fonts, and two
reference scenes (`src/scenes/Title.tsx`, `src/scenes/MapScene.tsx`) are DONE and
must NOT be changed. Your job: replace the 6 STUB scene files with polished,
animated scenes matching the existing dark aesthetic. Only edit these files:
`src/scenes/Question.tsx`, `Provenance.tsx`, `Method.tsx`, `Validation.tsx`,
`Brakes.tsx`, `Close.tsx`. Do not touch anything else. Keep exact named exports
(e.g. `export const Question: React.FC = () => (...)`).

## Available building blocks (import from `../lib/anim` and `../theme`)
- `Bg` — wraps a scene: dark bg + glows + grid + BRAKEPOINT wordmark + 118px padding. Put content as children in a vertical flex column.
- `Eyebrow` — pill label (uppercase). `<Eyebrow>THE QUESTION</Eyebrow>`.
- `Words` — staggered word-reveal heading. `<Words size={72} delay={10} maxWidth={1400} parts={[{t:'plain '},{t:'colored',color:C.amber}]} />`.
- `CountUp` — animated integer. `<CountUp to={2638736} delay={20} dur={45} style={{...}} />` renders with thousands separators.
- `Bullet` — `<Bullet color={C.teal} delay={20}>text with <b style={{color:C.ink}}>bold</b></Bullet>`.
- `Spacer` — `<Spacer/>` flexible gap (use to vertically center content).
- `useEnter(delay, dist)` — returns `{opacity, transform}`; spread onto any element for a spring fade-up.
- `C` — colors: `bg, bg2, ink(#fff), body, mut, teal(#2fd6bf), teal2, tealDk, amber(#f4b062), amber2, line`.
- `disp` (Space Grotesk display font family string), `sans` (Plus Jakarta Sans).
- From `remotion`: `useCurrentFrame`, `useVideoConfig`, `spring`, `interpolate`, `AbsoluteFill`.

Study `src/scenes/Title.tsx` for the exact pattern (Bg + Eyebrow + Spacer + Words + useEnter). Match its font sizes/spacing feel. Animations must be tasteful: spring entrances, staggered by ~4-8 frames, nothing bouncy/gaudy. Use `C.teal` for machinery/negative ideas and `C.amber` for brake/positive ideas.

## Scenes (content is fixed — do not change wording; make it beautiful + animated)

### Question.tsx (≈567 frames)
- Eyebrow: `The question`
- Heading (`Words`, size ~84, maxWidth 1500): "Which knockdowns make a T‑cell a **better** effector — and which just **break** it?" with the word `better` in `C.amber` and `break` in `C.teal` (split the parts accordingly).
- Then a KPI row (3 items, flex gap ~70, appears after the heading ~delay 60): each item = a big number (`disp`, ~74px, `#fff`) over a small label (~24px, `C.mut`). Use `CountUp` for the numbers:
  - `2,638,736` / "primary human CD4⁺ T cells"
  - `12,449` / "CRISPRi knockdowns"
  - `2 donors` (plain text, not CountUp) / "scVI-integrated · Stim 8h"

### Provenance.tsx (≈848 frames)
- Eyebrow: `How Claude Science got us there`
- Heading (`Words`, ~66): "Every number carries its **provenance**." (`provenance` gradient/amber).
- Three `Bullet`s, staggered (delays ~30/60/90):
  1. (teal) Each result is a **versioned artifact** — its exact code, environment, and the conversation that produced it.
  2. (amber) A background **reviewer** checks every claim against what actually ran — it caught a **real statistical bug** before it reached a figure.
  3. (teal) Heavy compute runs on an **NVIDIA DGX Spark**; the signed map over 2.6M cells finishes in **~40 seconds**.

### Method.tsx (≈805 frames)
- Eyebrow: `The method · two axes`
- Heading (`Words`, ~60): "Magnitude tells you **how much**. Only the sign tells you **which way**." (`how much` teal, `which way` amber).
- Two cards side-by-side (flex, gap ~40, margin-top ~40), each sliding/springing in (left card from x-30, right from x+30, delays 40 & 55). Each card: rounded 26, padding ~44, border `1px solid C.line`.
  - Left (teal-tinted bg `linear-gradient(180deg, rgba(13,148,136,0.16), rgba(13,148,136,0.03))`): title (disp 40, C.teal) "↓ direction < 0 — machinery"; body (29, C.body): "Knockdown pushes cells **away** from the effector program — required, not druggable."
  - Right (amber-tinted `linear-gradient(180deg, rgba(217,122,18,0.16), rgba(217,122,18,0.03))`): title (disp 40, C.amber) "↑ direction > 0 — a brake"; body: "Knockdown pushes cells **toward** the effector program — the therapeutic quadrant."
- A sub line under the cards (useEnter delay 80, size 31, C.mut, maxWidth 1500): "Axis 1 — power-equalized **energy distance** (causal magnitude). Axis 2 — a per-cell **effector minus dysfunction** score, over all 2.64 M cells."

### Validation.tsx (≈727 frames)
- Eyebrow: `Validation · it recovers ground truth`
- A flex row (align center, gap ~80): LEFT a huge stat — `<CountUp to={14} dur={40}/>` at ~150px disp `#fff` with a smaller "/15" (~80px, C.mut) beside it, and under it a ~26px C.mut caption "largest effects are machinery, not targets". RIGHT a column: Heading (`Words`, ~62, maxWidth 720): "Unsupervised, the biggest effects are the **TCR module**." (`TCR module` teal). Then a paragraph (useEnter delay 40, ~34px, C.body, maxWidth 760): "ZAP70, the CD3 complex, LAT — and the direction axis flags every one as machinery, **donor-consistently**. That machinery result is the load-bearing one."

### Brakes.tsx (≈790 frames)
- Eyebrow: `The therapeutic quadrant`
- Heading (`Words`, ~64): "The positive quadrant — **reported honestly**." (`reported honestly` amber).
- Three `Bullet`s (delays ~30/60/90):
  1. (amber) Known brakes **CD5, DGKA** land here and are donor-consistent — a consistency check.
  2. (teal) But at two donors the quadrant is **not yet enriched** for a known-brake set (Mann–Whitney p = 0.70); its strongest raw hits include likely artifacts.
  3. (teal) So the positive side is an honest, prioritized **hypothesis space** for the full four-donor cohort — the validated result is the machinery axis.

### Close.tsx (≈337 frames)
- Eyebrow: `Reproducible by design`
- Heading (`Words`, ~88): "One command. **Fixed seeds.** MIT." (`Fixed seeds.` gradient/teal).
- A code block (useEnter delay 30): monospace ~34px, bg `#0c1614`, border `1px solid C.line`, radius 22, padding "44px 48px", maxWidth ~640, with two teal lines: `make smoke` and `make figure` (and a muted `# runs anywhere` comment line above, color `#6f8f88`).
- Footer (useEnter delay 50): small brand line (disp, C.ink) "Brakepoint · Built with Claude Science."

## Definition of done
- `npx remotion still src/index.ts BrakepointVideo out/test.png --frame=700` renders with no TypeScript/render error (frame 700 is inside the Question scene). Try a few frames across scenes.
- Every scene is visually polished, animated, on-brand, and legible at 1920×1080. Content wording unchanged from above.
- Only the 6 named files changed. Report what you did.
