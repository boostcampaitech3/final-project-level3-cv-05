# -*-coding:UTF-8
import os
from PIL import Image, ImageFont, ImageDraw
import random
import pandas as pd
from generate import generate

FONT_PATA = "../font"
categories = {"UNKNOWN": 0, "name": 1, "phone": 2, "fax": 2, "call": 2, "email": 3, "position": 4, "company": 5, "department": 6, "address": 7, "site": 8, "account": 9, "wise": 10}


def get_TF(prob):
    return True if random.random() < prob else False


def get_font(
    feature, font, scale, font_size=500 // 10 + random.randint(-10, 2), padding=0,
):
    if padding:
        for _ in range(padding):
            feature = " ".join(feature)
    if type(scale) == tuple:
        m, M = scale
        scale = random.uniform(m, M)
    setFont = ImageFont.truetype(font, int(font_size * scale))
    return setFont, setFont.getsize(feature)


def draw_font(feature, image, font, color, loc_x, loc_y, category=0, align="left", width=900, height=500, padding=0):
    origin = feature
    if padding:
        for _ in range(padding):
            feature = " ".join(feature)
    while loc_x + font.getsize(feature)[0] >= width and font.size > 2:
        font = ImageFont.truetype(font.path, font.size - 1)
    if align == "right":
        loc_x = width - loc_x - font.getsize(feature)[0]
    ImageDraw.Draw(image).text(xy=(loc_x, loc_y), text=feature, font=font, fill=color)

    loc_x, loc_y = int(loc_x), int(loc_y)
    w, h = int(font.getsize(feature)[0]), int(font.getsize(feature)[1])

    annotation = {
        "category_id": category,
        "orientation": "Horizontal",
        "points": [[loc_x, loc_y], [loc_x + w, loc_y], [loc_x + w, loc_y + h,], [loc_x, loc_y + h]],
        "text": origin,
    }
    assert annotation["category_id"] in range(0, 11) and annotation["orientation"] and annotation["points"] and annotation["text"]
    return annotation


def image_generate(test_mode=False):
    info = generate()
    keywords = list(info.keys())
    # keyword 변수 선언
    company, position, position, department, name, phone, call, fax, email, site, address, company, license_number, wise = (
        info["company"],
        info["position"],
        info["position"],
        info["department"],
        info["name"],
        info["phone"],
        info["call"],
        info["fax"],
        info["email"],
        info["site"],
        info["address"],
        info["company"],
        info["license_number"],
        info["wise"],
    )
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

    random_bg = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    random_name = tuple([255 - c for c in random_bg])
    random_logo = tuple([int(c * 0.9) for c in random_name])
    random_sub = tuple([int(c * 1.1) for c in random_name])
    colormap = pd.read_csv("../data/colormap.csv")
    c_id = random.randint(0, len(colormap) - 1)
    Color_BG, Color_Logo, Color_Main, Color_Sub = colormap["Color_BG"][c_id], colormap["Color_Logo"][c_id], colormap["Color_Main"][c_id], colormap["Color_Sub"][c_id]

    if test_mode:
        includes = dict(zip(includes.keys(), [True for _ in range(len(includes.keys()))]))  # FOR TEST

    # font 지정
    Logo_font = "../font/logo/" + random.choice(os.listdir(FONT_PATA + "/logo"))
    Main_font = "../font/main/" + random.choice(os.listdir(FONT_PATA + "/main"))
    Sub_font = "../font/sub/" + random.choice(os.listdir(FONT_PATA + "/sub"))

    # 빈 이미지 생성
    height = 500
    width = 900

    # 배경색 지정
    image = Image.new("RGBA", (width, height), Color_BG)

    # bbox 정보
    image_info = []

    ################################## 위치 & 폰트 지정 #################################
    # 기준 font size
    standard = height // 10 + random.randint(-10, 0)
    margin = standard // 4 + random.randint(0, 3)
    logobox_x = width * (random.randint(5, 25) / 100)
    namebox_x = width * (random.randint(5, 30) / 100)
    optionbox_x = width * (random.randint(5, 10) / 100)

    # 박스 y축 최대 크기
    #   logobox: 25% namebox: 25% optionbox: 35%
    if random.random() < 0.8:
        logobox_y = height * (random.randint(6, 7) / 100)
        if random.random() < 0.8:
            namebox_y = height * (random.randint(40, 41) / 100)
            optionbox_y = height - height * (random.randint(5, 10) / 100)
        else:
            namebox_y = height - height * (random.randint(25, 30) / 100)
            optionbox_y = namebox_y - height * (random.randint(10, 15) / 100)
    else:
        logobox_y = height - height * (random.randint(23, 24) / 100)
        if random.random() < 0.8:
            namebox_y = height * (random.randint(10, 15) / 100)
            optionbox_y = logobox_y - height * (random.randint(10, 12) / 100)
        else:
            namebox_y = logobox_y - height * (random.randint(20, 22) / 100)
            optionbox_y = height * (random.randint(30, 35) / 100)

    ############################ 이름 & 직업(or 직급) & 부서 ############################
    namebox_align = random.choice(["left", "right"])
    name_padding = random.randint(0, 2) if len(name) < 4 else 0

    name_x, name_y = namebox_x, namebox_y
    name_font, name_size = get_font(name, Main_font, (0.95, 1.05), padding=name_padding)
    n_case = random.choice([0, 1])
    if includes["position"]:
        position_font, position_size = get_font(position, Main_font, (0.75, 0.85))
        position_x, position_y = namebox_x, namebox_y
        if n_case:
            name_x += position_size[0] + margin
            name_annotation = draw_font(name, image, name_font, Color_Main, name_x, name_y, categories["name"], namebox_align, padding=name_padding)
            position_y += name_size[1] - position_size[1]
            position_annotation = draw_font(position, image, position_font, Color_Main, position_x, position_y, categories["position"], namebox_align)
        else:
            name_annotation = draw_font(name, image, name_font, Color_Main, name_x, name_y, categories["name"], namebox_align, padding=name_padding)
            position_x += name_size[0] + margin
            position_y += name_size[1] - position_size[1]
            position_annotation = draw_font(position, image, position_font, Color_Main, position_x, position_y, categories["position"], namebox_align)
        image_info.append(position_annotation)
    else:
        name_annotation = draw_font(name, image, name_font, Color_Main, name_x, name_y, categories["name"], namebox_align, padding=name_padding)
    image_info.append(name_annotation)

    if includes["department"]:
        d_font, d_size = get_font(department, Main_font, (0.7, 0.8))
        d_x, d_y = namebox_x, namebox_y
        if namebox_align == "right" and n_case == 0 and random.random() < 0.25:
            d_x += name_size[0] + margin
            d_y += name_size[1] - d_size[1]
            if includes["position"]:
                d_x += position_size[0] + margin
        else:
            d_case = random.choice([0, 1, 2, 3])
            if d_case < 2:
                d_y -= d_size[1]
            else:
                d_y += name_size[1] + 10
            if d_case % 2:
                d_x = d_x + name_size[0] + position_size[0] + 10 - d_size[0]
        department_annotation = draw_font(department, image, d_font, Color_Main, d_x, d_y, categories["department"], namebox_align)
        image_info.append(department_annotation)

    ########################## 회사명 & 로고(추후 추가) & 사훈###########################
    # 로고 추가시 겹쳐도 글자 뒤에 오도록 앞에서 추가
    if includes["company"]:
        logobox_align = random.choice(["left", "right"])
        company_padding = random.randint(0, 2) if len(company) < 4 else 0
        company_x, company_y = logobox_x, logobox_y
        company_font, company_size = get_font(company, Logo_font, (0.5, 1.6), padding=company_padding)
        comapny_annotation = draw_font(company, image, company_font, Color_Logo, company_x, company_y, categories["company"], logobox_align, padding=company_padding)
        image_info.append(comapny_annotation)
        if includes["wise"]:
            wise_x, wise_y = logobox_x, logobox_y
            wise_font, wise_size = get_font(wise, Sub_font, (0.4, 0.5))
            wise_y = random.choice([wise_y + company_size[1] + 5, wise_y - wise_size[1] - 5])
            wise_annotation = draw_font(wise, image, wise_font, Color_Sub, wise_x, wise_y, categories["wise"], logobox_align)
            image_info.append(wise_annotation)
    ################################## 번호 & 메일 & 옵션###############################
    optional_scale = random.uniform(0.4, 0.45)
    option_align = "left"  # random.choice(["left", "right"])
    optional_x, optional_y = optionbox_x, optionbox_y

    for var in ["address", "license_number"]:
        if includes[var]:
            optional_x = optionbox_x
            var_font, var_size = get_font(info[var], Sub_font, optional_scale)
            optional_y -= var_size[1] + margin
            if header.get(var, -1) != -1:
                var_head_font, var_head_size = get_font(header[var], Sub_font, optional_scale)
                var_head_annotation = draw_font(header[var], image, var_head_font, Color_Main, optional_x, optional_y, categories["UNKNOWN"], option_align)
                image_info.append(var_head_annotation)
                optional_x += var_head_size[0]
            var_annotation = draw_font(info[var], image, var_font, Color_Main, optional_x + margin, optional_y, categories["UNKNOWN"], option_align)
            image_info.append(var_annotation)

    add_width = width // 2 + random.randint(-20, 20)

    up = 0
    head_kw = ["site", "email", "fax", "call", "phone"]
    random.shuffle(head_kw)
    for var in head_kw:
        if includes[var]:
            var_font, var_size = get_font(info[var], Sub_font, optional_scale)
            if up % 2:
                optional_x = optionbox_x + add_width
            else:
                optional_x = optionbox_x
                optional_y -= var_size[1] + margin
            if head:
                var_head_font, var_head_size = get_font(header[var], Sub_font, optional_scale)
                var_head_annotation = draw_font(header[var], image, var_head_font, Color_Sub, optional_x, optional_y, categories["UNKNOWN"], option_align)
                image_info.append(var_head_annotation)
                optional_x += var_head_size[0] + margin
            var_annotation = draw_font(info[var], image, var_font, Color_Main, optional_x, optional_y, categories[var], option_align)
            image_info.append(var_annotation)
            up += 1
    ####################################################################################

    return image, image_info, width, height