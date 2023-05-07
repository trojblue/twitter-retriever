from .gen_stats import DatasetMetrics as _DatasetMetrics
from .gen_stats import get_twitter_plot_configs as _get_twitter_plot_configs

def get_metrics(source_root, is_twitter=False):
    metrics = _DatasetMetrics(source_root, is_twitter=is_twitter)
    plot_configs = _get_twitter_plot_configs(metrics)
    metrics.create_subplots(plot_configs)
