import sys

import requests
import streamlit as st
from PIL import Image, ImageDraw
from streamlit import cli as stcli

from convert import converter
import io

def load_image(image_file):
    img = Image.open(image_file)
    return img


def draw_rectengle(image, point1, point2):
    draw = ImageDraw.Draw(image)
    draw.rectangle((point1[0], point1[1], point2[0], point2[1]), outline=(255, 30, 30), width=2)
    return image

def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format="JPEG")
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

def to_ocr(data):
    files = {"file": data.getvalue()}
    result = requests.post("http://127.0.0.1:8000/ocr", files=files).json()
    ocr_image = load_image(data)
    if result['result']:
        for i in result['result']['ocr']['word']:
            f, _, s, _ = i['points']
            draw_rectengle(ocr_image, f, s)
        st.write("Output")
        st.image(ocr_image)
    else:
        st.warning("Can not find any Data")


def main():
    st.sidebar.header("Select service")
    name = st.sidebar.selectbox("Service", ["ImageNet"])
    st.title("OCR API Test")

    with st.form('my_form'):
        image_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
        submitted = st.form_submit_button("Submit")
        if submitted:
            to_ocr(image_file)
    self_fix = st.checkbox("Auto Fix", value=True)
    col1, col2 = st.columns(2)
    if image_file:
        with col1:
            bytes_data = image_file.getvalue()
            st.write("clear the check box if you want directly adjust")
            threshold = "auto"
            invert = False
            
            if self_fix:
                st.warning("Automatic revision is appied on data.\nWe recommend uncheck above checkbox and self revision for fine data")
            else:
                img = load_image(image_file)
                st.write('Rotate Angle')
                angle_fix = st.slider('Fix Angle', value=0, min_value = -180, max_value=180)
                angle_fixed = img.rotate(-angle_fix)
                st.write('Crop Position & Length')
                start_x = st.slider('Start Position of X', value=0, min_value = 0, max_value=img.size[0])
                start_y = st.slider('Start Position of Y', value=0, min_value = 0, max_value=img.size[1])
                end_x = st.slider('End Position of X', value=img.size[0], min_value = 0, max_value=img.size[0])
                end_y = st.slider('End Position of Y', value=img.size[1], min_value = 0, max_value=img.size[1])
                if start_x > end_x or start_y > end_y:
                    st.warning("Position Error: fix x, y")
                else:
                    cropped = angle_fixed.convert("L").convert("RGB")
                    img = angle_fixed.crop((start_x, start_y, end_x, end_y))
                    cropped.paste(img, (start_x, start_y))
                    cropped = draw_rectengle(cropped, (start_x, start_y), (end_x, end_y))

                bytes_data = image_to_byte_array(img)

                invert = st.checkbox("Invert: Check if image darker than BG.")
                threshold = st.slider('Change Threshold value', value=180, min_value=0, max_value=255)

            
        with col2:
            if not self_fix:
                with st.form('self_fix'):
                    st.image(cropped)
                    resubmit = st.form_submit_button("Submit")
                    if resubmit:
                        value = (threshold, invert)
                        converted = converter(bytes_data, value)
                        st.write("Submitted Image.")
                        st.image(converted)
                        to_ocr(converted)

    
if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", "main.py"]
        sys.exit(stcli.main())