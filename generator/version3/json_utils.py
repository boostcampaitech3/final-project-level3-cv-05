import os
import glob
import json

########################
## json util funtions ##
########################

num = ["phone", "tel", "website", "license_number", "fax", "email", "address"]


def get_category_id(item: str):
    if item in "name":
        category_id = 1
    elif item in "phone":
        category_id = 2
    elif item == "email":
        category_id = 3
    elif item == "position":
        category_id = 4
    elif item == "company":
        category_id = 5
    elif item == "department":
        category_id = 6
    elif item == "address":
        category_id = 7
    elif item == "website":
        category_id = 8
    elif item == "account":
        category_id = 9
    else:
        category_id = 0
    return category_id


def make_json(directory: str):
    json_data = {}
    json_data["images"] = []
    json_data["categories"] = (
        {
            "0": "UNKNOWN",
            "1": "name",
            "2": "phone",
            "3": "email",
            "4": "position",
            "5": "company",
            "6": "department",
            "7": "address",
            "8": "site",
            "9": "account",
            "10": "wise",
        },
    )
    json_data["annotations"] = []
    with open(directory, "w", encoding="utf-8") as make_file:
        json.dump(json_data, make_file, indent="\t")
    return json_data


def make_dir(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def check_file_num(directory: str, ext: str):
    file_list = glob.glob(f"{directory}/*{ext}")
    length = len(file_list)
    return length
