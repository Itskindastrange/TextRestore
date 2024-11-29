import os

# Function to count the number of image files in each directory
def count_images_in_directories(folder_path):
    # Supported image file extensions (you can add more if needed)
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')
    count = []
    
    # Iterate through all subdirectories inside the folder
    for root, dirs, files in os.walk(folder_path):
        # Count the number of image files in the current directory
        image_count = sum(1 for file in files if file.lower().endswith(image_extensions))
        
        # Only print count for directories that have images
        if image_count > 0:
            print(f"Directory: {root} - Image count: {image_count}")
            count.append(image_count)  # Append the count for the current directory

    return count        

# Provide the path to the folder containing the directories
folder_path = 'rescaled_dataset'  

image_counts = count_images_in_directories(folder_path)

total_images = sum(image_counts)
print(f"Total images: {total_images}")
