import os
import shutil
import pandas as pd
from itertools import groupby
from operator import itemgetter

def move_by_phash_diff(root_dir: str, csv_file: str=None, phash_threshold: int=4):

    csv_file = csv_file or os.path.join(root_dir, 'metrics.csv')
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Construct the paths of all files
    file_paths = {}
    for foldername, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_paths[filename] = os.path.join(foldername, filename)

    # Group the files by phash values
    df['path'] = df['filename'].apply(lambda x: file_paths.get(x, None))
    df = df[df['path'].notnull()]
    df['phash_int'] = df['phash'].apply(lambda x: int(x, 16))
    df_sorted = df.sort_values('phash_int')
    grouped = groupby(df_sorted.itertuples(), key=lambda x: x.phash_int)

    # Define the target root directory
    target_root_dir = f"{root_dir}_phash_min{phash_threshold}"
    move_count = 0

    # Iterate through each group and compare the phash values to identify duplicates
    for phash_value, group in grouped:
        group_list = list(group)
        if len(group_list) <= 1:
            continue

        for i in range(len(group_list) - 1):
            file1 = group_list[i]
            file2 = group_list[i+1]

            # Check if the phash difference is within the threshold
            if file2.phash_int - file1.phash_int <= phash_threshold:
                # Construct the target file path
                relative_folder = os.path.relpath(os.path.dirname(file2.path), root_dir)
                target_folder = os.path.join(target_root_dir, relative_folder)
                target_file_path = os.path.join(target_folder, file2.filename)

                # Create the target folder if it doesn't exist
                os.makedirs(target_folder, exist_ok=True)

                # Move the file to the target folder
                shutil.move(file2.path, target_file_path)
                move_count += 1

    print(f"Moved {move_count} files to {target_root_dir}")


if __name__ == '__main__':
    # Usage example
    root_dir = input("root dir:")
    csv_file = os.path.join(root_dir, "metrics.csv")
    phash_threshold = 12  # Set the phash threshold value
    move_by_phash_diff(root_dir, csv_file, phash_threshold)
