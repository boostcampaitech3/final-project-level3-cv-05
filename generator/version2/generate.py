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

# 사명 및 주소
company_df = pd.read_csv(f"{data_directory}/company.csv")
address_df = pd.read_csv(f"{data_directory}/address.csv")

# 직책 및 부서
position_df = pd.read_csv(f"{data_directory}/position.csv")
department_df = pd.read_csv(f"{data_directory}/department.csv")

# 사훈
wise_df = pd.read_csv(f"{data_directory}/wise.csv")


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
    구분자를 포함한 숫자 문자열을 생성합니다. 
    구분자는 랜덤으로 선택됩니다.

    Returns:
        num (str): 생성된 문자열
    """
    if random.random() >= 0.5:  # 00-000-0000
        num = random_number(3, 4) + "-" + random_number(4, 4)
        if random.random() < 0.3:
            countrynum = country_num["num"][random.randint(0, len(country_num) - 1)]
            num = "(" + countrynum + ") " + num
    else:  # 00.000.0000
        num = random_number(3, 4) + "." + random_number(4, 4)
        if random.random() < 0.3:
            countrynum = country_num["num"][random.randint(0, len(country_num) - 1)]
            num = "(" + countrynum + ") " + num
    return num


def generate() -> dict:
    """랜덤으로 생성한 정보를 dict type으로 반환합니다.

    Returns:
        context (dict): 명함 데이터에 적용할 정보
    """
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
    license_number = (
        random_number(3, 3) + "-" + random_number(2, 2) + "-" + random_number(5, 5)
    )

    # 사훈
    wise = wise_df["wise"][random.randint(0, len(wise_df) - 1)]

    # 팩스 번호
    fax = number_generate()

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
