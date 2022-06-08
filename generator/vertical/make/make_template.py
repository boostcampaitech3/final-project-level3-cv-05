# make_template.py
"""
템플릿 생성에 관한 모듈입니다. 
"""

import random
from .make_component import *
from typing import List, Dict

# 정보 box의 시작 x, y 좌표 범위
MIN_X, MAX_X, MIN_Y, MAX_Y = 0.05, 0.1, 0, 0.05

# 부가 정보에 포함되는 카테고리
num = [
    "phone",
    "tel",
    "website",
    "license_number",
    "fax",
    "email",
    "address",
    "social_id",
]


####################
## template class ##
####################


class Template1:
    """
    회사명 (company), 직책 (position), 부서 (department),
    이름 (name), 부가 정보 (num info), SNS ID (social id) 를 토대로 생성하는 템플릿
    """

    def __init__(
        self,
        items: Dict,
        width: int,
        height: int,
        image,
        font_family: Dict,
        font_size: Dict,
        font_color: Dict,
        word: List,
    ):
        self.items = items
        self.width = width
        self.height = height
        self.image = image
        self.font_family = font_family
        self.font_size = font_size
        self.font_color = font_color
        self.word = word

    def make(self):
        x = self.width * random.uniform(MIN_X, MAX_X)
        y = self.height * random.uniform(0.1, 0.6)

        x = self.width * random.uniform(MIN_X, MAX_X)
        y += self.height * random.uniform(MIN_Y, MAX_Y)

        x, y = company(
            self.items,
            x,
            y,
            self.width,
            self.height,
            self.image,
            self.font_family,
            self.font_size,
            self.font_color,
            self.word,
        )

        x = self.width * random.uniform(MIN_X, MAX_X)
        if random.random() >= 0.5:
            x, y = name(
                self.items,
                x,
                y,
                self.width,
                self.height,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )

            x = self.width * random.uniform(-MIN_X, MIN_X)
            y += self.height * random.uniform(MIN_Y, MAX_Y)
            x, y = dep_pos(
                self.items,
                x,
                y,
                self.width,
                self.height,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )
        else:
            x, y = dep_pos(
                self.items,
                x,
                y,
                self.width,
                self.height,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )

            x = self.width * random.uniform(-MIN_X, MIN_X)
            y += self.height * random.uniform(MIN_Y, MAX_Y)
            x, y = name(
                self.items,
                x,
                y,
                self.width,
                self.height,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )

        x = self.width * random.uniform(MIN_X, MAX_X)
        y += self.height * random.uniform(MIN_Y, MAX_Y)

        # 부가 정보 중 명함 이미지에 적용할 항목을 랜덤하게 선택
        use = []
        while not use:
            use += use_item(num, 0.7)
        num_list = info_item(self.items, use)

        y, mode, y_margin = num_info(
            num_list,
            x,
            y,
            self.width,
            self.height,
            self.image,
            self.font_family,
            self.font_size,
            self.font_color,
            self.word,
        )

        # social id 추가
        if "social_id" not in use and random.random() >= 0.5:
            y += y_margin
            y = social_id(
                self.items,
                x,
                y,
                mode,
                self.width,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )


class Template2:
    """
    로고 (logo), 직책 (position), 부서 (department),
    이름 (name), 부가 정보 (num info), SNS ID (social id) 를 토대로 생성하는 템플릿
    """

    def __init__(
        self,
        items: Dict,
        width: int,
        height: int,
        image,
        font_family: Dict,
        font_size: Dict,
        font_color: Dict,
        word: List,
    ):
        self.items = items
        self.width = width
        self.height = height
        self.image = image
        self.font_family = font_family
        self.font_size = font_size
        self.font_color = font_color
        self.word = word

    def make(self):
        logo_image, logo_size = logo_info()
        x = random.randint(0, self.width - logo_size)
        y = self.height * random.uniform(0.1, 0.3)
        self.image.paste(logo_image, (int(x), int(y)), logo_image)

        x = self.width * random.uniform(MIN_X, MAX_X)
        y += logo_size + self.height * random.uniform(0, MAX_Y)
        if random.random() >= 0.5:
            x, y = name(
                self.items,
                x,
                y,
                self.width,
                self.height,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )

            x = self.width * random.uniform(-MIN_X, MIN_X)
            y += self.height * random.uniform(MIN_Y, MAX_Y)
            x, y = dep_pos(
                self.items,
                x,
                y,
                self.width,
                self.height,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )
        else:
            x, y = dep_pos(
                self.items,
                x,
                y,
                self.width,
                self.height,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )

            x = self.width * random.uniform(-MIN_X, MIN_X)
            y += self.height * random.uniform(MIN_Y, MAX_Y)
            x, y = name(
                self.items,
                x,
                y,
                self.width,
                self.height,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )

        x = self.width * random.uniform(MIN_X, MAX_X)
        y += self.height * random.uniform(MIN_Y, MAX_Y)

        # 부가 정보 중 명함 이미지에 적용할 항목을 랜덤하게 선택
        use = []
        while not use:
            use += use_item(num, 0.7)
        num_list = info_item(self.items, use)

        y, mode, y_margin = num_info(
            num_list,
            x,
            y,
            self.width,
            self.height,
            self.image,
            self.font_family,
            self.font_size,
            self.font_color,
            self.word,
        )

        # social id 추가
        if "social_id" not in use and random.random() >= 0.5:
            y += y_margin
            y = social_id(
                self.items,
                x,
                y,
                mode,
                self.width,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )


class Template3:
    """
    직책 (position), 부서 (department),
    이름 (name), 부가 정보 (num info), SNS ID (social id) 를 토대로 생성하는 템플릿
    """

    def __init__(
        self,
        items: Dict,
        width: int,
        height: int,
        image,
        font_family: Dict,
        font_size: Dict,
        font_color: Dict,
        word: List,
    ):
        self.items = items
        self.width = width
        self.height = height
        self.image = image
        self.font_family = font_family
        self.font_size = font_size
        self.font_color = font_color
        self.word = word

    def make(self):
        x = self.width * random.uniform(MIN_X, MAX_X)
        y = self.height * random.uniform(0.1, 0.6)
        if random.random() >= 0.5:
            x, y = name(
                self.items,
                x,
                y,
                self.width,
                self.height,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )

            x = self.width * random.uniform(-MIN_X, MIN_X)
            y += self.height * random.uniform(MIN_Y, MAX_Y)
            x, y = dep_pos(
                self.items,
                x,
                y,
                self.width,
                self.height,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )
        else:
            x, y = dep_pos(
                self.items,
                x,
                y,
                self.width,
                self.height,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )

            x = self.width * random.uniform(-MIN_X, MIN_X)
            y += self.height * random.uniform(MIN_Y, MAX_Y)
            x, y = name(
                self.items,
                x,
                y,
                self.width,
                self.height,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )

        x = self.width * random.uniform(MIN_X, MAX_X)
        y += self.height * random.uniform(MIN_Y, MAX_Y)

        # 부가 정보 중 명함 이미지에 적용할 항목을 랜덤하게 선택
        use = []
        while not use:
            use += use_item(num, 0.7)
        num_list = info_item(self.items, use)

        y, mode, y_margin = num_info(
            num_list,
            x,
            y,
            self.width,
            self.height,
            self.image,
            self.font_family,
            self.font_size,
            self.font_color,
            self.word,
        )

        # social id 추가
        if "social_id" not in use and random.random() >= 0.5:
            y += y_margin
            y = social_id(
                self.items,
                x,
                y,
                mode,
                self.width,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )


class Template4:
    """
    이름 (name), 부가 정보 (num info), SNS ID (social id) 를 토대로 생성하는 템플릿
    """

    def __init__(
        self,
        items: Dict,
        width: int,
        height: int,
        image,
        font_family: Dict,
        font_size: Dict,
        font_color: Dict,
        word: List,
    ):
        self.items = items
        self.width = width
        self.height = height
        self.image = image
        self.font_family = font_family
        self.font_size = font_size
        self.font_color = font_color
        self.word = word

    def make(self):
        x = self.width * random.uniform(MIN_X, MAX_X)
        y = self.height * random.uniform(0.1, 0.6)
        x, y = name(
            self.items,
            x,
            y,
            self.width,
            self.height,
            self.image,
            self.font_family,
            self.font_size,
            self.font_color,
            self.word,
        )

        x += self.width * random.uniform(-MIN_X, MIN_X)
        y += self.height * random.uniform(MIN_Y, MAX_Y)

        # 부가 정보 중 명함 이미지에 적용할 항목을 랜덤하게 선택
        use = []
        while not use:
            use += use_item(num, 0.7)
        num_list = info_item(self.items, use)

        y, mode, y_margin = num_info(
            num_list,
            x,
            y,
            self.width,
            self.height,
            self.image,
            self.font_family,
            self.font_size,
            self.font_color,
            self.word,
        )

        # social id 추가
        if "social_id" not in use and random.random() >= 0.5:
            y += y_margin
            y = social_id(
                self.items,
                x,
                y,
                mode,
                self.width,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )


class Template5:
    """
    회사명 (company), 부가 정보 (num info),
    SNS ID (social id), 이름 (name) 을 토대로 생성하는 템플릿
    """

    def __init__(
        self,
        items: Dict,
        width: int,
        height: int,
        image,
        font_family: Dict,
        font_size: Dict,
        font_color: Dict,
        word: List,
    ):
        self.items = items
        self.width = width
        self.height = height
        self.image = image
        self.font_family = font_family
        self.font_size = font_size
        self.font_color = font_color
        self.word = word

    def make(self):
        x = self.width * random.uniform(MIN_X, MAX_X)
        y = self.height * random.uniform(0.1, 0.6)
        x, y = company(
            self.items,
            x,
            y,
            self.width,
            self.height,
            self.image,
            self.font_family,
            self.font_size,
            self.font_color,
            self.word,
        )

        x = self.width * random.uniform(MIN_X, MAX_X)
        y += self.height * random.uniform(MIN_Y, MAX_Y)

        # 부가 정보 중 명함 이미지에 적용할 항목을 랜덤하게 선택
        use = []
        while not use:
            use += use_item(num, 0.7)
        num_list = info_item(self.items, use)

        y, mode, y_margin = num_info(
            num_list,
            x,
            y,
            self.width,
            self.height,
            self.image,
            self.font_family,
            self.font_size,
            self.font_color,
            self.word,
        )

        # social id 추가
        if "social_id" not in use and random.random() >= 0.5:
            y += y_margin
            y = social_id(
                self.items,
                x,
                y,
                mode,
                self.width,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )

        x = self.width * random.uniform(MIN_X, MAX_X)
        y += self.height * random.uniform(MIN_Y, MAX_Y)
        x, y = name(
            self.items,
            x,
            y,
            self.width,
            self.height,
            self.image,
            self.font_family,
            self.font_size,
            self.font_color,
            self.word,
        )


class Template6:
    """
    로고 (logo), 회사명 (company), 이름 (name), 직책 (position), 부서 (department),
    부가 정보 (num info), SNS ID (social id), 이름 (name) 을 토대로 생성하는 템플릿
    """

    def __init__(
        self,
        items: Dict,
        width: int,
        height: int,
        image,
        font_family: Dict,
        font_size: Dict,
        font_color: Dict,
        word: List,
    ):
        self.items = items
        self.width = width
        self.height = height
        self.image = image
        self.font_family = font_family
        self.font_size = font_size
        self.font_color = font_color
        self.word = word

    def make(self):
        logo_image, logo_size = logo_info()
        x = random.randint(0, self.width - logo_size)
        y = self.height * random.uniform(0.1, 0.2)
        self.image.paste(logo_image, (int(x), int(y)), logo_image)

        x = self.width * random.uniform(MIN_X, MAX_X)
        y += logo_size + self.height * random.uniform(0, MAX_Y)
        x, y = company(
            self.items,
            x,
            y,
            self.width,
            self.height,
            self.image,
            self.font_family,
            self.font_size,
            self.font_color,
            self.word,
        )

        x = self.width * random.uniform(MIN_X, MAX_X)
        y += self.height * random.uniform(MIN_Y, MAX_Y)
        if random.random() >= 0.5:
            x, y = name(
                self.items,
                x,
                y,
                self.width,
                self.height,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )

            x = self.width * random.uniform(-MIN_X, MIN_X)
            y += self.height * random.uniform(MIN_Y, MAX_Y)
            x, y = dep_pos(
                self.items,
                x,
                y,
                self.width,
                self.height,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )
        else:
            x, y = dep_pos(
                self.items,
                x,
                y,
                self.width,
                self.height,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )

            x = self.width * random.uniform(MIN_X, MAX_X)
            y += self.height * random.uniform(MIN_Y, MAX_Y)
            x, y = name(
                self.items,
                x,
                y,
                self.width,
                self.height,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )

        x = self.width * random.uniform(MIN_X, MAX_X)
        y += self.height * random.uniform(MIN_Y, MAX_Y)

        # 부가 정보 중 명함 이미지에 적용할 항목을 랜덤하게 선택
        use = []
        while not use:
            use += use_item(num, 0.7)
        num_list = info_item(self.items, use)

        y, mode, y_margin = num_info(
            num_list,
            x,
            y,
            self.width,
            self.height,
            self.image,
            self.font_family,
            self.font_size,
            self.font_color,
            self.word,
        )

        # social id 추가
        if "social_id" not in use and random.random() >= 0.5:
            y += y_margin
            y = social_id(
                self.items,
                x,
                y,
                mode,
                self.width,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )


class Template7:
    """
    로고 (logo), 회사명 (company), 이름 (name), 직책 (position), 부서 (department),
    부가 정보 (num info), SNS ID (social id), 이름 (name) 을 토대로 생성하는 템플릿
    """

    def __init__(
        self,
        items: Dict,
        width: int,
        height: int,
        image,
        font_family: Dict,
        font_size: Dict,
        font_color: Dict,
        word: List,
    ):
        self.items = items
        self.width = width
        self.height = height
        self.image = image
        self.font_family = font_family
        self.font_size = font_size
        self.font_color = font_color
        self.word = word

    def make(self):
        pre_x = self.width * random.uniform(MIN_X, MAX_X)
        pre_y = self.height * random.uniform(0.1, 0.6)
        post_x, post_y = company(
            self.items,
            pre_x,
            pre_y,
            self.width,
            self.height,
            self.image,
            self.font_family,
            self.font_size,
            self.font_color,
            self.word,
        )

        logo_image, logo_size = logo_info()

        # 로고를 회사명의 왼쪽/오른쪽
        if random.random() >= 0.5:
            if self.width > logo_size and int(post_x) < self.width - logo_size:
                x = random.randint(int(post_x), self.width - logo_size)
                self.image.paste(logo_image, (int(x), int(post_y)), logo_image)
                y = post_y + logo_size + self.height * random.uniform(0, MAX_Y)
            else:
                y = post_y + self.height * random.uniform(0, MAX_Y)
        else:
            if int(pre_x) - logo_size > 0:  # 로고 크기보다 여백이 크면 적용
                x = random.randint(0, int(pre_x) - logo_size)
                self.image.paste(logo_image, (int(x), int(post_y)), logo_image)
                y = post_y + logo_size + self.height * random.uniform(0, MAX_Y)
            else:
                y = post_y + self.height * random.uniform(0, MAX_Y)

        x = self.width * random.uniform(MIN_X, MAX_X)
        if random.random() >= 0.5:
            x, y = name(
                self.items,
                x,
                y,
                self.width,
                self.height,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )

            x = self.width * random.uniform(-MIN_X, MIN_X)
            y += self.height * random.uniform(MIN_Y, MAX_Y)
            x, y = dep_pos(
                self.items,
                x,
                y,
                self.width,
                self.height,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )
        else:
            x, y = dep_pos(
                self.items,
                x,
                y,
                self.width,
                self.height,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )

            x = self.width * random.uniform(-MIN_X, MIN_X)
            y += self.height * random.uniform(MIN_Y, MAX_Y)
            x, y = name(
                self.items,
                x,
                y,
                self.width,
                self.height,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )

        x = self.width * random.uniform(MIN_X, MAX_X)
        y += self.height * random.uniform(MIN_Y, MAX_Y)

        # 부가 정보 중 명함 이미지에 적용할 항목을 랜덤하게 선택
        use = []
        while not use:
            use += use_item(num, 0.7)
        num_list = info_item(self.items, use)

        y, mode, y_margin = num_info(
            num_list,
            x,
            y,
            self.width,
            self.height,
            self.image,
            self.font_family,
            self.font_size,
            self.font_color,
            self.word,
        )

        # social id 추가
        if "social_id" not in use and random.random() >= 0.5:
            y += y_margin
            y = social_id(
                self.items,
                x,
                y,
                mode,
                self.width,
                self.image,
                self.font_family,
                self.font_size,
                self.font_color,
                self.word,
            )


# 생성된 템플릿 클래스 이름
template_name = [
    Template1,
    Template2,
    Template3,
    Template4,
    Template5,
    Template6,
    Template7,
]
