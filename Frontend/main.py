import sys

import requests
import streamlit as st
from PIL import Image
from PIL import ImageDraw
from streamlit import cli as stcli
import seaborn as sns
import pandas as pd

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
palette = [tuple([int(i*255) for i in color]) for color in colors]

def load_image(image_file):
    img = Image.open(image_file)
    return img


def draw_rectengle(image, point1, point2, color_cat):
    draw = ImageDraw.Draw(image)
    draw.rectangle((point1[0], point1[1], point2[0], point2[1]), outline=palette[color_cat], width=3)
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
            img1 = load_image(image_file)
            text, category = [], []
            for i in result['result']['ocr']['word']:
                f, _, s, _ = i['points']
                text.append(i['text'])
                category.append(cat[i["total_cat"]])
                draw_rectengle(img1, f, s, i['total_cat'])
            st.image(img1)
            df = pd.DataFrame.from_dict({"text": text, "category": category})
            st.dataframe(data=df, width=600, height=500)


if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", "main.py"]
        sys.exit(stcli.main())
