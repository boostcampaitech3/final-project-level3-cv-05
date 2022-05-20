import random
import json
import argparse
import os
from generate import generate
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
from card_utils import *
from json_utils import *


#######################
### argument parser ###
#######################

parser = argparse.ArgumentParser()
parser.add_argument("--num", required=True, help="the number of images")
parser.add_argument("--dir", required=True, help="directory of json file")
# parser.add_argument(
#     "--width", required=False, default=900, help="the width of each image"
# )
# parser.add_argument(
#     "--height", required=False, default=500, help="the height of each image"
# )

#####################
### bbox function ###
#####################


def valid_num_bbox(
    mode: str, start: tuple, content: str, item_name: str, item: str, font
):
    # bbox 영역이 범위 내에 존재하는지 확인
    while True:
        if mode == "left":
            item_name_x, item_name_y = start[0], start[1] - font.getsize(content)[1]
            item_x, item_y = item_name_x + font.getsize(item_name)[0], item_name_y
        elif mode == "right":
            item_x, item_y = (
                start[0] - font.getsize(content)[0],
                start[1] - font.getsize(content)[1],
            )
            item_name_x, item_name_y = item_x - font.getsize(item_name)[0], item_y

        item_name_points = make_bbox(font, (item_name_x, item_name_y), item_name)

        content_points = make_bbox(font, (item_x, item_y), content)

        if check_bbox(content_points) and check_bbox(item_name_points):
            break
        else:
            content = regenerate(item)

    return (item_name_x, item_name_y), (item_x, item_y), content


def valid_name_company_bbox(mode: str, start: tuple, content: str, item: str, font):
    # bbox 영역이 범위 내에 존재하는지 확인
    while True:
        if mode == "left":
            x, y = start[0], start[1]
        elif mode == "right":
            x, y = start[0] - font.getsize(content)[0], start[1]
        elif mode == "center":
            x, y = start[0] - font.getsize(content)[0] // 2, start[1]

        content_points = make_bbox(font, (x, y), content)

        if check_bbox(content_points):
            break
        else:
            content = regenerate(item)

    return (x, y), content


def valid_department_position_bbox(
    mode: str, start: tuple, content: str, item: str, font
):
    # bbox 영역이 범위 내에 존재하는지 확인
    name_font = ImageFont.truetype(font_family["name"], font_size["name"])
    while True:
        x_list = [
            start[0] - font.getsize(content)[0] // 2,
            name_start - font.getsize(content)[0],
            name_end + 5,
            start[0] - font.getsize(content)[0] - 5,
            start[0],
        ]
        y_list = [start[1] + 5, start[1] - font.getsize(content)[1]]

        if name_template_mode == "left":
            if mode == "right":
                x, y = x_list[2], y_list[1]
            elif mode == "down":
                x, y = x_list[4], y_list[0]
        elif name_template_mode == "right":
            if mode == "left":
                x, y = x_list[1], y_list[1]
            elif mode == "down":
                x, y = x_list[3], y_list[0]
        elif name_template_mode == "center":
            if mode == "left":
                x, y = x_list[1], y_list[1]
            elif mode == "right":
                x, y = x_list[2], y_list[1]
            elif mode == "down":
                x, y = x_list[0], y_list[0]

        content_points = make_bbox(font, (x, y), content)

        if check_bbox(content_points):
            break
        else:
            content = regenerate(item)

    return (x, y), content


def draw_and_write(bbox: tuple, content: str, item: str, font, draw):
    draw.text(
        bbox,
        content,
        font=font,
        fill=font_color[item],
    )
    put_word(item, content.strip(), bbox, font)


def put_word(item: str, content: str, start: tuple, font):
    # json 파일
    temp_word = dict()  # cateogory_id 설정
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


####################
## template class ##
####################


class NumTemplate:
    def __init__(
        self,
        items: dict,
        start: tuple,
    ):
        self.items = items
        self.start = start

        #  mode
        self.mode = ["left", "right"]
        self.start = [(start[0], start[1]), (900 - start[0], start[1])]

    def make(self):
        draw = ImageDraw.Draw(image)
        sep = num_separator()

        mode_index = random.randint(0, len(self.mode) - 1)
        mode = self.mode[mode_index]
        start = self.start[mode_index]
        for item in self.items:
            item_name, content = item, self.items[item]

            font = ImageFont.truetype(font_family[item_name], font_size[item_name])

            if item_name == "license_number":
                item_name = "사업자등록번호" + sep
            else:
                item_name = item_name + sep

            # bbox 영역이 범위 내에 존재하는지 확인
            item_name_bbox, item_bbox, content = valid_num_bbox(
                mode, start, content, item_name, item, font
            )

            num_height = item_bbox[1] - font.getsize(content)[1]
            start = start[0], num_height

            if num_height >= name_height:
                draw_and_write(item_name_bbox, item_name, "UNKNOWN", font, draw)
                draw_and_write(item_bbox, content, item, font, draw)
            else:
                break


class NameCompanyTemplate:
    def __init__(
        self,
        items: dict,
        type: str,
    ):
        self.items = items
        self.type = type

        #  mode
        self.mode = ["center", "left", "right"]
        self.start_company = [(450, 50), (60, 50), (840, 50)]
        self.start_name = [
            (450, company_height + 15),
            (60, company_height + 15),
            (840, company_height + 15),
        ]

    def make(self):
        draw = ImageDraw.Draw(image)

        mode_index = random.randint(0, len(self.mode) - 1)
        mode = self.mode[mode_index]
        font = ImageFont.truetype(font_family[self.type], font_size[self.type])
        if self.type == "company":
            bbox, content = valid_name_company_bbox(
                mode,
                self.start_company[mode_index],
                self.items[self.type],
                self.type,
                font,
            )
        elif self.type == "name":
            global name_template_mode, name_end, name_start, name
            name_template_mode = mode
            bbox, content = valid_name_company_bbox(
                mode,
                self.start_name[mode_index],
                self.items[self.type],
                self.type,
                font,
            )
            name = content
            name_end, name_start = bbox[0] + font.getsize(name)[0], bbox[0]

        draw_and_write(bbox, content, self.type, font, draw)

        height = bbox[1] + font.getsize(content)[1]
        return height


class DepartmentPositionTemplate:
    def __init__(
        self,
        items: dict,
    ):
        self.items = items

        #  mode
        self.mode = ["down", "left", "right"]
        self.start = [(450, name_height), (60, name_height), (840, name_height)]

    def make(self):
        draw = ImageDraw.Draw(image)
        if name_template_mode == "left":
            self.mode = [self.mode[0], self.mode[2]]
            start = self.start[1]
        elif name_template_mode == "right":
            self.mode = self.mode[:2]
            start = self.start[2]
        elif name_template_mode == "center":
            start = self.start[0]

        if "position" in self.items.keys():
            self.type = "position"
        elif "department" in self.items.keys():
            self.type = "department"

        mode_index = random.randint(0, len(self.mode) - 1)
        mode = self.mode[mode_index]
        font = ImageFont.truetype(font_family[self.type], font_size[self.type])

        bbox, content = valid_department_position_bbox(
            mode, start, self.items[self.type], self.type, font
        )

        draw_and_write(bbox, content, self.type, font, draw)

        height = bbox[1] + font.getsize(content)[1]
        return height


########################
## component function ##
########################


def make_company(info: dict):
    use = ["company"]
    content = info_item(info, use)

    height = NameCompanyTemplate(content, "company").make()

    return height


def make_name(info: dict):
    use = ["name"]
    content = info_item(info, use)

    height = NameCompanyTemplate(content, "name").make()

    return height


def make_department_position(info: dict):
    sub = ["position", "department"]
    use = []
    while not use:
        use += use_item(sub, 0.7)

    content = info_item(info, use)

    height = DepartmentPositionTemplate(content).make()

    return height


def make_number(info: dict):
    start = (int(60), int(450))  # 명함의 왼쪽 아래 지점
    use = []
    while not use:
        if random.random() < 0.95:
            use.append("phone")

        use += use_item(num, 0.7)

    content = info_item(info, use)
    NumTemplate(content, start).make()


##################
## main funcion ##
##################


def main(args):
    global font_family, font_size, font_color, background_color
    global word
    global company_height, name_height
    global draw, image
    # global name_template_mode, name, name_start, name_end

    company_height = 50

    # 파일 경로
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
        json_images = {}
        json_images["width"] = 900
        json_images["height"] = 500
        json_images["file"] = f"{image_name+i:04}.png"
        json_images["id"] = image_name + i

        # annotations
        json_anno = {}
        json_anno["image_id"] = image_name + i

        font_family = make_font_family()
        font_size = make_font_size()
        background_color, font_color = make_font_color()

        image = img = Image.new("RGB", (900, 500), background_color)

        #  start
        company_height = make_company(info)
        name_height = make_name(info)
        name_height = make_department_position(info)

        make_number(info)
        #  end

        json_ocr = {}
        json_ocr["word"] = word
        json_anno["ocr"] = json_ocr

        # json 파일 업데이트
        json_data["images"].append(json_images)
        json_data["annotations"].append(json_anno)
        with open(args.dir, "w", encoding="utf-8") as make_file:
            json.dump(json_data, make_file, indent="\t", ensure_ascii=False)  # False 제거

        img.save(f"{example_directory}/{image_name+i:04}.png")


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
