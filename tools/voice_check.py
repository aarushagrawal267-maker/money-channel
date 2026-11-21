"""Catch AI-voice mispronunciations: transcribe the rendered voice track and diff it against the script.

Usage: python3 tools/voice_check.py SPEC.json AUDIO.wav [--model base.en]
Prints spans where what was heard differs from what was written. Expect some noise from
ASR itself (numbers, homophones); look for repeated or meaning-changing misses.
"""
import argparse, difflib, json, os, re, subprocess, sys, tempfile
import soundfile as sf

NUM = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six",
       "7": "seven", "8": "eight", "9": "nine", "10": "ten"}


def norm(text):
    text = text.lower().replace("’", "'").replace("-", " ")
    words = re.findall(r"[a-z0-9']+", text)
    return [NUM.get(w, w) for w in words]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("audio"); ap.add_argument("--model", default="base.en")
    a = ap.parse_args()
    from faster_whisper import WhisperModel
    spec = json.load(open(a.spec))
    script = norm(" ".join(s["say"] for s in spec["scenes"]))
    with tempfile.TemporaryDirectory() as td:
        a16 = os.path.join(td, "a16.wav")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", a.audio, "-ar", "16000", "-ac", "1", a16], check=True)
        audio, _ = sf.read(a16, dtype="float32")
    segs, _ = WhisperModel(a.model, device="cpu", compute_type="int8").transcribe(audio, beam_size=5)
    heard = norm(" ".join(s.text for s in segs))
    sm = difflib.SequenceMatcher(None, script, heard, autojunk=False)
    issues = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        issues += 1
        ctx = " ".join(script[max(0, i1 - 4):i1])
        print(f"  ...{ctx} [script: {' '.join(script[i1:i2]) or '-'}] [heard: {' '.join(heard[j1:j2]) or '-'}]")
    print(f"{spec['id']}: match {sm.ratio():.1%}, {issues} differing spans")


if __name__ == "__main__":
    main()
