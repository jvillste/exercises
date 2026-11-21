source_directory="come-with-me-regular"
target_directory="/Users/jukka/Documents/public/flashcards/"
mkdir -p "$target_directory"

cp "${source_directory}/flashcards.html" "${target_directory}/${source_directory}.html"
