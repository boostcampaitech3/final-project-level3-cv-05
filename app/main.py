import json
from io import BytesIO

import requests
from fastapi import FastAPI, UploadFile, File

import word2line

app = FastAPI()

with open("./api_info.json", "rb") as f:
    api_infos = json.load(f)


def read_imagefile(file) -> BytesIO:
    return BytesIO(file)


@app.post("/ocr")
async def classfication(file: UploadFile = File(...)):
    files = {"file": file.file}
    result = requests.post(
        api_infos["api_url"], headers=api_infos["headers"], files=files
    ).json()
    result = word2line.word2line(result)
    return {"result": result}
