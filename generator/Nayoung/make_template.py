import json
import os

########################
## template generator ##
########################

template_dir = "template"
dir = os.getcwd()

with open(f"{template_dir}/template.json", "r") as f:
    json_data = json.load(f)
    annotations = json_data["annotations"]
    categories = json_data["categories"]
    images = json_data["images"]

template_list = [{} for _ in range(0, len(images) + 1)]  # index로 template 정보에 접근

# background image size
for idx, item in enumerate(images):
    idx += 1
    width, height = item["width"], item["height"]
    template_list[idx]["size"] = [width, height]

# categories
category = {}
for item in categories:
    category[item["id"]] = item["name"]

# bbox
coord, sizes = {}, {}
index = 1
pre = annotations[0]["image_id"]
for item in annotations:
    if pre != item["image_id"]:
        template_list[index]["bbox"] = coord
        template_list[index]["bbox_size"] = sizes

        pre = item["image_id"]
        index += 1
        coord, sizes = {}, {}

    item_name = category[item["category_id"]]
    coord[item_name] = item["bbox"][:2]  # (x, y, w, h) -> (x, y)
    sizes[item_name] = item["bbox"][2:]  # (x, y, w, h) -> (w, h)

# 마지막 인덱스의 정보 업데이트
template_list[index]["bbox"] = coord
template_list[index]["bbox_size"] = sizes
