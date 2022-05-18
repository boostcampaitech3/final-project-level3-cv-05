import json
import re
import pandas as pd 


with open('/opt/final-project-level3-cv-05/image/info.json','r') as f:
    json_data = json.load(f)

#  해당부분 수정필요
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


### Rule-Base Check Function ###
# --- email Rule --- #
def email_check(x):
    if ('@' in x) and ('.' in x):
        return True
    else:
        return False

# --- site Rule --- #
def site_check(x):
    if ('www' in x) or ('.co.' in x):
        return True
    else:
        return False

# --- address Rule --- #
def check_address_si(x,elem):
    if elem in x:
        return True
    else:
        return False

def check_address_gu(x,elem):
    if elem in x:
        return True
    else: 
        return False

def address_check(x):
    for elem in address_si:
        if check_address_si(x,elem):
            return True
        else:
            continue
    for elem in address_gu:
        if check_address_gu(x,elem):
            return True
        else:
            continue

    return False

## --- Rule에 따른 Treat Function_현재는 label을 return 하도록 함 --- ##
def rulebase_label(x):
    if email_check(x):
        return 3
    elif address_check(x):
        return 7
    elif site_check(x):
        return 8
    else:
        return None

### Feature Generate Function ###
def kr_or_eng_check(x):
    if x.isalnum() :
        return 1
    else:
        return 0

def onlykr_check(x):
    for chr in x:
        if ord('가') <= ord(chr) <= ord('힣'):
            continue
        else:
            return 0
    return 1

def onlydigit_check(x):
    if x.isdigit() :
        return 1
    else:
        return 0

def krdigit_check(x):
    for chr in x:
        if onlykr_check(chr) or onlydigit_check(chr):
            continue
        else:
            return 0
    return 1 

## Main Function
def json_to_ndarray(json_data):
    image_id=[]
    label=[]

    kr_or_eng, onlykr, onlydigit, onlyeng, krdigit = [], [], [], [], []  # onlyeng는 구현 X 
    widthList, heightList, ratioList, areaList = [], [], [], []

    annotationsArray=json_data.get("annotations")

    for idx, annos in enumerate(annotationsArray):
        wordArray=annos.get("ocr").get("word")

        for words in wordArray:
            image_id.append(idx)

            ### text Rule-Base ###
            # email & address & site 
            txt=words.get("text")
            label.append(rulebase_label(txt))

            ### text feature engineering ###
            wrd = re.sub('\W+','', txt) # 언어, 숫자, _ 만 남도록 하는 정규표현식 
            kr_or_eng.append(kr_or_eng_check(wrd))
            onlykr.append(onlykr_check(wrd))
            onlydigit.append(onlydigit_check(wrd))
            krdigit.append(krdigit_check(wrd))

            ### points feature engineering ###
            p1, p2, p3, p4 = map(list, words.get("points"))

            width = max(abs(p2[0]-p1[0]),abs(p3[0]-p4[0]))  # 가로길이
            height = max(abs(p2[1]-p3[1]),abs(p1[1]-p4[1]))  # 세로길이 
            widthList.append(width)    
            heightList.append(height) 

            ratioList.append(width / height)  # 가로 세로 비율
            areaList.append(width * height)  # BBOX 넓이

    feature_df=pd.DataFrame(list(zip(image_id, label, kr_or_eng, onlykr, onlydigit, krdigit, widthList, heightList, ratioList, areaList)), columns=['image_id','pred_label', 'kr_or_eng', 'onlykr', 'onlydigit', 'krdigit', 'width', 'height', 'ratio', 'area'])
    return feature_df