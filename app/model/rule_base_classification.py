"""
Rule Base Classification 을 위한 모듈 

Classes:
    RuleBaseClassification : Rule Base classification 적용 
"""
from xmlrpc.client import Boolean


address_si=['서울','부산','대구','인천','광주','대전','울산','세종','경기','강원','충청북도','충북','충청남도','충북','전라북도','전북','전라남도','전남','경상북도','경북','경상남도','경남','제주']
address_gu_lst=['종로구','중구','용산구','성동구','광진구','동대문구','중랑구','성북구','강북구','도봉구','노원구','은평구','서대문구','마포구','양천구','강서구','구로구',
'금천구','영등포구','동작구','관악구','서초구','강남구','송파구','강동구','중구','서구','동구','영도구','부산진구','동래구','남구','북구','해운대구','사하구',
'금정구','강서구','연제구','수영구','사상구','기장군','중구','동구','서구','남구','북구','수성구','달서구','달성군','중구','동구','연수구','남동구','부평구',
'계양구','서구','미추홀구','강화군','옹진군','동구','서구','남구','북구','광산구','동구','중구','서구','유성구','대덕구','중구','남구','동구','북구','울주군',
'세종시','수원시','장안구','권선구','팔달구','영통구','성남시','수정구','중원구','분당구','의정부시','안양시','만안구','동안구','부천시','광명시','평택시',
'동두천시','안산시','상록구','단원구','고양시','덕양구','일산동구','일산서구','과천시','구리시','남양주시','오산시','시흥시','군포시','의왕시','하남시',
'용인시','처인구','기흥구','수지구','파주시','이천시','안성시','김포시','화성시','광주시','양주시','포천시','여주시','연천군','가평군','양평군','춘천시',
'원주시','강릉시','동해시','태백시','속초시','삼척시','홍천군','횡성군','영월군','평창군','정선군','철원군','화천군','양구군','인제군','고성군','양양군',
'충주시','제천시','청주시','상당구','서원구','흥덕구','청원구','보은군','옥천군','영동군','진천군','괴산군','음성군','단양군','증평군','천안시','동남구',
'서북구','공주시','보령시','아산시','서산시','논산시','계룡시','당진시','금산군','부여군','서천군','청양군','홍성군','예산군','태안군','전주시','완산구',
'덕진구','군산시','익산시','정읍시','남원시','김제시','완주군','진안군','무주군','장수군','임실군','순창군','고창군','부안군','목포시','여수시','순천시',
'나주시','광양시','담양군','곡성군','구례군','고흥군','보성군','화순군','장흥군','강진군','해남군','영암군','무안군','함평군','영광군','장성군','완도군',
'진도군','신안군','포항시','남구','북구','경주시','김천시','안동시','구미시','영주시','영천시','상주시','문경시','경산시','군위군','의성군','청송군','영양군',
'영덕군','청도군','고령군','성주군','칠곡군','예천군','봉화군','울진군','울릉군','진주시','통영시','사천시','김해시','밀양시','거제시','양산시','창원시','의창구',
'성산구','마산합포구','마산회원구','진해구','의령군','함안군','창녕군','고성군','남해군','하동군','산청군','함양군','거창군','합천군','제주시','서귀포시']
address_gu=list(set(address_gu_lst))


class RuleBaseClassification:
    def __init__(self) -> None:
        pass


    def check_email(self, text: str) -> Boolean:
        """
        이메일 형식인지 아닌지 체크한다

        Args:
            text (str): 전달받은 text 

        Returns:
            Boolean: TF - 이메일 형식 포함 여부  
        """

        if '@' in self and '.' in self :
            return True
        else:
            return False

    def check_site(self, text: str) -> Boolean:
        """
        사이트 주소 형식인지 아닌지 체크한다

        Args:
            text (str): 전달받은 text 

        Returns:
            Boolean: TF - 사이트주소 형식 포함 여부 
        """
        if ('www' in self)  or ('.co.' in self) :
            return True
        else:
            return False

    def check_address_si(self, text: str) -> Boolean:
        """
        check_address에서 활용하기 위해, 한국 시도 주소 정보의 포함 여부를 체크한다

        Args:
            text (str): 전달받은 text 

        Returns:
            Boolean: TF - 한국 시도 주소 포함 여부 
        """
        if text in self: 
            return True
        else:
            return False

    def check_address_gu(self, text: str) -> Boolean:
        """
        check_address에서 활용하기 위해, 한국 시군구 주소 정보의 포함 여부를 체크한다

        Args:
            text (str): 전달받은 text 

        Returns:
            Boolean: TF - 한국 시군구 주소 포함 여부
        """
        if text in self: 
            return True
        else: 
            return False

    def check_address(self, text: str) -> Boolean:
        """
        한국 주소 정보의 포함 여부를 체크한다

        Args:
            text (str): 전달받은 text 

        Returns:
            Boolean: TF - 한국 주소 포함 여부
        """
        for elem in address_si:
            if self.check_address_si(text, elem):
                return True
            else:
                continue
        for elem in address_gu:
            if self.check_address_gu(text, elem):
                return True
            else:
                continue

        return False

    def rulebase_label(self, text: str) -> int:
        """
        rule base에 따라 bbox text의 라벨을 구분 한다. 

        Args:
            text (str): 전달받은 text 

        Returns:
            int: 예측한 category_id 
        """
        if self.check_email(text) :
            return 3
        elif self.check_address(text) :
            return 7
        elif self.check_site(text) :
            return 8
        else:
            return None
