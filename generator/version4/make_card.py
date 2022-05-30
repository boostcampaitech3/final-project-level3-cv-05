import random
import json
import argparse
import os
from generate import generate
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
from card_utils import *
from json_utils import *

from typing import Tuple, Dict

# make_card.py 파일이 위치한 디렉토리
current_dir = os.getcwd()

#######################
### argument parser ###
#######################

parser = argparse.ArgumentParser()
parser.add_argument("--num", required=True, help="the number of images")
parser.add_argument("--dir", required=True, help="directory of json file")
parser.add_argument("--width", required=True, help="image width")
parser.add_argument(
    "--test", type=bool, required=False, default=False, help="test mode"
)
parser.add_argument("--template_name", default="", required=False, help="template name")

#####################
### bbox function ###
#####################


def change_font_size(item_type: str, content: str, mode: str, x: int, x_limit: int):
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


def change_content(item_type: str, mode: str, x: int, x_limit: int, font):
    content = regenerate(item_type)
    bbox_width, bbox_height = font.getsize(content)
    if mode in ["center", "left"] and x > 0 and x + bbox_width < width:
        return True, content
    if mode == "right" and x > 0 and x + bbox_width < width and x_limit <= x:
        return True, content
    return False, content


def change_dep_pos(start: Tuple[int, int], sep: str, mode: str, x_limit: int, font):
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


def define_bbox(
    start: Tuple[int, int], mode: str, content: str, item_type: str, x_limit: int
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
        check, font_scale = change_font_size(item_type, content, mode, x, x_limit)
        if check is True:
            return (x, y), content, font_scale
        # 내용 변경
        font = ImageFont.truetype(font_family["position"], font_scale)
        check, content = change_content(item_type, mode, x, x_limit, font)
        if check is True:
            return (x, y), content, font_scale
        else:
            return (x, y), content, 0  # font_scale = 0


def define_dep_pos_bbox(
    info: Dict[str, str], start: Tuple[int, int], mode: str, x_limit: int
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
        check, font_scale = change_font_size("department", content, mode, x, x_limit)
        if check is True:
            return (x, y), department, sep, position, font_scale
        # 내용 변경
        font = ImageFont.truetype(font_family["position"], font_scale)
        check, department, sep, position = change_dep_pos(
            start, sep, mode, x_limit, font
        )
        if check is True:
            return (x, y), department, sep, position, font_scale
        else:
            return (x, y), department, sep, position, 0  # font_scale = 0


def define_num_bbox(start: Tuple[int, int], content: str, item_type: str, mode: str):
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
            check, font_scale = change_font_size(item_type, full_content, mode, x, 0)

            if check is True:
                break
            # 내용 변경
            content = regenerate(item_type)

    return (x, y), full_content, font_scale


def draw_and_write(bbox_start: Tuple[int, int], content: str, item: str, font, draw):
    draw.text(
        bbox_start,
        content,
        font=font,
        fill=font_color[item],
    )
    put_word(item, content.strip(), bbox_start, font)


def put_word(item: str, content: str, start: Tuple[int, int], font):
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


#####################
## component class ##
#####################


def start(mode: str, bbox_x: int, bbox_y: int):
    start = dict()
    start["center"] = (
        width // 2 + width * random.uniform(-MIN_X, MIN_X),
        bbox_y,
    )
    start["left"] = (bbox_x, bbox_y)
    start["right"] = (width - width * random.uniform(0, MIN_X), bbox_y)

    start = start[mode]
    return start


class OneItemTemplate:
    # company # name # department # position
    def __init__(self, info: Dict[str, str], item_type: str, x: int, y: int, mode: str):
        self.items = info
        self.type = item_type
        self.bbox_x = x
        self.bbox_y = y
        self.mode = mode

        self.start = start(self.mode, self.bbox_x, self.bbox_y)

    def make(self):
        draw = ImageDraw.Draw(image)

        content = self.items[self.type]
        self.start, content, font_scale = define_bbox(
            self.start, self.mode, content, self.type, self.bbox_x
        )

        font = ImageFont.truetype(font_family[self.type], font_scale)
        bbox_x, bbox_y = self.start
        bbox_width, bbox_height = font.getsize(content)

        if (
            bbox_y + bbox_height > height or font_scale == 0
        ):  # y좌표가 범위를 벗어나는 경우, or 폰트 크기가 일정값 이하인 경우제외
            return (bbox_x, bbox_y)

        draw_and_write(self.start, content, self.type, font, draw)
        return (bbox_x + bbox_width, bbox_y + bbox_height)


def draw_dep_pos(
    start: Tuple[int, int], department: str, sep: str, position: str, font, draw
):
    item_list = [("department", department), ("position", position)]
    if random.random() >= 0.5:  # pos + dep 순서
        item_list = item_list[::-1]

    # department
    draw_and_write(
        start,
        item_list[0][1],
        item_list[0][0],
        font,
        draw,
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
    )


class TwoItemsTemplate:
    # department & position
    def __init__(self, items: Dict[str, str], x: int, y: int, mode: str):
        self.items = items

        self.bbox_x = x
        self.bbox_y = y
        self.mode = mode

        self.start = start(self.mode, self.bbox_x, self.bbox_y)

    def make(self):
        draw = ImageDraw.Draw(image)

        self.start, department, sep, position, font_scale = define_dep_pos_bbox(
            self.items, self.start, self.mode, self.bbox_x
        )
        font = ImageFont.truetype(font_family["position"], font_scale)
        bbox_x, bbox_y = self.start
        bbox_width, bbox_height = font.getsize(department + " " + sep + " " + position)

        if (
            bbox_y + bbox_height > height or font_scale == 0
        ):  # y좌표가 범위를 벗어나는 경우, or 폰트 크기가 일정값 이하인 경우, 제외
            return (bbox_x, bbox_y)

        draw_dep_pos(self.start, department, sep, position, font, draw)
        return (bbox_x + bbox_width, bbox_y + bbox_height)


class NumTemplate:
    # num info
    def __init__(
        self,
        items: Dict[str, str],
        x: int,
        y: int,
        mode: str,
    ):
        self.items = items
        self.bbox_x = x
        self.bbox_y = y
        self.mode = mode

        self.start = start(self.mode, self.bbox_x, self.bbox_y)

    def make(self):
        draw = ImageDraw.Draw(image)

        global y_margin
        y_margin = height * random.uniform(MIN_Y, MAX_Y)

        random_items = list(self.items.keys())
        random.shuffle(random_items)
        for item in random_items:
            item_name, content = item, self.items[item]

            # bbox 영역이 범위 내에 존재하는지 확인
            item_bbox, content, font_scale = define_num_bbox(
                (self.start[0], self.start[1] + y_margin), content, item, self.mode
            )
            font = ImageFont.truetype(font_family[item_name], font_scale)
            num_height = item_bbox[1] + font.getsize(content)[1]

            # 숫자 및 기타 정보가 이름 정보의 높이를 넘어가는지 확인
            if font_scale == 0:
                num_height = self.start[1]
            else:
                if num_height <= height:
                    draw_and_write(item_bbox, content, item, font, draw)
                else:
                    num_height = self.start[1]
                    break
            self.start = self.start[0], num_height
        return num_height


####################
## template class ##
####################


def company(info: Dict[str, str], x: int, y: int):
    index = random.randint(0, len(loc) - 1)
    x, y = OneItemTemplate(info, "company", x, y, loc[index]).make()
    return x, y


def name(info: Dict[str, str], x: int, y: int):
    index = random.randint(0, len(loc) - 1)
    x, y = OneItemTemplate(info, "name", x, y, loc[index]).make()
    return x, y


def dep_pos(info: Dict[str, str], x: int, y: int):
    index = random.randint(0, len(loc) - 1)
    if random.random() >= 0.5:
        x, y = TwoItemsTemplate(info, x, y, loc[index]).make()
    else:
        if random.random() >= 0.5:
            x, y = OneItemTemplate(info, "department", x, y, loc[index]).make()
        else:
            x, y = OneItemTemplate(info, "position", x, y, loc[index]).make()
    return x, y


def num_info(info: Dict[str, str], x: int, y: int):
    index = random.randint(0, len(loc) - 1)
    y = NumTemplate(info, x, y, loc[index]).make()
    return y, loc[index]


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


def social_id(info: Dict[str, str], x: int, y: int, mode: str):
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
                draw_and_write(item_bbox, content, "social_id", font, draw)
            else:
                height = item_bbox[1]
    return height


class Template1:
    def __init__(
        self,
        items: Dict[str, str],
    ):
        self.items = items

    def make(self):
        x, y = width * random.uniform(MIN_X, MAX_X), height * random.uniform(0.1, 0.6)

        x = width * random.uniform(MIN_X, MAX_X)
        y += height * random.uniform(MIN_Y, MAX_Y)

        x, y = company(self.items, x, y)

        x = width * random.uniform(MIN_X, MAX_X)
        if random.random() >= 0.5:
            x, y = name(self.items, x, y)

            x = width * random.uniform(-MIN_X, MIN_X)
            y += height * random.uniform(MIN_Y, MAX_Y)
            x, y = dep_pos(self.items, x, y)
        else:
            x, y = dep_pos(self.items, x, y)

            x = width * random.uniform(-MIN_X, MIN_X)
            y += height * random.uniform(MIN_Y, MAX_Y)
            x, y = name(self.items, x, y)

        x = width * random.uniform(MIN_X, MAX_X)
        y += height * random.uniform(MIN_Y, MAX_Y)

        use = []
        while not use:
            use += use_item(num, 0.7)
        num_list = info_item(self.items, use)

        y, mode = num_info(num_list, x, y)

        # social id 추가
        if "social_id" not in use and random.random() >= 0.5:
            y += y_margin
            y = social_id(self.items, x, y, mode)


class Template2:
    def __init__(
        self,
        items: Dict[str, str],
    ):
        self.items = items

    def make(self):
        logo_image, logo_size = logo_info()
        x = random.randint(0, width - logo_size)
        y = height * random.uniform(0.1, 0.3)
        image.paste(logo_image, (int(x), int(y)), logo_image)

        x = width * random.uniform(MIN_X, MAX_X)
        y += logo_size + height * random.uniform(0, MAX_Y)
        if random.random() >= 0.5:
            x, y = name(self.items, x, y)

            x = width * random.uniform(-MIN_X, MIN_X)
            y += height * random.uniform(MIN_Y, MAX_Y)
            x, y = dep_pos(self.items, x, y)
        else:
            x, y = dep_pos(self.items, x, y)

            x = width * random.uniform(-MIN_X, MIN_X)
            y += height * random.uniform(MIN_Y, MAX_Y)
            x, y = name(self.items, x, y)

        x = width * random.uniform(MIN_X, MAX_X)
        y += height * random.uniform(MIN_Y, MAX_Y)

        use = []
        while not use:
            use += use_item(num, 0.7)
        num_list = info_item(self.items, use)

        y, mode = num_info(num_list, x, y)

        # social id 추가
        if "social_id" not in use and random.random() >= 0.5:
            y += y_margin
            y = social_id(self.items, x, y, mode)


class Template3:
    def __init__(
        self,
        items: Dict[str, str],
    ):
        self.items = items

    def make(self):
        x = width * random.uniform(MIN_X, MAX_X)
        y = height * random.uniform(0.1, 0.6)
        if random.random() >= 0.5:
            x, y = name(self.items, x, y)

            x = width * random.uniform(-MIN_X, MIN_X)
            y += height * random.uniform(MIN_Y, MAX_Y)
            x, y = dep_pos(self.items, x, y)
        else:
            x, y = dep_pos(self.items, x, y)

            x = width * random.uniform(-MIN_X, MIN_X)
            y += height * random.uniform(MIN_Y, MAX_Y)
            x, y = name(self.items, x, y)

        x = width * random.uniform(MIN_X, MAX_X)
        y += height * random.uniform(MIN_Y, MAX_Y)

        use = []
        while not use:
            use += use_item(num, 0.7)
        num_list = info_item(self.items, use)

        y, mode = num_info(num_list, x, y)

        # social id 추가
        if "social_id" not in use and random.random() >= 0.5:
            y += y_margin
            y = social_id(self.items, x, y, mode)


class Template4:
    def __init__(
        self,
        items: Dict[str, str],
    ):
        self.items = items

    def make(self):
        x = width * random.uniform(MIN_X, MAX_X)
        y = height * random.uniform(0.1, 0.6)
        x, y = name(self.items, x, y)

        x += width * random.uniform(-MIN_X, MIN_X)
        y += height * random.uniform(MIN_Y, MAX_Y)

        use = []
        while not use:
            use += use_item(num, 0.7)
        num_list = info_item(self.items, use)

        y, mode = num_info(num_list, x, y)

        # social id 추가
        if "social_id" not in use and random.random() >= 0.5:
            y += y_margin
            y = social_id(self.items, x, y, mode)


class Template5:
    def __init__(
        self,
        items: Dict[str, str],
    ):
        self.items = items

    def make(self):
        x = width * random.uniform(MIN_X, MAX_X)
        y = height * random.uniform(0.1, 0.6)
        x, y = company(self.items, x, y)

        x = width * random.uniform(MIN_X, MAX_X)
        y += height * random.uniform(MIN_Y, MAX_Y)

        use = []
        while not use:
            use += use_item(num, 0.7)
        num_list = info_item(self.items, use)

        y, mode = num_info(num_list, x, y)

        # social id 추가
        if "social_id" not in use and random.random() >= 0.5:
            y += y_margin
            y = social_id(self.items, x, y, mode)

        x = width * random.uniform(MIN_X, MAX_X)
        y += height * random.uniform(MIN_Y, MAX_Y)
        x, y = name(self.items, x, y)


class Template6:
    def __init__(
        self,
        items: Dict[str, str],
    ):
        self.items = items

    def make(self):
        logo_image, logo_size = logo_info()
        x = random.randint(0, width - logo_size)
        y = height * random.uniform(0.1, 0.2)
        image.paste(logo_image, (int(x), int(y)), logo_image)

        x = width * random.uniform(MIN_X, MAX_X)
        y += logo_size + height * random.uniform(0, MAX_Y)
        x, y = company(self.items, x, y)

        x = width * random.uniform(MIN_X, MAX_X)
        y += height * random.uniform(MIN_Y, MAX_Y)
        if random.random() >= 0.5:
            x, y = name(self.items, x, y)

            x = width * random.uniform(-MIN_X, MIN_X)
            y += height * random.uniform(MIN_Y, MAX_Y)
            x, y = dep_pos(self.items, x, y)
        else:
            x, y = dep_pos(self.items, x, y)

            x = width * random.uniform(MIN_X, MAX_X)
            y += height * random.uniform(MIN_Y, MAX_Y)
            x, y = name(self.items, x, y)

        x = width * random.uniform(MIN_X, MAX_X)
        y += height * random.uniform(MIN_Y, MAX_Y)

        use = []
        while not use:
            use += use_item(num, 0.7)
        num_list = info_item(self.items, use)

        y, mode = num_info(num_list, x, y)

        # social id 추가
        if "social_id" not in use and random.random() >= 0.5:
            y += y_margin
            y = social_id(self.items, x, y, mode)


class Template7:
    def __init__(
        self,
        items: Dict[str, str],
    ):
        self.items = items

    def make(self):
        pre_x = width * random.uniform(MIN_X, MAX_X)
        pre_y = height * random.uniform(0.1, 0.6)
        post_x, post_y = company(self.items, pre_x, pre_y)

        logo_image, logo_size = logo_info()

        # 로고를 회사명의 왼쪽/오른쪽
        if random.random() >= 0.5:
            if width > logo_size and int(post_x) < width - logo_size:
                x = random.randint(int(post_x), width - logo_size)
                image.paste(logo_image, (int(x), int(post_y)), logo_image)
                y = post_y + logo_size + height * random.uniform(0, MAX_Y)
            else:
                y = post_y + height * random.uniform(0, MAX_Y)
        else:
            if int(pre_x) - logo_size > 0:  # 로고 크기보다 여백이 크면 적용
                x = random.randint(0, int(pre_x) - logo_size)
                image.paste(logo_image, (int(x), int(post_y)), logo_image)
                y = post_y + logo_size + height * random.uniform(0, MAX_Y)
            else:
                y = post_y + height * random.uniform(0, MAX_Y)

        x = width * random.uniform(MIN_X, MAX_X)
        if random.random() >= 0.5:
            x, y = name(self.items, x, y)

            x = width * random.uniform(-MIN_X, MIN_X)
            y += height * random.uniform(MIN_Y, MAX_Y)
            x, y = dep_pos(self.items, x, y)
        else:
            x, y = dep_pos(self.items, x, y)

            x = width * random.uniform(-MIN_X, MIN_X)
            y += height * random.uniform(MIN_Y, MAX_Y)
            x, y = name(self.items, x, y)

        x = width * random.uniform(MIN_X, MAX_X)
        y += height * random.uniform(MIN_Y, MAX_Y)

        use = []
        while not use:
            use += use_item(num, 0.7)
        num_list = info_item(self.items, use)

        y, mode = num_info(num_list, x, y)

        # social id 추가
        if "social_id" not in use and random.random() >= 0.5:
            y += y_margin
            y = social_id(self.items, x, y, mode)


##################
## main funcion ##
##################


def main(args):
    global font_family, font_size, font_color
    global word
    global draw, image
    global width, height
    global MIN_X, MAX_X, MIN_Y, MAX_Y
    global loc, num

    loc = ["center", "right", "left"]
    num = [
        "phone",
        "tel",
        "website",
        "license_number",
        "fax",
        "email",
        "address",
        "social_id",
    ]

    MIN_X, MAX_X, MIN_Y, MAX_Y = 0.05, 0.1, 0, 0.05

    template_name = [
        Template1,
        Template2,
        Template3,
        Template4,
        Template5,
        Template6,
        Template7,
    ]

    if args.test == True:
        example_directory = f"{current_dir}/test"
    else:
        example_directory = f"{current_dir}/sample"
    make_dir(example_directory)
    image_name = check_file_num(example_directory, ".png")

    # json 파일 저장
    if (
        not os.path.exists(args.dir) or os.path.getsize(args.dir) == 0
    ):  # json 파일이 없거나, 비어있는 경우
        json_data = make_json(args.dir)
    else:
        with open(args.dir, "r") as f:
            json_data = json.load(f)

    for i in tqdm(range(0, int(args.num))):
        info = generate()
        word = []

        # images
        width, height = int(args.width), int(int(args.width) * random.uniform(1.0, 1.8))
        json_images = {}
        json_images["width"] = width
        json_images["height"] = height
        json_images["file"] = f"{image_name+i:04}.png"
        json_images["id"] = image_name + i

        # annotations
        json_anno = {}
        json_anno["image_id"] = image_name + i

        font_family = make_font_family()
        font_size = make_font_size()
        background_color, font_color = make_font_color()

        image = Image.new("RGBA", (width, height), background_color)

        index = random.randint(0, len(template_name) - 1)
        if args.test is True:
            eval(args.template_name)(info).make()
        else:
            template_name[index](info).make()

        json_ocr = {}
        json_ocr["word"] = word
        json_anno["ocr"] = json_ocr

        # json 파일 업데이트
        json_data["images"].append(json_images)
        json_data["annotations"].append(json_anno)
        with open(args.dir, "w", encoding="utf-8") as make_file:
            json.dump(json_data, make_file, indent="\t")

        image.save(f"{example_directory}/{image_name+i:04}.png")


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
