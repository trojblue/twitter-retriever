import os
import torch
import time
import glob
import hashlib
import logging
import pandas as pd
from tqdm.auto import tqdm
from .mlp import MLPPredictor
from .embed import CLIPMapper, ImageReader


class AestheticPredictor:
    def __init__(
        self,
        clip_model="ViT-L/14",
        dim=768,
        mlp_model="sac+logos+ava1-l14-linearMSE.pth",
        device="cuda",
    ):
        # CLIP embedding dim is 768 for CLIP ViT L 14
        start_time = time.perf_counter()
        self.clip_mapper = CLIPMapper(clip_model, device)
        self.mlp = MLPPredictor(dim, mlp_model, device)
        logging.info("[init model]: time: %.4f", time.perf_counter() - start_time)

    def predict(self, images, batch_size=16, num_workers=2):
        reader = ImageReader(
            self.clip_mapper.preprocess, images, batch_size, num_workers
        )
        data_iter = reader.__iter__()
        scores = []
        pbar = tqdm(range(len(images)))
        while True:
            start_time = time.perf_counter()
            try:
                batch = data_iter.__next__()
            except StopIteration:
                break
            read_duration = time.perf_counter() - start_time
            logging.info("[read] time: %.4f", read_duration)

            start_time = time.perf_counter()
            results = self.clip_mapper(batch)
            inference_duration = time.perf_counter() - start_time
            logging.info("[inference] time: %.4f", inference_duration)

            start_time = time.perf_counter()
            predictions = self.mlp.predict(results["image_embs"])
            predict_duration = time.perf_counter() - start_time
            logging.info("[predict] time: %.4f", predict_duration)

            count = len(batch["image_path"])
            pbar.update(count)

            scores = scores + predictions.unbind(1)[0].tolist()

        return scores


if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    predictor = AestheticPredictor(
        "ViT-L/14", 768, "sac+logos+ava1-l14-linearMSE.pth", device
    )
    files = glob.glob("images/*")
    # predict score
    scores = predictor.predict(files, 16, 2)
    # calculate md5
    md5s = [hashlib.md5(open(f, "rb").read()).hexdigest() for f in tqdm(files)]
    df = pd.DataFrame(
        {"filename": [os.path.basename(p) for p in files], "score": scores, "md5": md5s}
    )
    df.to_csv("scores.csv")
