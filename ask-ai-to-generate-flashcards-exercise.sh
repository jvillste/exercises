#!/usr/bin/env bash
set -euo pipefail

script_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

exercise_directory="$1"

pi --model openrouter/deepseek/deepseek-v4.1-flash-1017 --mode json \
  "Create flash card exercise to exercises/${exercise_directory}/flashcards.html from the text exercises/${exercise_directory}/teksti.md. Read instructions from FLASHCARDS_TEMPLATE.md" |
  python3 "${script_directory}/format_pi_output.py"
