import json
from io import BytesIO

import requests
from fastapi import FastAPI, UploadFile, File

import word2line

app = FastAPI()

with open('./api_info.json', 'rb') as f:
    api_infos = json.load(f)


def read_imagefile(file) -> BytesIO:
    return BytesIO(file)


@app.post("/ocr")
async def classfication(file: UploadFile = File(...)):
    #files = read_imagefile(await file.read())
    files = {'file': file.file}
    ocr = requests.post(api_infos['api_url'], headers=api_infos['headers'], files=files).json()
    if ocr.get('ocr', 0):
        result = word2line.word2line(ocr)
    else:
        result = []
    return {'result': result}
