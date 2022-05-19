"""
Feature Engineering method 연산 적용을 위한 모듈

Classes:
    TabTransform: Feature Engineering 연산 및 적용
"""

from typing import List
import pandas as pd
import re

class TabTransform:
    """
    Feature Engineering 연산 및 적용하는 class
    """

    def __init__(self, df: pd.DataFrame) -> None:
        self.point_1 = df['point_1']
        self.point_2 = df['point_2']
        self.point_3 = df['point_3']
        self.point_4 = df['point_4']
        self.width = df['points'].transform(self.calculate_width)
        self.height = df['points'].transform(self.calculate_height)
        self.scaled_width = self.width / df['image_width']
        self.scaled_height = self.height / df['image_height']
        self.file_name = df['file_name']
        self.text = df['text']
        self.label = df['category_id']
    
    def transform(self) -> pd.DataFrame:
        """
        선정한 feature engineering 방법들을 적용한 결과를 반환한다

        Returns:
            pd.DataFrame: feature engineering이 적용된 DataFrame 결과
        """

        df_result = pd.DataFrame()

        # features not used for lenaring
        df_result['file_name'] = self.file_name
        df_result['point_1'] = self.point_1
        df_result['point_2'] = self.point_2
        df_result['point_3'] = self.point_3
        df_result['point_4'] = self.point_4
        df_result['text'] = self.text

        # features used for lenaring
        df_result['width'] = self.scaled_width
        df_result['height'] = self.scaled_height
        df_result['ratio(h/w)'] = self.height / self.width
        df_result['area'] = self.scaled_height * self.scaled_width
        df_result['include_AT_SIGN'] = self.text.transform(self.check_include_at_sign)
        df_result['is_phone_type_text'] = self.text.transform(self.check_phone_type_text)
        df_result['is_alpha'] = self.text.transform(self.check_is_alpha)
        df_result['is_alnum'] = self.text.transform(self.check_is_alnum)
        df_result['is_kr'] = self.text.transform(self.check_only_kr)
        df_result['is_digit'] = self.text.transform(self.check_only_digit)
        df_result['is_krdigit'] = self.text.transform(self.check_krdigit)
        df_result['text_length'] = self.text.transform(self.calculate_text_length)

        # label
        df_result['category_id'] = self.label

        return df_result

    def calculate_width(self, points: List) -> float:
        """
        bbox에 대한 width를 계산한다

        Args:
            points (List): bbox 내 시계 방향 순서의 4개의 point List

        Returns:
            float: width(가로 길이) - 시계 방향 기준 첫 번째 좌표와 두 번째 좌표의 x 값 차이
        """

        point_1, point_2, _, _ = points
        width = abs(point_2[0] - point_1[0])
        
        return width

    def calculate_height(self, points: List) -> float:
        """
        bbox에 대한 height를 계산한다

        Args:
            points (List): bbox 내 시계 방향 순서의 4개의 point List

        Returns:
            float: height(세로 길이) - 시계 방향 기준 첫 번째 좌표와 네 번째 좌표의 y 값 차이
        """

        point_1, _, _, point_4 = points
        height = abs(point_1[1] - point_4[1])
        
        return height

    def calculate_ratio(self, width: float, height: float) -> float:
        """
        bbox에 대한 비율(가로 길이에 대한 세로 길이의 비율(세로 길이/가로 길이))을 계산한다

        Args:
            width (float): bbox의 가로 길이
            height (float): bbox의 세로 길이

        Returns:
            float: bbox에 대한 비율(가로 길이에 대한 세로 길이의 비율)
        """

        ratio = height / width
        
        return ratio

    def check_include_at_sign(self, text: str) -> int:
        """
        text 내에 '@' 문자가 포함되어있는지 확인한다

        Args:
            text (str): bbox 내의 text

        Returns:
            int: text 안에 '@' 이 포함된 경우 1, 아닌 경우 0 을 반환
        """

        if '@' in text:
            return 1
        else:
            return 0

    def check_phone_type_text(self, text: str) -> int:
        """
        text 가 phone type text(숫자, '.', '+', '(', ')', '-', ' ') 로만 이루어졌는지 확인한다

        Args:
            text (str): bbox 내의 text

        Returns:
            int: 숫자 or '.' or '+' or '(' or ')' or '-' or ' ' 문자만 포함된 경우 1, 아닌 경우 0을 반환
        """

        phone_type_char = '0123456789.+()- '
        
        for c in text:
            if c not in phone_type_char:
                return 0
        return 1

    def check_is_alpha(self, text: str) -> int:
        """
        Text 구성이 알파벳 또는 한글로만 이루어졌는지 확인

        Args:
            text (str): 전달받은 text

        Returns:
            int: 0,1 - Text 구성이 알파벳 또는 한글로만 이루어졌는지 여부
        """

        post_text = re.sub('\W+','', text)

        if post_text.isalpha():
            return 1
        else:
            return 0

    def check_is_alnum(self, text: str) -> int:
        """
        알파벳 또는 한글 또는 숫자로만 이루어졌는지 확인

        Args:
            text (str): 전달받은 text

        Returns:
            int: 0,1 - 알파벳 또는 한글 또는 숫자로만 이루어졌는지 여부
        """

        post_text = re.sub('\W+','', text)
        
        if post_text.isalnum():
            return 1
        else:
            return 0    

    def calculate_text_length(self, text: str) -> int:
        """
        Text 의 길이를 계산한다

        Args:
            text (str): 전달받은 text

        Returns:
            int: text 길이
        """

        text_length = len(text)
        
        return text_length
    
    def check_only_kr(self, text: str) -> int:
        """
        한글로만 이뤄졌는지 체크한다

        Args:
            text (str): 전달받은 text 

        Returns:
            int: 0,1 - 한글만 포함 여부    
        """

        post_text = re.sub('\W+','', text)

        for chr in post_text:
            if ord('가') <= ord(chr) <= ord('힣'):
                continue
            else:
                return 0
        return 1
    
    def check_only_digit(self, text: str) -> int:
        """
        숫자로만 이뤄졌는지 체크한다

        Args:
            text (str): 전달받은 text 

        Returns:
            int: 0,1 - 숫자만 포함 여부    
        """

        post_text = re.sub('\W+','', text)

        if post_text.isdigit() :
            return 1
        else:
            return 0

    def check_krdigit(self, text: str) -> int:
        """
        한글과 숫자로만 이뤄졌는지 체크한다

        Args:
            text (str): 전달받은 text 

        Returns:
            int: 0,1 - 한글 및 숫자만 포함 여부    
        """

        post_text = re.sub('\W+','', text)

        for chr in post_text:
            if self.check_only_kr(chr) or self.check_only_digit(chr):
                continue
            else:
                return 0
        return 1 
