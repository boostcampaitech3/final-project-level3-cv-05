# -*-coding:UTF-8
import os
from PIL import Image, ImageFont, ImageDraw
import random

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
    while loc_x + font.getsize(feature)[0] >= width:
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


def image_generate(info, test_mode=False):
    keywords = list(info.keys())
    # keyword 변수 선언
    company = info["company"]
    position = info["position"]
    position = info["position"]
    department = info["department"]
    name = info["name"]
    head = True if random.random() < 0.9 else False
    splt = random.choice([".", " :", "", ")"])
    phone_head, call_head, fax_head, email_head, site_head = "Phone" + splt, "Call" + splt, "Fax" + splt, "Email" + splt, random.choice(["Web", "site"]) + splt
    phone = info["phone"][0]
    call = info["phone"][1]
    fax = info["phone"][2]
    email = info["email"]
    site = info["site"]
    address = info["address"]
    company = info["company"]
    license_head = "사업자등록번호 :"
    license_number = info["license_number"]
    wise = info["wise"]

    # includes: 특정 내용 포함 여부
    includes = dict(zip(keywords, [False for _ in range(len(keywords))]))
    includes["company"] = True if get_TF(0.8) else False
    includes["position"] = True if get_TF(0.8) else False
    if includes["position"]:
        includes["department"] = True if get_TF(0.75) else False
    includes["name"] = True
    includes["phone"] = True if get_TF(0.95) else False
    includes["call"] = True if get_TF(0.5) else False
    includes["fax"] = True if get_TF(0.5) else False
    includes["email"] = True if get_TF(0.9) else False
    if includes["company"]:
        includes["address"] = True if get_TF(0.7) else False
        includes["site"] = True if get_TF(0.5) else False
        includes["license_number"] = True if get_TF(0.5) else False
        includes["wise"] = True if get_TF(0.5) else False

    random_bg = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    random_name = tuple([255 - c for c in random_bg])
    random_logo = tuple([int(c * 0.9) for c in random_name])
    random_sub = tuple([int(c * 1.1) for c in random_name])
    colormap = [
        ("white", ["blue", "green", "red", "purple"][random.randint(0, 3)], "black", "gray",),
        (random_bg, random_logo, random_name, random_sub),
    ]
    Color_BG, Color_Logo, Color_Main, Color_Sub = colormap[random.randint(0, len(colormap) - 1)]

    if test_mode == True:
        includes = dict(zip(keywords, [True for _ in range(len(keywords))]))  # FOR TEST
        includes["call"] = True  # FOR TEST
        includes["fax"] = True  # FOR TEST

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
    logobox_x = width * (random.randint(5, 10) / 100)
    namebox_x = width * (random.randint(5, 30) / 100)
    optionbox_x = width * (random.randint(5, 16) / 100)

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
    if includes["position"]:
        position_font, position_size = get_font(position, Main_font, (0.75, 0.85))
        n_case = random.choice([0, 1])
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
    optional_x, optional_y = optionbox_x, optionbox_y
    optional_scale = random.uniform(0.4, 0.45)
    option_align = "left"  # random.choice(["left", "right"])

    if includes["license_number"]:
        license_number_font, license_number_size = get_font(license_number, Sub_font, optional_scale)
        optional_y -= license_number_size[1] + margin
        license_head_font, license_head_size = get_font(license_head, Sub_font, optional_scale)
        license_head_annotation = draw_font(license_head, image, license_head_font, Color_Main, optional_x, optional_y, categories["UNKNOWN"], option_align)
        image_info.append(license_head_annotation)
        license_number_annotation = draw_font(license_number, image, license_number_font, Color_Main, optional_x + license_head_size[0] + margin, optional_y, categories["UNKNOWN"], option_align)
        image_info.append(license_number_annotation)
    if includes["address"]:
        address_font, address_size = get_font(address, Sub_font, optional_scale)
        optional_y -= address_size[1] + margin
        address_annotation = draw_font(address, image, address_font, Color_Main, optional_x, optional_y, categories["address"], option_align)
        image_info.append(address_annotation)

    add_width = width // 2 + random.randint(-20, 20)

    up = 0
    if includes["site"]:
        site_font, site_size = get_font(site, Sub_font, optional_scale)
        if up % 2:
            optional_x = optionbox_x + add_width
        else:
            optional_x = optionbox_x
            optional_y -= site_size[1] + margin
        if head:
            site_head_font, site_head_size = get_font(site_head, Sub_font, optional_scale)
            site_head_annotation = draw_font(site_head, image, site_head_font, Color_Sub, optional_x, optional_y, categories["UNKNOWN"], option_align)
            image_info.append(site_head_annotation)
            optional_x += site_head_size[0] + margin
        site_annotation = draw_font(site, image, site_font, Color_Main, optional_x, optional_y, categories["site"], option_align)
        image_info.append(site_annotation)
        up += 1
    if includes["email"]:
        email_font, email_size = get_font(email, Sub_font, optional_scale)
        if up % 2:
            optional_x = optionbox_x + add_width
        else:
            optional_x = optionbox_x
            optional_y -= email_size[1] + margin
        if head:
            email_head_font, email_head_size = get_font(email_head, Sub_font, optional_scale)
            email_head_annotation = draw_font(email_head, image, email_head_font, Color_Sub, optional_x, optional_y, categories["UNKNOWN"], option_align)
            image_info.append(email_head_annotation)
            optional_x += email_head_size[0] + margin
        email_annotation = draw_font(email, image, email_font, Color_Main, optional_x, optional_y, categories["email"], option_align)
        image_info.append(email_annotation)
        up += 1
    if includes["fax"]:
        fax_font, fax_size = get_font(fax, Sub_font, optional_scale)
        if up % 2:
            optional_x = optionbox_x + add_width
        else:
            optional_x = optionbox_x
            optional_y -= fax_size[1] + margin
        if head:
            fax_head_font, fax_head_size = get_font(fax_head, Sub_font, optional_scale)
            fax_head_annotation = draw_font(fax_head, image, fax_head_font, Color_Sub, optional_x, optional_y, categories["UNKNOWN"], option_align)
            image_info.append(fax_head_annotation)
            optional_x += fax_head_size[0] + margin
        fax_annotation = draw_font(fax, image, fax_font, Color_Main, optional_x, optional_y, categories["fax"], option_align)
        image_info.append(fax_annotation)
        up += 1
    if includes["call"]:
        call_font, call_size = get_font(call, Sub_font, optional_scale)
        if up % 2:
            optional_x = optionbox_x + add_width
        else:
            optional_x = optionbox_x
            optional_y -= call_size[1] + margin
        if head:
            call_head_font, call_head_size = get_font(call_head, Sub_font, optional_scale)
            call_head_annotation = draw_font(call_head, image, call_head_font, Color_Sub, optional_x, optional_y, categories["UNKNOWN"], option_align)
            image_info.append(call_head_annotation)
            optional_x += call_head_size[0] + margin
        call_annotation = draw_font(call, image, call_font, Color_Main, optional_x, optional_y, categories["call"], option_align)
        image_info.append(call_annotation)
        up += 1
    if includes["phone"]:
        phone_font, phone_size = get_font(phone, Sub_font, optional_scale)
        if up % 2:
            optional_x = optionbox_x + add_width
        else:
            optional_x = optionbox_x
            optional_y -= phone_size[1] + margin
        if head:
            phone_head_font, phone_head_size = get_font(phone_head, Sub_font, optional_scale)
            phone_head_annotation = draw_font(phone_head, image, phone_head_font, Color_Sub, optional_x, optional_y, categories["UNKNOWN"], option_align)
            image_info.append(phone_head_annotation)
            optional_x += phone_head_size[0] + margin
        phone_annotation = draw_font(phone, image, phone_font, Color_Main, optional_x, optional_y, categories["phone"], option_align)
        image_info.append(phone_annotation)
        up += 1

    ####################################################################################

    return image, image_info, width, height
