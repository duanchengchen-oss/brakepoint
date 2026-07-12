"""gen_tts.py — voiceover clips (edge-tts, natural conversational voice)."""
import asyncio
import pathlib

import edge_tts

VOICE = "en-US-AndrewMultilingualNeural"  # warm, confident, natural
RATE = "-3%"
OUT = pathlib.Path(__file__).parent / "audio"
OUT.mkdir(exist_ok=True)

VO = [
 "Releasing the brakes on a T cell is how checkpoint immunotherapy works. This is Brakepoint — druggable-brake discovery from a 2.6-million-cell screen, built with Claude Science.",
 "Checkpoint blockade works by releasing the brakes on T cells; CAR-T engineers T cells to attack. Both point to the same prize. So we asked: across the genome, which druggable genes are the brakes — which knockdowns push a human T cell toward a stronger effector state?",
 "We started from a genome-scale CRISPR-interference screen — over twelve thousand gene knockdowns, across 2.6 million primary human CD4 T cells, from the Gladstone Institutes. Two donors, of an intended four.",
 "Ranking by effect size alone points at the wrong genes: the biggest hits are the cell's own essential signaling machinery. So we added a direction-of-effect axis — an 8-hour transcriptional readout. Now the machinery drops to the bottom, and the candidate brakes rise to the top.",
 "From that map, five candidate brakes — CBLB, CD5, DGKA, SMAD3, and UBASH3A — each scored across seven axes of convergent evidence: causal effect, direction, donor consistency, viability, druggability, human genetics, and clinical precedent.",
 "Our lead is CBLB. Its inhibitors are already in early-phase trials, it carries an autoimmune genetic association consistent with a T-cell brake role, and it sits squarely in our brake quadrant. CD5 and DGKA follow — consistent across both donors, with external tractability evidence.",
 "And we report it honestly. With just two donors, CD5 and DGKA hold up in both; CBLB and the higher-effect candidates are driven by one, and known brakes show no significant enrichment as a group. So this is a prioritized shortlist for the full four-donor cohort — a hypothesis to validate, not a finished target list.",
 "Every candidate traces back to code — open source, one command to reproduce, built with Claude Science.",
]


async def main() -> None:
    for i, text in enumerate(VO):
        await edge_tts.Communicate(text, VOICE, rate=RATE).save(str(OUT / f"slide_{i}.mp3"))
        print("wrote", f"slide_{i}.mp3")


if __name__ == "__main__":
    asyncio.run(main())
