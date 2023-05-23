import os
import imghdr
from PIL import Image
from typing import Tuple, List
from tqdm import tqdm


class ImgValidator:
    def __init__(self, src_dir: str):
        self.src_dir = src_dir

    @staticmethod
    def _validate_image(filename: str) -> Tuple[bool, str]:
        file_type = imghdr.what(filename)
        if file_type is None:
            return False, f"file_type is none: {filename}"

        _, file_extension = os.path.splitext(filename)
        file_extension = file_extension.strip(".").lower()

        if file_extension in ["jpg", "jpeg"] and file_type != "jpeg":
            return False, f"invalid jpeg file: {filename}"

        if file_extension == "png" and file_type != "png":
            return False, f"invalid png file: {filename}"

        try:
            image = Image.open(filename)
            image.verify()
            return True, ""
        except (IOError, SyntaxError, Image.DecompressionBombError):
            return False, f"IO/Syntax/DecompressionBomb Error: {filename}"

    def _get_image_files(self, directory: str) -> List[str]:
        return [
            os.path.join(directory, file)
            for file in os.listdir(directory)
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))
        ]

    def validate_compressed_images(
        self, original_dir: str, new_dir: str, img_files: List[str] = None
    ):
        if img_files is None:
            img_files = self._get_image_files(original_dir)

        new_dir_imgs = self._get_image_files(new_dir)

        if set(img_files) != set(new_dir_imgs):
            raise ValueError(
                "File names do not match between the original and new directories."
            )
        print("(1) file names match: √")

        invalid_files = []
        for img in tqdm(new_dir_imgs, desc="checking image integrity"):
            is_valid, error_msg = self._validate_image(img)
            if not is_valid:
                print(f"INVALID FILE: {img}")
                invalid_files.append(img)

        with open("invalid_files.txt", "a") as f:
            f.writelines(invalid_files)
        print(
            f"(2) image integrity: {len(invalid_files)} image(s) corrupted >>> invalid_files.txt"
        )


if __name__ == "__main__":
    src_dir = "path/to/source/images"
    original_dir = "path/to/original/images"
    new_dir = "path/to/compressed/images"

    validator = ImgValidator(src_dir)
    validator.validate_compressed_images(original_dir, new_dir)
