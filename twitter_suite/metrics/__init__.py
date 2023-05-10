# import _aesthetic from subdir
from .gen_stats import DatasetMetrics as _DatasetMetrics
from .gen_stats import get_twitter_plot_configs as _get_twitter_plot_configs
from .aesthetic.get_aesthetics import AestheticMonitor as _AestheticMonitor
from .insert_phash import insert_phash as _insert_phash
from .insert_cafe_metrics import insert_cafe_metrics as _insert_cafe_metrics

def get_metrics(source_root, is_twitter=False):
    metrics = _DatasetMetrics(source_root, is_twitter=is_twitter)
    plot_configs = _get_twitter_plot_configs(metrics)
    metrics.create_subplots(plot_configs)

def get_aesthetics(source_root, dry_run=False):
    predictor = _AestheticMonitor(source_root)
    predictor.predict_aesthetics(dry_run=dry_run)

def insert_phash(source_root, csv_file: str = None):
    _insert_phash(source_root, csv_file=csv_file)

def insert_cafe_metrics(source_root, csv_file: str = None):
    _insert_cafe_metrics(source_root, csv_file=csv_file)