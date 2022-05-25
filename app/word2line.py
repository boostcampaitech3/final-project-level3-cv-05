from typing import Dict, List, Tuple, Any, Union

import cv2
import numpy as np


def tup(point):
    return point[0], point[1]


# returns true if the two boxes overlap
def overlap(source: Union[List, Tuple], target: Dict, ratio: float = 0.6) -> bool:
    tl1, br1 = source
    tl2, br2 = target["points"][0], target["points"][2]

    source_height = br1[1] - tl1[1]
    target_height = br2[1] - tl2[1]
    if min(source_height / target_height, target_height / source_height) < ratio:
        return False

    # checks
    if tl1[0] >= br2[0] or tl2[0] >= br1[0]:
        return False
    if tl1[1] >= br2[1] or tl2[1] >= br1[1]:
        return False
    return True


# returns all overlapping boxes
def get_all_over_laps(boxes, bounds, index):
    overlaps = []
    for a in range(len(boxes)):
        if a != index:
            if overlap(bounds, boxes[a]):
                overlaps.append(a)
    return overlaps


# copy mutable list
def get2points(data: Dict) -> Tuple:
    return data['points'][0].copy(), data['points'][2].copy()


def word2line(ocr_words: Dict) -> Dict:
    words = ocr_words['ocr']['word']
    words.sort(key=lambda word: word['points'][3])
    finished = False
    while not finished:
        # set end con
        finished = True

        # loop through boxes
        index = 0
        while index < len(words):
            # grab current box
            curr = words[index]

            tl, br = get2points(curr)

            # set merge_margin
            merge_margin = br[1] - tl[1]
            br[0] += round(merge_margin * 1.5)

            # get matching boxes
            overlaps = get_all_over_laps(words, [tl, br], index);
            # check if empty
            if len(overlaps) > 0:
                # combine boxes
                # convert to a contour
                tl, br = curr["points"][0], curr["points"][2]
                con = [[tl], [br]]
                text = [curr['text']]
                for ind in overlaps:
                    tl, br = get2points(words[ind])
                    text.append(words[ind]['text'])
                    con.append([tl])
                    con.append([br])
                con = np.array(con)
                overlaps.append(index)
                # get bounding rect
                x, y, w, h = cv2.boundingRect(con)

                # stop growing
                w -= 1
                h -= 1
                # highlights
                merged_data = {
                    'points': [[x, y], [x + w, y], [x + w, y + h], [x, y + h]],
                    'orientation': curr['orientation'],
                    'text': " ".join(text)
                }
                # remove boxes from list
                overlaps.sort(reverse=True)
                for ind in overlaps:
                    del words[ind]
                words.append(merged_data)

                # set flag
                finished = False;
                break

            # increment
            index += 1
    ocr_words['ocr']['word'] = words
    return ocr_words
