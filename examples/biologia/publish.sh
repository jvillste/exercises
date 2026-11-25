target_directory="/Users/jukka/Documents/public/biologia/"
rm -rf "$target_directory"
mkdir -p "$target_directory"

cp -r extracted_images "$target_directory"
cp flashcards.html "$target_directory"
