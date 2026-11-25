#!/usr/bin/env bash
set -euo pipefail

script_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

exercise_directory="$1"

pi --model openrouter/deepseek/deepseek-v4.1-flash-1017 --mode json \
  "Create multiple choise exercise to exercises/${exercise_directory}/monivalinta.html from the text exercises/${exercise_directory}/teksti.md. Read instructions from MULTIPLE_CHOICE_TEMPLATE.md" |
  python3 "${script_directory}/format_pi_output.py"
