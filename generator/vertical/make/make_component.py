# make_component.py
"""
정보 box 생성에 관한 모듈입니다. 
"""

import glob
import random
import pandas as pd
from utils.card_utils import *
from utils.bbox_utils import *
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Tuple

# 정보 box의 정렬 mode
loc = ["center", "right", "left"]

# 정보 box의 시작 x, y 좌표 범위
MIN_X, MAX_X, MIN_Y, MAX_Y = 0.05, 0.1, 0, 0.05


##########################
## start point function ##
##########################


def start(mode: str, bbox_x: int, bbox_y: int, width: int):
    """
    정보 box의 시작점 (x, y)를 반환합니다.

    Args:
        mode (str): box의 정렬 mode (left/center/right)
        bbox_x (int): 정보 box의 시작 x좌표
        bbox_y (int): 정보 box의 시작 y좌표
        width (int): 명함 이미지의 너비

    Returns:
        Dict: 각 mode에 대한 시작 지점을 저장
    """
    start = dict()
    start["left"] = (bbox_x, bbox_y)
    start["center"] = (
        width // 2 + width * random.uniform(-MIN_X, MIN_X),
        bbox_y,
    )
    start["right"] = (width - width * random.uniform(0, MIN_X), bbox_y)
    start = start[mode]

    return start


#####################
## component class ##
#####################


class OneItemTemplate:
    """
    회사명(company), 이름(name), 직책(position), 부서(department)에 대한 정보 box 생성
    (단, 직책 및 부서가 함께 있지 않고, 둘 중 하나만 존재하는 경우)

    Returns:
        Tuple: 정보 box의 끝 지점 (bbox 우측 하단)
    """

    def __init__(
        self,
        info: Dict[str, str],
        item_type: str,
        x: int,
        y: int,
        mode: str,
        width: int,
        height: int,
        image,
        font_family: Dict,
        font_size: Dict,
        font_color: Dict,
        word: List,
    ):
        self.items = info
        self.type = item_type
        self.bbox_x = x
        self.bbox_y = y
        self.mode = mode
        self.width = width
        self.height = height
        self.image = image
        self.font_family = font_family
        self.font_size = font_size
        self.font_color = font_color
        self.word = word
        self.start = start(self.mode, self.bbox_x, self.bbox_y, self.width)

    def make(self):
        draw = ImageDraw.Draw(self.image)
        content = self.items[self.type]

        self.start, content, font_scale = define_bbox(
            self.start,
            self.mode,
            content,
            self.type,
            self.bbox_x,
            self.font_size,
            self.font_family,
            self.width,
        )

        font = ImageFont.truetype(self.font_family[self.type], font_scale)
        bbox_x, bbox_y = self.start
        bbox_width, bbox_height = font.getsize(content)

        if (
            bbox_y + bbox_height > self.height or font_scale == 0
        ):  # y좌표가 범위를 벗어나는 경우, or 폰트 크기가 일정값 이하인 경우 제외
            return (bbox_x, bbox_y)

        draw_and_write(
            self.start, content, self.type, font, draw, self.font_color, self.word
        )

        return (bbox_x + bbox_width, bbox_y + bbox_height)


class TwoItemsTemplate:
    """
    직책(position)과 부서(department)가 동시에 존재하는 정보 box 생성

    Returns:
        Tuple: 정보 box의 끝 지점 (bbox 우측 하단)
    """

    def __init__(
        self,
        items: Dict[str, str],
        x: int,
        y: int,
        mode: str,
        width: int,
        height: int,
        image,
        font_family: Dict,
        font_size: Dict,
        font_color: Dict,
        word: List,
    ):
        self.items = items
        self.bbox_x = x
        self.bbox_y = y
        self.mode = mode
        self.width = width
        self.height = height
        self.image = image
        self.font_family = font_family
        self.font_size = font_size
        self.font_color = font_color
        self.word = word
        self.start = start(self.mode, self.bbox_x, self.bbox_y, self.width)

    def make(self):
        draw = ImageDraw.Draw(self.image)

        self.start, department, sep, position, font_scale = define_dep_pos_bbox(
            self.items,
            self.start,
            self.mode,
            self.bbox_x,
            self.font_size,
            self.font_family,
            self.width,
        )

        font = ImageFont.truetype(self.font_family["position"], font_scale)
        bbox_x, bbox_y = self.start
        bbox_width, bbox_height = font.getsize(department + " " + sep + " " + position)

        if (
            bbox_y + bbox_height > self.height or font_scale == 0
        ):  # y좌표가 범위를 벗어나는 경우, or 폰트 크기가 일정값 이하인 경우, 제외
            return (bbox_x, bbox_y)

        draw_dep_pos(
            self.start,
            department,
            sep,
            position,
            font,
            draw,
            self.font_color,
            self.word,
        )

        return (bbox_x + bbox_width, bbox_y + bbox_height)


class NumTemplate:
    """
    핸드폰 번호, 팩스 번호, 이메일 주소 등 부가 정보 box 생성

    Returns:
        Tuple: 정보 box의 끝 지점 y 좌표 (bbox 우측 하단), 각 정보 box 사이의 높이 간격
    """

    def __init__(
        self,
        items: Dict[str, str],
        x: int,
        y: int,
        mode: str,
        width: int,
        height: int,
        image,
        font_family: Dict,
        font_size: Dict,
        font_color: Dict,
        word: List,
    ):
        self.items = items
        self.bbox_x = x
        self.bbox_y = y
        self.mode = mode
        self.width = width
        self.height = height
        self.image = image
        self.font_family = font_family
        self.font_size = font_size
        self.font_color = font_color
        self.word = word
        self.start = start(self.mode, self.bbox_x, self.bbox_y, self.width)

    def make(self):
        draw = ImageDraw.Draw(self.image)
        y_margin = self.height * random.uniform(MIN_Y, MAX_Y)
        random_items = list(self.items.keys())
        random.shuffle(random_items)

        for item in random_items:
            item_name, content = item, self.items[item]

            # bbox 영역이 범위 내에 존재하는지 확인
            item_bbox, content, font_scale = define_num_bbox(
                (self.start[0], self.start[1] + y_margin),
                content,
                item,
                self.mode,
                self.font_size,
                self.font_family,
                self.width,
            )

            font = ImageFont.truetype(self.font_family[item_name], font_scale)
            num_height = item_bbox[1] + font.getsize(content)[1]

            # 숫자 및 기타 정보가 다른 정보의 높이를 넘어가는지 확인
            if font_scale == 0:
                num_height = self.start[1]
            else:
                if num_height <= self.height:
                    draw_and_write(
                        item_bbox, content, item, font, draw, self.font_color, self.word
                    )
                else:
                    num_height = self.start[1]
                    break

            self.start = self.start[0], num_height

        return num_height, y_margin


########################
## component function ##
########################


def company(
    info: Dict,
    x: int,
    y: int,
    width: int,
    height: int,
    image,
    font_family: Dict,
    font_size: Dict,
    font_color: Dict,
    word: List,
) -> Tuple:
    """
    회사명에 대한 box를 생성하고, 이를 명함 이미지에 적용합니다.

    Args:
        info (Dict): 명함 데이터 생성에 필요한 카테고리 이름과 텍스트 내용을 저장
        x (int): 정보 box가 존재할 수 있는 범위 중 좌상단 x좌표
        y (int): 정보 box가 존재할 수 있는 범위 중 좌상단 y좌표
        width (int): 명함 이미지의 너비
        height (int): 명함 이미지의 높이
        image: 명함 이미지 객체
        font_family (Dict): 명함 내 정보의 글씨체 정보를 저장
        font_size (Dict): 명함 내 정보의 글씨 크기 정보를 저장
        font_color (Dict): 명함 내 정보의 글씨 색상 정보를 저장
        word (List): json 파일에 저장할 bbox 정보를 담은 리스트

    Returns:
        Tuple: 만들어진 정보 box의 끝 지점 (bbox 우측 하단)
    """

    index = random.randint(0, len(loc) - 1)
    x, y = OneItemTemplate(
        info,
        "company",
        x,
        y,
        loc[index],
        width,
        height,
        image,
        font_family,
        font_size,
        font_color,
        word,
    ).make()

    return x, y


def name(
    info: Dict,
    x: int,
    y: int,
    width: int,
    height: int,
    image,
    font_family: Dict,
    font_size: Dict,
    font_color: Dict,
    word: List,
) -> Tuple:
    """
    이름에 대한 box를 생성하고, 이를 명함 이미지에 적용합니다.

    Args:
        info (Dict): 명함 데이터 생성에 필요한 카테고리 이름과 텍스트 내용을 저장
        x (int): 정보 box가 존재할 수 있는 범위 중 좌상단 x좌표
        y (int): 정보 box가 존재할 수 있는 범위 중 좌상단 y좌표
        width (int): 명함 이미지의 너비
        height (int): 명함 이미지의 높이
        image: 명함 이미지 객체
        font_family (Dict): 명함 내 정보의 글씨체 정보를 저장
        font_size (Dict): 명함 내 정보의 글씨 크기 정보를 저장
        font_color (Dict): 명함 내 정보의 글씨 색상 정보를 저장
        word (List): json 파일에 저장할 bbox 정보를 담은 리스트

    Returns:
        Tuple: 만들어진 정보 box의 끝 지점 (bbox 우측 하단)
    """

    index = random.randint(0, len(loc) - 1)
    x, y = OneItemTemplate(
        info,
        "name",
        x,
        y,
        loc[index],
        width,
        height,
        image,
        font_family,
        font_size,
        font_color,
        word,
    ).make()

    return x, y


def dep_pos(
    info: Dict,
    x: int,
    y: int,
    width: int,
    height: int,
    image,
    font_family: Dict,
    font_size: Dict,
    font_color: Dict,
    word: List,
) -> Tuple:
    """
    직책 및 부서에 대한 box를 생성하고, 이를 명함 이미지에 적용합니다.

    Args:
        info (Dict): 명함 데이터 생성에 필요한 카테고리 이름과 텍스트 내용을 저장
        x (int): 정보 box가 존재할 수 있는 범위 중 좌상단 x좌표
        y (int): 정보 box가 존재할 수 있는 범위 중 좌상단 y좌표
        width (int): 명함 이미지의 너비
        height (int): 명함 이미지의 높이
        image: 명함 이미지 객체
        font_family (Dict): 명함 내 정보의 글씨체 정보를 저장
        font_size (Dict): 명함 내 정보의 글씨 크기 정보를 저장
        font_color (Dict): 명함 내 정보의 글씨 색상 정보를 저장
        word (List): json 파일에 저장할 bbox 정보를 담은 리스트

    Returns:
        Tuple: 만들어진 정보 box의 끝 지점 (bbox 우측 하단)
    """

    index = random.randint(0, len(loc) - 1)
    if random.random() >= 0.5:
        x, y = TwoItemsTemplate(
            info,
            x,
            y,
            loc[index],
            width,
            height,
            image,
            font_family,
            font_size,
            font_color,
            word,
        ).make()
    else:
        if random.random() >= 0.5:
            x, y = OneItemTemplate(
                info,
                "department",
                x,
                y,
                loc[index],
                width,
                height,
                image,
                font_family,
                font_size,
                font_color,
                word,
            ).make()
        else:
            x, y = OneItemTemplate(
                info,
                "position",
                x,
                y,
                loc[index],
                width,
                height,
                image,
                font_family,
                font_size,
                font_color,
                word,
            ).make()

    return x, y


def num_info(
    info: Dict,
    x: int,
    y: int,
    width: int,
    height: int,
    image,
    font_family: Dict,
    font_size: Dict,
    font_color: Dict,
    word: List,
) -> Tuple:
    """
    직책 및 부서에 대한 box를 생성하고, 이를 명함 이미지에 적용합니다.

    Args:
        info (Dict): 명함 데이터 생성에 필요한 카테고리 이름과 텍스트 내용을 저장
        x (int): 정보 box가 존재할 수 있는 범위 중 좌상단 x좌표
        y (int): 정보 box가 존재할 수 있는 범위 중 좌상단 y좌표
        width (int): 명함 이미지의 너비
        height (int): 명함 이미지의 높이
        image: 명함 이미지 객체
        font_family (Dict): 명함 내 정보의 글씨체 정보를 저장
        font_size (Dict): 명함 내 정보의 글씨 크기 정보를 저장
        font_color (Dict): 명함 내 정보의 글씨 색상 정보를 저장
        word (List): json 파일에 저장할 bbox 정보를 담은 리스트

    Returns:
        Tuple: 만들어진 정보 box의 끝 지점 y 좌표(bbox 우측 하단), 정보 box의 정렬 mode, 각 정보 box 사이의 높이 간격
    """

    index = random.randint(0, len(loc) - 1)
    y, y_margin = NumTemplate(
        info,
        x,
        y,
        loc[index],
        width,
        height,
        image,
        font_family,
        font_size,
        font_color,
        word,
    ).make()

    return y, loc[index], y_margin


def logo_info() -> Tuple:
    """
    로고 이미지에 대한 정보를 반환합니다.

    Returns:
        Tuple: 로고 이미지 객체, 로고 이미지 크기
    """

    # 로고 이미지의 경로
    logo_dir = "../data/images/logo"

    logo = glob.glob(f"{logo_dir}/*.png")
    logo_index = random.randint(0, len(logo) - 1)
    logo_image = Image.open(logo[logo_index]).convert("RGBA")
    logo_size = random.randint(50, 70)
    logo_image = logo_image.resize((logo_size, logo_size))

    return logo_image, logo_size


def icon_info(font) -> Tuple:
    """
    SNS 아이콘 이미지에 대한 정보를 반환합니다.

    Args:
        font: SNS 아이콘 이미지 주변에 표기되는 텍스트에 대한 폰트 정보

    Returns:
        Tuple: SNS 아이콘 이미지의 크기, SNS 아이콘 이미지 객체
    """

    # SNS 아이콘 이미지의 경로
    icon = pd.read_csv("../data/sns_logo.csv")

    icon_index = random.randint(0, len(icon) - 1)
    icon_dir = "../data/" + icon["images"][icon_index]
    icon_image = Image.open(icon_dir).convert("RGBA")
    icon_size = font.getsize("|")[1]  # SNS 아이콘의 크기는 글씨 크기에 맞추어서 결정
    icon_image = icon_image.resize((icon_size, icon_size))

    return icon_size, icon_image


def social_id(
    info: Dict,
    x: int,
    y: int,
    mode: str,
    width: int,
    image,
    font_family: Dict,
    font_size: Dict,
    font_color: Dict,
    word: List,
) -> int:
    """
    SNS ID에 대한 정보를 반환합니다.

    Args:
        info (Dict): 명함 데이터 생성에 필요한 카테고리 이름과 텍스트 내용을 저장
        x (int): 정보 box가 존재할 수 있는 범위 중 좌상단 x좌표
        y (int): 정보 box가 존재할 수 있는 범위 중 좌상단 y좌표
        mode (str): 정보 box의 정렬 mode (left/center/right)
        width (int): 명함 이미지의 너비
        height (int): 명함 이미지의 높이
        image: 명함 이미지 객체
        font_family (Dict): 명함 내 정보의 글씨체 정보를 저장
        font_size (Dict): 명함 내 정보의 글씨 크기 정보를 저장
        font_color (Dict): 명함 내 정보의 글씨 색상 정보를 저장
        word (List): json 파일에 저장할 bbox 정보를 담은 리스트

    Returns:
        int: 만들어진 정보 box의 끝 지점 y 좌표 (bbox 우측 하단)
    """

    draw = ImageDraw.Draw(image)
    content = info["social_id"]

    if random.random() >= 0:
        font = ImageFont.truetype(font_family["social_id"], font_size["social_id"])
        icon_size, icon_image = icon_info(font)

        while True:
            bbox_width = font.getsize(content)[0] + icon_size + font.getsize(" ")[0]
            if mode == "left":
                x, y = x, y
            elif mode == "right":
                x, y = x - bbox_width, y
            elif mode == "center":
                x, y = x - bbox_width // 2, y

            if x > 0 and x + bbox_width < width:
                image.paste(icon_image, (int(x), int(y)), icon_image)
                draw_and_write(
                    (x + font.getsize(" ")[0] + icon_size, y),
                    content,
                    "social_id",
                    font,
                    draw,
                    font_color,
                    word,
                )
                height = y + font.getsize(content)[1]
                break

            content = content[:-1]

            if len(content) == 0:
                height = y
                break
    else:
        item_bbox, content, font_scale = define_num_bbox(
            (x, y), content, "social_id", mode
        )
        font = ImageFont.truetype(font_family["social_id"], font_scale)
        height = item_bbox[1] + font.getsize(content)[1]

        # 숫자 및 기타 정보가 다른 정보의 높이를 넘어가는지 확인
        if font_scale == 0:
            height = item_bbox[1]
        else:
            if height <= height:
                draw_and_write(
                    item_bbox, content, "social_id", font, draw, font_color, word
                )
            else:
                height = item_bbox[1]

    return height
