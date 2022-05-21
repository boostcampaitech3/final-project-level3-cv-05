import argparse
import glob
import json
import os
import random

from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
from generate import generate
from make_template import *
from template.font import font_list
from typing Tuple, Dict

#######################
### argument parser ###
#######################

parser = argparse.ArgumentParser()
parser.add_argument("--num", required=True, help="the number of images")
parser.add_argument("--dir", required=True, help="directory of json file")

#######################
### load font, logo ###
#######################

logo_dir = "../../generator/logo"
font_dir = "../../generator/font"

ext = [".jpg", ".png"]
logo = []
for item in ext:
    logo += glob.glob(f"{logo_dir}/*{ext}")

font_families = glob.glob(f"{font_dir}/*.ttf")

cat_name = ["name", "ko_name", "eng_name"]  # name에 속하는 하위 카테고리
cat_num = ["phone_number", "tel", "fax"]  # num에 속하는 하위 카테고리


def regenerate(key: str) -> str:
    """
    명함에 적용할 정보 (str)를 다시 생성합니다.

    Args:
        key (str): 정보 항목의 이름

    Returns:
        content (str): 정보 항목의 내용
    """
    re_info = generate()
    content = re_info[key]
    return content


#######################
### image generator ###
#######################


def make_dir(directory: str):
    """ 
    디렉토리 존재 여부를 확인하고, 없으면 디렉토리를 새로 생성합니다. 

    Args:
        directory (str): 확인 및 생성할 디렉토리
    """    
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def check_file_num(directory: str, ext: str) -> int:
    """ 
    디렉토리에 존재하는 특정 확장자 파일의 개수를 반환합니다. 

    Args:
        directory (str): 확인할 디렉토리 
        ext (str): 확인할 확장자명 

    Returns:
        length (int): 디렉토리에 존재하는 파일의 개수 
    """    
    file_list = glob.glob(f"{directory}/*{ext}")
    length = len(file_list)
    return length


def make_json(directory: str) ->  dict:
    """ 
    디렉토리에 json 파일을 새로 생성하고, 
    json 파일에 들어갈 내용을 저장하는 dict type으로 반환합니다. 

    Args:
        directory (str): json 파일의 디렉토리 

    Returns:
        json_data (dict): json 파일에 들어갈 내용 저장하는 딕셔너리형 변수 
    """    
    json_data = dict()
    json_data["images"] = []
    json_data["categories"] = (
        {
            "0": "UNKNOWN",
            "1": "name",
            "2": "phone",
            "3": "email",
            "4": "position",
            "5": "company",
            "6": "department",
            "7": "address",
            "8": "site",
            "9": "account",
            "10": "wise",
        },
    )
    json_data["annotations"] = []
    with open(directory, "w", encoding="utf-8") as make_file:
        json.dump(json_data, make_file, indent="\t")
    return json_data


def shorten(
    type: int,
    bbox_length: int,
    font_size: int,
    font_family: str,
    content: str,
    item: str,
) -> int, str:
    """ 
    지정된 bbox 영역을 넘어가는 경우, 
    내용을 변경하거나 폰트 크기를 변경하여 bbox 영역에 들어오도록 만듭니다. 

    Args:
        type (int): width 이면, 0 / height 이면, 1
        bbox_length (int): type이 0 이면, bbox의 width / type이 1이면, bbox의 height 
        font_size (int): 해당 bbox에 적용되는 글씨 크기 
        font_family (str): 해당 bbox에 적용되는 글씨체 
        content (str): 해당 bbox에 적용되는 텍스트 내용 
        item (str): 해당 bbox에 적용되는 정보 항목의 이름 

    Returns:
        font_size (int), content (str): 지정된 bbox 영역에 들어오는 글씨 크기, 텍스트 내용 
    """    
    
    font = ImageFont.truetype(font_family, font_size)
    text_length = font.getsize(content)[type]

    while text_length > bbox_length:  # 내용 변경
        content = regenerate(item)
        text_length = font.getsize(content)[type]
        if text_length <= bbox_length:
            break

        font_size *= random.uniform(0.7, 1)  # 폰트 크기 변경 비율 (0.7, 1)
        font = ImageFont.truetype(font_family, int(font_size))
        text_length = font.getsize(content)[type]
        if text_length <= bbox_length:
            break
    return int(font_size), content


def check_size(
    bbox_size: Tuple[int, int], font_size: int, font_family: str, content: str, item: str
) -> int, str:
    """ 
    지정한 bbox 영역 내에 들어오는지 확인하고, 
    영역을 벗어날 경우, bbox 범위 내에 들어오도록 shorten() 함수를 적용합니다.

    Args:
        bbox_size (tuple): 지정된 bbox의 (width, height)
        font_size (int): 해당 bbox에 적용되는 글씨 크기 
        font_family (str): 해당 bbox에 적용되는 글씨체 
        content (str): 해당 bbox에 적용되는 텍스트 내용 
        item (str): 해당 bbox에 적용되는 정보 항목의 이름 

    Returns:
        font_size (int), content (str): 지정된 bbox 영역에 들어오는 글씨 크기, 텍스트 내용 
    """
    font = ImageFont.truetype(font_family, font_size)
    text_width, text_height = font.getsize(content)

    width_ratio = text_width / bbox_size[0]
    height_ratio = text_height / bbox_size[1]

    while width_ratio > 1 or height_ratio > 1:
        shorten_target = 0 if width_ratio > height_ratio else 1
        font_size, content = shorten(
            shorten_target,
            bbox_size[shorten_target],
            font_size,
            font_family,
            content,
            item,
        )

        font = ImageFont.truetype(font_family, font_size)
        text_width, text_height = font.getsize(content)
        width_ratio = text_width / bbox_size[0]
        height_ratio = text_height / bbox_size[1]
    return int(font_size), content


def get_category_id(item: str) -> int:
    """ 
    정보 항목의 이름에 맞는 category_id를 반환합니다.

    Args:
        item (str): 정보 항목의 이름

    Returns:
        category_id (int): 정보 항목의 이름에 맞는 category id 
    """    
    if item in cat_name:
        category_id = 1
    elif item in cat_num:
        category_id = 2
    elif item == "email":
        category_id = 3
    elif item == "position":
        category_id = 4
    elif item == "company_name":
        category_id = 5
    elif item == "company_address":
        category_id = 7
    elif item == "website":
        category_id = 8
    else:
        category_id = 0
    return category_id


def card_generator(info: Dict[str, str], info_dir: str):
    """ 
    명함 이미지를 생성하고, 저장합니다. 이와 관련한 json 파일도 생성하고 저장합니다. 

    Args:
        info (dict): 명함 이미지에 적용되는 정보
        info_dir (str): json 파일의 디렉토리 
    """    
    random_index = random.randint(2, len(images))
    open_shape = [2, 11, 17, 18]  # bbox의 길이에 관계없는 템플릿 인덱스 

    card_img = Image.open(
        f"{template_dir}/template_img/template{random_index}.png"
    ).convert(
        "RGB"
    )  # 템플릿을 배경 이미지로 사용
    draw = ImageDraw.Draw(card_img)

    # 파일 경로
    example_directory = f"{dir}/example"
    make_dir(example_directory + "/images")
    image_name = check_file_num(example_directory + "/images/", ".png")  

    items = info.keys()

    # json 파일 저장
    if not os.path.exists(info_dir):
        json_data = make_json(info_dir)  # json 파일이 없다면 새로 생성
    else:
        with open(info_dir, "r") as f:
            json_data = json.load(f)

    # images
    json_images = {}
    json_images["width"] = template_list[random_index]["size"][0]
    json_images["height"] = template_list[random_index]["size"][1]
    json_images["file"] = f"{image_name:04}.png"
    json_images["id"] = image_name

    # annotations
    json_anno = {}
    json_anno["image_id"] = image_name
    word = []

    number = ["tel", "phone_number"]
    for item in items:
        if (
            item not in template_list[random_index]["bbox"].keys()
        ):  # template에 있는 항목만 적용
            continue

        if item in number:
            font_item = "phone_number"
        else:
            font_item = item

        content = info[item]

        font_size = font_list[str(random_index)][font_item]["font_size"]
        font_family = font_families[random.randint(0, len(font_families) - 1)]
        font = ImageFont.truetype(font_family, font_size)
        font_color = font_list[str(random_index)][font_item]["font_color"]

        # 영역을 벗어나지 않는지 확인
        if random_index not in open_shape:
            bbox_size = template_list[random_index]["bbox_size"][item]
            font_size, content = check_size(
                bbox_size, font_size, font_family, content, item
            )
            font = ImageFont.truetype(font_family, font_size)

        # bbox 왼쪽 아래의 지점을 기준으로 생성
        x = template_list[random_index]["bbox"][item][0]
        y = (
            template_list[random_index]["bbox"][item][1]
            + template_list[random_index]["bbox_size"][item][1]
            - font.getsize(content)[1]
        )

        draw.text(
            (x, y),
            content,
            font=font,
            fill=font_color,
        )

        # json 파일
        temp_word = {}  # cateogory_id 설정
        temp_word["category_id"] = get_category_id(item)
        temp_word["orientation"] = "Horizontal"
        temp_word["text"] = content

        text_width, text_height = font.getsize(content)
        start_x, start_y = x, y
        temp_word["points"] = [
            [start_x, start_y],
            [start_x + text_width, start_y],
            [start_x + text_width, start_y + text_height],
            [start_x, start_y + text_height],
        ]
        word.append(temp_word)

    if "logo" in template_list[random_index]["bbox"].keys():
        logo_img = logo[random.randint(0, len(logo) - 1)]
        logo_img = Image.open(logo_img)

        # 템플릿의 로고 크기와 비슷하게 비율 조절
        width_ratio = (
            template_list[random_index]["bbox_size"]["logo"][0] / logo_img.size[0]
        )
        height_ratio = (
            template_list[random_index]["bbox_size"]["logo"][1] / logo_img.size[1]
        )
        ratio = height_ratio if width_ratio > height_ratio else width_ratio
        w, h = int(logo_img.size[0] * ratio), int(logo_img.size[1] * ratio)

        resized_logo = logo_img.resize((w, h))  # template의 로고 사이즈에 맞도록
        card_img.paste(
            resized_logo,
            (
                int(template_list[random_index]["bbox"]["logo"][0]),
                int(template_list[random_index]["bbox"]["logo"][1]),
            ),
            resized_logo,
        )

    json_ocr = {}
    json_ocr["word"] = word
    json_anno["ocr"] = json_ocr

    # json 파일 업데이트
    json_data["images"].append(json_images)
    json_data["annotations"].append(json_anno)
    with open(info_dir, "w", encoding="utf-8") as make_file:
        json.dump(json_data, make_file, indent="\t")

    card_img.save(f"{example_directory}/images/{image_name:04}.png")


def main(num: str, dir: str):
    """
    Args:
        num (str): 생성할 이미지의 개수 
        dir (str): json 파일의 디렉토리 
    """    
    for _ in tqdm(range(int(num))):
        info = generate()
        card_generator(info, dir)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args.num, args.dir)
