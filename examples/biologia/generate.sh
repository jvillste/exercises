source_directory="come-with-me-regular"

python3 build_flashcards.py "${source_directory}/${source_directory}.json" \
  -o "${source_directory}/flashcards.html" \
  -t "${source_directory}"
