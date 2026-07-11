"""build_narrated.py — narrated demo cut: slides + Ken-Burns + crossfades + TTS VO.

Video: per-slide subtle zoom, cross-dissolved. Audio: each voiceover clip placed
on a common timeline at its slide's visual start (+ lead-in), summed. Perfectly
synced because both use the same cumulative xfade offsets. 1080p / 30fps / H.264 + AAC.
Output: deliverables/demo.mp4.
"""
import pathlib
import subprocess

FPS = 30
CF = 0.7          # crossfade seconds
PRE = 0.5         # lead-in silence before each slide's narration
POST = 1.0        # tail after narration (> CF, so speech ends before the dissolve)
HERE = pathlib.Path(__file__).parent
FRAMES = HERE / "frames"
AUDIO = HERE / "audio"
OUT = HERE.parent / "demo.mp4"


def dur(path: pathlib.Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(r.stdout.strip())


n = 8
tts = [dur(AUDIO / f"slide_{i}.mp3") for i in range(n)]
D = [PRE + tts[i] + POST for i in range(n)]

# cumulative xfade offsets + narration start times
start = [0.0] * n
L = D[0]
offsets = []
for i in range(1, n):
    offsets.append(round(L - CF, 3))
    start[i] = round(L - CF, 3)  # slide i first appears here (blend start)
    L = L + D[i] - CF
total = round(L, 2)

inputs = []
for i in range(n):
    inputs += ["-loop", "1", "-t", f"{D[i]:.3f}", "-framerate", str(FPS),
               "-i", str(FRAMES / f"slide_{i}.png")]
for i in range(n):
    inputs += ["-i", str(AUDIO / f"slide_{i}.mp3")]

fc = []
for i in range(n):
    z = "min(1.0+0.0005*on,1.05)" if i % 2 == 0 else "max(1.05-0.0005*on,1.0)"
    fc.append(f"[{i}:v]scale=1920:1080,setsar=1,"
              f"zoompan=z='{z}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
              f"s=1920x1080:fps={FPS},format=yuv420p[v{i}]")
prev = "v0"
for i in range(1, n):
    out = f"x{i}"
    fc.append(f"[{prev}][v{i}]xfade=transition=fade:duration={CF}:offset={offsets[i-1]}[{out}]")
    prev = out

# audio: place each VO at (start_i + PRE) on a common stereo timeline, sum (no overlap)
for i in range(n):
    ms = int(round((start[i] + PRE) * 1000))
    fc.append(f"[{n+i}:a]aresample=48000,aformat=channel_layouts=stereo,"
              f"adelay={ms}|{ms}[a{i}]")
amix_in = "".join(f"[a{i}]" for i in range(n))
fc.append(f"{amix_in}amix=inputs={n}:normalize=0:dropout_transition=0[amz]")
fc.append(f"[amz]apad,atrim=0:{total},alimiter=limit=0.98[aout]")

cmd = ["ffmpeg", "-y", "-hide_banner", *inputs,
       "-filter_complex", ";".join(fc),
       "-map", f"[{prev}]", "-map", "[aout]",
       "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
       "-t", f"{total}", str(OUT)]

print("per-slide hold (s):", [round(d, 1) for d in D])
print("narration starts (s):", [round(s + PRE, 1) for s in start])
print(f"total ~ {total}s ({int(total//60)}:{int(total%60):02d})")
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print(r.stderr[-3000:]); raise SystemExit(r.returncode)
print("wrote", OUT, OUT.stat().st_size, "bytes")
