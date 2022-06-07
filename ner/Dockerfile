FROM python:3.8.5

WORKDIR ner_api

COPY ner_api ./

RUN pip install -r requirements.txt

ENTRYPOINT [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]