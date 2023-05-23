from .img_resizer import ImageResizer
from .img_validator import ImgValidator


def validate_images(src_dir: str, min_side: int = 768, format: str = "webp"):
    original_dir = src_dir
    new_dir = f"{src_dir}_{min_side}{format}"
    validator = ImgValidator(new_dir)
    validator.validate_compressed_images(original_dir, new_dir)


def resize_images(src_dir: str, min_side: int = 768, format: str = "webp"):
    # Create an instance of the ImageResizer class
    dst_dir = f"{src_dir}_{min_side}{format}"
    resizer = ImageResizer(src_dir, dst_dir, min_side, format=format)
    resizer.resize_images()
