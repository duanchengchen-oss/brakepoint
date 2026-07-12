"""gen_tts.py — voiceover clips via Azure AI Speech (SSML expression) with edge-tts fallback.

Azure Neural TTS is the SAME voice family as edge-tts BUT adds expression styles
(`mstts:express-as style='narration-professional'`) + prosody control — which makes
it read like a documentary narrator instead of a flat, "AI-sounding" clip. Auth is
the Azure AI Services key in $ANTHROPIC_FOUNDRY_API_KEY against the resource's
`/tts/cognitiveservices/v1` endpoint. If the key is absent, we fall back to edge-tts
so the repo still builds.

Gene/acronym names are respelled so the neural voice says them correctly (verified
by round-tripping each clip through Whisper):
  SMAD3 -> "SMAD three"  CRISPRi -> "CRISPR interference"  DGKA -> "DGK-alpha"
  CBLB -> "C B L B"      UBASH3A -> "UBASH three A"        CD4/CD5 -> "CD four/five"
Run `python gen_tts.py` to (1) synthesize, (2) transcribe-verify, (3) print
per-clip durations for durations.json, and (4) copy into the Remotion public dir.
"""
import asyncio
import html
import os
import pathlib
import shutil
import subprocess
import urllib.request

OUT = pathlib.Path(__file__).parent / "audio"
REMOTION_PUB = pathlib.Path(__file__).parent.parent / "_remotion" / "public" / "audio"
OUT.mkdir(exist_ok=True)

# --- Azure AI Speech config (preferred) ---
AZ_KEY = os.environ.get("ANTHROPIC_FOUNDRY_API_KEY", "")
AZ_ENDPOINT = "https://aif-hk-bioinfo-research.cognitiveservices.azure.com/tts/cognitiveservices/v1"
VOICE = "en-US-AndrewMultilingualNeural"   # warm, natural; supports expression styles
STYLE = "narration-professional"           # documentary-narrator delivery (the "not AI" fix)
RATE = "-3%"                                # a touch measured
FMT = "audio-48khz-192kbitrate-mono-mp3"   # high quality
EDGE_RATE = "-4%"                           # fallback only

# Scene order: 0 Title · 1 Question · 2 Provenance · 3 Significance · 4 MapScene
# 5 VsTraditional · 6 Method · 7 Validation(CBLB) · 8 Brakes(honesty) · 9 Close
VO = [
 "Checkpoint immunotherapy works by releasing the brakes on a T cell. So we went looking for those brakes — genome-wide. This is Brakepoint, built with Claude Science.",
 "Those brakes matter beyond checkpoint therapy — they also throttle engineered CAR-T. So across the genome, which genes are the brakes — which knockdowns push a human T cell toward a stronger effector state?",
 "We started from a genome-scale CRISPR interference screen: over twelve thousand gene knockdowns, across two-point-six million primary human CD four T cells, from the Gladstone Institutes. Two donors, out of an intended four.",
 "How do you find the brakes in twelve thousand knockdowns? The reflex is to rank by significance — but at two million cells that breaks down: over ninety-seven percent of the tested knockdowns clear the bar. So we rank by causal effect size instead.",
 "But effect size alone still points at the wrong genes — the biggest hits are the cell's own signaling machinery. So we add what a magnitude ranking leaves out: direction — toward the effector program, or away. Now the machinery falls away, and the candidate brakes rise into view.",
 "And that's the edge. Differential expression finds correlations — not what to drug. Genetics points to a locus, rarely a direction. We measure what a knockdown actually does, and which way it pushes — then weigh it against genetics and the clinic.",
 "From that map, five prior-informed candidates: C B L B, CD five, DGK-alpha, SMAD three, and UBASH three A — each scored across seven lines of evidence, from causal effect and direction to human genetics and clinical precedent.",
 "Our lead is C B L B. It's a natural off-switch for T-cell activation, and inhibitors are already in early-phase trials. Its genetics point the same way, and it lands in our brake quadrant. CD five and DGK-alpha come next — and both hold up across donors.",
 "And we're honest about what two donors can support. CD five and DGK-alpha hold up in both; the other three ride on one donor. As a group, known brakes aren't significantly enriched — so this is a ranked shortlist for the full cohort, a hypothesis to test, not a finished answer.",
 "Every number here traces back to versioned code — and to a self-check that caught a real bias in our effect-size code before it reached a figure. Open source; every figure regenerates with one command. This is Brakepoint, built with Claude Science.",
]

CHECKS = {
 3: ["significance", "effect", "ninety"],
 4: ["machinery", "direction", "effector"],
 5: ["differential", "genetics", "direction"],
 6: ["cblb", "cd5", "dgkalpha", "smad3", "ubash"],
 7: ["cblb", "trials", "cd5", "dgkalpha"],
 8: ["cd5", "dgkalpha", "shortlist"],
 9: ["code", "bias", "figure"],
}


def _norm(s: str) -> str:
    return "".join(c for c in s.lower() if c.isalnum())


def _ssml(text: str) -> str:
    return (f"<speak version='1.0' xml:lang='en-US' xmlns:mstts='http://www.w3.org/2001/mstts'>"
            f"<voice name='{VOICE}'><mstts:express-as style='{STYLE}'>"
            f"<prosody rate='{RATE}'>{html.escape(text)}</prosody>"
            f"</mstts:express-as></voice></speak>")


def _azure(text: str, path: pathlib.Path) -> None:
    req = urllib.request.Request(
        AZ_ENDPOINT, data=_ssml(text).encode("utf-8"), method="POST",
        headers={"Ocp-Apim-Subscription-Key": AZ_KEY, "Content-Type": "application/ssml+xml",
                 "X-Microsoft-OutputFormat": FMT, "User-Agent": "brakepoint"})
    with urllib.request.urlopen(req, timeout=40) as r:
        path.write_bytes(r.read())


async def _synth() -> None:
    if AZ_KEY:
        for i, text in enumerate(VO):
            _azure(text, OUT / f"slide_{i}.mp3")
            print("wrote (azure)", f"slide_{i}.mp3")
    else:
        import edge_tts
        for i, text in enumerate(VO):
            await edge_tts.Communicate(text, VOICE, rate=EDGE_RATE).save(str(OUT / f"slide_{i}.mp3"))
            print("wrote (edge fallback)", f"slide_{i}.mp3")


def _dur(p: pathlib.Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(p)],
        capture_output=True, text=True).stdout.strip()
    return float(out)


def _verify_and_report() -> None:
    import mlx_whisper
    LEAD, TAIL, FPS = 12, 36, 30
    durs, all_ok = [], True
    for i, _ in enumerate(VO):
        p = OUT / f"slide_{i}.mp3"; d = _dur(p)
        durs.append(LEAD + int(d * FPS + 0.999) + TAIL)
        r = mlx_whisper.transcribe(str(p), path_or_hf_repo="mlx-community/whisper-small.en-mlx")
        heard = _norm(r["text"])
        miss = [k for k in CHECKS.get(i, []) if _norm(k) not in heard]
        if miss:
            all_ok = False
        print(f"[{'OK ' if not miss else 'FAIL'}] slide_{i}  {d:5.2f}s  missing={miss}")
        if miss:
            print(f"        heard: {r['text'].strip()!r}")
    print("\nDUR =", durs, " (total frames:", sum(durs), "= %.1fs)" % (sum(durs) / FPS))
    print("PRONUNCIATION QA:", "ALL PASS" if all_ok else "REVIEW FAILURES ABOVE")


def _copy_out() -> None:
    REMOTION_PUB.mkdir(parents=True, exist_ok=True)
    for old in REMOTION_PUB.glob("slide_*.mp3"):
        old.unlink()
    for i in range(len(VO)):
        shutil.copy(OUT / f"slide_{i}.mp3", REMOTION_PUB / f"slide_{i}.mp3")
    print("copied", len(VO), "clips ->", REMOTION_PUB, "(engine:", "azure)" if AZ_KEY else "edge)")


if __name__ == "__main__":
    asyncio.run(_synth())
    _verify_and_report()
    _copy_out()
