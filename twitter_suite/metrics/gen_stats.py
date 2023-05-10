import os
import plotly.graph_objects as go
import plotly.subplots as sp
from PIL import Image
from collections import defaultdict
from tqdm.auto import tqdm
from pathlib import Path
from utils.data_loader import PipelineDataLoader


class DatasetMetrics:
    def __init__(self, source_root, is_twitter=False, logger=None):

        if is_twitter:
            print("twitter metrics ON; loading json files WILL BE SLOW")

        self.loader = PipelineDataLoader(logger)
        self.source_root = source_root
        self.is_twitter = is_twitter
        self.extensions = (".jpg", ".jpeg", ".png", ".webp")
        self.image_count = defaultdict(int)
        self.file_sizes = []
        self.dimensions = []
        self.fav_count = []
        self.process_files()

    def _load_json(self, json_path):
        json = self.loader.load_json(json_path)
        return json

    def process_files(self):
        total_files = sum([len(files) for r, d, files in os.walk(self.source_root)])
        progress_bar = tqdm(total=total_files, desc="Processing files")

        for foldername, _, filenames in os.walk(self.source_root):
            for filename in filenames:
                progress_bar.update(1)
                if filename.lower().endswith(self.extensions):
                    self.image_count[os.path.basename(foldername)] += 1
                    file_path = os.path.join(foldername, filename)

                    # File size
                    file_size = os.path.getsize(file_path)
                    self.file_sizes.append(file_size)

                    # likes
                    if self.is_twitter:
                        json_path = Path(file_path + ".json")
                        json_data = self._load_json(json_path)
                        fav_count = json_data.get("favorite_count", -1)
                        self.fav_count.append(int(fav_count))

                    # Image dimensions
                    try:
                        with Image.open(file_path) as img:
                            self.dimensions.append(img.size)
                    except IOError:
                        print(f"Invalid file: {file_path}")

        progress_bar.close()

    def create_subplots(self, plot_configs):
        fig = sp.make_subplots(
            rows=len(plot_configs),
            cols=len(plot_configs[0]),
            subplot_titles=[config["title"] for config_list in plot_configs for config in config_list],
        )

        for i, config_list in enumerate(plot_configs):
            for j, config in enumerate(config_list):
                fig.add_trace(config["trace"], row=i + 1, col=j + 1)

        name = Path(self.source_root).name
        fig.update_layout(title_text=f"Dataset Quality Metrics for {name}", showlegend=False)
        fig.show()

    def plot_number_of_images(self):
        topic_names, topic_counts = zip(*self.image_count.items())
        return go.Bar(x=topic_names, y=topic_counts, text=topic_counts, textposition="auto")

    def plot_file_size_distribution(self):
        return go.Histogram(x=self.file_sizes, nbinsx=50, histnorm="probability")

    def plot_image_dimensions(self):
        widths, heights = zip(*self.dimensions)
        return go.Scatter(x=widths, y=heights, mode="markers", marker=dict(opacity=0.2))

    def plot_class_imbalance(self):
        topic_names, topic_counts = zip(*self.image_count.items())
        return go.Bar(x=topic_names, y=topic_counts, text=topic_counts, textposition="auto")

    def plot_fav_count_distribution(self):
        return go.Histogram(x=self.fav_count, nbinsx=1000, histnorm="probability")


def get_plot_configs(metrics: DatasetMetrics):
    # Define which plots to display
    plot_configs = [
        [
            {"title": "Number of images per topic", "trace": metrics.plot_number_of_images()},
            {"title": "File size distribution", "trace": metrics.plot_file_size_distribution()},
        ],
        [
            {"title": "Image dimensions distribution", "trace": metrics.plot_image_dimensions()},
            {"title": "Class imbalance", "trace": metrics.plot_class_imbalance()},
        ],
    ]
    return plot_configs


def get_twitter_plot_configs(metrics: DatasetMetrics):
    # Define which plots to display
    plot_configs = [
        [
            {"title": "Number of images per topic", "trace": metrics.plot_number_of_images()},
            {"title": "File size distribution", "trace": metrics.plot_file_size_distribution()},
        ],
        [
            {"title": "Image dimensions distribution", "trace": metrics.plot_image_dimensions()},
            {"title": "Favorite counts distribution", "trace": metrics.plot_fav_count_distribution()},
        ],
    ]
    return plot_configs


if __name__ == '__main__':
    source_root = input("get a dir:")  # Replace with your source root folder path
    metrics = DatasetMetrics(source_root)
    plot_configs = get_plot_configs(metrics)
    metrics.create_subplots(plot_configs)
