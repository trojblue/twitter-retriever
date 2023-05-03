from .move_small_files import move_small_files as _move_small_files

def move_small_files(source_root, size_threshold_kb=70, dimensions_threshold=768):
    _move_small_files(source_root, size_threshold_kb, dimensions_threshold)
