import os
import shutil
from PIL import Image
from tqdm.auto import tqdm

extensions = (".jpg", ".jpeg", ".png", ".webp")


def is_small_or_low_resolution(
    filename: str, size_threshold_kb: int, dimensions_threshold: int
):
    file_size_kb = os.path.getsize(filename) / 1024

    if file_size_kb < size_threshold_kb:
        return True

    try:
        with Image.open(filename) as img:
            width, height = img.size
            img_pixels = width * height
            threshold_pixels = dimensions_threshold**2
            if img_pixels < threshold_pixels:
                return True
    except IOError:
        pass

    return False


def move_small_files(source_root, size_threshold_kb=70, dimensions_threshold=768):
    destination_root = f"{source_root}_sub{size_threshold_kb}_min{dimensions_threshold}"
    print(f"Moving smaller files to {destination_root}")

    # Accumulate list of directories
    directories = []
    for foldername, subfolders, filenames in os.walk(source_root):
        directories.append((foldername, filenames))

    # Process directories with a single tqdm progress bar
    for foldername, filenames in tqdm(directories, desc="Processing directories"):
        for filename in filenames:
            if filename.lower().endswith(extensions):
                source_path = os.path.join(foldername, filename)

                if is_small_or_low_resolution(
                    source_path, size_threshold_kb, dimensions_threshold
                ):
                    relative_path = os.path.relpath(foldername, source_root)
                    destination_path = os.path.join(destination_root, relative_path)

                    if not os.path.exists(destination_path):
                        os.makedirs(destination_path)

                    shutil.move(source_path, destination_path)


if __name__ == "__main__":
    size_threshold_kb = 70
    dimensions_threshold = 640
    source_root = input("source dir:")
    move_small_files(source_root, size_threshold_kb, dimensions_threshold)
