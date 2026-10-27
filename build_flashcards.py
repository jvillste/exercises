#!/usr/bin/env python3
"""Build a standalone HTML flashcard app from a JSON file.

Usage:
    python build_flashcards.py cards.json -o flashcards.html -t "My topic"

The JSON file may be either:
  * a list of card objects, or
  * an object with a "cards" key containing the list.

Each card can use these keys (aliases in parentheses):
  * image:    image, image_file_name, img
  * question: question, front, text, q
  * answer:   answer, back, correct_answer, a

A card must have an answer and either an image or a question. The generated
HTML embeds the cards, so it works when opened directly from disk.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

DEFAULT_TEMPLATE = Path(__file__).resolve().parent / "flashcards_template.html"


def first_present(mapping: dict, keys: tuple[str, ...]) -> str:
    for key in keys:
        value = mapping.get(key)
        if value is not None and str(value).strip():
            return str(value)
    return ""


def normalize_card(raw: object) -> dict[str, str] | None:
    if not isinstance(raw, dict):
        return None

    image = first_present(raw, ("image", "image_file_name", "img"))
    question = first_present(raw, ("question", "front", "text", "q"))
    answer = first_present(raw, ("answer", "back", "correct_answer", "a"))

    if not answer:
        return None

    if not image and not question:
        return None

    card: dict[str, str] = {}
    if image:
        card["image"] = image
    if question:
        card["question"] = question
    card["answer"] = answer
    return card


def load_cards(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)

    if isinstance(data, dict):
        data = data.get("cards", data)

    if not isinstance(data, list):
        raise ValueError("JSON root must be a list of cards or an object with a 'cards' list.")

    cards: list[dict[str, str]] = []
    skipped = 0
    for raw in data:
        card = normalize_card(raw)
        if card is None:
            skipped += 1
            continue
        cards.append(card)

    if skipped:
        print(f"Skipped {skipped} card(s) without an answer or without a front side.", file=sys.stderr)
    if not cards:
        print("Warning: no usable cards found in the JSON file.", file=sys.stderr)

    return cards


def safe_json_for_script(cards: list[dict[str, str]]) -> str:
    """Return JSON that cannot accidentally close or escape the surrounding <script> tag."""
    payload = json.dumps(cards, ensure_ascii=False, indent=2)
    payload = payload.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    payload = payload.replace("<!--", "<\\u0021--")
    return payload.replace("</", "<\\/")


def render_template(template: str, title: str, cards: list[dict[str, str]]) -> str:
    """Replace template placeholders in a single pass without rescanning."""
    replacements = {
        "__FLASHCARDS_TITLE__": html.escape(title),
        "__FLASHCARDS_JSON__": safe_json_for_script(cards),
    }
    pattern = re.compile("|".join(re.escape(placeholder) for placeholder in replacements))
    return pattern.sub(lambda match: replacements[match.group(0)], template)


def build(template_path: Path, cards: list[dict[str, str]], title: str, output_path: Path) -> None:
    template = template_path.read_text(encoding="utf-8")

    if "__FLASHCARDS_JSON__" not in template or "__FLASHCARDS_TITLE__" not in template:
        raise ValueError(
            f"Template {template_path} must contain both "
            "__FLASHCARDS_TITLE__ and __FLASHCARDS_JSON__ placeholders."
        )

    rendered = render_template(template, title, cards)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a standalone HTML flashcard app from JSON.")
    parser.add_argument("input", type=Path, help="Path to the cards JSON file.")
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
        cards = load_cards(args.input)
        build(args.template, cards, title, output_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Built {output_path} with {len(cards)} card(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
