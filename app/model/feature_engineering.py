"""
학습 시에 tabular type으로 사용할 data를 Feature Engineering하여 반환하는 모듈

Functions:
    tab_process(json_dir: str) : data를 Feature Engineering하여 반환하는 함수
"""

import pandas as pd
from tab_utils import convert_to_dataframe
from tab_transform import TabTransform
from typing import Dict


def tab_process(json_info: Dict) -> pd.DataFrame:
    """
    학습 시에 tabular type으로 사용할 data를 Feature Engineering하여 반환하는 함수

    Args:
        json_info (str): dat info를 담은 json data list

    Returns:
        pd.DataFrame: feature engineering 이 적용된 DataFrame
    """

    # info_paths = [DATA_DIR_HH + '/info.json', DATA_DIR_NY + '/info.json']
    info_list = [json_info]
    pre_features = ['file_name', 'image_width', 'image_height', 'category_id', 'points', 'point_1', 'point_2',
                    'point_3', 'point_4', 'orientation', 'text']

    df_namecard_pre = convert_to_dataframe(info_list, pre_features)
    tab_transform = TabTransform(df_namecard_pre)
    df_namecard_post = tab_transform.transform()

    return df_namecard_post
