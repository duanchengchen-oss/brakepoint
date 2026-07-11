# Skills / MCP recommendations — curated for this submission

From a deep handoff-session report (security-aware, license-checked). Below is the **tight cut** I'd actually install for a solo, near-deadline, life-sciences target-discovery entry — plus what to skip and why. Full report is in the chat paste.

## Install this (minimal, high-ROI, permissive licenses)
1. **create-readme** (github/awesome-copilot, MIT, GitHub-maintained) — generates a clean, fluff-free README from the codebase. Cheap, directly strengthens the OSS-repo deliverable, and doubles as landing-page copy.
   `npx -y skills add github/awesome-copilot --skill create-readme --agent claude-code`
2. **emilkowalski/skills** (motion craft; animations.dev philosophy — sub-300ms, GPU-only, `prefers-reduced-motion`) — elevates the landing page and any UI you film for the demo. Verify license at repo.
   `npx skills add emilkowalski/skills`
3. **Taste Skill** (tasteskill.dev — already chosen) — anti-slop landing-page design. Companion to #2.

That's it for "must add." These three cover the two real gaps (repo README + landing-page polish) with reputable, permissive skills.

## Optional (add only if a specific need appears)
- **superpowers** (obra, MIT) — 7-phase brainstorm→plan→TDD→verify workflow discipline. Excellent in general, but our repo is *already* disciplined (git, tests, one-command `make hero`, LICENSE), so marginal here. Add only if you want the extra verification harness. `/plugin marketplace add obra/superpowers-marketplace` → `/plugin install superpowers@superpowers-marketplace` (disable telemetry: `SUPERPOWERS_DISABLE_TELEMETRY=1`).
- **A demo-video skill** — you already have **HeyGen HyperFrames + Canva + Jam** connected, which cover a ≤3-min video. Add a code-driven renderer only if you want programmatic video: `splitbrain/ndemo` (narrated screen-capture MP4) or `EveryInc/product-launch-video` (Remotion; Remotion is free for solo). Otherwise **skip**.
- **K-Dense scientific-visualization** (MIT) — journal-grade static/vector figures (colorblind-safe, Nature/Science standards). Add **only if BioRender falls short**. `npx skills add K-Dense-AI/scientific-agent-skills --skill scientific-visualization`.

## Skip (bloat / covered / license issues)
- Any **new writing skill** — `internal-comms` + `docx` already cover the 100–180w summary.
- Any **new data connector** — bio-research MCPs already cover the science.
- **impeccable / dedicated a11y** — overlaps the Taste Skill; only if it lacks interaction-state/a11y coverage.
- **scdenney open-science packaging** (CC BY-NC, ~30 stars) — our repo already has reproducibility; NonCommercial + low-star → inspect-before-use, skip for now.
- **dmccreary readme-generator** (CC BY-NC-SA) — avoid; use create-readme instead.

## Security + license flags (do not skip)
- **Review every `SKILL.md` + bundled `scripts/` before enabling** — third-party skills run with your agent's permissions. Prefer high-star, named-author, MIT/Apache skills (create-readme, emilkowalski, superpowers, impeccable). Manually inspect any low-star one.
- **Verify star/install counts on the canonical GitHub repo** — the report's aggregator numbers (e.g. "251k stars") look inflated.
- **Licenses:** MIT/Apache = safe to ship. CC-NC (scdenney, dmccreary) = usable for a hackathon but not permissive — flag in `SOURCES.md` if used. Remotion = free for solo, paid for 4+ employee companies.

## Note on install environment
These install via Claude Code CLI / the plugin system. Install them where you'll build the deliverables; I (Cowork session) can't create or enable skills — you add them, I use them once enabled.
