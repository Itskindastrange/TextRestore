import os
import cv2
import pandas as pd

def rescale_to_original(image, original_width, original_height):
    """
    Rescale an image back to its original size as specified in metadata.
    """
    return cv2.resize(image, (original_width, original_height), interpolation=cv2.INTER_LINEAR)

def process_and_organize_dataset(input_dir, output_dir, metadata_csv):
    """
    Rescale images to their original sizes and save them in respective folders (handwritten/typed).
    """
    try:
        # Load metadata
        metadata = pd.read_csv(metadata_csv)
        if not all(col in metadata.columns for col in ["Image_Name", "Type", "Width", "Height"]):
            raise KeyError("Metadata must contain 'Image_Name', 'Type', 'Width', and 'Height' columns.")
    except Exception as e:
        print(f"Error loading metadata: {e}")
        return

    # Create handwritten and typed directories if not present
    handwritten_dir = os.path.join(output_dir, "handwritten")
    typed_dir = os.path.join(output_dir, "typed")
    os.makedirs(handwritten_dir, exist_ok=True)
    os.makedirs(typed_dir, exist_ok=True)

    # Create a lookup dictionary from metadata
    metadata_dict = {
        row["Image_Name"]: (row["Type"], int(row["Width"]), int(row["Height"]))
        for _, row in metadata.iterrows()
    }

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith((".jpg", ".png", ".jpeg")):
                input_path = os.path.join(root, file)

                if file not in metadata_dict:
                    print(f"Warning: No metadata found for {file}. Skipping...")
                    continue

                image_type, original_width, original_height = metadata_dict[file]

                # Determine output folder based on type
                if image_type.lower() == "handwritten":
                    output_folder = handwritten_dir
                elif image_type.lower() == "typed":
                    output_folder = typed_dir
                else:
                    print(f"Warning: Unknown type '{image_type}' for {file}. Skipping...")
                    continue

                output_path = os.path.join(output_folder, file)

                try:
                    # Read and rescale the image
                    image = cv2.imread(input_path)
                    if image is not None:
                        rescaled_image = rescale_to_original(image, original_width, original_height)

                        # Save the rescaled image
                        cv2.imwrite(output_path, rescaled_image)
                        print(f"Rescaled and saved: {input_path} -> {output_path}")
                    else:
                        print(f"Warning: Could not read file {input_path}")
                except Exception as e:
                    print(f"Error processing file {input_path}: {e}")

# Set paths
input_directory = "D:/data_fyp/changed_bg_dataset/scaled_LR/cycle_3"  # Replace with your LR images folder
output_directory = "D:/data_fyp/URDU_DATASET/LR"  # Replace with desired output folder
metadata_csv = "metadata.csv"  # Path to metadata.csv

# Process dataset
process_and_organize_dataset(input_directory, output_directory, metadata_csv)

print("Dataset rescaling and organization completed.")
