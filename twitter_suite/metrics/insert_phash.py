import os
import pandas as pd
from PIL import Image
from imagehash import phash
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from typing import Optional


extensions = (".jpg", ".jpeg", ".png", ".webp", ".tiff", ".bmp")


def calculate_phash(file_path: str) -> str:
    img = Image.open(file_path)
    phash_value = phash(img)
    return str(phash_value)


def insert_phash(source_root: str, csv_file: Optional[str] = None) -> None:
    csv_file = os.path.join(source_root, "metrics.csv") if not csv_file else csv_file

    # Read the existing CSV
    df = pd.read_csv(csv_file)

    if "phash" in df.columns:
        print("phash column already exists. Skipping entries with phash values.")
    else:
        df["phash"] = None

    # Get a list of all image file paths
    image_files = [
        os.path.join(foldername, filename)
        for foldername, _, filenames in os.walk(source_root)
        for filename in filenames
        if filename.lower().endswith(extensions)
    ]

    # Calculate phash values for image files without existing phash values
    file_dict = {os.path.basename(file): file for file in image_files}
    files_to_update = df[df["phash"].isna()]["filename"].tolist()

    # Calculate phash values for files that need to be updated using ProcessPoolExecutor
    num_cores = max(1, multiprocessing.cpu_count() - 1)
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        phash_values = list(
            tqdm(
                executor.map(
                    calculate_phash, [file_dict[file] for file in files_to_update]
                ),
                total=len(files_to_update),
                desc="Calculating phash values",
            )
        )

    updated_phash_values = dict(zip(files_to_update, phash_values))

    # Update the phash values in the DataFrame
    df.loc[df["filename"].isin(files_to_update), "phash"] = df["filename"].map(
        updated_phash_values
    )

    # Save the updated DataFrame to the CSV file
    df.to_csv(csv_file, index=False)


if __name__ == "__main__":
    # Set paths
    source_root = input("root dir:")
    csv_file = os.path.join(source_root, "metrics.csv")
    insert_phash(source_root, csv_file)
