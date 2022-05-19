import json
import re
import pandas as pd 
from rule_base_classification import RuleBaseClassification
from tab_transform import kr_or_eng_check, onlykr_check, onlydigit_check, krdigit_check


with open('/opt/final-project-level3-cv-05/image/info.json','r') as f:
    json = json.load(f)


def json_to_ndarray(json: str) -> pd.DataFrame:
    """
    Rule Base로 Classification 하고, 학습 시에 tabular data를 Feature Engineering하여 반환하는 함수

    Args:
        json (str): 하나의 이미지의 annotation 정보를 담은 json  

    Returns:
        pd.DataFrame: feature engineering 이 적용된 dataframe 자료형 
    """
    image_id=[]
    label=[]

    kr_or_eng, onlykr, onlydigit, onlyeng, krdigit = [], [], [], [], []  # onlyeng는 구현 X 
    widthList, heightList, ratioList, areaList = [], [], [], []

    annotationsArray=json.get("annotations")

    for idx, annos in enumerate(annotationsArray):
        wordArray=annos.get("ocr").get("word")

        for words in wordArray:
            image_id.append(idx)

            ### text Rule-Base ###
            # email & address & site 
            txt=words.get("text")
            label.append(RuleBaseClassification.rulebase_label(txt))

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

    feature_df=pd.DataFrame(list(zip([p1,p2,p3,p4],txt,image_id, label, kr_or_eng, onlykr, onlydigit, krdigit, widthList, heightList, ratioList, areaList)), columns=['points','text','image_id','pred_label', 'kr_or_eng', 'onlykr', 'onlydigit', 'krdigit', 'width', 'height', 'ratio', 'area'])
    
    return feature_df