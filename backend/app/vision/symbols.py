from __future__ import annotations

import cv2
import numpy as np


def segment_symbols(image: np.ndarray) -> list[dict]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    symbols = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 100:
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        symbols.append({"bbox": [x, y, w, h], "area": float(area)})
    return symbols


def dominant_colors(image: np.ndarray, k: int = 3) -> list[str]:
    if image.ndim == 3:
        pixels = image.reshape((-1, 3))
    else:
        pixels = np.stack([image] * 3, axis=-1).reshape((-1, 3))
    pixels = np.float32(pixels)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    colors = []
    for center in centers:
        b, g, r = map(int, center)
        colors.append(f"rgb({r},{g},{b})")
    return colors


def detect_symbol_shape(image: np.ndarray) -> dict:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return {"shape": "unknown", "confidence": 0.0}
    largest = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest)
    perimeter = cv2.arcLength(largest, True)
    if perimeter > 0:
        circularity = 4 * np.pi * area / (perimeter * perimeter)
    else:
        circularity = 0.0
    if circularity > 0.7:
        shape = "circle"
    elif area > 0 and gray.shape[0] > 0 and gray.shape[1] > 0:
        shape = "polygon"
    else:
        shape = "unknown"
    return {"shape": shape, "confidence": float(min(max(circularity, 0.0), 1.0))}
