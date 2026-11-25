# HTML multiple-choice template

A standalone HTML multiple-choice exercise app plus a small Python builder. The
generated HTML has no dependencies and works offline in a normal browser.

The visual style and the build workflow follow `flashcards_template.html` and
`build_flashcards.py`.

## Files

- `multiple_choice_template.html` — the HTML/CSS/JavaScript template. It contains
  two placeholders: `__QUIZ_TITLE__` and `__QUIZ_JSON__`.
- `build_multiple_choice.py` — reads a JSON file and writes a standalone HTML file.
- `multiple-choice-example/questions.json` — example JSON input.
- `multiple-choice-example/quiz.html` — example output built from that JSON.

## JSON format

The JSON root can be a list of questions:

```json
[
  {
    "question": "Mikä on Suomen pääkaupunki?",
    "options": ["Turku", "Helsinki", "Tampere", "Oulu"],
    "correct": 1,
    "explanation": "Helsinki on ollut Suomen pääkaupunki vuodesta 1812."
  }
]
```

It can also be an object with a `questions` list:

```json
{
  "questions": [
    {
      "question": "Mikä on maapallon suurin valtameri?",
      "options": ["Atlantti", "Intian valtameri", "Tyynimeri", "Pohjoinen jäämeri"],
      "correct": 2
    }
  ]
}
```

The correct answer is always a **zero-based index** into `options`. Only one
option can be correct. A question needs at least two options. The `explanation`
field is optional.

Accepted field names:

| Field | Accepted names |
| --- | --- |
| question | `question`, `front`, `text`, `q` |
| options | `options`, `choices`, `vaihtoehdot` |
| correct | `correct`, `correct_index`, `answer_index`, `oikea` |
| explanation | `explanation`, `perustelu`, `selitys` |

Questions that lack a question text, have fewer than two options, or have an
invalid correct index are skipped with a warning.

## Build

```bash
python3 build_multiple_choice.py questions.json -o quiz.html --title "Monivalintatehtävät"
```

If `-o` is omitted, the output is written next to the input file with an
`.html` extension. If `--title` is omitted, the title is derived from the input
file name.

Example:

```bash
python3 build_multiple_choice.py multiple-choice-example/questions.json \
  -o multiple-choice-example/quiz.html \
  -t "Monivalintatehtävät – esimerkki"
```

## Using the generated page

- Each question is shown once per round. Question order is kept as written in
  the JSON file.
- The answer options are shuffled visually every round.
- Click an option or press `1`–`9` to answer. Feedback is shown immediately.
- A wrong answer reveals the correct option. The optional explanation is shown
  after both correct and wrong answers.
- Press `Enter` or `n` (or click **Seuraava**) to move to the next question.
- At the end you see the score. If you answered some questions wrong, click
  **Harjoittele väärät vastaukset (v)** to practise only those questions.
  **Aloita alusta (r)** starts the whole exercise over.
- Refresh the page to reset the exercise completely.

## Editing the template

The template contains two placeholders:

- `__QUIZ_TITLE__`
- `__QUIZ_JSON__`

Keep both placeholders when customizing the template. The generator replaces
them with the escaped title and the question JSON.
