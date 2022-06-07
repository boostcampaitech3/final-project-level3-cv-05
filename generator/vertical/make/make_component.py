import random
from utils.card_utils import *
from utils.bbox_utils import *
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Tuple

loc = ["center", "right", "left"]
MIN_X, MAX_X, MIN_Y, MAX_Y = 0.05, 0.1, 0, 0.05


##########################
## start point function ##
##########################


def start(mode: str, bbox_x: int, bbox_y: int, width: int):
    start = dict()
    start["center"] = (
        width // 2 + width * random.uniform(-MIN_X, MIN_X),
        bbox_y,
    )
    start["left"] = (bbox_x, bbox_y)
    start["right"] = (width - width * random.uniform(0, MIN_X), bbox_y)

    start = start[mode]
    return start


#####################
## component class ##
#####################


class OneItemTemplate:
    # company # name # department # position
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
        ):  # y좌표가 범위를 벗어나는 경우, or 폰트 크기가 일정값 이하인 경우제외
            return (bbox_x, bbox_y)

        draw_and_write(
            self.start, content, self.type, font, draw, self.font_color, self.word
        )
        return (bbox_x + bbox_width, bbox_y + bbox_height)


class TwoItemsTemplate:
    # department & position
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
    # num info
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

            # 숫자 및 기타 정보가 이름 정보의 높이를 넘어가는지 확인
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
    info: Dict[str, str],
    x: int,
    y: int,
    width: int,
    height: int,
    image,
    font_family: Dict,
    font_size: Dict,
    font_color: Dict,
    word: List,
):
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
    info: Dict[str, str],
    x: int,
    y: int,
    width: int,
    height: int,
    image,
    font_family: Dict,
    font_size: Dict,
    font_color: Dict,
    word: List,
):
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
    info: Dict[str, str],
    x: int,
    y: int,
    width: int,
    height: int,
    image,
    font_family: Dict,
    font_size: Dict,
    font_color: Dict,
    word: List,
):
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
    info: Dict[str, str],
    x: int,
    y: int,
    width: int,
    height: int,
    image,
    font_family: Dict,
    font_size: Dict,
    font_color: Dict,
    word: List,
):
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


def logo_info():
    # 로고 이미지
    logo_index = random.randint(0, len(logo) - 1)
    logo_image = Image.open(logo[logo_index]).convert("RGBA")
    logo_size = random.randint(50, 70)
    logo_image = logo_image.resize((logo_size, logo_size))
    return logo_image, logo_size


def icon_info(x: int, y: int, font):
    global icon_size, icon_image
    icon_index = random.randint(0, len(icon) - 1)
    icon_dir = "data/" + icon["images"][icon_index]
    icon_image = Image.open(icon_dir).convert("RGBA")
    icon_size = font.getsize("|")[1]
    icon_image = icon_image.resize((icon_size, icon_size))


def social_id(
    info: Dict[str, str],
    x: int,
    y: int,
    mode: str,
    width: int,
    image,
    font_family: Dict,
    font_size: Dict,
    font_color: Dict,
    word: List,
):
    draw = ImageDraw.Draw(image)
    content = info["social_id"]
    if random.random() >= 0:
        font = ImageFont.truetype(font_family["social_id"], font_size["social_id"])
        icon_info(x, y, font)
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

        # 숫자 및 기타 정보가 이름 정보의 높이를 넘어가는지 확인
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
