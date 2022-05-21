# json_utils.py
"""
json 파일 생성에 필요한 모듈입니다.

Functions:
    get_category_id(item): 정보 항목의 이름에 맞는 category_id를 반환합니다.

    make_json(directory): 디렉토리에 json 파일을 새로 생성하고,
                          json 파일에 들어갈 내용을 딕셔너리에 담아 반환합니다.
    make_dir(directory): 디렉토리 존재 여부를 확인하고,
                              없으면 디렉토리를 새로 생성합니다.

    check_file_num(directory, ext): 디렉토리에 존재하는 특정 확장자 파일의 개수를 반환합니다.
"""
import os
import glob
import json
from typing import Dict, Any


def get_category_id(item: str) -> int:
    """
    정보 항목의 이름에 맞는 category_id를 반환합니다.

    Args:
        item (str): 정보 항목의 이름

    Returns:
        category_id (int): 정보 항목의 이름에 맞는 category id
    """
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


def make_json(directory: str) -> Dict[str, Any]:
    """
    디렉토리에 json 파일을 새로 생성하고,
    json 파일에 들어갈 내용을 딕셔너리에 담아 반환합니다.

    Args:
        directory (str): json 파일의 디렉토리

    Returns:
        json_data (dict): json 파일에 들어갈 내용 저장
    """
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
    """
    디렉토리 존재 여부를 확인하고,
    없으면 디렉토리를 새로 생성합니다.

    Args:
        directory (str): 확인 및 생성할 디렉토리
    """
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def check_file_num(directory: str, ext: str) -> int:
    """
    디렉토리에 존재하는 특정 확장자 파일의 개수를 반환합니다.

    Args:
        directory (str): 확인할 디렉토리
        ext (str): 확인할 확장자명

    Returns:
        length (int): 디렉토리에 존재하는 파일의 개수
    """
    file_list = glob.glob(f"{directory}/*{ext}")
    length = len(file_list)
    return length
