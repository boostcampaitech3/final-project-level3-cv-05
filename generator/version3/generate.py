# generate.py
"""
명함 이미지에 포함될 정보를 생성하는 모듈입니다. 

Functions:
    random_number(min_c, max_c): (min_c, max_c) 범위의 정수 중 하나를 랜덤으로 선택하여,
                                 이를 길이로 하는 숫자 문자열을 생성합니다.
    number_generate(): 구분자를 랜덤으로 선택하여, 숫자 문자열을 생성합니다.
    separator(sep): 구분자를 포함한 숫자 문자열을 생성합니다.
    generate(): 랜덤으로 생성한 정보를 반환합니다.

"""
import random
import pandas as pd
from typing import Dict

# 이름
name_df = pd.read_csv("data/name.csv")

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
domain = pd.read_csv("data/domain.csv")

# 사이트
site_df = pd.read_csv("data/site.csv")

# 전화번호
country_num = pd.read_csv("data/country_num.csv")

# 회사명
company_df = pd.read_csv("data/company.csv")

# 회사 주소
address_df = pd.read_csv("data/address.csv")

# 직책
position_df = pd.read_csv("data/position.csv")

# 부서
department_df = pd.read_csv("data/department.csv")

# 사훈
wise_df = pd.read_csv("data/wise.csv")


def random_number(min_c: int, max_c: int) -> str:
    """
    (min_c, max_c) 범위의 정수 중 하나를 랜덤으로 선택하여,
    이를 길이로 하는 숫자 문자열을 생성합니다.

    Args:
        min_c (int): 생성될 문자열 길이의 최솟값
        max_c (int): 생성될 문자열 길이의 최댓값

    Returns:
        num_string (str): 생성된 숫자 문자열
    """

    num_string = "".join(
        [str(random.randint(0, 9)) for _ in range(random.randint(min_c, max_c))]
    )
    return num_string


def number_generate() -> str:
    """
    구분자를 랜덤으로 선택하여,
    숫자 문자열을 생성합니다.

    Returns:
        num (str): 생성된 문자열
    """
    if random.random() >= 0.5:  # 00-000-0000
        num = separator("-")
    else:  # 00.000.0000
        num = separator(".")
    return num


def separator(sep: str) -> str:
    """
    구분자를 포함한 숫자 문자열을 생성합니다.

    Args:
        sep (str): 사용할 구분자

    Returns:
        num (str): 생성된 문자열
    """
    num = random_number(3, 4) + sep + random_number(4, 4)
    if random.random() < 0.3:
        countrynum = country_num["num"][random.randint(0, len(country_num) - 1)]
        num = "(" + countrynum + ") " + num
    return num


def generate() -> Dict[str, str]:
    """
    랜덤으로 생성한 정보를 반환합니다.

    Returns:
        context (dict): 명함 데이터에 적용할 정보
    """
    # 이름
    name = name_df["name"][random.randint(0, len(name_df) - 1)]
    
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

    # 핸드폰 번호
    phone = number_generate()

    # 전화 번호
    tel = number_generate()

    # 직위/직책
    position = position_df["position"][random.randint(0, len(position_df) - 1)]

    # 부서
    department = department_df["department"][random.randint(0, len(department_df) - 1)]

    # 사이트
    website = site_df["site"][random.randint(0, len(site_df) - 1)]

    # 사업자 등록 번호
    license_number = (random_number(3, 3) + "-" + random_number(2, 2) + "-" + random_number(5, 5))

    # 사훈
    wise = wise_df["wise"][random.randint(0, len(wise_df) - 1)]

    # 팩스 번호
    fax = number_generate()

    context = {
        "company": company,
        "department": department,
        "position": position,
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
        "license_number": license_number,
        "website": website,
        "wise": wise,
        "fax": fax,
        "tel": tel,
    }
    return context
