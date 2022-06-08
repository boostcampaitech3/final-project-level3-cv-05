# Feature Engineering 
## rule_base_classification.py 
- Email (category_id=3) : '@' & '.' 포함 여부  
- Address (category_id=4) : 한국 시도 & 시군구 주소 정보의 포함 여부 
- Site (category_id=8) : 'www' or '.co.' or 'http:' or 'https:' 포함 여부 

## feature_engineering.py 
-  `tab_utils.py`와 `tab_trainsform.py`를 통해, 받은 json 데이터로부터 13개의 features를 dataframe 형태로 반환   

## tab_utils.py  
- 'json'데이터를 'dataframe'데이터로 변경 
  
## tab_trainsform.py
- feature engineering _ feature 정의    

### BBOX 정보 기반 
- ‘width’ : bbox의 너비 비율 (명함너비 대비)  
- ‘height’ : bbox의 높이 비율 (명함높이 대비)    
- ‘ratio(h/w)’ : bbox의 가로 대비 세로 비율   
- ‘area’ : bbox의 면적 ( height * width )
- ‘center_x’ : 명함내 bbox의 중심점의 x 좌표 
- ‘center_y’ : 명함내 bbox의 중심점의 y 좌표   
### TEXT 정보 기반 
- 'include_AT_SIGN’ : text 내에 @ 포함 여부   
- 'is_alpha’ : Text 구성이 알파벳 또는 한글로만 이루어졌는지 확인  
- 'is_digit’ : text가 숫자로만 이루어졌는지 여부   
- 'is_alnum’ : text가 숫자 or 영어로만 이루어졌는지 여부   
- 'is_kr’ : text가 한글로만 이루어졌는지 여부   
- 'is_krdigit’ : text가 숫자 or 한글로만 이루어졌는지 여부   
- 'text_length’ : text의 길이   

