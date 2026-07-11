"""build_video.py — assemble the silent demo cut from the rendered slides.

Subtle Ken-Burns zoom per slide + cross-dissolves between them, timed to the
voiceover script. 1920x1080 / 30fps / H.264. Output: deliverables/demo.mp4.
"""
import pathlib
import subprocess

FPS = 30
CF = 0.7  # crossfade seconds
# per-slide hold seconds (matched to the VO script word counts)
DUR = [7, 22, 24, 24, 22, 27, 22, 13]
FRAMES = pathlib.Path(__file__).parent / "frames"
OUT = pathlib.Path(__file__).parent.parent / "demo.mp4"

n = len(DUR)
inputs = []
for i in range(n):
    inputs += ["-loop", "1", "-t", str(DUR[i]), "-framerate", str(FPS),
               "-i", str(FRAMES / f"slide_{i}.png")]

fc = []
for i in range(n):
    # alternate a gentle zoom-in / zoom-out for rhythm
    if i % 2 == 0:
        z = "min(1.0+0.00055*on,1.055)"
    else:
        z = "max(1.055-0.00055*on,1.0)"
    fc.append(
        f"[{i}:v]scale=1920:1080,setsar=1,"
        f"zoompan=z='{z}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"s=1920x1080:fps={FPS},format=yuv420p[v{i}]"
    )

# xfade chain with cumulative offsets
prev = "v0"
L = DUR[0]
for i in range(1, n):
    off = round(L - CF, 3)
    out = f"x{i}"
    fc.append(f"[{prev}][v{i}]xfade=transition=fade:duration={CF}:offset={off}[{out}]")
    prev = out
    L = L + DUR[i] - CF

cmd = ["ffmpeg", "-y", "-hide_banner", *inputs,
       "-filter_complex", ";".join(fc),
       "-map", f"[{prev}]",
       "-c:v", "libx264", "-crf", "18", "-preset", "medium",
       "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(OUT)]

print(f"total duration ~ {round(L,1)}s")
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print(r.stderr[-2500:])
    raise SystemExit(r.returncode)
print("wrote", OUT, OUT.stat().st_size, "bytes")
