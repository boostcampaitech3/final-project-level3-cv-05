# Backend
FastAPI를 이용하여 3개의 분리된 모듈로 구현한 Backend(OCR API / CNN + MLP / NER)

### 구성

```bash
app/
├── 📄 convert.py          # 이미지 각도, 크기 보정
├── 📄 main.py             # 구동 파일
├── 📄 requirements.txt    # 필요한 라이브러리
├── 📄 run.py              # 서버 구동 파일 
└── 🗒️ word2line.py        # OCR API로부터 나온 결과를 모델이 학습하기에 적합하도록 전처리
```   

### word2line.py
> **Task**   

OCR API의 output으로 나오는 bbox 정보 (bbox의 위치, bbox의 크기, 텍스트 내용)를 모델이 학습하기에 적합하도록,
각 카테고리 (ex. 이메일) 단위로 bbox 영역울 합쳐줍니다.

<img width="1000" alt="line parsing" src="https://user-images.githubusercontent.com/90603530/172527691-5e9ba6fb-258e-40d2-9e8f-02b8256a561a.png">

> **How**
<img width="1000" alt="설명" src="https://user-images.githubusercontent.com/90603530/172528851-a555082e-702e-4f9f-acc2-988d594e2907.png">



### 필요한 라이브러리 설치
```bash
pip install -r requirements.txt
```
