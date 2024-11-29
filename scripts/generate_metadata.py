import cv2
import os
import pandas as pd

# Paths
dataset_path = "D:/FAST/fyp/urdu dataset/HR"
metadata_file = "metadata.csv"

# list for metadata
metadata = []

for root, dirs, files in os.walk(dataset_path):
    for file in files:
        print(f"Processing folder: {root}, Image: {file}")
        if file.endswith((".jpg", ".png", ".jpeg")):  # Add other formats accordingly
            file_path = os.path.join(root, file)
            img = cv2.imread(file_path)
            h, w, _ = img.shape
            # Determine type and level based on file path or naming convention
            img_type = "handwritten" if "handwritten" in root else "typed"
            
            
            # Append metadata
            metadata.append({
                "Image_Name": file,
                "Type": img_type,
                "Width": w,
                "Height": h,
                "Aspect_Ratio": round(w / h, 2)
            })


df = pd.DataFrame(metadata)
df.to_csv(metadata_file, index=False)
print(f"Metadata saved to {metadata_file}")
