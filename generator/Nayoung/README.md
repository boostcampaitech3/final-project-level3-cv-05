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
├── 📝 image_generator.ipynb      # 데이터 생성용 노트북 파일 
├── 📝 make_card.py               # image & bbox return 
├── 📝 make_name.ipynb            # divide name.csv into ko_name.csv, eng_name.csv
├── 📝 make_template.py           # info & font info return 
│
└── 📂 example
    ├── 📂 images
    │   └── 📄 *.png              # sample images folder 
    └── 📄 info.json              # sample annotations file  
```
