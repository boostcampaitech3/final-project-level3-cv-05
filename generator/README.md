# Image Generator

#### 1. 이미지를 생성하는 이유

- **데이터 수집의 관점**
  명함 데이터는 개인정보를 많이 포함하고 있어 크롤링은 발생하는 개인정보 보호에 있어 문제가 발생할 수 있으며, 제조 업체의 예시 이미지가 다량 포함되나 이를 데이터로 활용하기 위한 작업이 생성보다 불리하다고 판단하였습니다.
- **모델 학습의 관점**
   우리 조는 NLP적인 요소를 제외하고 CV로 해당 Task를 해결한다면 명함에서 언어를 모르는 어떤 명함을 보았을 때, 뜻이나 발음을 몰라도 정보를 유추할 수 있듯, 언어나 내용에 관계없이 정보를 분류할 수 있을 것으로 기대하였습니다.
   특히 명함은 이름, 소속, 직책, 연락처 등 상대에게 전달하려는 정보를 강조하기 때문에, 다양한 틀이 있더라도 특정한 규칙이 있을 것으로 추측하였습니다. 이를 반영하기 위해 우리가 추측한 규칙을 기반으로 다양한 변동성을 가진 데이터를 학습시키면 단어들의 크기와 위치 관계에 따라 판단을 할 수 있을 것으로 기대하였습니다.



#### 2. 구성

```bash
generator/
├── 📂 data/
│   └── 🗒️ *.csv                        # DB
│
├── 📂 font/                            # 구글 드라이브에서 다운로드
│   ├── 📂 logo/
│   ├── 📂 main/
│   └── 📂 sub/
│    
├── 📂 horizontal/
│    ├── 📄 __init__.py
│    ├── 📄 colormap.csv                # colormap
│    ├── 📄 drawer.py                   # image & bbox return
│    ├── 📄 generate.py                 # csv load & random return
│    ├── 📄 generator_notebook.ipynb    # 이미지 생성용 노트북 파일
│    ├── 📄 make_image.py               # 이미지 생성용 py 파일
│    ├── 📄 sample.json                 # 최초 생성에 사용하는 template json
│    ├── 📄 viewer.ipynb                # 이미지 확인용 노트북 파일
│    │
│    └── 📂 results                     # 데이터 생성 폴더
│       ├── 📂 images                   # 이미지 폴더
│       └── 📄 info.json                # annotations
│
└── 📂 vertical/
    ├── 📂 make
    │    ├── 📝 make_component.py       # 정보 box (ex. name, company) 생성
    │    └── 📝 make_template.py        # 정보 box를 토대로 템플릿 클래스 생성 
    │
    ├── 📂 utils
    │    ├── 📝 bbox_utils.py           # bbox 생성 및 영역 확인에 필요한 파일
    │    ├── 📝 card_utils.py           # 명함 이미지 생성에 필요한 파일 
    │    └── 📝 json_utils.py           # json 파일 생성에 필요한 파일 
    │
    ├── 📝 data_visualization.ipynb     # 생성된 명함 이미지 시각화
    ├── 📝 generate.py                  # csv 파일을 토대로 정보 생성 
    ├── 📝 main.py                      # 템플릿을 토대로 명함 이미지 생성 
    │
    └── 📂 example
        ├── 📂 images                   # sample images folder 
        │    └── 📄 *.png                    
        └── 📄 info.json                # sample annotations file    	
```

> [글꼴 다운로드](https://drive.google.com/file/d/1DG2EJLKO-e9_tXyqEhh0aRguG21YKaBH/view?usp=sharing)(177MB)

크게 가로형([horizontal](horizontal)) 명함과 세로형([vertical](vertical)) 명함이 존재합니다. 상세한 내용과 사용법은 각 폴더 내 README파일을 확인하시기 바랍니다.
