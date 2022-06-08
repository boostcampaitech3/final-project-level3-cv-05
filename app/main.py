import base64
import json
import json
import requests
from fastapi import FastAPI, UploadFile, File
from io import BytesIO

import word2line
from convert import converter

app = FastAPI()

with open('./api_info.json', 'rb') as f:
    api_infos = json.load(f)


@app.post("/crop")
async def crop(threshold: int, invert: int, angle: int, file: UploadFile = File(...)):
    byteImage = converter(file.file, (threshold, invert, angle))

    # files = {'file': byteImage}
    # try:
    #     ocr = requests.post(api_infos['api_url'], headers=api_infos['headers'], files=files).json()
    # except:
    #     result = {'detail': "API Server Response Error."}
    #
    # if ocr.get('ocr', 0):
    #     result = word2line.word2line(ocr)
    # else:
    #     result = ocr
    #     result['ocr'] = []

    encoded_image_string = base64.b64encode(byteImage.getvalue())
    result['image'] = encoded_image_string
    return result


@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    file_data = await file.read()
    files = {'file': file_data}
    json_result = requests.post(api_infos['api_url'], headers=api_infos['headers'], files=files).json()
    json_data = word2line_new.word2line(json_result)
    files = {
        'ocr': (None, json.dumps(json_data), 'application/json'),
        'file': file_data
    }
    string_line = " ".join([data['text'] for data in json_data['ocr']['word']])
    data = {'text': [string_line]}
    ner_result = requests.post(api_infos['ner_url'], data=json.dumps(data)).json()[0]
    cnn_result = requests.post(api_infos['cnn_url'], files=files).json()
    for data, cat in zip(json_data['ocr']['word'], cnn_result['test']):
        data["total_cat"] = None
        data['cnn_category'] = cat
        data['rule_cat'] = RuleBaseClassification(data['text']).rulebase_label()
        data["PER_token"] = False
        data["ORG_token"] = False
        for i, per in enumerate(ner_result["PER"]):
            if per.strip() in data["text"]:
                data["PER_token"] = True
                data["total_cat"] = 1
                del ner_result["PER"][i]
                continue
        for i, org in enumerate(ner_result["ORG"]):
            if org.strip() in data["text"]:
                data["ORG_token"] = True
                data["total_cat"] = 5
                del ner_result["ORG"][i]
                continue
        if data["total_cat"]:
            continue
        else:
            if data['rule_cat']:
                data["total_cat"] = data['rule_cat']
            else:
                # data["total_cat"] = data['cnn_category']
                data["total_cat"] = 0 if data['cnn_category'] == 1 or data[
                    'cnn_category'] == 5 else data['cnn_category']
    return {'result': json_data}
