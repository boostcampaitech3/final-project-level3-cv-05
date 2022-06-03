import json
from io import BytesIO

import requests
from fastapi import FastAPI, UploadFile, File

import word2line
from convert import converter
import json, base64

app = FastAPI()

with open('./api_info.json', 'rb') as f:
    api_infos = json.load(f)



@app.post("/ocr/")
async def classfication(threshold:int, invert:int, angle:int, file: UploadFile = File(...)):
    #files = read_imagefile(await file.read())
    byteImage = converter(file.file, (threshold, invert, angle))
    files = {'file': byteImage}
    
    ocr = requests.post(api_infos['api_url'], headers=api_infos['headers'], files=files).json()
    if ocr.get('ocr', 0):
        result = word2line.word2line(ocr)
    else:
        result = {}
    
    encoded_image_string = base64.b64encode(byteImage.getvalue())
    result['image'] = encoded_image_string
    return result