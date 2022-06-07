from io import BytesIO

import torch
import cv2
import numpy as np
from PIL import Image
from fastapi import FastAPI, UploadFile, File, Form

from model import get_model, inference

app = FastAPI()
model = get_model('./date0604_epoch=9_val_accuracy=0.9945.ckpt', './config.yaml')
device = torch.device('cuda')


def read_image_file(file):
    encoded_img = np.fromstring(file, dtype=np.uint8)
    img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    return img


@app.post("/cls")
async def classification(ocr: str = Form(...), file: UploadFile = File(...)):
    image = read_image_file(await file.read())
    ocr = eval(ocr)
    input_data = {
        "images": [{
            'file': 'test.png',
            'height': image.shape[0],
            'width': image.shape[1],
            'id': 0
        }],
        "annotations": [
            {
                "image_id": 0,
                **ocr
            }
        ]
    }
    pred = inference(model, image, 30, input_data, device)
    result = pred.argmax(axis=1).tolist()
    return {"test": result}
