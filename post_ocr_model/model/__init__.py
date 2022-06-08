from typing import Dict

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
import yaml
from PIL import Image

from .dataset import get_transform
from .feature_engineering import tab_process
from .model import PostOCRLearner


def get_model(checkpoint_path: str = None, config_path: str = None) -> PostOCRLearner:
    with open(config_path, 'rb') as f:
        cfg = yaml.safe_load(f)
    model = PostOCRLearner(cfg)
    model.load_state_dict(torch.load(checkpoint_path)['state_dict'])
    return model


def inference(post_ocr_model: PostOCRLearner, image, margin: int, json_data: Dict, device):
    post_ocr_model.eval().to(device)
    feature_df = tab_process(json_data)
    data = test_loader(feature_df, image, margin)
    ret = torch.empty(0, 11)
    for image, ret_data in data:
        pred = post_ocr_model(image.unsqueeze(dim=0).to(device),
                              ret_data.unsqueeze(dim=0).to(device)).cpu().detach()
        p, m = torch.max(F.softmax(pred), 1)
        print(p, m)
        ret = torch.vstack([ret, F.softmax(pred)])
    return ret.numpy()


def test_loader(feature_df: pd.DataFrame, image, margin):
    ret = []
    transform = get_transform()['val']
    height, width, _ = image.shape
    for df_row in feature_df.iloc:
        p1, p3 = df_row['point_1'], df_row['point_3']
        n_p1 = [int(max(p1[0] - margin, 0)), int(max(p1[1] - margin, 0))]
        n_p3 = [int(min(p3[0] + margin, width - 1)), int(min(p3[1] + margin, height - 1))]
        crop_image = image[n_p1[1]:n_p3[1], n_p1[0]:n_p3[0]]
        crop_image = Image.fromarray(crop_image)
        crop_image = transform(crop_image)
        df_row = df_row.drop(labels=['category_id', 'point_1', 'point_2', 'point_3', 'point_4', 'text', 'file_name'])
        ret_data = torch.from_numpy(df_row.values.astype(np.float32))
        ret.append((crop_image, ret_data))
    return np.array(ret)
