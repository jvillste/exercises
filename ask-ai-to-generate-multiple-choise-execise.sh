#!/usr/bin/env bash
set -euo pipefail

exercise_directory="$1"

pi --model openrouter/deepseek/deepseek-v4.1-flash-1017 --print \
   "create multiple choise execise to exercises/${exercise_directory}/monivalinta.html from the text exercises/${exercise_directory}/teksti.md. Take a cue from mosaiikki-8-syksy. Use build_multiple_choise.py and "
