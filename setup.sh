#!/usr/bin/env bash
# Install everything the video pipeline needs in a fresh session.
set -euo pipefail
cd "$(dirname "$0")"
# Install for the exact python3 the pipeline runs with (pip3 can belong to a different Python),
# and make sure Pillow is built for it (a system copy for another version breaks rendering).
python3 -m pip install -q -r requirements.txt
python3 -m pip install -q --force-reinstall --no-deps pillow
python3 -c "import PIL.ImageFont, kokoro_onnx, faster_whisper, googleapiclient" || { echo "Setup check failed"; exit 1; }
mkdir -p models
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  # re-download if missing or suspiciously small (a failed or HTML error download)
  if [ ! -s "models/$f" ] || [ "$(stat -c %s "models/$f")" -lt 10000000 ]; then
    curl -fsSL --max-time 900 -o "models/$f.part" \
      "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f" && mv "models/$f.part" "models/$f"
  fi
  [ "$(stat -c %s "models/$f" 2>/dev/null || echo 0)" -ge 10000000 ] || { echo "Model download failed: $f"; exit 1; }
done
ls /usr/share/fonts/opentype/inter/InterDisplay-Black.otf >/dev/null 2>&1 || \
  { apt-get install -y -q fonts-inter >/dev/null 2>&1 || echo "WARNING: Inter fonts missing (apt install fonts-inter)"; }
echo "Setup complete."
