# Image Generator

모델 학습 이미지를 생성하기 위한 이미지 생성 프로그램입니다.

### **사용법**

1. `data/template.json` 을 통해 기입할 내용과 위치를 작성합니다.
2. `drawer.py` 내에 `scale`이 지정되어 있으므로 이를 참고하여 위치 시킵니다.
3. `logo`에 대해서는 삽입 방법 개선 중입니다.
4. 노트북 파일 또는 `make_image.py` 실행
   - 파이썬 파일 실행시 `--number [이미지 생성 수]` 기본 1000장에서 원하는 수 만큼 생성
   - `py` 파일에 multiprocessing이 적용되어 있으므로 테스트가 아니면 해당 파일 추천

```python
generator/
└── 📂 data/
    ├── 🗒️ *.csv					 # DB
    │
    📂 font/						# 구글 드라이브에서 다운로드
    ├── 📂 logo/
    ├── 📂 main/
    ├── 📂 sub/
    │
	📄 __itit__.py
    📄 colormap.csv			    	# colormap
    📄 drawer.py					# image & bbox return
    📄 generate.py					# csv load & random return
    📄 generator_notebook.ipynb		# 이미지 생성용 노트북 파일
    📄 make_image.py				# 이미지 생성용 py 파일
    📄 sample.json					# 최초 생성에 사용하는 template json
    📄 viewer.ipynb					# 이미지 확인용 노트북 파일(EDA 예정)
    │
    │
    │
    └── 📂 results					# 데이터 생성 폴더
    	├── 📂 images				# 이미지 폴더
    	└── 📄 info.json			# annotations
```

폰트는 [여기](https://drive.google.com/file/d/1DG2EJLKO-e9_tXyqEhh0aRguG21YKaBH/view?usp=sharing)를 눌러 다운로드

### workflow

![workflow](./workflow.png)

### caution

1. 데이터 셋 통일을 위해 반드시 팀 내에서 공유된 상태로 사용할 것
2. 너무 긴 문자열 등으로 발생하는 이상 데이터 체크할 것
3. 결과물에 따라 변동 가능성 인지