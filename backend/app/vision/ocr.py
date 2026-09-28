from __future__ import annotations

from typing import List

import cv2
import numpy as np
import pytesseract


def read_text_from_image(image: np.ndarray) -> List[str]:
    try:
        text = pytesseract.image_to_string(image)
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return lines
    except Exception:
        return []


def find_ocr_regions(image: np.ndarray) -> list[tuple[int, int, int, int]]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h > 120:
            boxes.append((x, y, w, h))
    return boxes
