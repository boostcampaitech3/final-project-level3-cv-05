# word2line.py
"""
OCR API로부터 나온 결과를 모델이 학습하기에 적합하도록 전처리하는 모듈입니다.
"""

from typing import Dict, List

##############################
###### sorting function ######
##############################


def standard_y(word_list: List) -> int:
    """
    리스트에 존재하는 단어들의 y좌표 중 가장 작은 값 선택

    Args:
        word_list (List): 해당 라인에 존재하는 단어들

    Returns:
        int: 해당 라인의 y좌표 중 가장 작은 값
    """

    y = int(1e9)

    for word in word_list:
        y = min(y, word["points"][3][1])

    return y


def delete_line(temp_words: List, line: List) -> List:
    """
    같은 라인에 위치한 word 정보 제거

    Args:
        temp_words (List): bbox 정보를 담고 있는 리스트
        line (List): 제거하려는 word 정보를 담고 있는 리스트

    Returns:
        List: 같은 라인에 위치한 word 정보가 제거된 리스트
    """

    for item in line:
        temp_words.remove(item)

    return temp_words


def sort_json(json_data: Dict) -> List:
    """
    json_data의 원소를 사람이 읽는 순서 (좌상단 -> 우하단) 대로 정렬

    Args:
        json_data (Dict): OCR API로부터 전달받은 bbox 정보

    Returns:
        List: 정렬이 완료된 json_data 정보를 담은 리스트
    """

    temp_words = json_data["ocr"]["word"]
    temp_words = [word for word in temp_words]
    words = []

    while temp_words:
        y = standard_y(temp_words)
        line = []

        # 같은 라인에 있으면 line에 추가
        for word in temp_words:
            if abs(word["points"][3][1] - y) < abs(
                word["points"][1][1] - word["points"][3][1]
            ):
                line.append(word)

        # 시작 x좌표를 기준으로 정렬
        words += sorted(line, key=lambda item: item["points"][0][0])

        # 같은 라인 요소들 제거
        temp_words = delete_line(temp_words, line)

    return words


############################
###### check function ######
############################


def check_height(word1: Dict, word2: Dict, threshold: float) -> bool:
    """
    두 단어의 높이 비율 확인

    Args:
        word1 (Dict): 확인할 첫 번째 단어의 bbox 정보
        word2 (Dict): 확인할 두 번째 단어의 bbox 정보
        threshold (float): 높이 비율의 기준

    Returns:
        bool: 기준 통과 여부
    """

    word1_text_height = abs(word1["points"][0][1] - word1["points"][2][1])
    word2_text_height = abs(word2["points"][0][1] - word2["points"][2][1])

    height_ratio = (
        word1_text_height / word2_text_height
        if word1_text_height <= word2_text_height
        else word2_text_height / word1_text_height
    )

    if height_ratio >= threshold:  # 기준 설정 필요
        return True
    else:
        return False


def check_y(word1: Dict, word2: Dict, threshold: float) -> bool:
    """
    두 단어가 비슷한 줄에 위치하는지/다른 줄에 위치하는지 확인

    Args:
        word1 (Dict): 확인할 첫 번째 단어의 bbox 정보
        word2 (Dict): 확인할 두 번째 단어의 bbox 정보
        threshold (float): 비슷한 줄에 위치하는지의 기준

    Returns:
        bool: 기준 통과 여부
    """

    word1_start_y = word1["points"][0][1]
    word2_start_y = word2["points"][0][1]
    y_gap = abs(word1_start_y - word2_start_y)

    word1_text_height = abs(word1["points"][0][1] - word1["points"][2][1])
    word2_text_height = abs(word2["points"][0][1] - word2["points"][2][1])
    text_height = min(word1_text_height, word2_text_height)

    if y_gap <= text_height * threshold:  # 기준 설정 필요
        return True
    else:
        return False


def check_slope(word1: Dict, word2: Dict, threshold: float) -> bool:
    """
    두 단어 사이의 간격에 대해, 기울기 확인

    가로의 길이가 가중치처럼 반영되도록 하기 위함
    => 두 단어 사이의 간격이 좁을수록 높이 비율을 엄격하게 적용
    ex. 두 단어 사이가 가까울 수록, 높이 비율의 차이가 크면 기울기는 급격하게 커짐

    Args:
        word1 (Dict): 확인할 첫 번째 단어의 bbox 정보
        word2 (Dict): 확인할 두 번째 단어의 bbox 정보
        threshold (float): 두 단어 사이의 기울기 기준

    Returns:
        bool: 기준 통과 여부
    """

    word1_text_height = abs(word1["points"][0][1] - word1["points"][2][1])
    word2_text_height = abs(word2["points"][0][1] - word2["points"][2][1])

    height_gap = abs(word1_text_height - word2_text_height)
    width_gap = abs(word1["points"][1][0] - word2["points"][0][0])

    if height_gap / width_gap <= threshold:
        return True
    else:
        return False


def check_font_size(word1: Dict, word2: Dict, threshold: float) -> bool:
    """
    두 단어의 폰트 크기의 비율 확인

    Args:
        word1 (Dict): 확인할 첫 번째 단어의 bbox 정보
        word2 (Dict): 확인할 두 번째 단어의 bbox 정보
        threshold (float): 폰트 크기 비율의 기준

    Returns:
        bool: 기준 통과 여부
    """

    font_size_ratio = (
        font_width(word1) / font_width(word2)
        if font_width(word1) <= font_width(word2)
        else font_width(word2) / font_width(word1)
    )

    if font_size_ratio >= threshold:
        return True
    else:
        return False


###################################
###### font feature function ######
###################################


def font_width(word: Dict) -> float:
    """
    '폰트의 세로 길이 * 종횡비 = 폰트의 가로 길이'임을 이용하여,
    단어의 폰트 크기 계산
    ex. Verdana 폰트의 종횡비 : 0.58

    Args:
        word (Dict): 단어의 bbox 정보

    Returns:
        float: 단어의 폰트 크기
    """

    text_height = abs(word["points"][0][1] - word["points"][3][1])

    return text_height * 0.58  # 기준 설정 필요


def font_space(word1: Dict, word2: Dict) -> float:
    """
    '폰트의 세로 길이 * 0.3 = 폰트의 띄어쓰기'라고 가정하여,
    단어의 띄어쓰기 간격 계산

    Args:
        word1 (Dict): 첫 번째 단어의 bbox 정보
        word2 (Dict): 두 번째 단어의 bbox 정보

    Returns:
        float: 단어의 띄어쓰기 간격
    """

    word1_text_height = abs(word1["points"][0][1] - word1["points"][2][1])
    word2_text_height = abs(word2["points"][0][1] - word2["points"][2][1])

    return min(word1_text_height * 0.3, word2_text_height * 0.3)  # 곱하는 값 기준?


###########################
###### json function ######
###########################


def make_bbox(word1: Dict, word2: Dict) -> List:
    """
    두 단어의 bbox 정보를 토대로, 합친 후의 bbox 좌표 계산

    Args:
        word1 (Dict): 첫 번째 단어의 bbox 정보
        word2 (Dict): 두 번째 단어의 bbox 정보

    Returns:
        List: 두 단어를 합친 후의 bbox 좌표
    """

    start_x = word1["points"][0][0]
    start_y = min(word1["points"][0][1], word2["points"][0][1])
    end_x = word2["points"][1][0]
    end_y = max(word1["points"][3][1], word2["points"][3][1])

    return [[start_x, start_y], [end_x, start_y], [end_x, end_y], [start_x, end_y]]


##############################
###### parsing function ######
##############################

# 글자 단위로 합침 # 띄어쓰기 고려할 필요 없음 # 높이 고려할 필요 없음
def connect_character(words: List) -> List:
    """
    같은 단어에 포함되어야 하는 글자를 합쳐 줌

    '같은' 단어에 포함되어야 하므로,
    각 글자 사이의 간격만 고려하여 합침

    Args:
        words (List): json_data 정보를 담은 리스트

    Returns:
        List: 글자를 합친 과정 이후, json_data 정보를 담은 리스트
    """

    while True:
        for index in range(0, len(words) - 1):
            gap = abs(words[index + 1]["points"][0][0] - words[index]["points"][1][0])
            space = font_space(words[index], words[index + 1])

            if gap < space:
                words[index]["points"] = make_bbox(words[index], words[index + 1])
                words[index]["text"] += words[index + 1]["text"]

                del words[index + 1]
                break
        else:
            break

    return words


def delete_sep(words: List) -> List:
    """
    특수문자 한 글자만 존재할 경우 삭제

    Args:
        words (List): json_data 정보를 담은 리스트

    Returns:
        List: 특수문자 제거하는 과정 이후, json_data 정보를 담은 리스트
    """

    sep = "■:/|."
    while True:
        for index in range(0, len(words)):
            if words[index]["text"] in sep and len(words[index]["text"]) == 1:
                del words[index]
                break
        else:
            break

    return words


def connect_name_company(words: List) -> List:
    """
    이름/회사명이 간격이 넓게 한 글자씩 떨어져 있는 경우, 이를 합쳐줌
    단, 한 글자씩 곧바로 합치는 대신, 각 글자를 모아서 추후 한 번에 합쳐줌

    1) 이름/회사명에 해당하는지 확인
    2) 두 단어 사이의 간격의 기울기 확인
    3) 두 단어가 같은 줄에 위치하는지 확인
    4) 두 단어가 같은 폰트 크기인지 확인

    Args:
        words (List): json_data 정보를 담은 리스트

    Returns:
        List: 특수문자 제거하는 과정 이후, json_data 정보를 담은 리스트
    """

    while True:
        name = []
        for index in range(0, len(words) - 1):
            name_condition = (
                len(words[index]["text"]) == 1 and len(words[index + 1]["text"]) == 1
            )
            company_condition = (
                "(주)" in words[index]["text"] and len(words[index + 1]["text"]) == 1
            )

            if (
                (name_condition or company_condition)
                and check_slope(words[index], words[index + 1], 0.3)
                and check_y(words[index], words[index + 1], 0.2)
                and check_font_size(words[index], words[index + 1], 0.8)
            ):

                if [index, words[index]] not in name:
                    name.append([index, words[index]])

                if [index + 1, words[index + 1]] not in name:
                    name.append([index + 1, words[index + 1]])
            else:
                if name:
                    break

        if not name:
            break

        start_index = name[0][0]
        bbox_start, bbox_end = name[0][1], name[-1][1]
        name = name[::-1]
        text = ""

        for index, word in name[:-1]:
            text += word["text"]
            del words[index]
        text = text[::-1]
        text = name[-1][1]["text"] + text

        words[start_index]["text"] = text
        words[start_index]["points"] = make_bbox(bbox_start, bbox_end)

    return words


def connect_word(words: List) -> List:
    """
    같은 카테고리에 포함되어야 하는 두 단어를 합쳐 줌

    1) 두 단어 사이의 간격 <= 두 폰트 너비 크기의 평균
    2) 두 단어 사이의 간격의 기울기 확인
    3) 두 단어가 같은 줄에 위치하는지 확인
    4) 두 단어가 같은 폰트 크기인지 확인

    Args:
        words (List): json_data 정보를 담은 리스트

    Returns:
        List: 특수문자 제거하는 과정 이후, json_data 정보를 담은 리스트
    """

    while True:
        for index in range(0, len(words) - 1):
            gap = abs(words[index]["points"][1][0] - words[index + 1]["points"][0][0])

            if (
                gap <= (font_width(words[index]) + font_width(words[index + 1])) / 2
                and check_slope(words[index], words[index + 1], 0.3)
                and check_y(words[index], words[index + 1], 0.2)
                and check_font_size(words[index], words[index + 1], 0.8)
            ):
                words[index]["points"] = make_bbox(words[index], words[index + 1])
                words[index]["text"] += " " + words[index + 1]["text"]

                del words[index + 1]
                break
        else:
            break

    return words


############################
#### word2line function ####
############################


def word2line(json_data: Dict) -> Dict:
    """
    OCR API로부터 전달받은 bbox 정보를
    모델이 학습하기에 적합하도록 바꾸어 리턴

    Args:
        json_data (Dict): OCR API로부터 전달받은 bbox 정보

    Returns:
        Dict: word2line()을 거쳐 변경된 bbox 정보
    """
    
    words = sort_json(json_data)

    words = connect_character(words)
    words = delete_sep(words)
    words = connect_name_company(words)
    words = connect_word(words)

    json_result = {"ocr": {"word": words}}
    return json_result
