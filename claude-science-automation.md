# Driving Claude Science automatically & getting results back to the laptop
**Your setup:** Claude Science not installed yet · on Claude Max · goal = trigger analyses programmatically and collect results unattended.

---

## The key architectural fact (read first)
Claude Science is a **local desktop app** (macOS/Linux beta). It runs Python/R/shell in a sandbox on *your* machine, reads folders you grant, pulls from scientific databases via connectors, and **saves results as versioned artifacts with a full provenance record** (exact code + environment + plain-language description + the conversation). A background **reviewer agent** checks claims against what actually ran.

Two consequences for your goal:
1. **"Get the result back to the laptop" is already solved** — artifacts are written locally by design. The real problem is *triggering* runs and *collecting/organizing* outputs without babysitting.
2. **Claude Science is approval-gated** (you OK each new folder, network host, and remote job). That's great for safety but means the *app itself* is not a fully-headless server. For true unattended automation you drive the **same tools** through the **Claude Agent SDK**. There's no documented public headless API for the CS app today — verify in-app once installed.

So there are three tiers, and you'll likely use two of them.

---

## Tier A — Interactive Claude Science (use this for the science)
Fastest path to real results during the hackathon.
1. **Install** (do this Day 1): Max plan; macOS 13+ or Linux x64; ~5 GB free; Linux also needs `socat` + `bubblewrap ≥0.8` + user namespaces. Get it from Claude Science (beta).
2. **Grant the project folder** (`~/Claude Hackathon`) so artifacts land where the rest of your repo lives.
3. Describe the analysis in plain language; it writes/runs code in the sandbox and saves versioned artifacts + provenance.
4. **Save your pipeline as a reusable skill** — this is the repeatability unlock and directly answers the brief's "show us how Claude Science got you there."
5. **Compute backends:** local kernel, **Slurm over SSH**, or **Modal**. Point heavy jobs (single-cell, E-distance across the screen) at a cluster/Modal; artifacts still return to the local app.

**Best for:** the Perturb-seq analysis, QC, signature scoring, figures — the parts that need judgment and iteration.

---

## Tier B — Semi-automated Claude Science (repeatable, low-babysit)
Turn the interactive run into a re-runnable one:
- **Reusable skill** encapsulating audit → effects → gates → figures.
- **Pre-approve** the project folder, the specific network hosts (Open Targets, ChEMBL, etc.), and the remote compute *once*, so re-runs need minimal clicks.
- Re-invoke the skill on new inputs (e.g., a new shortlist, a swapped signature).

**Best for:** re-running the whole pipeline after a data-audit change or a signature swap, without rebuilding.

---

## Tier C — Headless Agent SDK (true unattended + scheduled)
This is what "control automatically to finish a task and get results back" really means. Build a small agent with the **Claude Agent SDK** — a *process* that observes, acts, and iterates to a goal — wired to the **same MCP connectors + skills + a code-execution tool**, run on a schedule, writing artifacts to `~/Claude Hackathon/outputs`.

**Perfect first target: the per-target dossier enrichment** (from `target-assessment-framework.md`). It's embarrassingly parallel, API-driven, and exactly your `$200-API` budget — ideal for unattended batch while you sleep.

### Reference architecture
```
~/Claude Hackathon/
  agent/
    run_dossiers.py        # Agent SDK entrypoint (headless)
    mcp_servers.json       # PubMed, Consensus, Solve Intelligence, Helix, LatchBio...
    skills/dossier/        # SKILL.md: how to fill the dossier schema
    prompts/dossier.md     # task spec + output contract (YAML schema)
  data/shortlist.csv       # input: gene list from the causal pipeline
  outputs/dossiers/        # output: <gene>.yaml + provenance + sources
  outputs/run_log.jsonl    # what ran, when, tokens, cost
```

### Skeleton (verify exact SDK signatures against current docs — shape is right)
```python
# run_dossiers.py — headless dossier enrichment
import csv, json, pathlib
from claude_agent_sdk import Agent  # see code.claude.com/docs agent-sdk

OUT = pathlib.Path("outputs/dossiers"); OUT.mkdir(parents=True, exist_ok=True)
shortlist = [r["gene"] for r in csv.DictReader(open("data/shortlist.csv"))]

agent = Agent(
    model_router={"extract": "claude-haiku-4-5", "reason": "claude-sonnet-5",
                  "synthesize": "claude-opus-4-8"},   # tier by difficulty
    mcp_servers="agent/mcp_servers.json",             # PubMed, patents, genomics...
    skills=["agent/skills/dossier"],
    tools=["code_execution", "web_fetch"],            # for Open Targets/ChEMBL/gnomAD APIs
    permission_mode="auto",                            # unattended; scope hosts tightly
)

for gene in shortlist:
    task = open("prompts/dossier.md").read().replace("{{GENE}}", gene)
    result = agent.run(task, output_dir=OUT)           # writes <gene>.yaml + sources
    (OUT / "run_log.jsonl").open("a").write(json.dumps(result.meta) + "\n")
```

### Scheduling / triggering it
- **cron / launchd** on the Mac: `0 * * * * cd ~/Claude\ Hackathon && python agent/run_dossiers.py`.
- **Or trigger from *this* Cowork app**: I can set up a **scheduled task** that runs the agent (or a wrapper) on a cadence and drops results into the project folder — say the word and I'll wire it.
- **Idempotence:** skip genes whose `<gene>.yaml` already exists so re-runs only fill gaps.

**Best for:** dossier enrichment, novelty/patent sweeps, literature refreshes, nightly re-scoring — anything API-shaped and parallel.

---

## Recommended split for *this* hackathon (solo, 6 days)
| Work | Tier | Why |
|---|---|---|
| Perturb-seq analysis, QC, figures, hero-target reasoning | **A** (interactive CS) | needs judgment + iteration; artifacts auto-saved & provenance-tracked (demo gold) |
| Whole-pipeline re-run after audit/signature change | **B** (CS skill) | repeatable without rebuild |
| Per-target dossier enrichment across the shortlist | **C** (Agent SDK, unattended) | parallel, API-driven, runs while you sleep; spends the $200 well |

**Compliance:** all of this is *new work built during the event* (fine), uses public data/tools (fine), and stays open-source. Keep the CS provenance artifacts and the agent's `run_log.jsonl` — they *are* the "how Claude Science got you there" evidence the brief asks for, and the reviewer-agent trail is a credibility signal for judges.

---

## Honest caveats
- No public *headless API for the CS app* is documented today; Tier C uses the **Agent SDK + MCP + skills** to reproduce the workflow unattended, not the app itself. Re-check once CS is installed — beta features move fast.
- CS's per-action approvals exist for safety; "fully unattended" always means *you pre-scoped the folders/hosts/compute it may touch*. Keep network scopes tight in `permission_mode="auto"`.
- Verify the Agent SDK class/method names, model IDs, and MCP-config format against the current docs before relying on the skeleton — the architecture is correct; the exact signatures may differ.

## Next actions I can take for you
- Install-readiness check + a Day-1 CS setup checklist.
- Scaffold the `agent/` folder above (real files) once you confirm which MCPs you've connected.
- Wire a scheduled task in this app to run the dossier agent and collect results into `~/Claude Hackathon/outputs`.
