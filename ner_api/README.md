## NER API 사용법

### 필요 파일
- checkpoints directory 하위에 ner weight 파일을 다운 받아 넣어주세요.
  - [ner weight drive link](https://drive.google.com/file/d/1-USuCT7FYF3p9UFTalHl-RsQoJZxLaue/view?usp=sharing)
  - 결과 : ner_api/checkpoints/best-epoch-12-step-1000-acc-0.961.bin

### 환경 설정
- AI stage 의 경우
  - docker in docker issue 로 내부에서 docker 를 사용할 수 없기에,  
  ```pip install -r requirements.txt``` 을 이용하여 필요 라이브러리 설치
  
- Local 환경의 경우 (or docker 사용 가능한 경우)
  - docker Image 생성 (Dockerfile이 존재하는 경로에서 실행)
    - ```docker build -f Dockerfile -t ner_api-img .```
  - docker container 생성 및 실행 (FastAPI 서버 자동 실행)
    - ```docker run —name ner_api-con -p 8000:8000 -d ner_api-img```

### 서버 동작
- AI stage 의 경우
  - 환경 설정 완료 후, ner_api directory 에서 (현재 directory 에 app directory 가 존재)   
  ```python3 -m app``` 실행

- Local 환경의 경우 (or docker 사용 가능한 경우)
  - docker container 를 동작시키면 자동으로 서버 동작

### API 명세
- NER Inference 결과 값 요청
  - METHOD : POST
  - URI : /ner
  - 요쳥 변수 및 사용 example : [api_test_examlpy.py](https://github.com/boostcampaitech3/final-project-level3-cv-05/blob/ner/ner_api/api_test_example.py) (API TEST EXAMPLE) 참조

