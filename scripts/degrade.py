import os
import random
import cv2
import numpy as np

# Degradation functions

def apply_gaussian_blur(image, kernel_size=5):
    if kernel_size % 2 == 0:
        kernel_size += 1
    print(f"Applying Gaussian Blur with kernel size: {kernel_size}")
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def apply_motion_blur(image, kernel_size=15):
    if kernel_size % 2 == 0:
        kernel_size += 1
    kernel = np.zeros((kernel_size, kernel_size))
    kernel[int((kernel_size - 1) / 2), :] = np.ones(kernel_size)
    kernel = kernel / kernel_size
    print(f"Applying Motion Blur with kernel size: {kernel_size}")
    return cv2.filter2D(image, -1, kernel)

def add_gaussian_noise(image, mean=0, var=0.01):
    sigma = var ** 0.5
    gaussian = np.random.normal(mean, sigma, image.shape) * 255
    noisy_image = image + gaussian
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    print("Adding Gaussian Noise")
    return noisy_image

def add_speckle_noise(image):
    noise = np.random.randn(*image.shape) * 0.1
    noisy_image = image + image * noise
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    print("Adding Speckle Noise")
    return noisy_image

def simulate_low_light(image, factor=0.5):
    print(f"Simulating Low Light with factor: {factor}")
    return np.clip(image * factor, 0, 255).astype(np.uint8)

def add_water_damage(image, mask_size=50):
    if mask_size % 2 == 0:
        mask_size += 1
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    for _ in range(15):
        x, y = np.random.randint(0, image.shape[1]), np.random.randint(0, image.shape[0])
        cv2.line(mask, (x, y), (x + random.randint(-mask_size, mask_size), y + random.randint(-mask_size, mask_size)), (255), random.randint(5, 20))
    blurred_mask = cv2.GaussianBlur(mask, (mask_size, mask_size), 0)
    blurred_mask_colored = cv2.merge([blurred_mask] * 3)
    damaged = cv2.addWeighted(image, 0.8, blurred_mask_colored, 0.2, 0)
    print(f"Adding Water Damage with mask size: {mask_size}")
    return damaged

def add_scanner_artifacts(image, line_intensity=30):
    for _ in range(random.randint(1, 5)):
        y = random.randint(0, image.shape[0] - 1)
        cv2.line(image, (0, y), (image.shape[1], y), (line_intensity,), 1)
    print(f"Adding Scanner Artifacts with line intensity: {line_intensity}")
    return image

def add_compression_artifacts(image, quality=20):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, encoded_img = cv2.imencode('.jpg', image, encode_param)
    decoded_img = cv2.imdecode(encoded_img, 1)
    print(f"Adding Compression Artifacts with quality: {quality}")
    return decoded_img

def smoothen_image(image, kernel_size=3):
    """Applies a slight Gaussian blur to blend text with the background."""
    print(f"Smoothening the image with kernel size: {kernel_size}")
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

# Random degradation function
def random_degradation(image, degradation_set=None):
    print("Applying degradation...")

    # Choose degradation if not predefined
    if degradation_set is None:
        degradation_set = {
            "gaussian_blur": random.choice([True, False]),
            "motion_blur": random.choice([True, False]),
            "gaussian_noise": random.choice([True, False]),
            "speckle_noise": random.choice([True, False]),
            "low_light": random.choice([True, False]),
            "water_damage": random.choice([True, False]),
            "scanner_artifacts": random.choice([True, False]),
            "compression_artifacts": random.choice([True, False]),
        }

    # Apply the selected degradations
    if degradation_set["gaussian_blur"]:
        image = apply_gaussian_blur(image, kernel_size=random.randint(3, 9))
    if degradation_set["motion_blur"]:
        image = apply_motion_blur(image, kernel_size=random.randint(5, 15))
    if degradation_set["gaussian_noise"]:
        image = add_gaussian_noise(image, var=random.uniform(0.01, 0.05))
    if degradation_set["speckle_noise"]:
        image = add_speckle_noise(image)
    if degradation_set["low_light"]:
        image = simulate_low_light(image, factor=random.uniform(0.2, 0.5))
    if degradation_set["water_damage"]:
        image = add_water_damage(image, mask_size=random.randint(20, 100))
    if degradation_set["scanner_artifacts"]:
        image = add_scanner_artifacts(image, line_intensity=random.randint(10, 50))
    if degradation_set["compression_artifacts"]:
        image = add_compression_artifacts(image, quality=random.randint(10, 30))

    # Smoothen the final image to blend everything together
    image = smoothen_image(image, kernel_size=random.randint(3, 5))
    print("Degradation applied and image smoothened.")
    return image

def adjust_brightness(image, factor=None):
    """Adjusts the brightness of the image."""
    if factor is None:
        factor = random.uniform(0.5, 1.5)  # Randomly choose between dark and bright
    print(f"Adjusting brightness with factor: {factor}")
    return np.clip(image * factor, 0, 255).astype(np.uint8)

# Main script
high_res_path = "D:/data_fyp/changed_bg_dataset/HR"
low_res_path = "D:/data_fyp/changed_bg_dataset/LR"

# Generate a random degradation set
degradation_set = {
    "gaussian_blur": random.choice([True, False]),
    "motion_blur": random.choice([True, False]),
    "gaussian_noise": random.choice([True, False]),
    "speckle_noise": random.choice([True, False]),
    "low_light": random.choice([True, False]),
    "water_damage": random.choice([True, False]),
    "scanner_artifacts": random.choice([True, False]),
    "compression_artifacts": random.choice([True, False]),
}
print(f"Selected degradation set: {degradation_set}")

# Process dataset
for root, dirs, files in os.walk(high_res_path):
    for folder in ['typed', 'handwritten']:
        folder_path = os.path.join(root, folder)
        if os.path.exists(folder_path):
            output_folder = os.path.join(low_res_path, folder)

            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            print(f"Processing folder: {folder_path}")
            folder_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
            print(f"Number of files: {len(folder_files)}")

            # Apply the same degradation and save the images
            for filename in folder_files:
                image_path = os.path.join(folder_path, filename)
                output_path = os.path.join(output_folder, filename)

                print(f"Reading image: {image_path}")
                image = cv2.imread(image_path, cv2.IMREAD_COLOR)

                if image is not None:
                    print(f"Image read successfully: {image_path}")
                    
                    # Apply random degradation and brightness adjustment
                    degraded_image = random_degradation(image, degradation_set)
                    bright_image = adjust_brightness(degraded_image)

                    print(f"Saving degraded image: {output_path}")
                    cv2.imwrite(output_path, bright_image)
                else:
                    print(f"Failed to read image: {image_path}")

print("Degradation process completed successfully!")
