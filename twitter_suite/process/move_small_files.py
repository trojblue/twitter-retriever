import os
import shutil
from PIL import Image
from tqdm import tqdm


extensions = ('.jpg', '.jpeg', '.png', '.webp')

def is_small_or_low_resolution(filename, size_threshold_kb=70, dimensions_threshold=768):
    file_size_kb = os.path.getsize(filename) / 1024

    if file_size_kb < size_threshold_kb:
        return True

    try:
        with Image.open(filename) as img:
            width, height = img.size
            if width < dimensions_threshold or height < dimensions_threshold:
                return True
    except IOError:
        pass

    return False


def move_small_files(source_root, size_threshold_kb=70, dimensions_threshold=768):
    destination_root = f"{source_root}_sub{size_threshold_kb}_min{dimensions_threshold}"  # Replace with your destination root folder path
    for foldername, subfolders, filenames in os.walk(source_root):
        for filename in tqdm(filenames):
            if filename.lower().endswith(extensions):
                source_path = os.path.join(foldername, filename)

                if is_small_or_low_resolution(source_path, size_threshold_kb, dimensions_threshold):
                    relative_path = os.path.relpath(foldername, source_root)
                    destination_path = os.path.join(destination_root, relative_path)

                    if not os.path.exists(destination_path):
                        os.makedirs(destination_path)

                    shutil.move(source_path, destination_path)


if __name__ == '__main__':
    size_threshold_kb = 70
    dimensions_threshold = 768
    source_root = input("source dir:")
    move_small_files(source_root, size_threshold_kb, dimensions_threshold)
