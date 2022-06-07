# folder structure 
모델 학습 이미지를 생성하기 위한 이미지 생성 프로그램 
- 세로 명함 
- 회사 이름/이름/직책&부서/숫자 정보 등에 대해 템플릿 클래스를 만든 후, 이를 랜덤하게 조합하여 명함 이미지 생성 

```python
vertical/
├── 📝 card_utils.py              # 명함 템플릿 생성에 필요한 파일 
├── 📝 generate.py                # csv 파일을 토대로 정보 생성 
├── 📝 json_utils.py              # json 파일 생성에 필요한 파일 
├── 📝 make_card.py               # 명함 이미지를 생성하는 파일 
├── 📝 data_visualization.ipynb   # 생성된 명함 이미지를 시각화하는 파일
│
└── 📂 example
    ├── 📂 images
    └── 📄 *.png                  # sample images folder 
    └── 📄 info.json              # sample annotations file  
```
### 실행
아래와 같이 명령어를 작성하여 실행
```
python make_card --num [생성될 이미지 개수] --dir [json 파일 경로] --width [이미지 크기의 너비]
```   
각 템플릿 별로 생성되는 이미지를 확인하고 싶은 경우, 아래와 같이 명령어를 작성하여 실행 
```
python make_card --num [생성될 이미지 개수] --dir [json 파일 경로] --width [이미지 크기의 너비] \
--test True --template_name [Template{숫자}]
```

# 구현 내용
### **각 요소의 위치**


mode ('left'/'center'/'right') 를 랜덤하게 선택하고, 각 mode에서 시작점에 해당하는 x좌표, y좌표를 랜덤하게 움직입니다.
```
# x, y 좌표를 랜덤하게 움직임

x, y = width * random.uniform(MIN_X, MAX_X), height * random.uniform(0.1, 0.6)
```




### **각 요소 선택 & 순서**

1 ) num info (ex. fax, phone 등) 의 포함여부를 랜덤하게 결정합니다. 


```
num = ["phone", "tel", "website", "license_number", "fax", "email", "address"]

use = []
while not use:
    use += use_item(num, 0.7)
num_list = info_item(self.items, use)
```


2 ) num info (ex. fax, phone 등) 의 출력 순서를 랜덤하게 결정합니다.


```
random_items = list(num_list.keys())
random.shuffle(random_items)
```

### **텍스트 내용이 bbox 영역을 벗어나는 경우**

1 ) 폰트 크기 축소  


폰트 크기를 1pt씩 줄이며, 원래 폰트 크기의 30%가 되었어도 bbox 영역을 벗어나는 경우, 내용을 변경합니다. 


```
check, font_scale = change_font_size(item_type, content, mode, x, x_limit)
```



2 ) 내용 변경 


내용을 변경했어도 bbox 영역을 벗어나는 경우, 명함 이미지에 출력하지 않습니다. 


```
check, content = change_content(item_type, mode, x, x_limit, font)
```


###  **각 요소의 내용**


1 ) 이름


이름의 각 글자 사이에 공백을 랜덤하게 추가합니다.


ex. '가나다' / '가 나 다' / '가  나  다'


```
if random.random() >= 0.7:
    name = " ".join(name)
elif random.random() >= 0.4:
    name = "  ".join(name)
```
2 ) num info


- 구분자 (ex. - . ) 를 추가하여 정보를 나타냅니다. 


ex. 000-0000-0000 / ex. 000.0000.0000


- 카테고리 헤드를 사용하여 해당 정보 항목을 표시합니다. 이때, 카테고리 헤드의 적용 유무는 랜덤하게 결정됩니다.


ex. **tel.** 000-0000-0000


### **전체 이미지 크기**


파일을 실행할 때, width를 전달하면, height는 아래와 같이 결정됩니다.


```
height = int(width * random.uniform(1.0, 1.8)) # width의 1.0배~1.8배로 조정
```

### **생성한 이미지 시각화**


`data_visualization.ipynb` 파일에서 images 폴더와 json 파일의 경로를 수정하고, 생성된 명함 이미지를 확인합니다. 


# Template 
📑 템플릿 및 생성된 이미지 예시 : [Template & Image.pdf](https://github.com/boostcampaitech3/final-project-level3-cv-05/files/8771457/Template.Image.pdf)
