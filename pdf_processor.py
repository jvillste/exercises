import pymupdf  # PyMuPDF
import os
import csv
from PIL import Image
import io

def process_pdf_for_flashcards(pdf_path="biologia.pdf", output_csv="flashcards.csv", output_dir="extracted_images"):
    """
    Extracts images from a PDF, combines multiple images on the same slide into one JPG,
    and creates a CSV for flashcards. Slides 1 and 2 are skipped as they do not contain images.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        return

    print(f"Processing PDF: {pdf_path}")
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    document = pymupdf.open(pdf_path)
    flashcards = []
    
    # Start from slide 3 (index 2) to skip slides 1 and 2 which have no images
    for page_num in range(2, len(document)):
        page = document.load_page(page_num)
        slide_number = page_num + 1
        
        # Extract text for the "Correct Answer" context
        page_text = page.get_text("text").strip()
        
        if not page_text:
            correct_answer = f"Slide {slide_number}"
        else:
            correct_answer = page_text.replace('\n', ' ')
            
        # Get embedded images from the page
        image_list = page.get_images(full=True)
        
        if not image_list:
            print(f"Skipped slide {slide_number} (no images found)")
            continue
        
        # Collect all images for this slide
        images_to_combine = []
        
        for img in image_list:
            xref = img[0]
            base_image = document.extract_image(xref)
            
            if not base_image:
                continue
                
            img_bytes = base_image["image"]
            
            # Open image with PIL for combining
            img_pil = Image.open(io.BytesIO(img_bytes))
            
            # Convert to RGB to ensure compatibility with JPG
            if img_pil.mode != 'RGB':
                img_pil = img_pil.convert('RGB')
                
            images_to_combine.append(img_pil)
            
        if not images_to_combine:
            print(f"No valid images extracted for slide {slide_number}")
            continue

        # Combine images if there are multiple
        if len(images_to_combine) == 1:
            combined_img = images_to_combine[0]
        else:
            # Combine horizontally with a small padding
            padding = 10
            total_width = sum(img.width for img in images_to_combine) + (padding * (len(images_to_combine) - 1))
            max_height = max(img.height for img in images_to_combine)
            
            combined_img = Image.new('RGB', (total_width, max_height), (255, 255, 255))
            
            current_x = 0
            for img in images_to_combine:
                combined_img.paste(img, (current_x, 0))
                current_x += img.width + padding

        # Save the combined image as a single JPG per slide
        image_filename = f"slide_{slide_number:03d}.jpg"
        image_path = os.path.join(output_dir, image_filename)
        combined_img.save(image_path, "JPEG")
        
        flashcards.append({
            "image_file_name": image_filename,
            "correct_answer": correct_answer
        })
        print(f"Processed slide {slide_number} -> {image_filename}")

    # Write the CSV file
    fieldnames = ["image_file_name", "correct_answer"]
    try:
        with open(output_csv, "w", newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flashcards)
        print(f"\nSuccessfully created flashcards CSV: {output_csv}")
    except Exception as e:
        print(f"Failed to create CSV: {e}")

    document.close()

if __name__ == "__main__":
    process_pdf_for_flashcards()