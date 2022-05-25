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


def draw_font(feature, imagefont, axis, loc_x, padding=False):
    if padding and len(feature) < 5:
        for _ in range(random.randint(0, 2)):
            feature = " ".join(feature)
    width, height = imagefont.getsize(feature)
    while axis % 900 < loc_x % 450 + width and imagefont.size > 1:
        imagefont = ImageFont.truetype(imagefont.path, imagefont.size - 1)
        width, height = imagefont.getsize(feature)
    return feature, imagefont, (width, height)


def get_annotation(category, x, y, w, h, feature, dir="Horizontal"):
    annotation = {
        "category_id": category,
        "orientation": dir,
        "points": [[x, y], [x + w, y], [x + w, y + h,], [x, y + h]],
        "text": feature,
    }
    return annotation


def draw_logo(background, loc_x, loc_y, includes, align):
    image = Image.open(includes["logo"]).convert("RGBA")
    l = random.randint(50, 100)
    image = image.resize((l, l))
    background.paste(image, (loc_x, loc_y), image)
    return background, l


def draw_box(background, font, font_color, box_info, infos, vertical=1):  # type = ["grid", "double", "stack", "single"]
    draw = ImageDraw.Draw(background)
    draw_list, box_x, box_y, formation, axis = box_info
    includes, info, header, scale = infos
    annotation = []
    align = get_TF(0.5)
    # logo 포함된 상자의 경우 로고 그리고 밀기
    if "logo" in draw_list:
        pos_x = axis - box_x - 50 if align else box_x
        background, x_push = draw_logo(background, pos_x, box_y, includes, align=align)
        box_x += x_push + int(axis * random.uniform(0.01, 0.05))
        draw_list.remove("logo")
    # 순서 셔플
    random.shuffle(draw_list)
    x_gap = random.randint(10, 14)
    y_gap = random.randint(4, 10)
    if formation in ["single", "double"]:
        loc_x, loc_y = box_x, box_y
        splt = len(draw_list) if formation == "single" else int(len(draw_list) // 2)
        if len(draw_list) > 2:
            splt += random.randint(0, 1)
        idx = 0
        for var in draw_list:
            if splt == idx:
                loc_x, loc_y = box_x, box_y
            padding = True if var in ["company", "name"] else False
            if includes[var]:
                var_font = get_font(font, scale[var])
                feature, var_font, (width, height) = draw_font(info[var], var_font, axis, loc_x, padding=padding)
                line_y = loc_y - height - 5 if idx < splt else loc_y + 5
                line_x = background.size[0] // vertical - loc_x - width if align else loc_x
                draw.text((line_x, line_y), feature, fill=font_color, font=var_font)
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
                feature, var_font, (width, height) = draw_font(info[var], var_font, axis, loc_x, padding=padding)
                fix = 0
                if header.get(var, 0):
                    var_head_font = get_font(font, scale[var])
                    head_feature, head_font, (head_width, head_height) = draw_font(header[var], var_head_font, axis, loc_x)
                    fix += head_width + x_gap
                    head_x = axis - loc_x - width - fix if align else loc_x
                    draw.text((head_x, loc_y), head_feature, fill=font_color, font=head_font)
                    annotation.append(get_annotation(categories[var], head_x, loc_y, head_width + x_gap + width, head_height, header[var] + info[var]))
                fix_x = axis - loc_x - width if align else loc_x + fix
                draw.text((fix_x, loc_y), feature, fill=font_color, font=var_font)
                if not fix:
                    annotation.append(get_annotation(categories[var], fix_x, loc_y, width, height, info[var]))
                if formation == "grid" and col:
                    col = 0
                else:
                    loc_y += height + y_gap
                    col = 1
    return annotation


def image_generate(select="random", test_mode=False):
    info = generate()
    keywords = list(info.keys())
    splt = random.choice([".", ":", "", ")"])
    header = random.choice(
        [
            {
                "phone": random.choice(["Phone", "Mobile"]) + splt,
                "call": "Tel" + splt,
                "fax": "Fax" + splt,
                "email": "Email" + splt,
                "site": random.choice(["Web", "Site"]) + splt,
                "license_number": random.choice(["사업자등록번호", "등록번호", "허가번호"]) + splt,
            },
            {
                "phone": random.choice(["M", "P"]) + splt,
                "call": "T" + splt,
                "fax": "F" + splt,
                "email": "E" + splt,
                "site": "H" + splt,
                "license_number": random.choice(["사업자등록번호", "등록번호", "허가번호"]) + splt,
            },
            {
                "phone": random.choice(["휴대전화", "휴대폰", "무선전화", "핸드폰", "연락처", "무선"]) + splt,
                "call": random.choice(["유선", "유선전화", "전화", "연락처"]) + splt,
                "fax": "팩스" + splt,
                "email": random.choice(["메일", "이메일", "전자우편"]) + splt,
                "site": random.choice(["웹", "사이트", "홈페이지"]) + splt,
                "license_number": random.choice(["사업자등록번호", "등록번호", "허가번호"]) + splt,
            },
            {"license_number": random.choice(["사업자등록번호", "등록번호", "허가번호"]) + splt,},
        ]
    )

    # includes: 특정 내용 포함 여부
    includes = dict(zip(keywords, [False for _ in range(len(keywords))]))
    includes["position"] = True if get_TF(0.9) else False
    includes["department"] = True if get_TF(0.75) else False
    includes["name"] = True
    includes["phone"] = True if get_TF(0.95) else False
    includes["call"] = True if get_TF(0.6) else False
    includes["fax"] = True if get_TF(0.6) else False
    includes["email"] = True if get_TF(0.9) else False
    includes["company"] = True if get_TF(0.8) else False
    includes["wise"] = True if get_TF(0.5) else False
    includes["site"] = True if get_TF(0.5) else False
    includes["address"] = True if get_TF(0.7) else False
    includes["license_number"] = True if get_TF(0.5) else False
    logo = True if get_TF(0.5) else False

    # FOR TEST
    if test_mode:
        includes = dict(zip(includes.keys(), [True for _ in range(len(includes.keys()))]))
        logo = True

    includes["logo"] = "../data/images/" + random.choice(os.listdir("../data/images"))

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
    Color_BG, Color_Logo, Color_Main, Color_Sub = (colormap["Color_BG"][c_id], colormap["Color_Logo"][c_id], colormap["Color_Main"][c_id], colormap["Color_Sub"][c_id])

    # Font 지정
    Logo_font = "../font/logo/" + random.choice(os.listdir(FONT_PATA + "/logo"))
    Main_font = "../font/main/" + random.choice(os.listdir(FONT_PATA + "/main"))
    Sub_font = "../font/sub/" + random.choice(os.listdir(FONT_PATA + "/sub"))

    # Case Load
    with open("../data/template.json", "r") as j:
        json_object = json.load(j)
    if select == "random":
        case = json_object[random.choice(list(json_object.keys()))]
    else:
        case = json_object[select]
    width = case["width"]
    height = case["height"]
    assert height / width == 5 / 9

    # Set Backgroud
    image = Image.new("RGBA", (width, height), Color_BG)

    # Set Boxes
    logobox = (
        case["logobox"]["draw_list"],
        case["logobox"]["loc_x"] + get_random_margin(width, 3, 25),
        case["logobox"]["loc_y"] + get_random_margin(height, 5, 10),
        case["logobox"]["formation"],
        case["logobox"]["axis"],
    )
    namebox = (
        case["namebox"]["draw_list"],
        case["namebox"]["loc_x"] + get_random_margin(width, 3, 5),
        case["namebox"]["loc_y"] + get_random_margin(height, -2, 2),
        case["namebox"]["formation"],
        case["namebox"]["axis"],
    )
    optionbox1 = (
        case["optionbox1"]["draw_list"],
        case["optionbox1"]["loc_x"] + get_random_margin(width, 3, 5),
        case["optionbox1"]["loc_y"] + get_random_margin(height, -2, 2),
        case["optionbox1"]["formation"],
        case["optionbox1"]["axis"],
    )
    optionbox2 = (
        case["optionbox2"]["draw_list"],
        case["optionbox2"]["loc_x"] + get_random_margin(width, 3, 5),
        case["optionbox2"]["loc_y"] + get_random_margin(height, -2, 2),
        case["optionbox2"]["formation"],
        case["optionbox2"]["axis"],
    )

    # bbox 정보
    image_info = []
    infos = includes, info, header, scale
    if logobox[0]:
        if logo:
            logobox[0].append("logo")
        image_info.extend(draw_box(image, Logo_font, Color_Logo, logobox, infos))
    if namebox[0]:
        image_info.extend(draw_box(image, Main_font, Color_Main, namebox, infos))
    if optionbox1[0]:
        image_info.extend(draw_box(image, Sub_font, Color_Sub, optionbox1, infos))
    if optionbox2[0]:
        image_info.extend(draw_box(image, Sub_font, Color_Sub, optionbox2, infos))

    return image, image_info, width, height
