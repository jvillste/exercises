source_directory="$1"
target_directory="/Users/jukka/Documents/public/flashcards/"
mkdir -p "$target_directory"

cp "${source_directory}/flashcards.html" "${target_directory}/${source_directory}.html"
