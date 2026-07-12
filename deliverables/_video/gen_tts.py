"""gen_tts.py — voiceover clips (edge-tts, natural conversational voice)."""
import asyncio
import pathlib

import edge_tts

VOICE = "en-US-AndrewMultilingualNeural"  # warm, confident, natural — replaces robotic Sonia
RATE = "-3%"
OUT = pathlib.Path(__file__).parent / "audio"
OUT.mkdir(exist_ok=True)

VO = [
 "A T cell's brakes are its best drug targets. This is Brakepoint — druggable-brake discovery from a two-and-a-half-million-cell screen, built with Claude Science.",
 "The most powerful immunotherapies — checkpoint blockade, CAR-T — all work by releasing brakes on T cells. So we asked a simple question: across the entire genome, which druggable genes are those brakes? Which knockdowns make a human T cell a stronger effector?",
 "We started from a genome-scale CRISPR-interference screen — twelve thousand gene knockdowns, across two and a half million primary human CD4 T cells, from the Gladstone Institutes.",
 "Ranking by effect size alone points at the wrong genes: the biggest hits are the cell's own essential signaling machinery. So we added a direction-of-effect axis. Now the machinery drops to the bottom, and the drug-relevant brakes rise to the top. This map is our discovery engine.",
 "From that map, a shortlist of five druggable brakes — each scored across seven axes of convergent evidence: causal effect, direction, donor consistency, druggability, human genetics, and clinical precedent.",
 "Our lead is CBLB — a brake that's already a drug. Two oral CBL-B inhibitors are in trials, losing it causes autoimmunity in people, and it sits squarely in our brake quadrant. CD5 and DGKA follow — both consistent across donors, both clinically tractable.",
 "And we report it honestly. With two donors, CD5 and DGKA hold up in both; CBLB and the higher-effect candidates are driven by one donor, and known brakes aren't yet enriched as a group. So this is a prioritized shortlist for the full cohort — not a finished target list.",
 "Every target traces back to code — open source, one command to reproduce, built with Claude Science.",
]


async def main() -> None:
    for i, text in enumerate(VO):
        await edge_tts.Communicate(text, VOICE, rate=RATE).save(str(OUT / f"slide_{i}.mp3"))
        print("wrote", f"slide_{i}.mp3")


if __name__ == "__main__":
    asyncio.run(main())
