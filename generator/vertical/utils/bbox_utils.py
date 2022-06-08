# bbox_utils.py
"""
bbox 생성 및 영역 범위 내에 존재하는지 확인하는 모듈입니다. 
"""
import random
from generate import *
from .card_utils import *
from PIL import ImageFont
from typing import Tuple, List, Dict


#####################
### make function ###
#####################


def make_bbox(font, start: Tuple, content: str) -> List:
    """
    주어진 시작 지점을 토대로, bbox 좌표 리스트를 만듭니다.

    Args:
        font : 텍스트에 대한 폰트 정보
        start (Tuple): 텍스트 bbox 시작 지점 (bbox의 좌측 상단)
        content (str): 텍스트 내용

    Returns:
        points (List): bbox 좌표
    """

    w, h = font.getsize(content)
    x, y = start

    points = [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]

    return points


#######################
### change function ###
#######################


def change_font_size(
    item_type: str,
    content: str,
    mode: str,
    x: int,
    x_limit: int,
    font_size: Dict,
    font_family: Dict,
    width: int,
) -> Tuple:
    """
    텍스트가 정보 box의 영역을 벗어나는 경우,
    폰트 크기를 줄여서 텍스트가 정보 box 영역 내부로 들어오도록 만듭니다.

    Args:
        item_type (str): 해당 카테고리의 이름
        content (str): 해당 카테고리의 텍스트 내용
        mode (str): 정보 box의 정렬 mode (left/center/right)
        x (int): 정보 box의 시작 x좌표
        x_limit (int): 정보 box가 존재할 수 있는 범위 중 좌상단 x좌표
        font_size (Dict): 명함 내 정보의 글씨 크기 정보를 저장
        font_family (Dict): 명함 내 정보의 글씨체 정보를 저장
        width (int): 명함 이미지의 너비

    Returns:
        Tuple: 항목 적용 여부, 적용된 글씨 크기
    """

    font_scale = font_size[item_type]

    while True:
        font_scale -= 1
        font = ImageFont.truetype(font_family[item_type], font_scale)
        bbox_width, bbox_height = font.getsize(content)

        if mode in ["center", "left"] and x > 0 and x + bbox_width < width:
            return True, font_scale

        if mode == "right" and x > 0 and x + bbox_width < width and x_limit <= x:
            return True, font_scale

        if (
            font_scale < font_size[item_type] * 0.5
        ):  # 최소한의 크기를 넘지 못하면, 해당 항목을 명함 이미지에 적용하지 않음
            return False, 0


def change_content(
    item_type: str, mode: str, x: int, x_limit: int, font, width: int
) -> Tuple:
    """
    텍스트가 정보 box의 영역을 벗어나는 경우,
    텍스트 내용을 변경하여 텍스트가 정보 box 영역 내부로 들어오도록 만듭니다.
    (단, 직책 및 부서가 동시에 포함되는 경우,
    두 가지 카테고리를 모두 고려해야 하므로 함수를 따로 생성했습니다.)

    Args:
        item_type (str): 해당 카테고리의 이름
        mode (str): 정보 box의 정렬 mode (left/center/right)
        x (int): 정보 box의 시작 x좌표
        x_limit (int): 정보 box가 존재할 수 있는 범위 중 좌상단 x좌표
        font: 텍스트에 대한 폰트 정보
        width (int): 명함 이미지의 너비

    Returns:
        Tuple: 항목 적용 여부, 적용된 텍스트 내용
    """

    content = regenerate(item_type)
    bbox_width, bbox_height = font.getsize(content)

    if mode in ["center", "left"] and x > 0 and x + bbox_width < width:
        return True, content

    if mode == "right" and x > 0 and x + bbox_width < width and x_limit <= x:
        return True, content

    # 텍스트 내용을 변경해도 정보 box 영역을 벗어날 경우, 해당 항목을 명함 이미지에 적용하지 않음
    return False, content


def change_dep_pos(
    start: Tuple, sep: str, mode: str, x_limit: int, font, width: int
) -> Tuple:
    """
    직책 및 부서의 텍스트가 정보 box의 영역을 벗어나는 경우,
    텍스트 내용을 변경하여 텍스트가 정보 box 영역 내부로 들어오도록 만듭니다.

    Args:
        start (Tuple): 텍스트 bbox의 시작 x 좌표, y 좌표
        sep (str): 직책과 부서를 구분하는 구분자
        mode (str): 정보 box의 정렬 mode (left/center/right)
        x_limit (int): 정보 box가 존재할 수 있는 범위 중 좌상단 x좌표
        font: 텍스트에 대한 폰트 정보
        width (int): 명함 이미지의 너비

    Returns:
        Tuple: 항목 적용 여부, 적용된 부서 텍스트 내용, 적용된 구분자 텍스트 내용, 적용된 직책 텍스트 내용
    """

    info = generate()
    department, position = info["department"], info["position"]
    content = department + " " + sep + " " + position
    if mode == "left":
        x, y = start[0], start[1]
    elif mode == "right":
        x, y = start[0] - font.getsize(content)[0], start[1]
    elif mode == "center":
        x, y = start[0] - font.getsize(content)[0] // 2, start[1]

    bbox_width, bbox_height = font.getsize(content)

    if mode in ["center", "left"] and x >= 0 and x + bbox_width <= width:
        return True, department, sep, position

    if mode == "right" and x >= 0 and x + bbox_width <= width and x_limit <= x:
        return True, department, sep, position

    # 텍스트 내용을 변경해도 정보 box 영역을 벗어날 경우, 해당 항목을 명함 이미지에 적용하지 않음
    return False, department, sep, position


############################
### define bbox function ###
############################


def define_bbox(
    start: Tuple,
    mode: str,
    content: str,
    item_type: str,
    x_limit: int,
    font_size: Dict,
    font_family: Dict,
    width: int,
) -> Tuple:
    """
    텍스트 bbox를 생성합니다.
    (단, 직책 및 부서가 동시에 포함되는 경우,
    두 가지 카테고리를 모두 고려해야 하므로 함수를 따로 생성했습니다.)

    Args:
        start (Tuple): 텍스트 bbox의 시작 x 좌표, y 좌표
        mode (str): 정보 box의 정렬 mode (left/center/right)
        content (str): 해당 카테고리의 텍스트 내용
        item_type (str): 해당 카테고리의 이름
        x_limit (int): 정보 box가 존재할 수 있는 범위 중 좌상단 x좌표
        font_size (Dict): 명함 내 정보의 글씨 크기 정보를 저장
        font_family (Dict): 명함 내 정보의 글씨체 정보를 저장
        width (int): 명함 이미지의 너비

    Returns:
        Tuple: 텍스트 bbox의 시작 지점, 텍스트 내용, 텍스트의 글씨 크기
    """

    font = ImageFont.truetype(font_family[item_type], font_size[item_type])
    font_scale = font_size[item_type]

    if mode == "left":
        x, y = start[0], start[1]
    elif mode == "right":
        x, y = start[0] - font.getsize(content)[0], start[1]
    elif mode == "center":
        x, y = start[0] - font.getsize(content)[0] // 2, start[1]

    bbox_width, bbox_height = font.getsize(content)
    if mode in ["center", "left"] and x > 0 and x + bbox_width < width:
        return (x, y), content, font_scale

    if mode == "right" and x > 0 and x + bbox_width < width and x_limit <= x:
        return (x, y), content, font_scale

    # 글씨 크기 변경
    check, font_scale = change_font_size(
        item_type, content, mode, x, x_limit, font_size, font_family, width
    )
    if check is True:
        return (x, y), content, font_scale

    # 내용 변경
    font = ImageFont.truetype(font_family["position"], font_scale)
    check, content = change_content(item_type, mode, x, x_limit, font, width)
    if check is True:
        return (x, y), content, font_scale
    else:
        return (x, y), content, 0  # font_scale = 0


def define_dep_pos_bbox(
    info: Dict,
    start: Tuple,
    mode: str,
    x_limit: int,
    font_size: Dict,
    font_family: Dict,
    width: int,
) -> Tuple:
    """
    직책 및 부서에 대해, 텍스트 bbox를 생성합니다.

    Args:
        info (Dict): 명함 데이터 생성에 필요한 카테고리 이름과 텍스트 내용을 저장
        start (Tuple): 텍스트 bbox의 시작 x 좌표, y 좌표
        mode (str): 정보 box의 정렬 mode (left/center/right)
        x_limit (int): 정보 box가 존재할 수 있는 범위 중 좌상단 x좌표
        font_size (Dict): 명함 내 정보의 글씨 크기 정보를 저장
        font_family (Dict): 명함 내 정보의 글씨체 정보를 저장
        width (int): 명함 이미지의 너비

    Returns:
        Tuple: 텍스트 bbox의 시작 지점, 부서 텍스트 내용, 구분자 텍스트 내용, 직책 텍스트 내용, 텍스트의 글씨 크기
    """

    sep = position_separator()
    font = ImageFont.truetype(font_family["position"], font_size["position"])
    font_scale = font_size["position"]

    department, position = info["department"], info["position"]
    content = department + " " + sep + " " + position
    if mode == "left":
        x, y = start[0], start[1]
    elif mode == "right":
        x, y = start[0] - font.getsize(content)[0], start[1]
    elif mode == "center":
        x, y = start[0] - font.getsize(content)[0] // 2, start[1]

    bbox_width, bbox_height = font.getsize(content)
    if mode in ["center", "left"] and x >= 0 and x + bbox_width <= width:
        return (x, y), department, sep, position, font_scale

    if mode == "right" and x >= 0 and x + bbox_width <= width and x_limit <= x:
        return (x, y), department, sep, position, font_scale

    # 글씨 크기 변경
    check, font_scale = change_font_size(
        "department", content, mode, x, x_limit, font_size, font_family, width
    )
    if check is True:
        return (x, y), department, sep, position, font_scale

    # 내용 변경
    font = ImageFont.truetype(font_family["position"], font_scale)
    check, department, sep, position = change_dep_pos(
        start, sep, mode, x_limit, font, width
    )
    if check is True:
        return (x, y), department, sep, position, font_scale
    else:
        return (x, y), department, sep, position, 0  # font_scale = 0


def define_num_bbox(
    start: Tuple,
    content: str,
    item_type: str,
    mode: str,
    font_size: Dict,
    font_family: Dict,
    width: int,
) -> Tuple:
    """
    핸드폰 번호 등 부가 정보에 대해, 텍스트 bbox를 생성합니다.

    Args:
        start (Tuple): 텍스트 bbox의 시작 x 좌표, y 좌표
        content (str): 해당 카테고리의 텍스트 내용
        item_type (str): 해당 카테고리의 이름
        mode (str): 정보 box의 정렬 mode (left/center/right)
        font_size (Dict): 명함 내 정보의 글씨 크기 정보를 저장
        font_family (Dict): 명함 내 정보의 글씨체 정보를 저장
        width (int): 명함 이미지의 너비

    Returns:
        Tuple: 텍스트 bbox의 시작 지점, 카테고리 이름 + 구분자 + 부가 정보의 텍스트 내용, 텍스트의 글씨 크기
    """

    sep = num_separator()
    font_scale = font_size[item_type]

    if item_type == "license_number":
        item_name = "사업자등록번호" + sep
    elif item_type == "social_id":
        social = [
            "kakao",
            "Kakao",
            "instagram",
            "Instagram",
            "youtube",
            "Youtube",
            "facebook",
            "Facebook",
        ]
        random_index = random.randint(0, len(social) - 1)
        item_name = social[random_index] + sep
    else:
        item_name = item_type + sep

    # 부가 정보의 특성 상 내용을 변경했을 때, 영역 내부로 들어올 가능성이 높다고 판단하여,
    # 다른 항목과 달리 내용 변경 후 글씨 크기를 바꾸는 과정을 한 번 더 거침
    check = True
    while True:
        font = ImageFont.truetype(font_family[item_type], font_scale)
        full_content = item_name + content
        bbox_width, bbox_height = font.getsize(full_content)

        if mode == "left":
            x, y = start[0], start[1]
        elif mode == "right":
            x, y = start[0] - bbox_width, start[1]
        elif mode == "center":
            x, y = start[0] - bbox_width // 2, start[1]

        if x > 0 and x + bbox_width < width:
            break
        else:
            # 두 바퀴에서도 False 인 경우
            if check is False:
                return (x, y), full_content, 0

            # 폰트 크기 변경
            check, font_scale = change_font_size(
                item_type, full_content, mode, x, 0, font_size, font_family, width
            )

            if check is True:
                break
            # 내용 변경
            content = regenerate(item_type)

    return (x, y), full_content, font_scale
