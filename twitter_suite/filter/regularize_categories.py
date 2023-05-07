import os
import math
import random
import shutil
import numpy as np

# Set the percentile for the target image count
percentile_target = 80

# Set the exponential penalty factor
penalty_factor = 0.7

source_root = r"D:\Andrew\Pictures\Grabber\mai_saver"
destination_root = (
    f"{source_root}_penalties_percentile{percentile_target}_factor{penalty_factor}"
)
extensions = (".jpg", ".jpeg", ".png", ".webp")

# Count the number of images in each subfolder
image_count = {}
for foldername, _, filenames in os.walk(source_root):
    image_files = [f for f in filenames if f.lower().endswith(extensions)]
    if image_files:
        image_count[foldername] = len(image_files)

# Calculate the target image count based on the given percentile
image_counts = list(image_count.values())
target_image_count = int(np.percentile(image_counts, percentile_target))

# Calculate how many images to move for each category
move_counts = {}
for folder, count in image_count.items():
    if count > target_image_count:
        # Apply exponential penalty
        move_count = int(
            count
            - target_image_count * (1 - penalty_factor ** (count - target_image_count))
        )
        move_counts[folder] = move_count
    else:
        move_counts[folder] = 0

# Move the images with the earliest dates
for folder, move_count in move_counts.items():
    if move_count > 0:
        all_files = [f for f in os.listdir(folder) if f.lower().endswith(extensions)]

        # Sort the files by date (in ascending order)
        sorted_files = sorted(all_files, key=lambda x: x.split("__")[1])

        files_to_move = sorted_files[:move_count]

        for filename in files_to_move:
            source_path = os.path.join(folder, filename)
            relative_path = os.path.relpath(folder, source_root)
            destination_path = os.path.join(destination_root, relative_path)

            if not os.path.exists(destination_path):
                os.makedirs(destination_path)

            shutil.move(source_path, os.path.join(destination_path, filename))
