#!/usr/bin/env python3
"""Build a standalone HTML multiple-choice exercise app from a JSON file.

Usage:
    python build_multiple_choice.py questions.json -o quiz.html -t "My topic"

The JSON file may be either:
  * a list of question objects, or
  * an object with a "questions", "exercises" or "cards" key containing the list.

Each question can use these keys (aliases in parentheses):
  * question:    question, front, text, q
  * options:     options, choices, vaihtoehdot
  * correct:     correct, correct_index, answer_index, oikea
  * explanation: explanation, perustelu, selitys

The correct answer is a zero-based index into the options list. A question must
have a text, at least two options and a valid correct index. The explanation is
optional. The generated HTML embeds the questions, so it works when opened
directly from disk.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

DEFAULT_TEMPLATE = Path(__file__).resolve().parent / "multiple_choice_template.html"


def first_present(mapping: dict, keys: tuple[str, ...]) -> str:
    for key in keys:
        value = mapping.get(key)
        if value is not None and str(value).strip():
            return str(value)
    return ""


def first_present_raw(mapping: dict, keys: tuple[str, ...]) -> object:
    for key in keys:
        value = mapping.get(key)
        if value is not None:
            return value
    return None


def normalize_question(raw: object) -> dict | None:
    if not isinstance(raw, dict):
        return None

    question = first_present(raw, ("question", "front", "text", "q"))
    options_raw = first_present_raw(raw, ("options", "choices", "vaihtoehdot"))
    correct_raw = first_present_raw(raw, ("correct", "correct_index", "answer_index", "oikea"))
    explanation = first_present(raw, ("explanation", "perustelu", "selitys"))

    if not question or not isinstance(options_raw, list):
        return None

    options: list[str] = []
    for option in options_raw:
        if isinstance(option, (dict, list)) or option is None:
            return None
        text = str(option).strip()
        if not text:
            return None
        options.append(text)

    if len(options) < 2:
        return None

    if isinstance(correct_raw, bool):
        return None

    try:
        correct = int(str(correct_raw).strip())
    except (TypeError, ValueError):
        return None

    if not 0 <= correct < len(options):
        return None

    normalized: dict = {
        "question": question,
        "options": options,
        "correct": correct,
    }
    if explanation:
        normalized["explanation"] = explanation
    return normalized


def load_questions(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)

    if isinstance(data, dict):
        for key in ("questions", "exercises", "cards"):
            if key in data:
                data = data[key]
                break

    if not isinstance(data, list):
        raise ValueError(
            "JSON root must be a list of questions or an object with a "
            "'questions', 'exercises' or 'cards' list."
        )

    questions: list[dict] = []
    skipped = 0
    for raw in data:
        question = normalize_question(raw)
        if question is None:
            skipped += 1
            continue
        questions.append(question)

    if skipped:
        print(
            f"Skipped {skipped} question(s) without a text, at least two options "
            "or a valid correct index.",
            file=sys.stderr,
        )
    if not questions:
        print("Warning: no usable questions found in the JSON file.", file=sys.stderr)

    return questions


def safe_json_for_script(questions: list[dict]) -> str:
    """Return JSON that cannot accidentally close or escape the surrounding <script> tag."""
    payload = json.dumps(questions, ensure_ascii=False, indent=2)
    payload = payload.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    payload = payload.replace("<!--", "<\\u0021--")
    return payload.replace("</", "<\\/")


def render_template(template: str, title: str, questions: list[dict]) -> str:
    """Replace template placeholders in a single pass without rescanning."""
    replacements = {
        "__QUIZ_TITLE__": html.escape(title),
        "__QUIZ_JSON__": safe_json_for_script(questions),
    }
    pattern = re.compile("|".join(re.escape(placeholder) for placeholder in replacements))
    return pattern.sub(lambda match: replacements[match.group(0)], template)


def build(template_path: Path, questions: list[dict], title: str, output_path: Path) -> None:
    template = template_path.read_text(encoding="utf-8")

    if "__QUIZ_JSON__" not in template or "__QUIZ_TITLE__" not in template:
        raise ValueError(
            f"Template {template_path} must contain both "
            "__QUIZ_TITLE__ and __QUIZ_JSON__ placeholders."
        )

    rendered = render_template(template, title, questions)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a standalone HTML multiple-choice exercise app from JSON."
    )
    parser.add_argument("input", type=Path, help="Path to the questions JSON file.")
    parser.add_argument("-o", "--output", type=Path, help="Output HTML file (default: <input>.html).")
    parser.add_argument("-t", "--title", default=None, help="Title shown in the HTML page.")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE, help="HTML template file.")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: input file not found: {args.input}", file=sys.stderr)
        return 1

    output_path = args.output or args.input.with_suffix(".html")
    title = args.title or args.input.stem.replace("_", " ").replace("-", " ").title()

    try:
        questions = load_questions(args.input)
        build(args.template, questions, title, output_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Built {output_path} with {len(questions)} question(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
