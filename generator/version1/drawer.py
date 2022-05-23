# -*-coding:UTF-8
import os
from PIL import Image, ImageFont, ImageDraw
import random
import pandas as pd
from generate import generate
import json

FONT_PATA = "../font"
categories = {
    "UNKNOWN": 0,
    # UNKNOWN list
    "license_number": 0,
    # classification list
    "name": 1,
    "phone": 2,
    "fax": 2,
    "call": 2,
    "email": 3,
    "position": 4,
    "company": 5,
    "department": 6,
    "address": 7,
    "site": 8,
    "account": 9,
    "wise": 10,
}


def get_TF(prob):
    return True if random.random() < prob else False


def get_random_margin(axis, min, max):
    min = min / 100
    max = max / 100
    return int(axis * random.uniform(min, max))


def get_font(font, scale, font_size=500 // 10 + random.randint(-10, 2)):
    if type(scale) == tuple:
        m, M = scale
        scale = random.uniform(m, M)
    imagefont = ImageFont.truetype(font, int(font_size * scale))
    return imagefont


def draw_font(feature, imagefont, bg_color, font_color, padding=False):
    if padding and len(feature) < 5:
        for _ in range(random.randint(0, 2)):
            feature = " ".join(feature)
    width, height = imagefont.getsize(feature)
    image = Image.new("RGBA", (width, height), bg_color)
    ImageDraw.Draw(image).text(xy=(0, 0), text=feature, font=imagefont, fill=font_color)
    return image, (width, height)


def get_annotation(category, x, y, w, h, feature, dir="Horizontal"):
    annotation = {
        "category_id": category,
        "orientation": "Horizontal",
        "points": [[x, y], [x + w, y], [x + w, y + h,], [x, y + h]],
        "text": feature,
    }
    return annotation


def draw_box(background, font, font_color, box_x, box_y, draw_list, includes, bg_color, info, header, scale, head=False, formation="stack", vertical=1):  # type = ["grid", "double", "stack", "solo"]
    annotation = []
    random.shuffle(draw_list)
    x_gap = random.randint(10, 14)
    y_gap = random.randint(4, 10)
    align = get_TF(0.5)
    if formation in ["solo", "double"]:
        var = draw_list[0]
        splt = len(draw_list) if formation == "solo" else int(len(draw_list) // 2)
        if len(draw_list) > 2:
            splt += random.randint(0, 1)
        loc_x, loc_y = box_x, box_y
        idx = 0
        for var in draw_list:
            if splt == idx:
                loc_x, loc_y = box_x, box_y
            padding = True if var in ["company", "name"] else False
            if includes[var]:
                var_font = get_font(font, scale[var])
                image, (width, height) = draw_font(info[var], var_font, bg_color, font_color, padding=padding)
                line_y = loc_y - height - 5 if idx < splt else loc_y + 5
                line_x = 900 // vertical - loc_x - width if align else loc_x
                background.paste(image, (line_x, line_y))
                annotation.append(get_annotation(categories[var], line_x, line_y, width, height, info[var]))
                loc_x += width + x_gap
            idx += 1
    else:
        grid_gap = random.randint(400, 420)
        loc_y = box_y
        col = 1
        for var in draw_list:
            loc_x = box_x if col else box_x + grid_gap
            padding = True if var in ["company", "name"] else False
            if includes[var]:
                var_font = get_font(font, scale[var])
                image, (width, height) = draw_font(info[var], var_font, bg_color, font_color, padding=padding)
                fix = 0
                if head and header.get(var, 0):
                    var_head_font = get_font(font, scale[var])
                    head_image, (head_width, head_height) = draw_font(header[var], var_head_font, bg_color, font_color)
                    add_head = Image.new("RGBA", (width + head_width + x_gap, head_height + 10), bg_color)
                    add_head.paste(head_image, (0, 0))
                    add_head.paste(image, (head_width + x_gap, 0))
                    image = add_head
                    fix += head_width + x_gap
                    head_x = loc_x + grid_gap - width - fix - 100 if align and formation == "stack" else loc_x
                    annotation.append(get_annotation(categories["UNKNOWN"], head_x, loc_y, head_width, height, header[var]))

                fix_x = loc_x + grid_gap - (width) - 100 if align and formation == "stack" else loc_x + fix
                annotation.append(get_annotation(categories[var], fix_x, loc_y, width, height, info[var]))

                line_x = loc_x + grid_gap - (width + fix) - 100 if align and formation == "stack" else loc_x
                background.paste(image, (line_x, loc_y))
                if formation == "grid" and col:
                    col = 0
                else:
                    loc_y += height + y_gap
                    col = 1
    return annotation


def image_generate(select="random", test_mode=False):
    info = generate()
    keywords = list(info.keys())
    head = True if get_TF(0.9) else False
    splt = random.choice([".", " :", "", ")"])
    header = {"phone": "Phone" + splt, "call": "Call" + splt, "fax": "Fax" + splt, "email": "Email" + splt, "site": random.choice(["Web", "site"]) + splt, "license_number": "사업자등록번호 :"}

    # includes: 특정 내용 포함 여부
    includes = dict(zip(keywords, [False for _ in range(len(keywords))]))
    includes["position"] = True if get_TF(0.8) else False
    if includes["position"]:
        includes["department"] = True if get_TF(0.75) else False
    includes["name"] = True
    includes["phone"] = True if get_TF(0.95) else False
    includes["call"] = True if get_TF(0.5) else False
    includes["fax"] = True if get_TF(0.5) else False
    includes["email"] = True if get_TF(0.9) else False
    includes["company"] = True if get_TF(0.8) else False
    if includes["company"]:
        includes["address"] = True if get_TF(0.7) else False
        includes["site"] = True if get_TF(0.5) else False
        includes["license_number"] = True if get_TF(0.5) else False
        includes["wise"] = True if get_TF(0.5) else False

    scale = {}
    # scale: 글자 크기 범위
    # logobox
    scale["company"] = (0.5, 1.6)
    scale["wise"] = (0.3, 0.5)
    # namebox
    scale["name"] = (0.9, 1.1)
    scale["position"] = (0.7, 0.9)
    scale["department"] = (0.7, 0.9)
    # optionbox
    option_scale = random.uniform(0.4, 0.5)
    scale["phone"] = option_scale
    scale["call"] = option_scale
    scale["fax"] = option_scale
    scale["email"] = option_scale
    scale["address"] = option_scale
    scale["site"] = option_scale
    scale["license_number"] = option_scale

    colormap = pd.read_csv("../data/colormap.csv")
    c_id = random.randint(0, len(colormap) - 1)
    Color_BG, Color_Logo, Color_Main, Color_Sub = colormap["Color_BG"][c_id], colormap["Color_Logo"][c_id], colormap["Color_Main"][c_id], colormap["Color_Sub"][c_id]

    if test_mode:
        includes = dict(zip(includes.keys(), [True for _ in range(len(includes.keys()))]))  # FOR TEST

    # font 지정
    Logo_font = "../font/logo/" + random.choice(os.listdir(FONT_PATA + "/logo"))
    Main_font = "../font/main/" + random.choice(os.listdir(FONT_PATA + "/main"))
    Sub_font = "../font/sub/" + random.choice(os.listdir(FONT_PATA + "/sub"))

    # case load
    with open("../data/template.json", "r") as j:
        json_object = json.load(j)
    if select == "random":
        case = json_object[random.choice(list(json_object.keys()))]
    else:
        case = json_object[select]
    width = case["width"]
    height = case["height"]
    assert height / width == 5 / 9
    image = Image.new("RGBA", (width, height), Color_BG)
    logobox_list, logobox_x, logobox_y, logo_format = (
        case["logobox"]["draw_list"],
        case["logobox"]["loc_x"] + get_random_margin(width, 5, 25),
        case["logobox"]["loc_y"] + get_random_margin(height, -2, 2),
        case["logobox"]["formation"],
    )
    namebox_list, namebox_x, namebox_y, name_format = (
        case["namebox"]["draw_list"],
        case["namebox"]["loc_x"] + get_random_margin(width, 5, 8),
        case["namebox"]["loc_y"] + get_random_margin(height, -2, 2),
        case["namebox"]["formation"],
    )
    optionbox1_list, optionbox1_x, optionbox1_y, opt1_format = (
        case["optionbox1"]["draw_list"],
        case["optionbox1"]["loc_x"] + get_random_margin(width, 5, 8),
        case["optionbox1"]["loc_y"] + get_random_margin(height, -2, 2),
        case["optionbox1"]["formation"],
    )
    optionbox2_list, optionbox2_x, optionbox2_y, opt2_format = (
        case["optionbox2"]["draw_list"],
        case["optionbox2"]["loc_x"] + get_random_margin(width, 5, 8),
        case["optionbox2"]["loc_y"] + get_random_margin(height, -2, 2),
        case["optionbox2"]["formation"],
    )

    # bbox 정보
    image_info = []
    image_info.extend(draw_box(image, Logo_font, Color_Logo, logobox_x, logobox_y, logobox_list, includes, Color_BG, info, header, scale, formation=logo_format))
    image_info.extend(draw_box(image, Main_font, Color_Main, namebox_x, namebox_y, namebox_list, includes, Color_BG, info, header, scale, formation=name_format))
    image_info.extend(draw_box(image, Sub_font, Color_Sub, optionbox1_x, optionbox1_y, optionbox1_list, includes, Color_BG, info, header, scale, head, formation=opt1_format))
    image_info.extend(draw_box(image, Sub_font, Color_Sub, optionbox2_x, optionbox2_y, optionbox2_list, includes, Color_BG, info, header, scale, head, formation=opt2_format))

    return image, image_info, width, height

