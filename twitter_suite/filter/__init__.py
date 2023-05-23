from .move_small_files import move_small_files as _move_small_files
from .move_folders_by_txt import move_folders_by_txt as _move_folders_by_txt
from .move_low_aesthetic_files import (
    move_low_aesthetic_files as _move_low_aesthetic_files,
)
from .move_old_files import move_files_older_than as _move_files_older_than
from .copy_file_newer_than import (
    copy_files_newer_than_year as _copy_files_newer_than_year,
)
from .move_by_phash_diff_v2 import move_by_phash_diff as _move_by_phash_diff
from .move_file_older_than import (
    move_files_older_than_year as _move_files_older_than_year,
)
from .move_non_anime_files import move_non_anime_files as _move_non_anime_files


def move_small_files(source_root: str, size_threshold_kb=70, dimensions_threshold=768):
    """
    将小于size_threshold_kb的文件移动到source_root_small中
    """
    _move_small_files(source_root, size_threshold_kb, dimensions_threshold)


def move_folders_by_txt(
    txt_file: str, base_dir: str, dst_dir: str, copy: bool = False, min_year: int = 2018
):
    """
    根据txt_file中的文件夹名字，从base_dir中移动文件夹到destination_dir中
    :param copy: 复制文件夹 (or 移动)
    :param min_year: 复制的最小年份 (早于此年份的文件不会被复制)
    """
    _move_folders_by_txt(txt_file, base_dir, dst_dir, copy=copy, min_year=min_year)


def move_low_aesthetic_files(source_root: str, aesthetic_threshold: float = 5.0):
    """
    移动source_root里美学分数低于aesthetic_score_threshold的文件
    """
    _move_low_aesthetic_files(source_root, aesthetic_threshold)


def move_files_older_than(source_root: str, min_year: int = 2020):
    """
    移动source_root里创建时间早于min_year的文件
    """
    _move_files_older_than(source_root, min_year)


def copy_files_newer_than_year(
    source_root: str, dest_dir: str = None, min_year: int = 2018
):
    """
    复制source_root里创建时间晚于min_year的文件
    """
    _copy_files_newer_than_year(source_root, dest_dir, min_year)


def move_by_phash_diff(source_root: str, csv_file: str = None, threshold: int = 4):
    """
    移动source_root里phash差异大于threshold的文件
    """
    _move_by_phash_diff(source_root, csv_file=csv_file, phash_threshold=threshold)


def move_files_older_than_year(
    source_root: str, dest_dir: str = None, min_year: int = 2019
):
    """
    移动source_root里创建时间早于min_year的文件
    """
    _move_files_older_than_year(source_root, dest_dir, min_year)


def move_non_anime_files(source_root: str, dest_dir: str = None):
    """
    移动source_root里不是动漫的文件
    """
    _move_non_anime_files(source_root, dest_dir)
