import json, subprocess, pathlib
DUR = json.load(open("_remotion/public/durations.json"))
TR, LEAD, FPS = 18, 12, 30
# display-form captions, one per scene — single source of truth: _video/captions_v4.txt
CAPS = [l.strip() for l in pathlib.Path("_video/captions_v4.txt").read_text().splitlines() if l.strip()]
assert len(CAPS) == len(DUR), f"caption/scene count mismatch: {len(CAPS)} captions vs {len(DUR)} scenes"
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
pathlib.Path("brakepoint_video.vtt").write_text("\n".join(out))
print("wrote brakepoint_video.vtt with",len(cues),"cues; last cue ends", round(cues[-1][1],1),"s")
