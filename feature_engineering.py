"""
학습 시에 tabular type으로 사용할 data를 Feature Engineering하여 반환하는 모듈

Functions:
    tab_process(json_dir: str) : data를 Feature Engineering하여 반환하는 함수
"""

from typing import List
import numpy as np
from tab_utils import convert_to_dataframe
from tab_transform import TabTransform


# Set Path (Test 용 Path)
WORK_DIR = "/mnt/d/sjeon/BoostCamp_AI_Tech/main_course/Project/workspace/local"
DATA_DIR_HH = WORK_DIR + '/sample_data_HH'
DATA_DIR_NY = WORK_DIR + '/sample_data_NY'


def tab_process(json_dir: str) -> List[np.numpy]:
    """
    학습 시에 tabular type으로 사용할 data를 Feature Engineering하여 반환하는 함수

    Args:
        json_dir (str): dat info를 담은 json 파일의 path

    Returns:
        List[np.numpy]: feature engineering 이 적용된 numpy 자료형 List
    """

    info_paths = [DATA_DIR_HH + '/info.json', DATA_DIR_NY + '/info.json']
    # info_paths = json_dir
    pre_features = ['image_id', 'category_id', 'points', 'orientation', 'text']

    df_namecard_pre = convert_to_dataframe(info_paths, pre_features)
    tab_transform = TabTransform(df_namecard_pre)
    df_namecard_post = tab_transform.transform()
    tab_data = df_namecard_post.to_numpy()

    print(tab_data) # test

    return tab_data

tab_process('test')
