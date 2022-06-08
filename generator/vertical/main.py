# main.py
"""
명함 이미지과 이에 대한 json 파일을 생성하는 메인 모듈입니다.
"""

import os
import json
import random
import argparse
from tqdm import tqdm
from PIL import Image
from utils.card_utils import *
from utils.bbox_utils import *
from utils.json_utils import *
from generate import generate
from make.make_template import *

# main.py 파일이 위치한 디렉토리
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
parser.add_argument(
    "--split", type=bool, required=False, default=False, help="split mode"
)
parser.add_argument(
    "--split_num",
    type=int,
    required=False,
    default=100,
    help="the number of images for each template",
)


##################
## main funcion ##
##################


def main(args):
    if args.test is True:
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

    if args.split is True:
        progress_bar = [0 for _ in template_name]

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
            eval(args.template_name)(
                info, width, height, image, font_family, font_size, font_color, word
            ).make()
        elif args.split is True:
            template_name[index](
                info, width, height, image, font_family, font_size, font_color, word
            ).make()
            progress_bar[index] += 1

            if progress_bar[index] == args.split_num:
                del template_name[index]
                del progress_bar[index]

        else:
            template_name[index](
                info, width, height, image, font_family, font_size, font_color, word
            ).make()

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
    print("Done!")
