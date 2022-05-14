import sys

import requests
import streamlit as st
from PIL import Image
from PIL import ImageDraw
from streamlit import cli as stcli


def load_image(image_file):
    img = Image.open(image_file)
    return img


def draw_rectengle(image, point1, point2):
    draw = ImageDraw.Draw(image)
    draw.rectangle((point1[0], point1[1], point2[0], point2[1]), outline=(0, 0, 255), width=1)
    return image


def main():
    st.sidebar.header("Select service")
    name = st.sidebar.selectbox("Service", ["ImageNet"])

    st.title("OCR API Test")
    with st.form('my_form'):
        image_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
        submitted = st.form_submit_button("Submit")
        if submitted:
            files = {"file": image_file.getvalue()}
            st.write("Result")
            result = requests.post("http://127.0.0.1:8000/ocr", files=files).json()
            img = load_image(image_file)
            for i in result['result']['ocr']['word']:
                f, _, s, _ = i['points']
                draw_rectengle(img, f, s)
            st.image(img)


if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", "main.py"]
        sys.exit(stcli.main())