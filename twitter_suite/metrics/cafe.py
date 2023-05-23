import gradio as gr
from transformers import pipeline
from PIL import Image
import os
import torch


class CafePredictor:
    def __init__(self):
        device = 0 if torch.cuda.is_available() else -1
        self.pipe_aesthetic = pipeline(
            "image-classification", "cafeai/cafe_aesthetic", device=device
        )
        self.pipe_style = pipeline(
            "image-classification", "cafeai/cafe_style", device=device
        )
        self.pipe_waifu = pipeline(
            "image-classification", "cafeai/cafe_waifu", device=device
        )

    def _aesthetic(self, input_img):
        data = self.pipe_aesthetic(input_img, top_k=2)
        final = {}
        for d in data:
            final[d["label"]] = d["score"]
        return final

    def _style(self, input_img):
        data = self.pipe_style(input_img, top_k=5)
        final = {}
        for d in data:
            final[d["label"]] = d["score"]
        return final

    def _waifu(self, input_img):
        data = self.pipe_waifu(input_img, top_k=5)
        final = {}
        for d in data:
            final[d["label"]] = d["score"]
        return final

    def get_metrics(self, input_img):
        return {
            "aesthetic": self._aesthetic(input_img),
            "style": self._style(input_img),
            "waifu": self._waifu(input_img),
        }

    def get_string_metrics(self, input_img):
        """返回字符串格式的预测

        Returns:
            dict: {
            "aesthetic": aesthetic | not_aesthetic,
            "style": anime | other | 3d | manga_like | real_life,
            "waifu": waifu | not_waifu,
            }

        """
        m = self.get_metrics(input_img)
        aes = m["aesthetic"]
        aes_str = max(aes, key=aes.get)
        style = m["style"]
        style_str = max(style, key=style.get)
        waifu = m["waifu"]
        waifu_str = max(waifu, key=waifu.get)

        return_dict = {
            "cafe_aesthetic": aes_str,
            "cafe_style": style_str,
            "cafe_waifu": waifu_str,
        }

        return return_dict

    def get_style_string(self, input_img):
        styule = self._style(input_img)
        return max(styule, key=styule.get)

    def demo(self):
        demo_aesthetic = gr.Interface(
            fn=self._aesthetic,
            inputs=gr.Image(type="pil"),
            outputs=gr.Label(label="aesthetic"),
            live=True,
        )
        demo_style = gr.Interface(
            fn=self._style,
            inputs=gr.Image(type="pil"),
            outputs=gr.Label(label="style"),
            live=True,
        )
        demo_waifu = gr.Interface(
            fn=self._waifu,
            inputs=gr.Image(type="pil"),
            outputs=gr.Label(label="waifu"),
            live=True,
        )
        parallel_interface = gr.Parallel(demo_aesthetic, demo_style, demo_waifu)
        return parallel_interface


if __name__ == "__main__":
    predictor = CafePredictor()
    folder_path = input("input folder path:")
    while True:
        filename = input("input filename:")
        img = Image.open(os.path.join(folder_path, filename))
        m = predictor.get_metrics(img)
        print(m)
