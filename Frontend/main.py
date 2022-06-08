import base64
import pandas as pd
import requests
import seaborn as sns
import streamlit as st
import sys
from PIL import Image, ImageDraw
from io import BytesIO
from streamlit import cli as stcli

cat = {
    0: "UNKNOWN",
    1: "name",
    2: "phone",
    3: "email",
    4: "position",
    5: "company",
    6: "department",
    7: "address",
    8: "site",
    9: "account",
    10: "wise",
}
colors = sns.color_palette('bright', 11)
palette = [tuple([int(i * 255) for i in color]) for color in colors]


def load_image(image_file):
    img = Image.open(BytesIO(image_file))
    return img


def draw_polygon(image, points):
    draw = ImageDraw.Draw(image)
    draw.polygon(points, outline=(255, 30, 30), width=2)
    return image


def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = BytesIO()
    image.save(imgByteArr, format="JPEG")
    return imgByteArr


def to_crop(bytesImage, threshold, invert, angle):
    """This function requests to back-end and response image, ocr output.
    Image is transformed(crop, angle, Etc..) output in back-end.
    OCR output is also transformed by back-end function 'word2line'.

    Args:
        bytesImage (Image(type: bytes)): auto inserted
        threshold (int): auto inserted
        invert (bool): It True or False from streamlit checkbox
        angle (int): auto inserted
    """
    param = {"threshold": threshold, "invert": invert, "angle": angle}
    files = {"file": bytesImage.getvalue()}
    result = requests.post(f"http://127.0.0.1:8000/crop/", params=param, files=files).json()
    image = base64.b64decode(result['image'])
    ocr_image = load_image(image)
    st.write("Server recognized image")
    st.image(ocr_image)


def to_ocr(bytesImage):
    """This function requests to back-end and response image, ocr output.
    Image is transformed(crop, angle, Etc..) output in back-end.
    OCR output is also transformed by back-end function 'word2line'.

    Args:
        bytesImage (Image(type: bytes)): auto inserted
    """
    files = {"file": bytesImage.getvalue()}
    result = requests.post(f"http://127.0.0.1:8000/ocr", files=files).json()
    image = base64.b64decode(result['image'])
    ocr_image = load_image(image)
    st.write("Server recognized image")
    st.image(ocr_image)


def main():
    st.sidebar.header("Select service")
    st.title("OCR API Test")
    image_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
    if image_file:
        to_crop(image_file, -1, 0, 1)
        st.warning("Use sidebar menu 'Fix Input' to fix input image by yourself")
        col1, col2 = st.columns(2)
        with col1:
            bytes_data = image_file.getvalue()
            threshold = -1
            img = load_image(bytes_data)
            st.write('Rotate Angle')
            angle_fix = st.slider('Fix Angle', value=0, min_value=-180, max_value=180)
            angle_fixed = img.rotate(-angle_fix)
            st.write('Crop Position & Length')
            start_x = st.slider('Start Position of X', value=0, min_value=0, max_value=img.size[0])
            start_y = st.slider('Start Position of Y', value=0, min_value=0, max_value=img.size[1])
            end_x = st.slider('End Position of X', value=img.size[0], min_value=0, max_value=img.size[0])
            end_y = st.slider('End Position of Y', value=img.size[1], min_value=0, max_value=img.size[1])
            if start_x > end_x or start_y > end_y:
                st.warning("Position Error: fix x, y")
            else:
                cropped = angle_fixed.convert("L").convert("RGB")
                img = angle_fixed.crop((start_x, start_y, end_x, end_y))
                cropped.paste(img, (start_x, start_y))
                cropped = draw_polygon(cropped,
                                       [(start_x, start_y), (end_x, start_y), (end_x, end_y), (start_x, end_y)])
            bytes_data = image_to_byte_array(img)
            invert = 1 if st.checkbox("Invert: Check if image darker than BG.") else 0
            threshold = st.slider('Change Threshold value', value=180, min_value=0, max_value=255)
        with col2:
            with st.form('self_fix'):
                st.image(cropped)
                resubmit = st.form_submit_button("Submit")
                if resubmit:
                    st.write("Submitted Image.")
                    st.image(bytes_data)
        if resubmit:
            to_ocr(bytes_data, threshold, invert, 0)


if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", "main.py"]
        sys.exit(stcli.main())
