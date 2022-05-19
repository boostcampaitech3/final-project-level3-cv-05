import json
import os
from functools import partial
from typing import List, Dict

import cv2
from PIL import Image
import torchvision.transforms as transform
from pytorch_lightning import LightningDataModule
from torch.utils.data import Dataset, DataLoader

import feature_engineering


def insert_image_id(word: Dict, image_id) -> Dict:
    word['image_id'] = image_id
    return word


def get_annotations(annotations: List) -> List[Dict]:
    annotation_list = []
    for annotation in annotations:
        cur_image_id = annotation['image_id']
        func = partial(insert_image_id, image_id=cur_image_id)
        words = annotation['ocr']['word']
        words = list(map(func, words))
        annotation_list.extend(words)
    return annotation_list


def get_transform():
    transforms = {
        "train": transform.Compose([
            transform.Resize((224, 224)),
            transform.ToTensor(),
            transform.Normalize(std=(50, 50, 50), mean=(50, 50, 50)),
        ]),
        "val": transform.Compose([
            transform.Resize((224, 224)),
            transform.ToTensor(),
            transform.Normalize(std=(50, 50, 50), mean=(50, 50, 50)),
        ])
    }
    return transforms


class PostOCRDataset(Dataset):
    def __init__(self, data_dir: str,
                 json_dir: str,
                 transforms: transform = None,
                 margin: int = 3):
        self.data_dir = data_dir
        self.data = feature_engineering.tab_process(json_dir)
        self.transform = transforms
        self.margin = margin

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        data = self.data.iloc[index]
        image = cv2.imread(os.path.join(self.data_dir, data["file_name"]))

        p1, p3 = data['point_1'], data['point_3']
        image = image[p1[1]-self.margin:p3[1]+self.margin, p1[0]-self.margin:p3[0]+self.margin]
        image = Image.fromarray(image)
        label = data['category_id']
        if self.transform:
            image = self.transform(image)

        # ret = {'image': image, "tabs": data.to_numpy()[6:]}
        ret_data = data.to_numpy()[6:].astype(float)
        return image, ret_data, label


class PostOCRDataLoader(LightningDataModule):
    def __init__(self, cfg, data_dir, train_json: str, val_json: str = None, test_json: str = None, margin=3):
        super().__init__()
        self.data_dir = data_dir
        self.train_json = train_json
        self.val_json = val_json
        self.test_json = test_json
        self.transform = get_transform()
        self.config = cfg
        self.margin = margin

    def train_dataloader(self):
        train_dataset = PostOCRDataset(self.data_dir, self.train_json, self.transform['train'], self.margin)
        return DataLoader(train_dataset, **self.config.Dataloader)

    def val_dataloader(self):
        val_dataset = PostOCRDataset(self.data_dir, self.val_json, self.transform['val'], self.margin)
        return DataLoader(val_dataset, **self.config.Dataloader)
