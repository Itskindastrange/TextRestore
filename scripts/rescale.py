# Rescaling with Aspect Ratio Preservation and Edge Padding
# combination of rescaling, normalization and padding to maintain the aspect ratio and ensure all images fit within a uniform target size
# apply if your dataset contains variation in sizes of imgs

import os
import cv2
import numpy as np
import pandas as pd

def rescale_and_pad_image(image, max_width, max_height):
    # Get original dimensions
    h_orig, w_orig = image.shape[:2]

    # Calculate the scaling factor
    r = min(max_width / w_orig, max_height / h_orig)

    # Resize the image while maintaining aspect ratio
    w_new = int(w_orig * r)
    h_new = int(h_orig * r)
    resized_image = cv2.resize(image, (w_new, h_new), interpolation=cv2.INTER_LINEAR)

    # Calculate padding
    top_padding = (max_height - h_new) // 2
    bottom_padding = max_height - h_new - top_padding
    left_padding = (max_width - w_new) // 2
    right_padding = max_width - w_new - left_padding

    # Apply padding with edge replication
    padded_image = cv2.copyMakeBorder(
        resized_image,
        top_padding, bottom_padding, left_padding, right_padding,
        cv2.BORDER_REPLICATE
    )

    return padded_image

def process_dataset(input_dir, output_dir, metadata_csv):
    # Load metadata to get max width and height
    metadata = pd.read_csv(metadata_csv)
    max_width = metadata["Width"].max() 
    max_height = metadata["Height"].max() 

    print(f"Max Width: {max_width}, Max Height: {max_height}")

    # Walk through the input directory
    for root, dirs, files in os.walk(input_dir):
        # Compute the relative path for maintaining folder structure
        rel_path = os.path.relpath(root, input_dir)
        new_dir = os.path.join(output_dir, rel_path)

        # Create the corresponding output directory
        os.makedirs(new_dir, exist_ok=True)

       
        for file in files:
            if file.lower().endswith((".jpg", ".png", ".jpeg")):  
                input_path = os.path.join(root, file)
                output_path = os.path.join(new_dir, file)

                # Read and process the image
                image = cv2.imread(input_path)
                if image is not None:
                    processed_image = rescale_and_pad_image(image, max_width, max_height)

                    # Save the processed image
                    cv2.imwrite(output_path, processed_image)
                else:
                    print(f"Warning: Could not read file {input_path}")

# Set paths
input_directory = "D:/FAST/fyp/urdu dataset/HR"  # Replace with your dataset folder path
output_directory = "rescaled_dataset"  # Replace with your desired output folder name
metadata_csv = "metadata.csv"  # Replace with the path to your metadata.csv file

# Process the dataset
process_dataset(input_directory, output_directory, metadata_csv)
