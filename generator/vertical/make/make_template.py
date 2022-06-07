import random
from .make_component import *


MIN_X, MAX_X, MIN_Y, MAX_Y = 0.05, 0.1, 0, 0.05

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
    def __init__(
        self,
        items: Dict[str, str],
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
    def __init__(
        self,
        items: Dict[str, str],
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
    def __init__(
        self,
        items: Dict[str, str],
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
    def __init__(
        self,
        items: Dict[str, str],
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
    def __init__(
        self,
        items: Dict[str, str],
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
    def __init__(
        self,
        items: Dict[str, str],
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
    def __init__(
        self,
        items: Dict[str, str],
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


template_name = [
    Template1,
    Template2,
    Template3,
    Template4,
    Template5,
    Template6,
    Template7,
]
