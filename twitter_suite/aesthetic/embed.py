import torch
import clip
import numpy as np
from PIL import Image
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.utils.data.dataloader import default_collate


def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2 == 0] = 1
    return a / np.expand_dims(l2, axis)


class CLIPMapper:
    def __init__(self, clip_model, device):
        model, preprocess = clip.load(clip_model, device=device)
        self.model = model
        self.preprocess = preprocess
        self.device = device

    @torch.no_grad()
    def __call__(self, batch):
        image_path = batch["image_path"]
        image = batch["image_tensor"].to(self.device)
        image_features = self.model.encode_image(image)
        im_emb_arr = normalized(image_features.cpu().detach().numpy())
        image_embs = torch.from_numpy(im_emb_arr).to(self.device)
        if self.device == "cuda":
            image_embs = image_embs.type(torch.cuda.FloatTensor)
        return {
            "image_path": image_path,
            "image_embs": image_embs,
        }


class ImageDataset(Dataset):
    def __init__(
        self,
        preprocess,
        images,
    ):
        super().__init__()
        self.images = images
        self.preprocess = preprocess

    def __len__(self):
        return len(self.images)

    def __getitem__(self, ind):
        image_path = self.images[ind]
        output = {}
        try:
            image_tensor = self.preprocess(Image.open(image_path))
        except Exception as e:
            image_tensor = self.preprocess(Image.new("RGB", (256, 256)))
            print(f"load image error: {image_path}, {str(e)}")
        output["image_path"] = image_path
        output["image_tensor"] = image_tensor
        return output


def collate_fn(batch):
    batch = list(filter(lambda x: x["image_tensor"] is not None, batch))
    if len(batch):
        return default_collate(batch)
    return {"image_path": [], "image_tensor": None}


def dataset_to_dataloader(dataset, batch_size, num_workers):
    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
        prefetch_factor=2,
        collate_fn=collate_fn,
    )
    return dataloader


class ImageReader:
    def __init__(self, processor, images, batch_size, num_workers):
        super().__init__()
        dataset = ImageDataset(processor, images)
        self.dataloader = dataset_to_dataloader(dataset, batch_size, num_workers)

    def __iter__(self):
        for batch in self.dataloader:
            yield batch


class CLIPEmbedder:
    def __init__(self, clip_model, device):
        model, preprocess = clip.load(clip_model, device=device)
        self.model = model
        self.preprocess = preprocess
        self.device = device

    def get_embed(self, pil_image: Image):
        image = self.preprocess(pil_image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            image_features = self.model.encode_image(image)
        im_emb_arr = normalized(image_features.cpu().detach().numpy())
        return torch.from_numpy(im_emb_arr).to(self.device).type(torch.cuda.FloatTensor)
