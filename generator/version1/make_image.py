import os
from generate import generate
from drawer import image_generate
import json
import argparse


# number of make images
def makeImage(number):
    for dir in ["results", "results/images"]:
        os.makedirs(dir, exist_ok=True)

    idx = len(os.listdir("results/images"))
    if os.path.exists("results/info.json"):
        with open("results/info.json", "r", encoding="UTF-8") as j:
            json_object = json.load(j)
    else:
        with open("sample.json", "r", encoding="UTF-8") as j:
            json_object = json.load(j)
    for _ in range(number):
        info = generate()
        image, image_info, width, height = image_generate(info)
        json_object["images"].append({"width": width, "height": height, "file": f"{idx:04}.png", "id": idx})
        annotation = {"image_id": idx, "ocr": {"word": image_info}}
        json_object["annotations"].append(annotation)
        image.save(f"results/images/{idx:04}.png")
        idx += 1

    with open("results/info.json", "w", encoding="UTF-8") as j:
        json_string = json.dump(json_object, j, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image Generator")
    parser.add_argument("--number", required=True, default=1000, type=int, help="Number of generation")
    args = parser.parse_args()
    number = int(args.number)
    makeImage(number)
