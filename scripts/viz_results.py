import os
import cv2
import matplotlib.pyplot as plt

def show_image_pairs(lr_dir, hr_dir, start_idx, end_idx):
    """
    Display LR and HR image pairs side by side.
    Parameters:
    - lr_dir: Directory containing LR images.
    - hr_dir: Directory containing HR images.
    - start_idx: Starting index for the range of images to display.
    - end_idx: Ending index for the range of images to display.
    """
    # Get sorted lists of image files
    lr_images = sorted(os.listdir(lr_dir))
    hr_images = sorted(os.listdir(hr_dir))
    
    # Ensure the range is valid
    if start_idx < 0 or end_idx > len(lr_images) or end_idx > len(hr_images):
        print("Invalid range. Please check the indices and try again.")
        return

    # Loop through the range and display 5 pairs at a time
    for i in range(start_idx, min(end_idx, start_idx + 10)):
        lr_path = os.path.join(lr_dir, lr_images[i])
        hr_path = os.path.join(hr_dir, hr_images[i])

        # Load images
        lr_image = cv2.imread(lr_path)
        hr_image = cv2.imread(hr_path)

        if lr_image is None or hr_image is None:
            print(f"Warning: Unable to load LR or HR image for index {i}.")
            continue

        # Convert images from BGR to RGB for matplotlib
        lr_image = cv2.cvtColor(lr_image, cv2.COLOR_BGR2RGB)
        hr_image = cv2.cvtColor(hr_image, cv2.COLOR_BGR2RGB)

        # Plot side by side
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.imshow(lr_image)
        plt.title(f"LR Image: {lr_images[i]}")
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.imshow(hr_image)
        plt.title(f"HR Image: {hr_images[i]}")
        plt.axis('off')

        plt.show()

# Define paths and range
lr_images_dir = "D:/data_fyp/changed_bg_dataset/scaled_LR/cycle_3/typed"  # Replace with your LR images folder
hr_images_dir = "rescaled_dataset/HR/typed"      # Replace with your HR images folder
start_index = 0                                   # Starting index for image pairs
end_index = 200                                    # Ending index for image pairs

# Display the image pairs
show_image_pairs(lr_images_dir, hr_images_dir, start_index, end_index)
