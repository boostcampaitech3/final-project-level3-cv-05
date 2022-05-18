"""
Feature Engineerin을 위한 유틸리티 함수 들을 모아놓은 모듈

Functions:
    _read_json(path: str): 
"""

import json
from typing import List
import pandas as pd

def _read_json(path: str) -> dict:
    with open(path, 'r', encoding = 'utf-8') as f:
        info = json.load(f)
    return info


def _json_to_dataframe(info: dict, pre_features: List[str]) -> pd.DataFrame:
    image_len = len(info['images'])
    df_result = pd.DataFrame(columns = pre_features)

    for idx in range(image_len):
        image_id = info['annotations'][idx]['image_id']
        words = info['annotations'][idx]['ocr']['word']
        temp_dict = {}
        
        for word in words:
            category_id = word['category_id']
            points = word['points']
            orientation = word['orientation']
            text = word['text']
            temp_dict = {
                'image_id' : image_id,
                'category_id' : category_id,
                'points' : [points],
                'orientation' : orientation,
                'text' : text
            }
            df_result = pd.concat([df_result, pd.DataFrame(temp_dict)])
    
    return df_result


def convert_to_dataframe(paths: List[str], pre_features: List[str]) -> pd.DataFrame:
    
    df_infos = []
    for path in paths:
        json_info = _read_json(path)
        df_info = _json_to_dataframe(json_info, pre_features)
        df_infos.append(df_info)

    df_result = pd.concat(df_infos)
    return df_result
