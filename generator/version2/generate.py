import random

import pandas as pd

data_directory = "../../generator/data"

# 이름
name_df = pd.read_csv(f"{data_directory}/name.csv")
ko_name_df = pd.read_csv(f"{data_directory}/ko_name.csv")
eng_name_df = pd.read_csv(f"{data_directory}/eng_name.csv")
# 이메일
id_word = (
    [
        "-",
        "_",
    ]
    + list(map(chr, range(97, 123)))
    + list(map(chr, range(65, 91)))
    + list(map(chr, range(48, 57)))
)
domain = pd.read_csv(f"{data_directory}/domain.csv")
# 사이트
site_df = pd.read_csv(f"{data_directory}/site.csv")
# 전화번호
country_num = pd.read_csv(f"{data_directory}/country_num.csv")


def random_number(min_c: int, max_c: int):
    return "".join(
        [str(random.randint(0, 9)) for _ in range(random.randint(min_c, max_c))]
    )


# 사명 및 주소
company_df = pd.read_csv(f"{data_directory}/company.csv")
address_df = pd.read_csv(f"{data_directory}/address.csv")
# 직책 및 부서
position_df = pd.read_csv(f"{data_directory}/position.csv")
department_df = pd.read_csv(f"{data_directory}/department.csv")
# optional
wise_df = pd.read_csv(f"{data_directory}/wise.csv")


def number_generate(mode: str):
    select = random.random()
    if select >= 0.5:  # 00-000-0000
        num = random_number(3, 4) + "-" + random_number(4, 4)
        if mode != "fax":
            num = random_number(2, 3) + "-" + num
        if random.random() < 0.3:
            countrynum = country_num["num"][random.randint(0, len(country_num) - 1)]
            num = "(" + countrynum + ") " + num
    else:  # 00.000.0000
        num = random_number(3, 4) + "." + random_number(4, 4)
        if mode != "fax":
            num = random_number(2, 3) + "." + num
        if random.random() < 0.3:
            countrynum = country_num["num"][random.randint(0, len(country_num) - 1)]
            num = "(" + countrynum + ") " + num

    return num


def generate():
    # 이름
    name = name_df["name"][random.randint(0, len(name_df) - 1)]
    ko_name = ko_name_df["name"][random.randint(0, len(ko_name_df) - 1)]
    eng_name = eng_name_df["name"][random.randint(0, len(eng_name_df) - 1)]
    # 이메일
    email = (
        "".join(
            [
                str(id_word[random.randint(0, len(id_word) - 1)])
                for _ in range(random.randint(2, 15))
            ]
        )
        + "@"
        + str(domain["domain"][random.randint(0, len(domain) - 1)])
    )
    # 회사
    company = company_df["company"][random.randint(0, len(company_df) - 1)]
    # 주소
    address = address_df["address"][random.randint(0, len(address_df) - 1)]
    # 연락처
    phone = number_generate("phone")
    tel = number_generate("tel")

    # 직위/직책
    position = position_df["position"][random.randint(0, len(position_df) - 1)]
    # 부서

    # 사이트
    website = site_df["site"][random.randint(0, len(site_df) - 1)]
    # 사업자 등록 번호
    license_number = (
        random_number(3, 3) + "-" + random_number(2, 2) + "-" + random_number(5, 5)
    )
    # 소속
    department = department_df["department"][random.randint(0, len(department_df) - 1)]

    # optional
    wise = wise_df["wise"][random.randint(0, len(wise_df) - 1)]

    fax = number_generate("fax")

    context = {
        "company_name": company,
        "department": department,
        "position": position,
        "name": name,
        "phone_number": phone,
        "email": email,
        "company_address": address,
        "license_number": license_number,
        "website": website,
        "wise": wise,
        "fax": fax,
        "tel": tel,
        "eng_name": eng_name,
        "ko_name": ko_name,
    }
    return context
