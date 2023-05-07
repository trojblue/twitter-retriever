import os
import shutil
import pandas as pd
from tqdm import tqdm

score_threshold = 5.5

source_root = input("sources root:")
destination_root = f"{source_root}_aes_sub{score_threshold}"  # Replace with your
csv_file_path = os.path.join(source_root, "aesthetic_scores.csv")

# Create a dictionary that maps filenames to their paths
file_paths = {}
for foldername, _, filenames in os.walk(source_root):
    for filename in filenames:
        file_paths[filename] = os.path.join(foldername, filename)

# Read the CSV file
df = pd.read_csv(csv_file_path)

# Filter the rows with a score less than 5
filtered_df = df[df["score"] < score_threshold]

# Iterate through the filtered rows and move the files
for _, row in tqdm(filtered_df.iterrows(), total=filtered_df.shape[0]):
    filename = row["filename"]
    source_path = file_paths.get(filename)

    if source_path:
        relative_path = os.path.relpath(os.path.dirname(source_path), source_root)
        destination_path = os.path.join(destination_root, relative_path)

        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        shutil.move(source_path, destination_path)
