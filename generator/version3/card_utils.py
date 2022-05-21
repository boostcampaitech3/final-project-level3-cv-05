# card_utils.py
"""
글씨 정보, 구분자, 명함에 적용할 정보 생성 및 확인, bbox 생성 및 확인에 관한 모듈입니다. 

Functions:
    # 1) font functions
    make_font_size(): 각 정보 항목별 글씨 크기를 지정합니다.
    make_font_color(): 각 정보 항목별 글씨 색상을 지정합니다.
    make_font_family(): 각 정보 항목별 글씨체를 지정합니다.

    # 2) separator functions
    num_separator(): 숫자 및 기타 정보 문자열의 구분자를 지정합니다.
    position_separator(): 직책 및 부서 문자열의 구분자를 지정합니다. 

    # 3) info generate functions
    use_item(items, threshold): 선택 후보가 되는 정보 항목의 이름 리스트를 전달하면, 
                                그 중에서 사용할 항목 이름을 랜덤으로 선택하여 리스트로 반환합니다.
    info_item(info, use): 정보 항목의 이름 리스트를 전달하면, 
                          각 항목에 해당하는 텍스트 내용을 딕셔너리에 담아서 반환합니다.
    regenerate(item_name): 정보 항목의 이름을 전달하면, 
                           이 항목에 해당하는 텍스트 내용을 다시 생성하여 반환합니다.

    # 4) bbox functions
    check_bbox(bbox_points): bbox가 이미지 영역 안에 존재하는지 확인합니다.
    make_bbox(font, start, content): 주어진 시작 지점을 토대로, bbox 좌표 리스트를 만듭니다.
 
"""

import glob
import random
from generate import generate
import pandas as pd

from typing import Dict, Tuple, List

# 글씨체 파일의 경로
sub_font_dir = f"font/sub"
main_font_dir = f"font/main"
sub_font_families = glob.glob(f"{sub_font_dir}/*.ttf")
main_font_families = glob.glob(f"{main_font_dir}/*.ttf")

# 컬러맵 파일의 경로
colormap = pd.read_csv("data/colormap.csv")


def make_font_size() -> Dict[str, str]:
    """
    각 정보 항목별 글씨 크기를 지정합니다.

    Returns:
        font_size (dict): 각 정보 항목별 글씨 크기
    """
    font_size = dict()
    font_size["name"] = random.randint(40, 50)
    font_size["phone"] = font_size["tel"] = font_size["website"] \
        = font_size["license_number"] = font_size["fax"] = font_size["email"] \
        = font_size["address"] = random.randint(15, 20)
    font_size["position"] = font_size["department"] = random.randint(20, 30)
    font_size["company"] = random.randint(60, 70)
    font_size["wise"] = random.randint(15, 20)
    return font_size


def make_font_color() -> Tuple[str, dict]:
    """
    각 정보 항목별 글씨 색상을 지정합니다.

    Returns:
        Color_BG (str), font_color (dict): 명함 이미지 배경색, 각 정보 항목별 글씨 색상
    """
    font_color = dict()

    c_id = random.randint(0, len(colormap) - 1)
    Color_BG, Color_Logo, Color_Main, Color_Sub = (
        colormap["Color_BG"][c_id],
        colormap["Color_Logo"][c_id],
        colormap["Color_Main"][c_id],
        colormap["Color_Sub"][c_id],
    )

    font_color["name"] = font_color["company"] = Color_Main
    font_color["phone"] = font_color["tel"] = font_color["website"] \
        = font_color["license_number"] = font_color["fax"] = font_color["email"] \
        = font_color["address"] = font_color["position"] \
        = font_color["department"] = font_color["wise"] = font_color["UNKNOWN"] \
        = Color_Sub
    return Color_BG, font_color


def make_font_family() -> Dict[str, str]:
    """
    각 정보 항목별 글씨체를 지정합니다.

    Returns:
        font_family (dict): 각 정보 항목별 글씨체
    """
    font_family = dict()

    sub_length = len(sub_font_families)
    main_length = len(main_font_families)

    font_family["name"] = main_font_families[random.randint(0, main_length - 1)]
    font_family["phone"] = font_family["tel"] = font_family["website"] \
        = font_family["license_number"] = font_family["fax"] = font_family["email"] \
        = font_family["address"] = sub_font_families[random.randint(0, sub_length - 1)]
    font_family["position"] = font_family["department"] = sub_font_families[random.randint(0, sub_length - 1)]
    font_family["company"] = main_font_families[random.randint(0, main_length - 1)]
    font_family["wise"] = sub_font_families[random.randint(0, sub_length - 1)]
    return font_family


def num_separator() -> str:
    """
    숫자 및 기타 정보 문자열의 구분자를 지정합니다.

    Returns:
        item (str): 사용할 구분자
    """
    if random.random() > 0.7:
        item = ". "
    elif random.random() > 0.4:
        item = " "
    else:
        item = ": "
    return item


def position_separator() -> str:
    """
    직책 및 부서 문자열의 구분자를 지정합니다.

    Returns:
        item (str): 사용할 구분자
    """
    if random.random() > 0.5:
        item = " | "
    else:
        item = " / "
    return item


def use_item(items: List[str], threshold: float) -> List[str]:
    """
    선택 후보가 되는 정보 항목의 이름 리스트를 전달하면,
    그 중에서 사용할 항목을 랜덤으로 선택하여 리스트로 반환합니다.

    Args:
        items (list): 선택 후보가 되는 정보 항목의 이름 리스트
        threshold (float): 각 정보 항목이 선택될 확률

    Returns:
        use (list): 선택된 정보 항목의 이름 리스트
    """
    use = []
    for item in items:
        if random.random() < threshold:
            use.append(item)
    return use


def info_item(info: Dict[str, str], use: List[str]) -> Dict[str, str]:
    """
    정보 항목의 이름 리스트를 전달하면,
    각 항목에 해당하는 텍스트 내용을 딕셔너리에 담아서 반환합니다.

    Args:
        info (dict): 전체 정보를 저장하고 있는 딕셔너리
        use (list): 사용할 정보 항목의 이름 리스트

    Returns:
        content (dict): 사용할 정보 항목의 텍스트 내용을 담은 딕셔너리
    """
    content = dict()
    for item in use:
        content[item] = info[item]
    return content


def regenerate(item_name: str) -> str:
    """
    정보 항목의 이름을 전달하면,
    이 항목에 해당하는 텍스트 내용을 다시 생성하여 반환합니다.

    Args:
        item_name (str): 정보 항목의 이름

    Returns:
        content (str): 정보 항목에 해당하는 텍스트 내용
    """
    re_info = generate()
    content = re_info[item_name]
    return content


def check_bbox(bbox_points: List[Tuple[int, int]]) -> bool:
    """
    bbox가 이미지 영역 안에 존재하는지 확인합니다. (단, 테두리로부터 5의 간격을 둡니다.)

    Args:
        bbox_points (list): 확인할 bbox 좌표

    Returns:
        bool: 영역 안에 존재하면 Treu, 그렇지 않으면 False
    """
    condition_x = 5 < bbox_points[0][0] < 900 - 5 and 5 < bbox_points[1][0] < 900 - 5
    condition_y = 5 < bbox_points[0][1] < 500 - 5 and 5 < bbox_points[1][1] < 500 - 5

    if condition_x and condition_y:
        return True
    return False


def make_bbox(font, start: Tuple[int, int], content: str) -> List[Tuple[int, int]]:
    """
    주어진 시작 지점을 토대로, bbox 좌표 리스트를 만듭니다.

    Args:
        font : 사용한 글씨 정보
        start (tuple): 시작 지점 (bbox의 왼쪽 상단)
        content (str): 사용한 텍스트 내용

    Returns:
        points (list): bbox 좌표 리스트
    """
    w, h = font.getsize(content)
    x, y = start

    points = [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]
    return points
