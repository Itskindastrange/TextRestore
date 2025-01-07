import os
import cv2
import random
import numpy as np

def blend_images(text_image, bg_image, alpha=0.7):
    """Blend text and background images to create a smooth composition."""
    text_image_resized = cv2.resize(bg_image, (text_image.shape[1], text_image.shape[0]))
    blended_image = cv2.addWeighted(text_image, alpha, text_image_resized, 1 - alpha, 0)
    return blended_image

def apply_damaged_backgrounds_evenly(text_dir, background_dir, output_dir, skip_percentage=30):
    """Apply damaged backgrounds to text images with even distribution of skipping and backgrounds."""
    # Get list of damaged backgrounds
    background_images = [os.path.join(background_dir, bg) for bg in os.listdir(background_dir) if bg.lower().endswith(('.jpg', '.png'))]
    if not background_images:
        raise ValueError("No background images found in the background directory!")

    # Collect all image paths and maintain folder structure
    all_images = []
    folder_structure = {}

    for root, _, files in os.walk(text_dir):
        rel_path = os.path.relpath(root, text_dir)  # Maintain folder structure
        output_path = os.path.join(output_dir, rel_path)
        os.makedirs(output_path, exist_ok=True)

        # Filter only image files
        image_files = [os.path.join(root, f) for f in files if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        all_images.extend(image_files)
        folder_structure[root] = output_path

    # Determine total images to skip
    num_to_skip = int(len(all_images) * skip_percentage / 100)
    skip_indices = set(random.sample(range(len(all_images)), num_to_skip))

    # Evenly distribute backgrounds
    bg_cycle = iter(random.sample(background_images * (len(all_images) // len(background_images) + 1), len(all_images)))

    # Process images
    for idx, image_path in enumerate(all_images):
        rel_folder = os.path.relpath(os.path.dirname(image_path), text_dir)
        output_folder = os.path.join(output_dir, rel_folder)

        if idx in skip_indices:  # Skip images evenly
            # Save skipped images in the same folder
            skipped_image_path = os.path.join(output_folder, os.path.basename(image_path))
            os.makedirs(os.path.dirname(skipped_image_path), exist_ok=True)
            cv2.imwrite(skipped_image_path, cv2.imread(image_path))
            print(f"Skipped: {image_path} -> {skipped_image_path}")
            continue

        # Read the text image
        text_image = cv2.imread(image_path)
        if text_image is None:
            print(f"Warning: Failed to read {image_path}")
            continue

        # Select a damaged background
        background_path = next(bg_cycle)
        background_image = cv2.imread(background_path)
        if background_image is None:
            print(f"Warning: Failed to read {background_path}")
            continue

        # Blend the text and background images
        blended_image = blend_images(text_image, background_image)

        # Save the blended image
        output_image_path = os.path.join(output_folder, os.path.basename(image_path))
        os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
        cv2.imwrite(output_image_path, blended_image)
        print(f"Processed: {image_path} -> {output_image_path}")

# Set paths
text_directory = "rescaled_dataset"  # Replace with your text images directory
background_directory = "D:/data_fyp/damaged_bg"  # Replace with your damaged backgrounds directory
output_directory = "D:/data_fyp/changed_bg_dataset"  # Replace with your desired output directory

skip_percent = 30  # Percentage of images to skip

# Apply damaged backgrounds
apply_damaged_backgrounds_evenly(text_directory, background_directory, output_directory, skip_percentage=skip_percent)
