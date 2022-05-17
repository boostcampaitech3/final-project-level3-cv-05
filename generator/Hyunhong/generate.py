import random
import pandas as pd


# 이름
name_df = pd.read_csv("../data/name.csv")
# 이메일
id_word = (
    ["-", "_",]
    + list(map(chr, range(97, 123)))
    + list(map(chr, range(65, 91)))
    + list(map(chr, range(48, 57)))
)
domain = pd.read_csv("../data/domain.csv")
# 사이트
site_df = pd.read_csv("../data/site.csv")
# 전화번호
country_num = pd.read_csv("../data/country_num.csv")


def random_number(min_c, max_c):
    return "".join([str(random.randint(0, 9)) for _ in range(random.randint(min_c, max_c))])


# 사명 및 주소
company_df = pd.read_csv("../data/company.csv")
address_df = pd.read_csv("../data/address.csv")
# 직책 및 부서
position_df = pd.read_csv("../data/position.csv")
department_df = pd.read_csv("../data/department.csv")
# optional
wise_df = pd.read_csv("../data/wise.csv")


def generate():
    # 이름
    name = name_df["name"][random.randint(0, len(name_df) - 1)]
    # 이메일
    email = (
        "".join(
            [id_word[random.randint(0, len(id_word) - 1)] for _ in range(random.randint(2, 15))]
        )
        + "@"
        + domain["domain"][random.randint(0, len(domain) - 1)]
    )
    # 회사
    company = company_df["company"][random.randint(0, len(company_df) - 1)]
    # 주소
    address = address_df["address"][random.randint(0, len(address_df) - 1)]
    # 연락처
    splt = "-" if random.random() < 0.8 else "."
    phone = random_number(2, 4) + splt + random_number(2, 4) + splt + random_number(3, 4)
    if random.random() < 0.3:
        countrynum = country_num["num"][random.randint(0, len(country_num) - 1)]
        phone = "(" + countrynum + ")" + phone
    # 직위/직책
    position = position_df["position"][random.randint(0, len(position_df) - 1)]
    # 부서

    # 사이트
    site = site_df["site"][random.randint(0, len(site_df) - 1)]
    # 사업자 등록 번호
    license_number = random_number(3, 3) + "-" + random_number(2, 2) + "-" + random_number(5, 5)
    # 소속
    department = department_df["department"][random.randint(0, len(department_df) - 1)]

    # optional
    wise = wise_df["wise"][random.randint(0, len(wise_df) - 1)]

    context = {
        "company": company,
        "department": department,
        "position": position,
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
        "license_number": license_number,
        "site": site,
        "wise": wise,
    }
    return context
