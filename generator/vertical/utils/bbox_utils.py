# bbox_utils.py
"""
글씨 정보, 구분자, 명함에 적용할 정보 생성 및 확인, bbox 생성 및 확인에 관한 모듈입니다. 

Functions:
    # 1) bbox functions
    make_bbox(font, start, content): 주어진 시작 지점을 토대로, bbox 좌표 리스트를 만듭니다.
 
"""
import random
from generate import *
from .card_utils import *
from typing import Tuple, List, Dict
from PIL import Image, ImageDraw, ImageFont


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
) -> Tuple[bool, int]:
    font_scale = font_size[item_type]
    while True:
        font_scale -= 1
        font = ImageFont.truetype(font_family[item_type], font_scale)
        bbox_width, bbox_height = font.getsize(content)
        if mode in ["center", "left"] and x > 0 and x + bbox_width < width:
            return True, font_scale
        if mode == "right" and x > 0 and x + bbox_width < width and x_limit <= x:
            return True, font_scale

        if font_scale < font_size[item_type] * 0.5:  # 최소한의 크기
            return False, 0


def change_content(
    item_type: str, mode: str, x: int, x_limit: int, font, width: int
) -> Tuple[bool, str]:
    content = regenerate(item_type)
    bbox_width, bbox_height = font.getsize(content)
    if mode in ["center", "left"] and x > 0 and x + bbox_width < width:
        return True, content
    if mode == "right" and x > 0 and x + bbox_width < width and x_limit <= x:
        return True, content
    return False, content


def change_dep_pos(
    start: Tuple[int, int], sep: str, mode: str, x_limit: int, font, width: int
) -> Tuple[bool, str, str, str]:
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
    return False, department, sep, position


############################
### define bbox function ###
############################


def define_bbox(
    start: Tuple[int, int],
    mode: str,
    content: str,
    item_type: str,
    x_limit: int,
    font_size: Dict,
    font_family: Dict,
    width: int,
):
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
    else:
        # 폰트 크기 변경
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
    info: Dict[str, str],
    start: Tuple[int, int],
    mode: str,
    x_limit: int,
    font_size: Dict,
    font_family: Dict,
    width: int,
):
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
    else:
        # 폰트 크기 변경
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
    start: Tuple[int, int],
    content: str,
    item_type: str,
    mode: str,
    font_size: Dict,
    font_family: Dict,
    width: int,
):
    sep = num_separator()
    font_scale = font_size[item_type]

    if item_type == "license_number":
        item_name = "사업자등록번호" + sep
    elif item_type == "social_id":
        social = ["kakao", "instagram", "youtube", "facebook"]
        random_index = random.randint(0, len(social) - 1)
        item_name = social[random_index] + sep
    else:
        item_name = item_type + sep

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
