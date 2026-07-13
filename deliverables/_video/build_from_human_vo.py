"""build_from_human_vo.py — swap in a human voiceover and rebuild the demo in one step.

Drop your recordings in deliverables/_video/human_vo/ as slide_0..slide_10
(.mp3/.m4a/.wav/.aac), following RECORD_SCRIPT.md, then run this. It normalizes each
clip, recomputes the per-scene frame timing, rewrites durations.json, regenerates the
captions (demo.vtt), renders the Remotion video, and copies it to demo.mp4 — no other
edits needed. (This is the human-voice path; gen_tts.py is the Azure-TTS path.)
"""
import glob
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
HUMAN = HERE / "human_vo"
REMOTION = HERE.parent / "_remotion"
PUB_AUDIO = REMOTION / "public" / "audio"
DUR_JSON = REMOTION / "public" / "durations.json"
N = 11
LEAD, TAIL, FPS, TR = 12, 18, 30, 18
TEMPO = 1.07  # gentle, near-imperceptible time-tighten so the 11-scene cut stays < 3:00
EXTS = (".mp3", ".m4a", ".wav", ".aac", ".flac", ".ogg")


def _find(i: int):
    for e in EXTS:
        p = HUMAN / f"slide_{i}{e}"
        if p.exists():
            return p
    return None


def _dur(p: pathlib.Path) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(p)],
        capture_output=True, text=True).stdout.strip())


def main() -> None:
    missing = [i for i in range(N) if _find(i) is None]
    if missing:
        print(f"Missing recordings for slides {missing} in {HUMAN}/ .")
        print("Record slide_0..slide_10 (see RECORD_SCRIPT.md), then re-run.")
        sys.exit(1)

    PUB_AUDIO.mkdir(parents=True, exist_ok=True)
    for old in PUB_AUDIO.glob("slide_*.mp3"):
        old.unlink()
    durs = []
    for i in range(N):
        src = _find(i)
        out = PUB_AUDIO / f"slide_{i}.mp3"
        # normalize loudness + resample to a clean 48k mono mp3
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-af",
                        f"loudnorm=I=-16:TP=-1.5:LRA=11,atempo={TEMPO}", "-ar", "48000", "-ac", "1",
                        "-b:a", "192k", str(out), "-y"], check=True)
        d = _dur(out)
        durs.append(LEAD + int(d * FPS + 0.999) + TAIL)
        print(f"slide_{i}: {src.name}  {d:5.2f}s -> {durs[-1]} frames")

    DUR_JSON.write_text(json.dumps(durs) + "\n")
    total = sum(durs) - TR * (N - 1)
    print(f"durations.json updated. Video length = {total/FPS:.1f}s "
          f"({int(total/FPS//60)}:{int(total/FPS%60):02d})")

    # regenerate captions to the new timing
    subprocess.run([sys.executable, str(HERE / "gen_vtt.py")], check=True)

    # render + install (SCALE=2 → 3840x2160 4K; CRF lower = higher quality; both env-overridable)
    import os
    scale = os.environ.get("SCALE", "2")
    crf = os.environ.get("CRF", "19")
    conc = os.environ.get("CONC", "4")
    print(f"rendering (Remotion) scale={scale} crf={crf}…")
    subprocess.run(["npx", "remotion", "render", "BrakepointVideo", "out/video.mp4",
                    "--scale", scale, "--crf", crf, "--concurrency", conc], cwd=REMOTION, check=True)
    shutil_out = REMOTION / "out" / "video.mp4"
    (HERE.parent / "brakepoint_video.mp4").write_bytes(shutil_out.read_bytes())
    print("done -> deliverables/brakepoint_video.mp4 (human voiceover)")


if __name__ == "__main__":
    main()
