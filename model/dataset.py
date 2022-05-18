import json
import torch
import os
from torch.utils.data import Dataset, DataLoader
from pytorch_lightning import LightningDataModule
import torchvision.transforms as transform
from typing import List, Dict, Union
from functools import partial
import cv2
import numpy as np


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


class PostTabProcess:
    def __init__(self):
        pass

    def __call__(self, target_data: Dict, tabs: Union[List, Dict]) -> np.ndarray:
        return np.array(tabs)


class PostOCRDataset(Dataset):
    def __init__(self, data_dir: str,
                 json_dir: str,
                 transforms: transform = None,
                 tab_process: PostTabProcess = None,
                 margin: int = 3):
        self.data_dir = data_dir
        with open(json_dir, "rb") as f:
            json_data = json.load(f)
        self.data = get_annotations(json_data['annotations'])
        self.group_data = json_data['annotations']
        self.image_data = json_data['images']
        self.transform = transforms
        self.tab_process = tab_process
        self.margin = margin

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        data = self.data[index]
        group_data = self.group_data[data['image_id']]
        image_info = self.image_data[data['image_id']]
        image = cv2.imread(os.path.join(self.data_dir, image_info['file']))

        p1, p2, p3, p4 = data['points']
        image = image[p1[0]:p4[0], p1[1]:p4[1]]

        label = data['category_id']
        if self.transform:
            image = self.transform(image)
        if self.tab_process:
            data = self.tab_process(data, group_data)

        return image, data, label


class PostOCRDataLoader(LightningDataModule):
    pass
