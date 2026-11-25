#!/usr/bin/env bash
set -euo pipefail

script_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

exercise_directory="$1"

pi --model omlx/Qwen3.6-35B-A3B-oQ4e-mtp --mode json \
  "Extract text from photos in exercies/${exercise_directory} to exercises/${exercise_directory}/teksti.md. Use the read tool to read the images. Do not use OCR." |
  python3 "${script_directory}/format_pi_output.py"
