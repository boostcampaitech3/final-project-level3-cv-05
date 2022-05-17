# -*-coding:UTF-8
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import random

FONT_PATA = "../font"


def get_TF(prob):
    return True if random.random() < prob else False


def image_generate(info):
    keywords = list(info.keys())
    # keyword 변수 선언
    company = info["company"]
    position = info["position"]
    position = info["position"]
    department = info["department"]
    name = info["name"]
    phone = info["phone"]
    email = info["email"]
    company = info["company"]
    address = info["address"]
    site = info["site"]
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
    Color_BG, Color_Logo, Color_Name, Color_Sub = colormap[random.randint(0, len(colormap) - 1)]

    # includes = dict(zip(keywords, [True for _ in range(len(keywords))]))        # FOR TEST
    # font 지정
    fonts = os.listdir(FONT_PATA)
    font = fonts[random.randint(0, len(fonts) - 1)]

    # 빈 이미지 생성
    height = 500
    width = 900

    # 이름 font size
    standard = height // 10 + random.randint(-10, 2)

    # 배경색 지정
    image = Image.new("RGBA", (width, height), Color_BG)

    # bbox 정보
    image_info = []

    ############################## 이름 & 직업(or 직급) & 부서 ##########################
    origin = name
    if len(name) < 4:
        for _ in range(random.randint(0, 3)):
            name = " ".join(name)

    reverse = True if random.random() < 0.5 else False
    nameFont = ImageFont.truetype(f"font/{font}", standard)
    name_x = width * random.randint(85, 95) // 100 - nameFont.getsize(name)[0]
    if reverse:
        name_x = width * random.randint(5, 15) // 100
    name_y = height * 0.5 - nameFont.getsize(name)[1] // 2
    ImageDraw.Draw(image).text(xy=(name_x, name_y), text=name, font=nameFont, fill=Color_Name)
    image_info.append(
        {
            "category_id": 1,
            "points": [
                [name_x, name_y],
                [name_x + nameFont.getsize(name)[0], name_y],
                [name_x + nameFont.getsize(name)[0], name_y + nameFont.getsize(name)[1],],
                [name_x, name_y + nameFont.getsize(name)[1]],
            ],
            "orientation": "Horizontal",
            "text": origin,
        }
    )
    positionFont = ImageFont.truetype(f"font/{font}", standard * random.randint(7, 9) // 10)
    position_x = name_x - width * 0.05 - positionFont.getsize(position)[0]
    if reverse:
        position_x = name_x + width * 0.05 + nameFont.getsize(name)[0]
        while position_x + positionFont.getsize(position)[0] >= width:
            positionFont = ImageFont.truetype(f"{font}", positionFont.size - 1)
    position_y = name_y + nameFont.getsize(name)[1] - positionFont.getsize(position)[1]
    ImageDraw.Draw(image).text(
        xy=(position_x, position_y), text=position, font=positionFont, fill=Color_Name
    )
    image_info.append(
        {
            "category_id": 4,
            "orientation": "Horizontal",
            "points": [
                [position_x, position_y],
                [position_x + positionFont.getsize(position)[0], position_y],
                [
                    position_x + positionFont.getsize(position)[0],
                    position_y + positionFont.getsize(position)[1],
                ],
                [position_x, position_y + positionFont.getsize(position)[1]],
            ],
            "text": position,
        }
    )
    if includes["department"]:
        departmentFont = ImageFont.truetype(f"font/{font}", standard * random.randint(5, 7) // 10)
        department_x = name_x + nameFont.getsize(name)[0] - departmentFont.getsize(department)[0]
        if reverse:
            department_x = (
                position_x
                + positionFont.getsize(position)[0]
                - departmentFont.getsize(department)[0]
            )
        department_y = position_y + positionFont.getsize(position)[1] + height * 0.03
        if reverse:
            department_y = name_y - positionFont.getsize(position)[1] - height * 0.01
        ImageDraw.Draw(image).text(
            xy=(department_x, department_y), text=department, font=departmentFont, fill=Color_Sub,
        )
        image_info.append(
            {
                "category_id": 6,
                "orientation": "Horizontal",
                "points": [
                    [department_x, department_y],
                    [department_x + departmentFont.getsize(department)[0], department_y,],
                    [
                        department_x + departmentFont.getsize(department)[0],
                        department_y + departmentFont.getsize(department)[1],
                    ],
                    [department_x, department_y + departmentFont.getsize(department)[1],],
                ],
                "text": department,
            }
        )

    ################################### 사명 & 사훈 ####################################
    if includes["company"]:
        companyFont = ImageFont.truetype(f"font/{font}", standard * random.randint(11, 16) // 10)
        company_x = width * random.randint(5, 15) // 100
        while company_x + companyFont.getsize(company)[0] >= width:
            companyFont = ImageFont.truetype(f"{font}", companyFont.size - 1)
        if reverse:
            company_x = width * random.randint(85, 95) // 100 - companyFont.getsize(company)[0]
        company_y = height * random.randint(5, 15) // 100
        ImageDraw.Draw(image).text(
            xy=(company_x, company_y), text=company, font=companyFont, fill=Color_Logo
        )
        image_info.append(
            {
                "category_id": 5,
                "orientation": "Horizontal",
                "points": [
                    [company_x, company_y],
                    [company_x + companyFont.getsize(company)[0], company_y],
                    [
                        company_x + companyFont.getsize(company)[0],
                        company_y + companyFont.getsize(company)[1],
                    ],
                    [company_x, company_y + companyFont.getsize(company)[1]],
                ],
                "text": company,
            }
        )

    if includes["wise"]:
        wiseFont = ImageFont.truetype(f"font/{font}", standard * random.randint(35, 45) // 100)
        wise_x = company_x
        if reverse:
            wise_x = company_x + companyFont.getsize(company)[0] - wiseFont.getsize(wise)[0]
        wise_y = company_y - wiseFont.getsize(wise)[1]
        ImageDraw.Draw(image).text(xy=(wise_x, wise_y), text=wise, font=wiseFont, fill=Color_Sub)
        image_info.append(
            {
                "category_id": 10,
                "orientation": "Horizontal",
                "points": [
                    [wise_x, wise_y],
                    [wise_x + wiseFont.getsize(wise)[0], wise_y],
                    [wise_x + wiseFont.getsize(wise)[0], wise_y + wiseFont.getsize(wise)[1],],
                    [wise_x, wise_y + wiseFont.getsize(wise)[1]],
                ],
                "text": wise,
            }
        )
    ####################################################################################

    lower = []
    if includes["phone"]:
        lower.append(phone)
    if includes["email"]:
        lower.append(email)
    if includes["site"]:
        lower.append(site)
    if includes["address"]:
        lower.append(address)
    if includes["license_number"]:
        lower.append(license_number)

    optional = 0
    ####################################### 번호 #######################################
    optional_size = standard * random.randint(40, 45) // 100
    if includes["phone"]:
        phoneFont = ImageFont.truetype(f"font/{font}", optional_size)
        phone_x = name_x + nameFont.getsize(name)[0] - phoneFont.getsize(phone)[0]
        if reverse:
            phone_x = name_x
        phone_y = height * 0.7 + height * 0.05 * optional
        if reverse:
            phone_y = name_y + nameFont.getsize(name)[1] + height * 0.03 + height * 0.05 * optional
        ImageDraw.Draw(image).text(
            xy=(phone_x, phone_y), text=phone, font=phoneFont, fill=Color_Name
        )
        optional += 1
        image_info.append(
            {
                "category_id": 2,
                "orientation": "Horizontal",
                "points": [
                    [phone_x, phone_y],
                    [phone_x + phoneFont.getsize(phone)[0], phone_y],
                    [phone_x + phoneFont.getsize(phone)[0], phone_y + phoneFont.getsize(phone)[1],],
                    [phone_x, phone_y + phoneFont.getsize(phone)[1]],
                ],
                "text": phone,
            }
        )
    ####################################### 메일 #######################################
    if includes["email"]:
        emailFont = ImageFont.truetype(f"font/{font}", optional_size)
        email_x = name_x + nameFont.getsize(name)[0] - emailFont.getsize(email)[0]
        if reverse:
            email_x = name_x
        email_y = height * 0.7 + height * 0.05 * optional
        if reverse:
            email_y = name_y + nameFont.getsize(name)[1] + height * 0.03 + height * 0.05 * optional
        ImageDraw.Draw(image).text(
            xy=(email_x, email_y), text=email, font=emailFont, fill=Color_Name
        )
        optional += 1
        image_info.append(
            {
                "category_id": 3,
                "orientation": "Horizontal",
                "points": [
                    [email_x, email_y],
                    [email_x + emailFont.getsize(email)[0], email_y],
                    [email_x + emailFont.getsize(email)[0], email_y + emailFont.getsize(email)[1],],
                    [email_x, email_y + emailFont.getsize(email)[1]],
                ],
                "text": email,
            }
        )

    ####################################### 사이트 #####################################
    if includes["site"]:
        siteFont = ImageFont.truetype(f"font/{font}", optional_size)
        site_x = name_x + nameFont.getsize(name)[0] - siteFont.getsize(site)[0]
        if reverse:
            site_x = name_x
        site_y = height * 0.7 + height * 0.05 * optional
        if reverse:
            site_y = name_y + nameFont.getsize(name)[1] + height * 0.03 + height * 0.05 * optional
        ImageDraw.Draw(image).text(xy=(site_x, site_y), text=site, font=siteFont, fill=Color_Name)
        image_info.append(
            {
                "category_id": 8,
                "orientation": "Horizontal",
                "points": [
                    [site_x, site_y],
                    [site_x + siteFont.getsize(site)[0], site_y],
                    [site_x + siteFont.getsize(site)[0], site_y + siteFont.getsize(site)[1],],
                    [site_x, site_y + siteFont.getsize(site)[1]],
                ],
                "text": site,
            }
        )
        optional += 1

    ####################################### 주소 #######################################
    if includes["address"]:
        addressFont = ImageFont.truetype(f"font/{font}", optional_size)
        address_x = name_x + nameFont.getsize(name)[0] - addressFont.getsize(address)[0]
        if reverse:
            address_x = name_x
        address_y = height * 0.7 + height * 0.06 * optional
        if reverse:
            address_y = (
                name_y + nameFont.getsize(name)[1] + height * 0.03 + height * 0.05 * optional
            )
        ImageDraw.Draw(image).text(
            xy=(address_x, address_y), text=address, font=addressFont, fill=Color_Sub
        )
        image_info.append(
            {
                "category_id": 7,
                "orientation": "Horizontal",
                "points": [
                    [address_x, address_y],
                    [address_x + addressFont.getsize(address)[0], address_y],
                    [
                        address_x + addressFont.getsize(address)[0],
                        address_y + addressFont.getsize(address)[1],
                    ],
                    [address_x, address_y + addressFont.getsize(address)[1]],
                ],
                "text": address,
            }
        )
        optional += 1

    ################################### 사업자 등록번호 ################################
    if includes["license_number"]:
        license_number = "사업자등록번호 :" + license_number
        license_numberFont = ImageFont.truetype(f"font/{font}", optional_size)
        license_number_x = (
            name_x + nameFont.getsize(name)[0] - license_numberFont.getsize(license_number)[0]
        )
        if reverse:
            license_number_x = name_x
        license_number_y = height * 0.7 + height * 0.06 * optional
        if reverse:
            license_number_y = (
                name_y + nameFont.getsize(name)[1] + height * 0.03 + height * 0.05 * optional
            )
        ImageDraw.Draw(image).text(
            xy=(license_number_x, license_number_y),
            text=license_number,
            font=license_numberFont,
            fill=Color_Sub,
        )
        image_info.append(
            {
                "category_id": 0,
                "orientation": "Horizontal",
                "points": [
                    [license_number_x, license_number_y],
                    [
                        license_number_x + license_numberFont.getsize(license_number)[0],
                        license_number_y,
                    ],
                    [
                        license_number_x + license_numberFont.getsize(license_number)[0],
                        license_number_y + license_numberFont.getsize(license_number)[1],
                    ],
                    [
                        license_number_x,
                        license_number_y + license_numberFont.getsize(license_number)[1],
                    ],
                ],
                "text": license_number,
            }
        )
    ####################################################################################
    return image, image_info, width, height
