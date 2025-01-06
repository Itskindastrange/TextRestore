import os
import cv2

# Function to rename files in a folder with a consistent pattern
def rename_files_in_folder(folder_path):
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    for index, file_name in enumerate(files, 1):
        new_name = f"damage_{index}{os.path.splitext(file_name)[1]}"  # Keeps original extension
        old_file_path = os.path.join(folder_path, file_name)
        new_file_path = os.path.join(folder_path, new_name)
        os.rename(old_file_path, new_file_path)
    print(f"Renamed {len(files)} files in folder: {folder_path}")


# Function to resize images to match the resolution of the original dataset (or reference image)
def resize_images_to_match_resolution(input_folder, reference_image_path):
    # Read the reference image
    reference_image = cv2.imread(reference_image_path)
    if reference_image is None:
        print(f"Error: Unable to load reference image {reference_image_path}")
        return

    reference_height, reference_width = reference_image.shape[:2]

    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(('png', 'jpg', 'jpeg')):
            file_path = os.path.join(input_folder, file_name)
            image = cv2.imread(file_path)

            if image is None:
                print(f"Error reading {file_path}. Skipping.")
                continue

            # Resize the image to match the reference resolution
            resized_image = cv2.resize(image, (reference_width, reference_height))

            # Save the resized image
            cv2.imwrite(file_path, resized_image)

    print(f"Resized all images to match the resolution of {reference_image_path}.")



if __name__ == "__main__":
    # Specify the input folder and reference image
    input_folder = "D:/data_fyp/damaged_bg"  # Folder containing the images to rename and resize
    reference_image_path = "D:/data_fyp/1-1.png" # Path to a reference image from the original dataset

    # Step 1: Rename files
    rename_files_in_folder(input_folder)

    # Step 2: Resize images to match the reference resolution
    resize_images_to_match_resolution(input_folder, reference_image_path)
