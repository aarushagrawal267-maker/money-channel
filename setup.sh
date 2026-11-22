#!/usr/bin/env bash
# Install everything the video pipeline needs in a fresh session.
set -euo pipefail
cd "$(dirname "$0")"
# Install for the exact python3 the pipeline runs with (pip3 can belong to a different Python),
# and make sure Pillow is built for it (a system copy for another version breaks rendering).
python3 -m pip install -q kokoro-onnx soundfile faster-whisper numpy google-api-python-client google-auth-oauthlib
python3 -m pip install -q --force-reinstall --no-deps pillow
python3 -c "import PIL.ImageFont, kokoro_onnx, faster_whisper, googleapiclient" || { echo "Setup check failed"; exit 1; }
mkdir -p models
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  [ -s "models/$f" ] || curl -sSL --max-time 600 -o "models/$f" \
    "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f"
done
echo "Setup complete."
