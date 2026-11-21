#!/usr/bin/env bash
# Install everything the video pipeline needs in a fresh session.
set -euo pipefail
cd "$(dirname "$0")"
pip3 install -q kokoro-onnx soundfile faster-whisper numpy pillow google-api-python-client google-auth-oauthlib
mkdir -p models
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  [ -s "models/$f" ] || curl -sSL --max-time 600 -o "models/$f" \
    "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f"
done
echo "Setup complete."
