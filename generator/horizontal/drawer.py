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
    "social_id": 11,
}


def get_TF(prob: float):
    """Get True or False compar with prob
    Args:
        prob (float)
    Returns:
        bool
    """
    return True if random.random() < prob else False


def get_random_margin(axis: int, min: int, max: int):
    """get random margin for axis size ratio (min, max)
    Args:
        axis (int): _description_
        min (int): _description_
        max (int): _description_
    Returns:
        int
    """
    min = min / 100
    max = max / 100
    return int(axis * random.uniform(min, max))


def get_font(font, scale, font_size=500 // 10 + random.randint(-10, 2)):
    """get image font
    Args:
        font (str): font path
        scale (float tuple or float): image font size
        font_size (int, optional): font size. Defaults to 500//10+random.randint(-10, 2).
    Returns:
        imagefont
    """
    if type(scale) == tuple:
        m, M = scale
        scale = random.uniform(m, M)
    imagefont = ImageFont.truetype(font, int(font_size * scale))
    return imagefont


def draw_font(feature, imagefont, axis, loc_x, padding=False):
    """
    make feature to image and get size
    """
    if padding and len(feature) < 5:
        for _ in range(random.randint(0, 2)):
            feature = " ".join(feature)
    width, height = imagefont.getsize(feature)
    while (axis - loc_x < width) and imagefont.size > 10:
        imagefont = ImageFont.truetype(imagefont.path, imagefont.size - 1)
        width, height = imagefont.getsize(feature)
    return feature, imagefont, (width, height)


def get_annotation(category, x: int, y: int, w: int, h: int, feature, dir="Horizontal"):
    """get annotation with location and Etc
    Args:
        category (int): category value
        x (int): horizontal location of start point
        y (int): vertical location of start point
        w (int): width
        h (int): height
        feature (var): word or sentence
        dir (str, optional): Defaults to "Horizontal".
    Returns:
        annotation dict
    """
    annotation = {
        "category_id": category,
        "orientation": dir,
        "points": [[x, y], [x + w, y], [x + w, y + h,], [x, y + h]],
        "text": feature,
    }
    return annotation


def draw_logo(background, loc_x, loc_y, logo_size, path):
    """
    draw logo on background
    """
    image = Image.open(path).convert("RGBA")
    image = image.resize((logo_size, logo_size))
    background.paste(image, (loc_x, loc_y), image)
    return background


def draw_box(background, font, font_color, box_info, infos):  # type = ["grid", "double", "stack", "single"]
    """_summary_
    Args:
        background (image)
        font (str): font path
        font_color: auto selected
        box_info (tuple): write in template (draw_list, box_x, box_y, formation, axis...)
        infos (tuple): includes, info, header, scale

    Returns:
        annotations list
    """
    draw = ImageDraw.Draw(background)
    draw_list, box_x, box_y, formation, axis = box_info
    includes, info, header, scale = infos
    annotation = []
    align = get_TF(0.5)
    # logo 포함된 상자의 경우 로고 그리고 밀기
    if "logo" in draw_list:
        logo_size = random.randint(30, 80)
        pos_x = axis - box_x - logo_size if align else box_x
        background = draw_logo(background, pos_x, box_y, logo_size, includes["logo"])
        box_x += logo_size + int(axis * random.uniform(0.01, 0.05))
        draw_list.remove("logo")
    # 순서 셔플
    random.shuffle(draw_list)
    x_gap = random.randint(10, 14)
    y_gap = random.randint(4, 10)
    grid_gap = random.randint(400, 420)
    idx = 0
    col = 1
    splt = int(len(draw_list) // 2) if formation == "double" else len(draw_list)
    if len(draw_list) > 2 and formation == "double":
        splt += random.randint(0, 1)

    loc_x, loc_y = box_x, box_y
    for var in draw_list:
        word = info[var] if type(info[var]) == str else random.choice(info[var])
        if splt == idx:
            loc_x, loc_y = box_x, box_y
        padding = True if var in ["company", "name"] else False
        if includes[var]:
            var_font = get_font(font, scale[var])
            feature, var_font, (width, height) = draw_font(word, var_font, axis, loc_x, padding=padding)
            if formation in ["double", "single"]:
                line_y = loc_y - height - 5 if idx < splt else loc_y + 5
            else:
                loc_x = box_x if col else box_x + grid_gap
                line_y = loc_y

            fix = 0
            head_height = 0
            if header.get(var, 0):
                if var == "social_id":
                    if get_TF(0.3):
                        var_head_font = get_font(font, scale[var])
                        social_header = random.choice(["kakao.", "instagram.", "facebook."])
                        head_feature, head_font, (head_width, head_height) = draw_font(social_header, var_head_font, axis, loc_x)
                        fix += head_width + x_gap
                        head_x = axis - loc_x - width - fix if align else loc_x
                        if head_x < 900:
                            draw.text((head_x, line_y), head_feature, fill=font_color, font=head_font)
                            annotation.append(get_annotation(categories[var], head_x, line_y, head_width + x_gap + width, head_height, social_header + word))
                    else:
                        icon_path = "../data/" + random.choice(header[var])
                        head_width = var_font.size
                        fix += head_width + x_gap
                        icon_x = axis - loc_x - width - fix if align else loc_x
                        if icon_x < 900:
                            background = draw_logo(background, icon_x, line_y, head_width, icon_path)
                            annotation.append(get_annotation(categories[var], icon_x + x_gap + head_width, line_y, width, height, word))
                else:
                    var_head_font = get_font(font, scale[var])
                    head_feature, head_font, (head_width, head_height) = draw_font(header[var], var_head_font, axis, loc_x)
                    fix += head_width + x_gap
                    head_x = axis - loc_x - width - fix if align else loc_x
                    if head_x < 900:
                        draw.text((head_x, line_y), head_feature, fill=font_color, font=head_font)
                        annotation.append(get_annotation(categories[var], head_x, line_y, head_width + x_gap + width, head_height, header[var] + word))
            fix_x = axis - loc_x - width if align else loc_x + fix
            if fix_x < 900:
                draw.text((fix_x, line_y), feature, fill=font_color, font=var_font)
                if not fix:
                    annotation.append(get_annotation(categories[var], fix_x, line_y, width, height, word))

            if formation == "grid" and col:
                col = 0
            else:
                if formation in ["single", "double"]:
                    loc_x += width + x_gap + fix
                else:
                    if head_height:
                        height = head_height
                    loc_y += height + y_gap
                    col = 1
        idx += 1
    return annotation


def image_generate(select="random", test_mode=False):
    """
    includes: key = category, value = bool.
    scale: key = category, value = float tuple 


    Args:
        select (str, optional): random is all case. Else, output is selected case. Defaults to "random".
        test_mode (bool, optional): if True, set all includes values True. Defaults to False.

    Returns:
        image, image_info, width, height
    """
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
                "social_id": list(pd.read_csv("../data/sns_logo.csv")["images"]),
            },
            {
                "phone": random.choice(["M", "P"]) + splt,
                "call": "T" + splt,
                "fax": "F" + splt,
                "email": "E" + splt,
                "site": "H" + splt,
                "license_number": random.choice(["사업자등록번호", "등록번호", "허가번호"]) + splt,
                "social_id": list(pd.read_csv("../data/sns_logo.csv")["images"]),
            },
            {
                "phone": random.choice(["휴대전화", "휴대폰", "무선전화", "핸드폰", "연락처", "무선"]) + splt,
                "call": random.choice(["유선", "유선전화", "전화", "연락처"]) + splt,
                "fax": "팩스" + splt,
                "email": random.choice(["메일", "이메일", "전자우편"]) + splt,
                "site": random.choice(["웹", "사이트", "홈페이지"]) + splt,
                "license_number": random.choice(["사업자등록번호", "등록번호", "허가번호"]) + splt,
                "social_id": list(pd.read_csv("../data/sns_logo.csv")["images"]),
            },
            {"license_number": random.choice(["사업자등록번호", "등록번호", "허가번호"]) + splt, "social_id": list(pd.read_csv("../data/sns_logo.csv")["images"]),},
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
    includes["social_id"] = True if get_TF(0.7) else False
    logo = True if get_TF(0.5) else False

    # FOR TEST
    if test_mode:
        includes = dict(zip(includes.keys(), [True for _ in range(len(includes.keys()))]))
        logo = True

    includes["logo"] = "../data/images/logo/" + random.choice(os.listdir("../data/images/logo"))

    scale = {}
    # scale: 글자 크기 범위
    # logobox
    scale["company"] = (0.5, 1.6)
    scale["wise"] = (0.3, 0.5)
    # namebox
    scale["name"] = (0.9, 1.1)
    scale["position"] = (0.6, 0.9)
    scale["department"] = (0.6, 0.9)
    # optionbox
    option_scale = random.uniform(0.4, 0.5)
    scale["phone"] = option_scale
    scale["call"] = option_scale
    scale["fax"] = option_scale
    scale["email"] = option_scale
    scale["address"] = option_scale
    scale["site"] = option_scale
    scale["license_number"] = option_scale
    scale["social_id"] = option_scale

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

    # Set Backgroud
    image = Image.new("RGBA", (width, height), Color_BG)

    # Set Boxes
    logobox = (
        case["logobox"]["draw_list"],
        case["logobox"]["loc_x"] + get_random_margin(width, 3, 10),
        case["logobox"]["loc_y"] + get_random_margin(height, 0, 5),
        case["logobox"]["formation"],
        case["logobox"]["axis"],
    )
    namebox = (
        case["namebox"]["draw_list"],
        case["namebox"]["loc_x"] + get_random_margin(width, 3, 5),
        case["namebox"]["loc_y"] + get_random_margin(height, 0, 2),
        case["namebox"]["formation"],
        case["namebox"]["axis"],
    )
    optionbox1 = (
        case["optionbox1"]["draw_list"],
        case["optionbox1"]["loc_x"] + get_random_margin(width, 3, 5),
        case["optionbox1"]["loc_y"] + get_random_margin(height, 0, 2),
        case["optionbox1"]["formation"],
        case["optionbox1"]["axis"],
    )
    optionbox2 = (
        case["optionbox2"]["draw_list"],
        case["optionbox2"]["loc_x"] + get_random_margin(width, 3, 5),
        case["optionbox2"]["loc_y"] + get_random_margin(height, 0, 2),
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
