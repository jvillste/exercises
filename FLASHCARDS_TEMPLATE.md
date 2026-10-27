# HTML flashcard template

Two files make it easy to turn any JSON file into a standalone flashcard app:

- `flashcards_template.html` – the reusable HTML/CSS/JS template.
- `build_flashcards.py` – injects a JSON card list into the template.

## JSON format

The JSON root can be a list of cards, or an object with a `"cards"` list:

```json
[
  {
    "question": "Kenelle ihmisoikeudet kuuluvat?",
    "answer": "Kaikille ihmisille."
  },
  {
    "image": "images/slide_003.jpg",
    "answer": "Sinivuokko"
  },
  {
    "image": "images/slide_010.jpg",
    "question": "Mikä kasvi?",
    "answer": "Kanerva"
  }
]
```

Each card needs an `answer` and at least one front side:

| Field      | Aliases                              | Meaning                         |
|------------|--------------------------------------|---------------------------------|
| `image`    | `image_file_name`, `img`             | Image shown on the front.       |
| `question` | `front`, `text`, `q`                 | Text shown on the front.        |
| `answer`   | `back`, `correct_answer`, `a`        | Text shown on the back.         |

If a card has both `image` and `question`, the question is shown as a caption
under the image. If it only has `question`, the card is text-only. Image paths
are relative to the generated HTML file.

## Build

```bash
python3 build_flashcards.py cards.json -o flashcards.html -t "My topic"
```

Options:

- `-o`, `--output` – output HTML path (default: same name as the input with `.html`).
- `-t`, `--title` – page title (default: derived from the JSON filename).
- `--template` – use a different template file.

Example for this project:

```bash
python3 build_flashcards.py geoidi-5/cards.json \
  -o geoidi/flashcards.html \
  -t "Geoidi – Ihmisoikeudet"
```

## Using the generated app

Open the generated `.html` file in a browser. The cards are embedded in the
file, so no web server or network connection is needed.

Buttons show their keyboard shortcuts:

- **Show Answer (f)** / `f` – reveal the answer.
- **Learned! (d)** / `d` – mark the card as learned and move to the next card.
- **Needs More Training (f)** / `f` – after revealing the answer, put the card back into the queue.

There is no restart button or restart shortcut; refresh the page to start over.

## Editing the template

The template contains two placeholders:

- `__FLASHCARDS_TITLE__`
- `__FLASHCARDS_JSON__`

Keep both placeholders when customizing the template. The generator replaces
them with the escaped title and the card JSON.
