import os
import glob
import random
from generate import generate

########################
## card util funtions ##
########################

current_dir = os.getcwd()

sub_font_dir = f"{current_dir}/font/sub"
main_font_dir = f"{current_dir}/font/main"
sub_font_families = glob.glob(f"{sub_font_dir}/*.ttf")
main_font_families = glob.glob(f"{main_font_dir}/*.ttf")

font_color = (0, 0, 0)


def make_font_size():
    font_size = dict()
    font_size["name"] = random.randint(40, 50)
    font_size["phone"] = font_size["tel"] = font_size["website"] = font_size[
        "license_number"
    ] = font_size["fax"] = font_size["email"] = font_size["address"] = random.randint(
        15, 20
    )
    font_size["position"] = font_size["department"] = random.randint(20, 30)
    font_size["company"] = random.randint(60, 70)
    font_size["wise"] = random.randint(15, 20)
    return font_size


def make_font_family():
    font_family = dict()
    sub_length = len(sub_font_families)
    main_length = len(main_font_families)
    font_family["name"] = main_font_families[random.randint(0, main_length - 1)]
    font_family["phone"] = font_family["tel"] = font_family["website"] = font_family[
        "license_number"
    ] = font_family["fax"] = font_family["email"] = font_family[
        "address"
    ] = sub_font_families[
        random.randint(0, sub_length - 1)
    ]
    font_family["position"] = font_family["department"] = sub_font_families[
        random.randint(0, sub_length - 1)
    ]
    font_family["company"] = main_font_families[random.randint(0, main_length - 1)]
    font_family["wise"] = sub_font_families[random.randint(0, sub_length - 1)]
    return font_family


def num_separator():
    if random.random() > 0.7:
        item = ". "
    elif random.random() > 0.4:
        item = " "
    else:
        item = ": "
    return item


def position_separator():
    if random.random() > 0.5:
        item = " | "
    else:
        item = " / "
    return item


def use_item(items: list, threshold: float):
    use = []
    for item in items:
        if random.random() < threshold:
            use.append(item)
    return use


def info_item(info: dict, use: list):
    content = dict()
    for item in use:
        content[item] = info[item]
    return content


def check_bbox(bbox_points: list):
    condition_x = 5 < bbox_points[0][0] < 900 - 5 and 5 < bbox_points[1][0] < 900 - 5
    condition_y = 5 < bbox_points[0][1] < 500 - 5 and 5 < bbox_points[1][1] < 500 - 5
    if condition_x and condition_y:
        return True
    return False


def make_bbox(font, start: tuple, content: str):
    w, h = font.getsize(content)
    x, y = start

    points = [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]
    return points


def regenerate(item_name: str):
    re_info = generate()
    content = re_info[item_name]
    return content
