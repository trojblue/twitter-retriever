import time
from typing import List


import time
from concurrent.futures import ThreadPoolExecutor
from typing import List
from tqdm import tqdm
import sdtools.fileops as fops

import os
from PIL import Image

import os
import time
from typing import List
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from tqdm import tqdm


class ImageResizer:
    def __init__(
        self,
        src_dir: str,
        dst_dir: str,
        min_side: int = 768,
        format: str = "webp",
        quality=95,
    ):
        self.src_dir = src_dir
        self.dst_dir = dst_dir
        self.min_side = min_side
        self.format = format
        self.quality = quality

    def resize_img_single(self, filepath: str, relative_path: str, filename: str):
        src_path = os.path.join(filepath, filename)
        dst_path = os.path.join(
            self.dst_dir,
            relative_path,
            os.path.splitext(filename)[0] + f".{self.format}",
        )

        # Create the destination directory if it doesn't exist
        os.makedirs(os.path.join(self.dst_dir, relative_path), exist_ok=True)

        # Open the image file
        image = Image.open(src_path)
        width, height = image.size
        min_res = min(width, height)

        if min_res < self.min_side:
            new_width, new_height = width, height
        elif width < height:
            new_width = self.min_side
            new_height = int(height * (new_width / width))
        else:
            new_height = self.min_side
            new_width = int(width * (new_height / height))

        # Resize the image
        image = image.resize((new_width, new_height), Image.LANCZOS)

        # Save the image with the specified format and quality
        if self.format == "jpg":
            image.save(dst_path, format="JPEG", quality=self.quality)
        elif self.format == "webp":
            image.save(dst_path, format="WEBP", quality=self.quality)
        else:
            image.save(dst_path, format="PNG")

    def resize_images(self):
        image_files = []

        for root, _, files in os.walk(self.src_dir):
            for file in files:
                if file.lower().endswith(
                    (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp")
                ):
                    relative_path = os.path.relpath(root, self.src_dir)
                    image_files.append((root, relative_path, file))

        n_imgs = len(image_files)

        with tqdm(
            total=n_imgs, desc=f"Resizing images to min_side={self.min_side}: "
        ) as pbar:
            with ThreadPoolExecutor() as executor:
                tasks = [
                    executor.submit(
                        self.resize_img_single,
                        filepath,
                        relative_path,
                        filename,
                    )
                    for filepath, relative_path, filename in image_files
                ]

                for task in tasks:
                    task.add_done_callback(lambda _: pbar.update())

                for task in tasks:
                    task.result()

        return f"Resized {n_imgs} images to min_side={self.min_side}"


if __name__ == "__main__":
    # Define the source and destination directories and the minimum side length for resizing
    src_dir = "path/to/source/images"
    dst_dir = "path/to/destination/images"
    min_side = 1024

    # Create an instance of the ImageResizer class
    resizer = ImageResizer(src_dir, dst_dir, min_side)

    # Get a list of image files from the source directory
    resizer.resize_images()
