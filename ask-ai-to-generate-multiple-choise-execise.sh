#!/usr/bin/env bash
set -euo pipefail

exercise_directory="$1"

pi --model openrouter/deepseek/deepseek-v4.1-flash-1017 --print \
   "Create multiple choise exercise to exercises/${exercise_directory}/monivalinta.html from the text exercises/${exercise_directory}/teksti.md. Read instructions from MULTIPLE_CHOICE_TEMPLATE.md"
