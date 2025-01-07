import os
import cv2
import numpy as np
import random

def apply_degradations(image):
    """
    Apply random degradations to simulate real-world LR images.
    """
    # Random brightness adjustment
    brightness_factor = random.uniform(0.5, 1.5)
    image = np.clip(image * brightness_factor, 0, 255).astype(np.uint8)
    
    # Add Gaussian blur
    if random.choice([True, False]):
        kernel_size = random.choice([3, 5, 7])
        image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    
    # Add Gaussian noise
    if random.choice([True, False]):
        mean = 0
        var = random.uniform(0.01, 0.05)
        sigma = var ** 0.5
        noise = np.random.normal(mean, sigma, image.shape) * 255
        image = np.clip(image + noise, 0, 255).astype(np.uint8)
    
    # Simulate low light
    if random.choice([True, False]):
        low_light_factor = random.uniform(0.2, 0.5)
        image = np.clip(image * low_light_factor, 0, 255).astype(np.uint8)
    
    return image

def create_lr_hr_pairs_and_upscale(hr_images_dir, lr_images_dir, upscaled_lr_images_dir, scale_factor=8, cycles=3):
    """
    Create LR-HR image pairs over multiple cycles, save LR images, and upscale LR back to HR.
    """
    for cycle in range(cycles):
        print(f"Cycle {cycle + 1}/{cycles}")
        
        # Walk through the HR directory
        for root, dirs, files in os.walk(hr_images_dir):
            # Determine the relative path for the current subdirectory
            relative_path = os.path.relpath(root, hr_images_dir)
            
            # Create corresponding subdirectories in the LR and upscaled LR directories
            lr_subdir = os.path.join(lr_images_dir, f"cycle_{cycle + 1}", relative_path)
            upscaled_lr_subdir = os.path.join(upscaled_lr_images_dir, f"cycle_{cycle + 1}", relative_path)
            
            # Ensure the directories exist
            os.makedirs(lr_subdir, exist_ok=True)
            os.makedirs(upscaled_lr_subdir, exist_ok=True)
            
            for file in files:
                if file.endswith(('.png', '.jpg', '.jpeg')):  # Process only image files
                    # Full path to the HR image
                    hr_image_path = os.path.join(root, file)
                    
                    # Read the HR image
                    hr_image = cv2.imread(hr_image_path)
                    if hr_image is None:
                        print(f"Warning: {hr_image_path} is not a valid image or couldn't be loaded.")
                        continue
                    
                    # Generate the LR image (downscaled)
                    lr_image = cv2.resize(
                        hr_image, 
                        (hr_image.shape[1] // scale_factor, hr_image.shape[0] // scale_factor), 
                        interpolation=cv2.INTER_LINEAR
                    )
                    
                    # Apply degradations
                    lr_image = apply_degradations(lr_image)
                    
                    # Save the LR image
                    lr_image_path = os.path.join(lr_subdir, file)
                    cv2.imwrite(lr_image_path, lr_image)
                    
                    # Upscale the LR image back to HR size
                    upscaled_lr_image = cv2.resize(
                        lr_image, 
                        (hr_image.shape[1], hr_image.shape[0]), 
                        interpolation=cv2.INTER_CUBIC
                    )
                    
                    # Save the upscaled LR image
                    upscaled_lr_image_path = os.path.join(upscaled_lr_subdir, file)
                    cv2.imwrite(upscaled_lr_image_path, upscaled_lr_image)
                    
                    print(f"Processed: {file}")
                else:
                    print(f"Skipped non-image file: {file}")

# Define paths
hr_images_dir = "D:/data_fyp/changed_bg_dataset/HR"  # HR images root directory
lr_images_dir = "D:/data_fyp/changed_bg_dataset/LR_temp"  # LR images root directory
upscaled_lr_images_dir = "D:/data_fyp/changed_bg_dataset/scaled_LR"  # Upscaled LR images root directory

# Create LR-HR pairs and upscale LR images back to HR over multiple cycles
create_lr_hr_pairs_and_upscale(hr_images_dir, lr_images_dir, upscaled_lr_images_dir, scale_factor=8, cycles=3)
