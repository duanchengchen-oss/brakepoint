"""gen_tts.py — generate the voiceover clips with edge-tts (en-GB-SoniaNeural)."""
import asyncio
import pathlib

import edge_tts

VOICE = "en-GB-SoniaNeural"
RATE = "-4%"   # a touch slower = clearer
OUT = pathlib.Path(__file__).parent / "audio"
OUT.mkdir(exist_ok=True)

VO = [
 "What if the biggest hit in your screen is the worst drug target? This is Brakepoint — a signed causal map of T-cell function, built with Claude Science.",
 "Our question: in human T cells, which knockdowns make the cell a better effector, and which just break it? The better-effector genes are the brakes — release them, and you boost immunity. But they hide among twelve thousand knockdowns, across two and a half million cells.",
 "Everything here was built with Claude Science, and every number carries its provenance. Each result is a versioned artifact — its code, its environment, the conversation behind it. A background reviewer checks every claim against what actually ran; it caught a real statistical bug before it reached a figure. The heavy compute runs on a DGX Spark — the map over two-point-six million cells, in forty seconds.",
 "The method has two axes. Effect size — an energy distance — tells you how much a knockdown changes the cell. But magnitude can't separate a drug target from essential machinery; both land far from control. So we add direction: a per-cell score. Positive, the knockdown pushes cells toward the effector program — a brake. Negative, it's required machinery.",
 "And the map validates itself. Unsupervised, eight of the nine largest effects are the T-cell-receptor module — ZAP70, the CD3 complex, LAT. The direction axis flags fourteen of the top fifteen as machinery, not targets — and both donors agree, every time. That machinery result is the load-bearing one.",
 "This is the map. Effect size across the bottom, direction up the side. In teal, the largest, most consistent effects — the machinery: knock it down, you cripple the cell. Up top, in amber, the sparse positive quadrant: knockdowns that enhance effector function — the therapeutic hypothesis space a magnitude-only ranking would never have looked at.",
 "And we report that quadrant honestly. Known brakes like CD5 and DGKA do land there, donor-consistent — a consistency check. But at two donors it isn't yet enriched for known brakes, and its strongest raw hits include likely artifacts. So the positive side is a prioritized hypothesis space for the full cohort; the validated result is the machinery axis.",
 "Fully open source — fixed seeds, one command to reproduce. The whole map, from raw cells to this figure, built with Claude Science.",
]


async def main() -> None:
    for i, text in enumerate(VO):
        out = OUT / f"slide_{i}.mp3"
        await edge_tts.Communicate(text, VOICE, rate=RATE).save(str(out))
        print("wrote", out.name)


if __name__ == "__main__":
    asyncio.run(main())
