# folder structure 
모델 학습 이미지를 생성하기 위한 이미지 생성 프로그램 version3
- 회사 이름/이름/직책&부서/숫자 정보 등에 대해 템플릿 클래스를 만든 후, 이를 랜덤하게 조합하여 명함 이미지 생성 

```python
version3/
├── 📝 card_utils.py              # 명함 템플릿 생성에 필요한 파일 
├── 📝 generate.py                # csv 파일을 토대로 정보 생성 
├── 📝 json_utils.py              # json 파일 생성에 필요한 파일 
├── 📝 make_card.py               # 명함 이미지를 생성하는 파일 
│
└── 📂 example
    ├── 📂 images
    └── 📄 *.png                  # sample images folder 
    └── 📄 info.json              # sample annotations file  
```
### 실행
아래와 같이 명령어를 작성하여 실행
```
python make_card --num [생성될 이미지 개수] --dir [json 파일 경로]
```   
