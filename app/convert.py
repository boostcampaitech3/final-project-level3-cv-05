import cv2
import numpy as np
import io
import math
from scipy import ndimage

def reorder(points):
    left = points[points[:,0].argsort(axis=0)][:2]
    left = left[left[:, 1].argsort(axis=0)]
    right = points[points[:,0].argsort(axis=0)][2:]
    right = right[right[:, 1].argsort(axis=0)][::-1]
    concat = np.concatenate((left, right))
    width = abs(concat[0][0] - concat[2][0])
    height = abs(concat[0][1] - concat[1][1])
    return concat, (width, height)


def biggestContour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 5000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest.squeeze(), max_area


def angleFix(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)
    angles = []
    if len(lines) > 1:
        for [[x1, y1, x2, y2]] in lines:
            angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
            angles.append(angle)
        median_angle = np.median(angles)
    else:
        median_angle = 0
    img_rotated = ndimage.rotate(image, median_angle)
    return img_rotated


def converter(tmpFile, value):
    threshold, invert, angle = value
    bytes_data = tmpFile.read()
    src = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    if angle:
        pass
    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    method = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
    if threshold == -1:
        _, src_bin = cv2.threshold(src_gray, 0, 255, method|cv2.THRESH_OTSU)
    else:
        _, src_bin = cv2.threshold(src_gray, threshold, 255, method)
    contours, _ = cv2.findContours(src_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    biggest, max_area = biggestContour(contours)
    if len(biggest) > 0 and max_area < src.shape[0] * src.shape[1] * 0.9:
        reordered, (width, height) = reorder(biggest)
        srcQuad = np.array(reordered).astype(np.float32)
        dstQuad = np.array([
            [
            [0, 0],
            [0, height],
            [width, height],
            [width, 0],
            ]]).astype(np.float32)
        pers = cv2.getPerspectiveTransform(srcQuad, dstQuad)
        dst = cv2.warpPerspective(src, pers, (width, height))
        bytes_data = cv2.imencode('.jpg', dst)[1].tobytes()
    else:
        anglefixed = angleFix(src)
        bytes_data = cv2.imencode('.jpg', anglefixed)[1].tobytes()

    bytesImage = io.BytesIO(bytes_data)
    
    return bytesImage


if __name__ == "__main__":
    pass