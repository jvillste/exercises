# HTML flashcard template

A standalone HTML flashcard app plus a small Python builder. The generated HTML
has no dependencies and works offline in a normal browser.

## Files

- `flashcards_template.html` — the HTML/CSS/JavaScript template. It contains two
  placeholders: `__FLASHCARDS_TITLE__` and `__FLASHCARDS_JSON__`.
- `build_flashcards.py` — reads a JSON file and writes a standalone HTML file.
- `geoidi-5/cards.json` — example JSON input.
- `geoidi/flashcards.html` — example output built from `geoidi-5/cards.json`.
- `geoidi-5/flashcards.html` — another example output.

## JSON format

The JSON root can be a list of cards:

```json
[
  {
    "question": "What is the capital of Finland?",
    "answer": "Helsinki"
  }
]
```

It can also be an object with a `cards` list:

```json
{
  "cards": [
    {
      "image": "images/example.jpg",
      "question": "What does the image show?",
      "answer": "A textual answer"
    }
  ]
}
```

Each card needs an `answer`. The front side needs either an `image`, a
`question`, or both. Accepted field names:

| Field | Accepted names |
| --- | --- |
| image | `image`, `image_file_name`, `img` |
| question | `question`, `front`, `text`, `q` |
| answer | `answer`, `back`, `correct_answer`, `a` |

Image paths are used as written in the generated HTML. Relative paths are
resolved relative to the HTML file, so keep images in a folder next to the HTML
file or use absolute/URL paths.

## Build

```bash
python3 build_flashcards.py cards.json -o flashcards.html --title "My Flashcards"
```

If `-o` is omitted, the output is written next to the input file with an
`.html` extension. If `--title` is omitted, the title is derived from the input
file name.

## Using the generated page

- Click **Show Answer (f)** to reveal the answer on the back.
- Click **Learned! (d)** to mark the card as learned and move to the next card.
- Click **Needs More Training (f)** to put the card back into the queue.
- The button labels show the keyboard shortcuts: `F` shows the answer and
  then marks needs training; `D` marks learned. Refresh the page to start
  over.
