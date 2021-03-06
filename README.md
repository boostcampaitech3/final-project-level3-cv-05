# Demo ๐ป

![demo](https://user-images.githubusercontent.com/90603530/172541502-36019954-a31a-488b-8f61-a03a823e4b7e.gif)


# Project Overview ๐

### ํ๋ก์ ํธ ์๊ฐ ๋ฐ ๊ฐ๋ฐ ๋ชฉํ

Upstage OCR API๋ก๋ถํฐ ์ถ์ถํ OCR ์ ๋ณด๋ฅผ ์๋ง๊ฒ ๋ถ๋ฅํ๋ **Post OCR Parsing Task**

\* **OCR** (Optical Character Recognition) : ํ์คํธ ์ด๋ฏธ์ง๋ฅผ ๊ธฐ๊ณ๊ฐ ์ฝ์ ์ ์๋ **๋ฌธ์๋ก ๋ณํ**ํ๋ ๊ณผ์ ์๋๋ค.

\* **Post OCR Parsing** : ํ์คํธ ์ด๋ฏธ์ง์ OCR ๊ฒฐ๊ณผ๋ฅผ ๊ธฐ๋ฐ์ผ๋ก, ํด๋น ์ด๋ฏธ์ง ๋ด์์ ์ป๊ณ ์ ํ๋ **์ ๋ณด๋ฅผ ์ถ์ถ**ํ๋ ๊ณผ์ ์๋๋ค.

### ์ ๊ทผ ๋ฐฉ๋ฒ

> **Dataset**
> 

๊ฐ์ธ์ ๋ณด๊ฐ ํฌํจ๋ ๋ชํจ ์ธ์๋ฌผ์ ํน์ฑ์, ํฌ๋กค๋งํ์ฌ ์์งํ  ๊ฒฝ์ฐ ๊ฐ์ธ์ ๋ณด ๋ณดํธ ์ด์๊ฐ ๋ฐ์ํ  ๊ฒ์ด๋ผ๊ณ  ์๊ฐํ์ต๋๋ค.  
๋ํ, ์ง์  ์์งํ  ๊ฒฝ์ฐ, ๋ชจ๋ธ์ด ํ์ตํ๊ธฐ์ ์ถฉ๋ถํ ์์ ๋ฐ์ดํฐ๋ฅผ ๊ตฌ์ถํ๊ธฐ ์ด๋ ค์ธ ๊ฒ์ด๋ผ๊ณ  ํ๋จํ์ฌ **๋ฐ์ดํฐ๋ฅผ ์ง์  ์์ฑ**ํ๋ ๊ฒ์ผ๋ก ๊ฒฐ์ ํ์ต๋๋ค. 

> **Feature Engineering**
> 

OCR API๋ก๋ถํฐ ์ ๋ฌ๋ฐ์ ๊ฒฐ๊ณผ๋ก๋ถํฐ, ๋ชํจ ์ด๋ฏธ์ง ํน์ฑ์ ๋ง๋ feature๋ค์ ์์ฑํด์ฃผ๋ ์์์ด ํ์ํ์ต๋๋ค.  
๋ฐ์ ์ ๋ณด์ธ bounding box ์ขํ์ ํด๋น text ์ ๋ณด๋ฅผ ์ด์ฉํด feature๋ค์ ์์ฑํด์ฃผ์์ต๋๋ค.

> **Model**
> 

- **CNN (image data) + MLP (tabular data)** 

์ค์  ๋ชํจ ์ด๋ฏธ์ง๋ฅผ ์กฐ์ฌํ ๊ฒฐ๊ณผ, ๋ชํจ ๋ด **์ ๋ณด ์์น**์ **๊ธ์** **ํฌ๊ธฐ**๊ฐ ํน์ ํ ์ ๋ณด๋ฅผ ๊ฐ์กฐํ๊ธฐ ์ํ ํํ๋ฅผ ์ด๋ฃจ๊ณ  ์๋ค๊ณ  ํ๋จํ์ต๋๋ค.  
์ด๋ฅผ ํ ๋๋ก Computer Vision ๊ด์ ์์ ๋ชํจ **Image data**์ ํจ๊ป, ๋ชํจ ๋ด ์ ๋ณด์ ์์น๊ด๊ณ์ ๊ฐ์ **Tabular data**๋ฅผ ์ด์ฉํ ๋ชจ๋ธ์ ์ ์ฉํ์ต๋๋ค.

- **NER** 

๋ชํจ ์ ๋ณด ๋ถ๋ฅ๋ฅผ ์ํด ์์ฐ์ด ์ฒ๋ฆฌ์ ๊ฐ์ฒด๋ช ์ธ์ task ๋ฅผ ์ ์ฉํ๋ฉด ์ฑ๋ฅ ํฅ์์ด ์์ ๊ฒ์ด๋ผ๊ณ  ํ๋จํ์ฌ NER Model ์ ์ฌ์ฉํ์์ต๋๋ค.   
**ํ๊ตญ์ด๋ฅผ ์ํ KoBERT ๋ชจ๋ธ์ Conditional Random Field (CRF)** Layer๊ฐ ์ถ๊ฐ๋ KoBERT + CRF ๊ธฐ๋ฐ์ Opensource NER Model ์ ์ฌ์ฉํ์์ต๋๋ค.    
ํ๊ตญ์ด ๊ฐ์ฒด๋ช ํ๊น์ด ๋์ด์๋ Open dataset ์ ํตํด ํ์ต์ ์งํํ์์ผ๋ฉฐ, ํด๋น Dataset์ ์ฌ๋ ์ด๋ฆ, ๊ธฐ๊ด๋ช, ์๊ฐ, ๋ ์ง, ํตํ๋ฅผ ํฌํจํ 8๊ฐ category ๊ฐ ์กด์ฌํ๋ Dataset ์ด์์ต๋๋ค.    
์ด ์ค์์ ๋ชํจ ์ ๋ณด ๋ถ๋ฅ์ ์ ์ฉํ  ์ ์๋ ์ฌ๋ ์ด๋ฆ, ๊ธฐ๊ด๋ช category์ ๋ํ inference ๊ฒฐ๊ณผ๊ฐ ๋ง์ ์ถ์ถํ๊ณ  ์ ์ฉํ์ฌ ๋ชจ๋ธ ์ฑ๋ฅ์ ํฅ์์์ผฐ์ต๋๋ค.    

# Project Result ๐

### ๊ตฌํ Task

๊ธฐ๋ณธ์ ์ผ๋ก ์ถ์ถํด์ผ ํ๋ ์ด๋ฆ/์ ํ๋ฒํธ/์ด๋ฉ์ผ์ฃผ์/์ง์ฑ์ 4๊ฐ์ง ์นดํ๊ณ ๋ฆฌ๋ฅผ ํฌํจํ์ฌ, ์ด 10๊ฐ์ง (UNKNOWN ํฌํจ 11๊ฐ์ง) ์ ์นดํ๊ณ ๋ฆฌ๋ฅผ ๋ถ๋ฅํ  ์ ์์ต๋๋ค.

### ํ๊ฐ Metric

> **Accuracy**
> 

์ ๋ณด๋ฅผ ๊ฐ์ง ๋ชจ๋  bounding box์ ๋ํด์ **์นดํ๊ณ ๋ฆฌ๋ฅผ ๋ง์ถ ๋น์จ**๋ก ํ๊ฐ metric์ ์ค์ ํ์ต๋๋ค.  

> **Result**
> 

```diff
train accuracy : 1
validation accuracy : 0.9945
```

# Learn More ๐

| Task | Description |
| --- | --- |
| [Data Generation](https://github.com/boostcampaitech3/final-project-level3-cv-05/blob/develop/generator/README.md)  | ํ์ต์ ์ฌ์ฉํ  ๋ชํจ ์ด๋ฏธ์ง ๋ฐ์ดํฐ + json ํ์ผ ์์ฑ  |
| [Data Pre-processing](https://github.com/boostcampaitech3/final-project-level3-cv-05/blob/BE/app/README.md) | OCR API๋ก๋ถํฐ ๋์จ ๊ฒฐ๊ณผ๋ฅผ ๋ชจ๋ธ์ด ํ์ตํ๊ธฐ์ ์ ํฉํ๋๋ก ์ ์ฒ๋ฆฌ  |
| [Model - CNN + MLP](https://github.com/boostcampaitech3/final-project-level3-cv-05/blob/develop/post_ocr_model/README.md) | Image data (CNN) ์ Tabular data (MLP) ๋ฅผ ๋ชจ๋ ๊ณ ๋ คํ์ฌ ํ์ตํ๋ ๋ชจ๋ธ  |
| [Model - NER](https://github.com/boostcampaitech3/final-project-level3-cv-05/blob/develop/ner/README.md) | ํ์ต๋ ๋ชจ๋ธ์ ํตํด ์ผ๋ถ feature์ category ๋ถ๋ฅ |
| [Feature Engineering](https://github.com/boostcampaitech3/final-project-level3-cv-05/blob/feature-engineering/README.md) | ๋ฐ์ดํฐ์ ํน์ฑ์ ๊ณ ๋ คํ feature ์์ฑ |
| [Frontend](https://github.com/boostcampaitech3/final-project-level3-cv-05/blob/develop/Frontend/README.md) | Auto fix / Fix input ๊ธฐ๋ฅ์ด ์ถ๊ฐ๋, Streamlit์ผ๋ก ๊ตฌํํ ํ๋กํ ํ์ |
| [Backend](https://github.com/boostcampaitech3/final-project-level3-cv-05/blob/BE/app/README.md) | FastAPI๋ฅผ ์ด์ฉํ์ฌ 3๊ฐ์ ๋ถ๋ฆฌ๋ ๋ชจ๋๋ก ๊ตฌํํ Backend(OCR API / CNN + MLP / NER) |

# Pipeline ๐

### **๊ฐ์**

<image width = "50%" src = "https://user-images.githubusercontent.com/90603530/172541879-3dfae2dd-8c9a-4556-a4d2-0caed4477ac4.png">

Demo Front-end๋ Streamlit์ ํตํด ๊ตฌํํ์์ต๋๋ค. Streamlit Front-end๋ FastAPI ๊ธฐ๋ฐ์ Back-end๋ฅผ ํตํด ์ถ๋ ฅ๋ฌผ์ ์ฌ์ฉ์์๊ฒ ์ ๊ณตํฉ๋๋ค.

### **Pipeline**

<image width = "100%" src = "https://user-images.githubusercontent.com/90603530/172560268-2ac7458b-5607-49db-888c-222b21832e45.png">

- **Data Pre-processing**       
  ์ฌ์ฉ์๊ฐ ์ด๋ฏธ์ง๋ฅผ ์ ์ถํ๋ฉด, ๊ฐ๋ฅํ ๊ฒฝ์ฐ Back-end ์๋ฒ์์ ์ด๋ฏธ์ง์ ๊ฐ๋์ ๋ฒ์๋ฅผ ๋ณด์ ํฉ๋๋ค. 
  ํด๋น ์ด๋ฏธ์ง๋ฅผ OCR API ์๋ฒ๋ก ์์ฒญํ์ฌ json output์ ์๋ต์ผ๋ก ๋ฐ๊ณ , ์ถ๋ ฅ๋ ์ ๋ณด๋ฅผ ์กฐ๊ฑด์ ๋ฐ๋ผ ์ค ๋จ์๋ก ๋ณ๊ฒฝํฉ๋๋ค.
- ์ ์ฒ๋ฆฌ๋ ์ ๋ณด๊ฐ ๊ฐ ์กฐ๊ฑด์ ๋ฐ๋ผ ๋ชจ๋ธ ๋ฐ rule-base๊ธฐ๋ฐ์ผ๋ก ์ฒ๋ฆฌ๋๊ณ , ์ถ๋ ฅ๊ฐ์ ๋ฐ๋ผ ๊ฐ ํญ๋ชฉ์ category๋ฅผ ์ ๊ณตํฉ๋๋ค.

# Getting Started ๐

### Demo Site

- TBA

### Requirements

`Learn More`์ ๊ธฐ๋กํ ๊ฐ README ํ์ผ์ ์ฐธ๊ณ ํ์ฌ ํ์ํ ๋ผ์ด๋ธ๋ฌ๋ฆฌ๋ฅผ ์ค์นํด์ฃผ์๋ฉด ๋ฉ๋๋ค.

# Team ๐งโ๐ป

### ConVinsight

ConVinsight(CV-05)๋ Computer Vision์ ์ด๋์์ธ '**CV**'์, 

'์ด์ฉ์์ **Conv**enience(ํธ๋ฆฌ)๋ฅผ ์ฐพ๋ **insight**(ํต์ฐฐ๋ ฅ)' ์ ์๋ฏธํฉ๋๋ค.

### Member

| Member  | Role  | Github |
| --- | --- | --- |
| ๊น๋์ | OCR Output ์ ์ฒ๋ฆฌ / ๋ฐ์ดํฐ ์์ฑ | [Github](https://github.com/dudskrla) |
| ์ ๊ท๋ฒ | PM / ๋ชจ๋ธ ์ค๊ณ ๋ฐ ๊ตฌํ / OCR Output ์ ์ฒ๋ฆฌ / ์๋น์ค ๊ตฌํ | [Github](https://github.com/KyubumShin) |
| ์ด์ ์ | Feature ์ค๊ณ / ๋ชจ๋ธ ํ์ต / Test ๋ฐ์ดํฐ์ ๊ตฌํ | [Github](https://github.com/sw930718) |
| ์ดํํ | ๋ฐ์ดํฐ ์์ฑ / ์ด๋ฏธ์ง ์ ์ฒ๋ฆฌ | [Github](https://github.com/Heruing) |
| ์ ์๋ฏผ | Feature ์ค๊ณ / ๋ชจ๋ธ ๊ตฌํ ๋ฐ ๋ชจ๋ธ ํ์ต / Test ๋ฐ์ดํฐ์ ๊ตฌํ | [Github](https://github.com/Su-minn) |
