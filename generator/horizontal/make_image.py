import os
from generate import generate
from drawer import image_generate
import json
import argparse
from multiprocessing import Process, cpu_count, Value, Manager
import time

start = time.time()

# number of make images
def makeImage(idx, amount, images_list, annotations_list, number, progress, select, testmode, process_num=1, process_nums=1):
    s = idx + amount * process_num
    e = s + amount if not process_num + 1 == process_nums else idx + number

    for i in range(s, e):
        image, image_info, width, height = image_generate(select=select, test_mode=testmode)
        images_list.append({"width": width, "height": height, "file": f"{i:05}.png", "id": i})
        annotation = {"image_id": i, "ocr": {"word": image_info}}
        annotations_list.append(annotation)
        image.save(f"results/images/{i:05}.png")
        progress.value += 1 / number * 100
        print(f"\r▷  Progress is {progress.value:0.2f}% Completed...", end="")


if __name__ == "__main__":
    process_nums = cpu_count()
    print("▶  Number of CPU :", process_nums)
    print("▷  Load Json")

    for dir in ["results", "results/images"]:
        os.makedirs(dir, exist_ok=True)
    if os.path.exists("results/info.json"):
        with open("results/info.json", "r", encoding="UTF-8") as j:
            json_object = json.load(j)
    else:
        with open("sample.json", "r", encoding="UTF-8") as j:
            json_object = json.load(j)

    images_list = Manager().list(json_object["images"])
    annotations_list = Manager().list(json_object["annotations"])
    parser = argparse.ArgumentParser(description="Image Generator")
    parser.add_argument("--number", required=False, default=1000, type=int, help="Number of generation")
    parser.add_argument("--select", required=False, default="random", type=str, help="case")
    parser.add_argument("--testmode", required=False, default=False, type=bool, help="testmode")
    args = parser.parse_args()
    number = int(args.number)
    testmode = args.testmode
    select = args.select

    progress = Value("d", 0.000)
    idx = len(os.listdir("results/images"))

    if process_nums > 2:
        print("▶  Start Multiprocess Work")
    else:
        print("▶  Start Process")
    amounts = number // process_nums
    for process_num in range(process_nums):
        globals()[f"p{process_num}"] = Process(target=makeImage, args=(idx, amounts, images_list, annotations_list, number, progress, select, testmode, process_num, process_nums))
        globals()[f"p{process_num}"].start()

    for process_num in range(process_nums):
        globals()[f"p{process_num}"].join()
    print("")
    print(f"▶  {number} Images are Generated")
    print("▷ Set Json File...")
    json_object["images"] = sorted(list(images_list), key=(lambda x: x["file"]))
    json_object["annotations"] = sorted(list(annotations_list), key=(lambda x: int(x["image_id"])))
    with open("results/info.json", "w", encoding="UTF-8") as j:
        json_string = json.dump(json_object, j, indent=2)
    print("▶  Completed")
    lag = time.time() - start
    print(f"▷  Time spended : {lag:.2f} seconds")
