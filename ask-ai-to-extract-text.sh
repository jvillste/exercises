#!/usr/bin/env bash
set -euo pipefail

exercise_directory="$1"

pi --model omlx/Qwen3.6-35B-A3B-oQ4e-mtp --print \
  "Extract text from photos in exercies/${exercise_directory} to exercises/${exercise_directory}/teksti.md. Use the read tool to read the images. Do not use OCR."
