import os
import pandas as pd
from PIL import Image
from imagehash import phash
from tqdm import tqdm
import concurrent.futures

# Set paths
source_root = input("root dir:")
csv_file = os.path.join(source_root, "aesthetic_scores.csv")
new_csv_file = os.path.join(source_root, "aesthetic_scores_with_phash.csv")
extensions = (".jpg", ".jpeg", ".png", ".webp")


# Function to calculate the phash of an image file
def calculate_phash(file_path):
    img = Image.open(file_path)
    phash_value = phash(img)
    return phash_value


# Read the existing CSV
df = pd.read_csv(csv_file)

# Create an empty dictionary to store the phash values
phash_dict = {}

# Get a list of all image file paths
image_files = []
for foldername, _, filenames in os.walk(source_root):
    for filename in filenames:
        if filename.lower().endswith(extensions):
            file_path = os.path.join(foldername, filename)
            image_files.append(file_path)

# Calculate phash values for all image files in subdirectories using multithreading
with concurrent.futures.ThreadPoolExecutor() as executor:
    for file_path, phash_value in tqdm(
        zip(image_files, executor.map(calculate_phash, image_files)),
        total=len(image_files),
    ):
        phash_dict[os.path.basename(file_path)] = str(phash_value)

# Add a new column 'phash' to the DataFrame with the phash values
df["phash"] = df["filename"].apply(lambda x: phash_dict.get(x, None))

# Save the updated DataFrame to a new CSV file
df.to_csv(new_csv_file, index=False)
