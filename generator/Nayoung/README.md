# folder structure 

모델 학습 이미지를 생성하기 위한 이미지 생성 프로그램입니다.

```python
Nayoung/
├── 📂 template/
│   ├── 📂 template_img           # template background image 
│   │   └── 📄 *.png
│   ├── 🗒️ font.py                # template font_size, font_color info 
│   └── 📄 template.json          # template bbox, category_id info 
│
├── 📝 generate.py                # csv load & random return        
├── 📝 make_card.py               # image & bbox return 
├── 📝 make_name.ipynb            # divide name.csv into ko_name.csv, eng_name.csv
├── 📝 make_template.py           # info & font info return 
│
└── 📂 example
    ├── 📂 images
    │   └── 📄 *.png              # sample images folder 
    └── 📄 info.json              # sample annotations file  
```
### 실행
아래와 같이 명령어를 작성하여 실행 
```
python make_card --num [생성될 이미지 개수] --dir [json 파일 경로]
```   
