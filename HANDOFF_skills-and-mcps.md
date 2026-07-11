# Handoff prompt — skill & free-MCP discovery + install (paste into a fresh session with ~/Claude Hackathon connected)

Your job: **find, curate, and surface for one-click install the best skills and free (or free-tier) MCP connectors** that will make our hackathon deliverables stand out. Context: solo **research-track** entry in "Built with Claude: Life Sciences" (**life-sciences target discovery**); deliverables are a **≤3-minute demo video**, an **open-source repo + landing page**, and a **100–180 word summary**. Working folder: `~/Claude Hackathon`. **Prioritize FREE / free-tier and genuinely useful — avoid bloat.**

## Step 1 — See what's already installed/connected (don't duplicate)
Call `list_plugins` and `list_skills`. Already in place: the **bio-research** plugin (Open Targets, ChEMBL, ClinicalTrials, PubMed, Consensus, bioRxiv); connected design MCPs **BioRender, Canva, HeyGen HyperFrames, SlidesGPT, Jam**; skills **theme-factory, canvas-design, brand-guidelines, pptx, docx, pdf, deep-research**. Fill *gaps*, don't re-suggest these.

## Step 2 — Search the catalogs
- **MCP connectors:** `mcp__mcp-registry__search_mcp_registry` across our needs — keywords like: scientific figures, design, slides, presentation, video, motion graphics, screen recording, voiceover / text-to-speech, diagram, data visualization, image generation, asset hosting, animation. Then `mcp__mcp-registry__suggest_connectors` to render **Connect** cards for the relevant, mostly-free ones.
- **Skills / plugins:** `mcp__skills__suggest_skills` + `mcp__plugins__search_plugins` (+ `suggest_plugin_install`) for design, data-viz, presentation, scientific-writing, and general craft skills. (If `search_plugins` output is huge, it's saved to a file — `grep` it for keywords.)
- **External craft skills (web search):** the addable catalog is limited, so also search **SkillsMP (skillsmp.com)**, **crossaitools**, **tasteskill.dev**, and the "**63 design skills for Claude**" collections for high-craft `SKILL.md` skills — especially the **Taste Skill** (anti-slop frontend design: real design systems, grid, phosphor icons, no purple-gradient/centered-hero/emoji slop) for the **repo landing page**. Third-party — always point to the **official source**.

## Step 3 — Curate + surface (render the install cards)
For each recommendation give: **name · what it does · free vs paid · where it helps (video / report / landing page / science) · install path**. Render the **Connect** (connectors) and **Add** (skills) cards so the user installs with one click. Be honest:
- Connectors require the **user** to click Connect + sign in (you can't OAuth for them).
- **You cannot create or install skills yourself** — you surface addable ones (Add card) or give manual `SKILL.md` install steps from the official source (Settings → Capabilities).
- No paid sign-ups or credentials without the user.

## Step 4 — Save the shortlist
Write `toolkit.md` in the folder: the curated list + one-line rationale + free/paid + install steps, as a durable reference. Group by **Science · Figures · Slides/Report · Video/Media · Landing-page craft**.

## Quality bar
Only surface tools that clearly earn their place for *this* submission. Prefer free. Flag free-tier limits (e.g., HeyGen/BioRender render/export caps). Recommend the smallest high-impact set, not a dump.
