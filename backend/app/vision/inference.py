from __future__ import annotations

from typing import Any

import cv2
import numpy as np

from app.vision.cnn import SYMBOLS, predict_symbol
from app.vision.colors import dominant_color_names
from app.vision.ocr import read_text_from_image
from app.vision.symbols import dominant_colors, segment_symbols


def analyze_image(image: Any, model=None) -> dict[str, Any]:
    if isinstance(image, str):
        image_bgr = cv2.imread(image)
        if image_bgr is None:
            raise FileNotFoundError(f"Could not read image: {image}")
    else:
        image_bgr = np.asarray(image)
    symbol, confidence = predict_symbol(image_bgr, model=model)
    detected = segment_symbols(image_bgr)
    return {
        "symbol": symbol,
        "confidence": float(confidence),
        "bounding_boxes": detected[:5],
        "dominant_colors": dominant_color_names(image_bgr),
        "detected_text": read_text_from_image(image_bgr),
        "known_symbols": SYMBOLS,
    }
