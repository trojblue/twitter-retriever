import os
import shutil
import pandas as pd


def move_not_anime_files(root_dir: str, csv_file: str):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Filter the DataFrame to keep only the rows where cafe_style is not "anime"
    not_anime_df = df[df['cafe_style'] != 'anime']

    # Define the target root directory
    target_root_dir = f"{root_dir}_not_anime"

    # Iterate through each row in the filtered DataFrame
    for index, row in not_anime_df.iterrows():
        filename = row['filename']

        # Find the source file path
        source_file_path = None
        for foldername, _, filenames in os.walk(root_dir):
            if filename in filenames:
                source_file_path = os.path.join(foldername, filename)
                break

        if source_file_path is None:
            print(f"File not found: {filename}")
            continue

        # Construct the target file path
        relative_folder = os.path.relpath(os.path.dirname(source_file_path), root_dir)
        target_folder = os.path.join(target_root_dir, relative_folder)
        target_file_path = os.path.join(target_folder, filename)

        # Create the target folder if it doesn't exist
        os.makedirs(target_folder, exist_ok=True)

        # Move the file to the target folder
        shutil.move(source_file_path, target_file_path)

if __name__ == '__main__':
    # Usage example
    root_dir = input("root dir:")
    csv_file = os.path.join(root_dir, "aesthetic_scores_with_metrics.csv")
    move_not_anime_files(root_dir, csv_file)
