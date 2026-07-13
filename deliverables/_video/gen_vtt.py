import json, subprocess, pathlib
DUR = json.load(open("_remotion/public/durations.json"))
TR, LEAD, FPS = 18, 12, 30
# display-form captions, one per scene (matches demo_script.md)
CAPS = [
 "Checkpoint drugs work by releasing the brakes on a T cell — but they help only a minority of patients, because only a handful of those brakes are drugged. So we went looking for the rest, genome-wide. This is Brakepoint, built with Claude Science.",
 "Those brakes matter beyond checkpoint therapy — they also throttle engineered CAR-T. So across the genome: which genes are the brakes? And which knockdowns push a human T cell toward a stronger effector state?",
 "We started from a genome-scale CRISPR-interference screen: over twelve thousand gene knockdowns, across 2.6 million primary human CD4 T cells, from the Gladstone Institutes. Two donors, out of an intended four.",
 "How do you find the brakes in twelve thousand knockdowns? The reflex is to rank by significance — but at two million cells, that breaks down: over 97% of the tested knockdowns clear the bar. So we rank by causal effect size instead.",
 "But effect size alone still points at the wrong genes — the biggest hits are the cell's own signaling machinery. So we add what a magnitude ranking leaves out: direction — toward the effector program, or away. Now the machinery falls away, and the candidate brakes rise into view.",
 "And this isn't a static picture. Every one of the eleven thousand that passed our testing threshold is here to explore — search any gene, hover any point, and read its causal effect and its direction. It's the real leaderboard, live.",
 "And that's the edge. Differential expression finds correlations — not what to drug. Genetics points to a locus, rarely a direction. We measure what a knockdown actually does, and which way it pushes — then weigh it against genetics and the clinic.",
 "From that map, five prior-informed candidates: CBLB, CD5, DGKA, SMAD3, and UBASH3A — each scored across seven lines of evidence, from causal effect and direction to human genetics and clinical precedent.",
 "Our lead is CBLB. It's a natural off-switch for T-cell activation, and inhibitors are already in early-phase trials. Its genetics point the same way, and it lands in our brake quadrant. CD5 and DGKA come next.",
 "We're honest about what two donors can support. CD5 and DGKA hold up in both; the other three ride on one donor. Known brakes aren't significantly enriched — but that's a two-donor power limit, not a null result. So this stays a ranked shortlist for the full cohort, a hypothesis to test, not a finished answer.",
 "Five candidate brakes, led by CBLB — a target the industry already drugs, so recovering it validates our method. Every figure regenerates from cached outputs with one command, checked against a real bug we caught ourselves. Explore the live map, clone the code, and help find the brakes today's drugs still miss. Built with Claude Science.",
]
def adur(i):
    o=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",f"_remotion/public/audio/slide_{i}.mp3"],capture_output=True,text=True).stdout.strip()
    return float(o)
def ts(sec):
    h=int(sec//3600); m=int((sec%3600)//60); s=sec%60
    return f"{h:02d}:{m:02d}:{s:06.3f}"
import re
def sents(t):
    # split into sentences (keep terminal punctuation), so captions advance in
    # short readable lines instead of one long block per scene
    parts = re.findall(r'[^.?!]+[.?!]+(?:\s|$)|\S[^.?!]*$', t)
    return [s.strip() for s in parts if s.strip()]

cues=[]
for i,txt in enumerate(CAPS):
    gstart = sum(DUR[:i]) - TR*i          # scene global start (transition-adjusted), frames
    a_start = (gstart + LEAD)/FPS
    a_end = a_start + adur(i)
    ss = sents(txt)
    tot = sum(len(s) for s in ss) or 1
    t = a_start
    for s in ss:                          # allocate time proportional to sentence length
        seg = (a_end - a_start) * (len(s)/tot)
        cues.append((t, min(a_end, t+seg), s))
        t += seg
out=["WEBVTT",""]
for k,(a,b,t) in enumerate(cues):
    out.append(str(k+1)); out.append(f"{ts(a)} --> {ts(b)} line:88% align:center"); out.append(t); out.append("")
pathlib.Path("demo.vtt").write_text("\n".join(out))
print("wrote demo.vtt with",len(cues),"cues; last cue ends", round(cues[-1][1],1),"s")
