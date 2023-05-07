import os
import plotly.graph_objects as go
import plotly.subplots as sp
from PIL import Image
from collections import defaultdict
from tqdm import tqdm
from pathlib import Path


source_root = input("get a dir:")  # Replace with your source root folder path
extensions = (".jpg", ".jpeg", ".png", ".webp")

image_count = defaultdict(int)
file_sizes = []
dimensions = []

total_files = sum([len(files) for r, d, files in os.walk(source_root)])
progress_bar = tqdm(total=total_files, desc="Processing files")

for foldername, _, filenames in os.walk(source_root):
    for filename in filenames:
        progress_bar.update(1)
        if filename.lower().endswith(extensions):
            image_count[os.path.basename(foldername)] += 1
            file_path = os.path.join(foldername, filename)

            # File size
            file_size = os.path.getsize(file_path)
            file_sizes.append(file_size)

            # Image dimensions
            try:
                with Image.open(file_path) as img:
                    dimensions.append(img.size)
            except IOError:
                print(f"Invalid file: {file_path}")

progress_bar.close()

# Create subplots
fig = sp.make_subplots(
    rows=2,
    cols=2,
    subplot_titles=(
        "Number of images per topic",
        "File size distribution",
        "Image dimensions distribution",
        "Class imbalance",
    ),
)

# Number of images per topic
topic_names, topic_counts = zip(*image_count.items())
fig.add_trace(
    go.Bar(x=topic_names, y=topic_counts, text=topic_counts, textposition="auto"),
    row=1,
    col=1,
)

# File size distribution
fig.add_trace(
    go.Histogram(x=file_sizes, nbinsx=50, histnorm="probability"), row=1, col=2
)

# Image dimensions distribution
widths, heights = zip(*dimensions)
fig.add_trace(
    go.Scatter(x=widths, y=heights, mode="markers", marker=dict(opacity=0.2)),
    row=2,
    col=1,
)

# Class imbalance
fig.add_trace(
    go.Bar(x=topic_names, y=topic_counts, text=topic_counts, textposition="auto"),
    row=2,
    col=2,
)

# Update layout
name = Path(source_root).name
fig.update_layout(title_text=f"Dataset Quality Metrics for {name}", showlegend=False)
fig.show()
