"""
Feature Engineering method 연산 적용을 위한 모듈

Classes:
    TabTransform : Feature Engineering 연산 및 적용 
"""

from xmlrpc.client import Boolean


class TabTransform :
    def __init__(self) -> None:
        pass


    def kr_or_eng_check(self, text: str) -> int:
        """
        한글과 영어로만 이뤄졌는지 체크한다

        Args:
            text (str): 전달받은 text 

        Returns:
            int: 0,1 - 한글 및 영어만 포함 여부  
        """
        if text.isalnum() :
            return 1
        else:
            return 0

    def onlykr_check(self, text: str) -> int:
        """
        한글로만 이뤄졌는지 체크한다

        Args:
            text (str): 전달받은 text 

        Returns:
            int: 0,1 - 한글만 포함 여부    
        """
        for chr in text:
            if ord('가') <= ord(chr) <= ord('힣'):
                continue
            else:
                return 0
        return 1

    def onlydigit_check(self, text: str) -> int:
        """
        숫자로만 이뤄졌는지 체크한다

        Args:
            text (str): 전달받은 text 

        Returns:
            int: 0,1 - 숫자만 포함 여부    
        """
        if text.isdigit() :
            return 1
        else:
            return 0

    def krdigit_check(self, text: str) -> int:
        """
        한글과 숫자로만 이뤄졌는지 체크한다

        Args:
            text (str): 전달받은 text 

        Returns:
            int: 0,1 - 한글 및 숫자만 포함 여부    
        """
        for chr in text:
            if self.onlykr_check(chr) or self.onlydigit_check(chr):
                continue
            else:
                return 0
        return 1 