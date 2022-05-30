from typing import Dict

import numpy as np
import pandas as pd
import torch
import yaml
from PIL import Image

from dataset import get_transform
from feature_engineering import tab_process
from .model import PostOCRLearner


def get_model(checkpoint_path: str = None, config_path: str = None) -> PostOCRLearner:
    with open(config_path, 'rb') as f:
        cfg = yaml.safe_load(f)
    model = PostOCRLearner(cfg)
    model.load_state_dict(torch.load(checkpoint_path)['state_dict'])
    return model


def inference(post_ocr_model: PostOCRLearner, image: Image, margin: int, json_data: Dict, device):
    feature_df = tab_process(json_data)
    data = test_loader(feature_df, image, margin)
    ret = []
    for image, ret_data in data:
        pred = post_ocr_model(image.unsqueeze(dim=0).to(device),
                              ret_data.unsqueeze(dim=0).to(device)).cpu().detach().numpy()
    return np.array(ret)


def test_loader(feature_df: pd.DataFrame, image, margin):
    ret = []
    for df_row in feature_df.iloc:
        p1, p3 = df_row['point_1'], df_row['point_3']
        p1 = [max(p1[0] - margin, 0), max(p1[1] - margin, 0)]
        p3 = [min(p3[0] + margin, 900 - 1), min(p3[1] + margin, 500 - 1)]
        image = image[p1[1]:p3[1], p1[0]:p3[0]]
        image = Image.fromarray(image)
        transform = get_transform()['val']
        image = transform(image)
        df_row = df_row.drop(labels=['category_id', 'point_1', 'point_2', 'point_3', 'point_4', 'text', 'file_name'])
        ret_data = torch.from_numpy(df_row.values.astype(np.float32))
        ret.append((image, ret_data))
    return ret
