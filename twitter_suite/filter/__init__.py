from .move_small_files import move_small_files as _move_small_files
from .move_folders_by_txt import move_folders_by_txt as _move_folders_by_txt
from .move_low_aesthetic_files import move_low_aesthetic_files as _move_low_aesthetic_files
from .move_old_files import move_files_older_than as _move_files_older_than

def move_small_files(source_root: str, size_threshold_kb=70, dimensions_threshold=768):
    """
    将小于size_threshold_kb的文件移动到source_root_small中
    """
    _move_small_files(source_root, size_threshold_kb, dimensions_threshold)


def move_folders_by_txt(txt_file: str, base_dir: str, dst_dir: str, copy:bool=False):
    """
    根据txt_file中的文件夹名字，从base_dir中移动文件夹到destination_dir中
    :param copy: 复制文件夹 (or 移动)
    """
    _move_folders_by_txt(txt_file, base_dir, dst_dir, copy)

def move_low_aesthetic_files(source_root: str, aesthetic_threshold: float=5.0):
    """
    移动source_root里美学分数低于aesthetic_score_threshold的文件
    """
    _move_low_aesthetic_files(source_root, aesthetic_threshold)

def move_files_older_than(source_root: str, min_year: int=2020):
    """
    移动source_root里创建时间早于min_year的文件
    """
    _move_files_older_than(source_root, min_year)