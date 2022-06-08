# card_utils.py
"""
폰트 정보, 구분자, 명함에 적용할 정보 생성 및 확인에 관한 모듈입니다. 
"""

import glob
import random
import pandas as pd
from .json_utils import *
from generate import generate
from typing import Tuple, List, Dict

# 글씨체 파일의 경로
sub_font_dir = "../font/sub"
main_font_dir = "../font/main"
sub_font_families = glob.glob(f"{sub_font_dir}/*.ttf")
main_font_families = glob.glob(f"{main_font_dir}/*.ttf")

# 컬러맵 파일의 경로
colormap = pd.read_csv("../data/colormap.csv")


#####################
### make function ###
#####################


def make_font_size() -> Dict:
    """
    각 카테고리별 글씨 크기를 지정합니다.

    Returns:
        Dict: 각 카테고리별 글씨 크기
    """

    font_size = dict()
    font_size["name"] = random.randint(40, 50)
    font_size["phone"] = font_size["tel"] = font_size["website"] = font_size[
        "license_number"
    ] = font_size["fax"] = font_size["email"] = font_size["address"] = font_size[
        "social_id"
    ] = random.randint(
        15, 20
    )
    font_size["position"] = font_size["department"] = random.randint(20, 30)
    font_size["company"] = random.randint(60, 70)
    font_size["wise"] = random.randint(15, 20)

    return font_size


def make_font_color() -> Tuple:
    """
    각 카테고리별 글씨 색상을 지정합니다.

    Returns:
        Tuple: 명함 이미지 배경색, 각 카테고리별 글씨 색상
    """

    font_color = dict()

    c_id = random.randint(0, len(colormap) - 1)
    Color_BG, Color_Main, Color_Sub = (
        colormap["Color_BG"][c_id],
        colormap["Color_Main"][c_id],
        colormap["Color_Sub"][c_id],
    )

    font_color["name"] = font_color["company"] = Color_Main
    font_color["phone"] = font_color["tel"] = font_color["website"] = font_color[
        "license_number"
    ] = font_color["fax"] = font_color["email"] = font_color["address"] = font_color[
        "position"
    ] = font_color[
        "department"
    ] = font_color[
        "wise"
    ] = font_color[
        "UNKNOWN"
    ] = font_color[
        "social_id"
    ] = Color_Sub

    return Color_BG, font_color


def make_font_family() -> Dict:
    """
    각 카테고리별 글씨체를 지정합니다.

    Returns:
        Dict: 각 카테고리별 글씨체
    """

    font_family = dict()

    sub_length = len(sub_font_families)
    main_length = len(main_font_families)

    font_family["name"] = main_font_families[random.randint(0, main_length - 1)]
    font_family["phone"] = font_family["tel"] = font_family["website"] = font_family[
        "license_number"
    ] = font_family["fax"] = font_family["email"] = font_family[
        "address"
    ] = font_family[
        "social_id"
    ] = sub_font_families[
        random.randint(0, sub_length - 1)
    ]
    font_family["position"] = font_family["department"] = sub_font_families[
        random.randint(0, sub_length - 1)
    ]
    font_family["company"] = main_font_families[random.randint(0, main_length - 1)]
    font_family["wise"] = sub_font_families[random.randint(0, sub_length - 1)]

    return font_family


##########################
### separator function ###
##########################


def num_separator() -> str:
    """
    숫자 및 기타 정보 문자열의 구분자를 지정합니다.

    Returns:
        str: 사용할 구분자
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
        str: 사용할 구분자
    """

    if random.random() > 0.5:
        item = "|"
    else:
        item = "/"

    return item


#####################
### item function ###
#####################


def use_item(items: List, threshold: float) -> List:
    """
    선택 후보가 되는 카테고리의 이름 리스트를 전달하면,
    그 중에서 사용할 항목을 랜덤으로 선택하여 리스트로 반환합니다.

    Args:
        items (List): 선택 후보가 되는 카테고리의 이름 리스트
        threshold (float): 각 카테고리가 선택될 확률

    Returns:
        List: 선택된 카테고리의 이름
    """

    use = []
    for item in items:
        if random.random() < threshold:
            use.append(item)

    return use


def info_item(info: Dict, use: List) -> Dict:
    """
    카테고리의 이름 리스트를 전달하면,
    각 항목에 해당하는 텍스트 내용을 딕셔너리에 담아서 반환합니다.

    Args:
        info (Dict): 전체 정보를 저장하고 있는 딕셔너리
        use (List): 사용할 카테고리의 이름 리스트

    Returns:
        Dict: 사용할 카테고리의 텍스트 내용을 담은 딕셔너리
    """
    content = dict()
    for item in use:
        content[item] = info[item]

    return content


def regenerate(item_name: str) -> str:
    """
    카테고리의 이름을 전달하면,
    이 항목에 해당하는 텍스트 내용을 다시 생성하여 반환합니다.

    Args:
        item_name (str): 카테고리의 이름

    Returns:
        str: 카테고리에 해당하는 텍스트 내용
    """
    re_info = generate()
    content = re_info[item_name]

    return content


#############################
### draw & write function ###
#############################


def draw_and_write(
    start: Tuple,
    content: str,
    item: str,
    font,
    draw,
    font_color: Dict,
    word: List,
):
    """
    명함 이미지에 텍스트 내용을 작성하고,
    json 파일에 annotation 정보를 저장합니다.
    (단, 직책 및 부서가 동시에 포함되는 경우,
    두 가지 카테고리를 모두 고려해야 하므로 함수를 따로 생성했습니다.)

    Args:
        start (Tuple): 텍스트 bbox 시작 지점 (bbox의 좌측 상단)
        content (str): 해당 카테고리의 텍스트 내용
        item (str): 해당 카테고리의 이름
        font: 텍스트에 대한 폰트 정보
        draw: 이미지에 정보를 그리는 (표기하는) 객체
        font_color (Dict): 명함 내 정보의 글씨 색상 정보를 저장
        word (List): json 파일에 저장할 bbox 정보를 담은 리스트
    """

    draw.text(
        start,
        content,
        font=font,
        fill=font_color[item],
    )
    put_word(item, content.strip(), start, font, word)


def draw_dep_pos(
    start: Tuple,
    department: str,
    sep: str,
    position: str,
    font,
    draw,
    font_color: Dict,
    word: List,
):
    """
    명함 이미지에 '직책 및 부서'에 대한 텍스트 내용을 작성하고,
    json 파일에 annotation 정보를 저장합니다.

    Args:
        start (Tuple): 텍스트 bbox 시작 지점 (bbox의 좌측 상단)
        department (str): 부서 텍스트 내용
        sep (str): 구분자 텍스트 내용
        position (str): 직책 텍스트 내용
        font: 텍스트에 대한 폰트 정보
        draw: 이미지에 정보를 그리는 (표기하는) 객체
        font_color (Dict): 명함 내 정보의 글씨 색상 정보를 저장
        word (List): json 파일에 저장할 bbox 정보를 담은 리스트
    """

    item_list = [("department", department), ("position", position)]
    if random.random() >= 0.5:  # pos + dep 순서
        item_list = item_list[::-1]

    # department
    draw_and_write(
        start, item_list[0][1], item_list[0][0], font, draw, font_color, word
    )

    # sep
    draw_and_write(
        (
            start[0] + font.getsize(item_list[0][1])[0] + font.getsize(" ")[0],
            start[1],
        ),
        sep,
        "UNKNOWN",
        font,
        draw,
        font_color,
        word,
    )

    # position
    draw_and_write(
        (
            start[0]
            + font.getsize(item_list[0][1])[0]
            + font.getsize(" ")[0]
            + font.getsize(sep)[0]
            + font.getsize(" ")[0],
            start[1],
        ),
        item_list[1][1],
        item_list[1][0],
        font,
        draw,
        font_color,
        word,
    )


def put_word(item: str, content: str, start: Tuple, font, word: List) -> List:
    """
    json 파일에 저장할 bbox 정보를 담은 리스트인 word에,
    새로 추가하려는 카테고리의 bbox와 텍스트 내용을 추가합니다.

    Args:
        item (str): 해당 카테고리의 이름
        content (str): 해당 카테고리의 텍스트 내용
        start (Tuple): 텍스트 bbox 시작 지점 (bbox의 좌측 상단)
        font: 텍스트에 대한 폰트 정보
        word (List): json 파일에 저장할 bbox 정보를 담은 리스트

    Returns:
        List: json 파일에 저장할 bbox 정보를 담은 리스트
    """

    temp_word = dict()
    temp_word["category_id"] = get_category_id(item)
    temp_word["orientation"] = "Horizontal"
    temp_word["text"] = content

    text_width, text_height = int(font.getsize(content)[0]), int(
        font.getsize(content)[1]
    )
    start_x, start_y = int(start[0]), int(start[1])
    temp_word["points"] = [
        [start_x, start_y],
        [start_x + text_width, start_y],
        [start_x + text_width, start_y + text_height],
        [start_x, start_y + text_height],
    ]
    word.append(temp_word)

    return word
