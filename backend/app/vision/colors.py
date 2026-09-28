from __future__ import annotations

import colorsys
from typing import List

import cv2
import numpy as np


def convert_rgb_to_name(r: int, g: int, b: int) -> str:
    named = {
        "red": (255, 0, 0),
        "blue": (0, 0, 255),
        "green": (0, 128, 0),
        "yellow": (255, 255, 0),
        "orange": (255, 165, 0),
        "purple": (128, 0, 128),
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "gold": (218, 165, 32),
        "silver": (192, 192, 192),
    }
    best = "unknown"
    best_distance = 999999
    for name, rgb in named.items():
        distance = abs(r - rgb[0]) + abs(g - rgb[1]) + abs(b - rgb[2])
        if distance < best_distance:
            best_distance = distance
            best = name
    return best


def dominant_color_names(image: np.ndarray) -> List[str]:
    if image.ndim == 3:
        pixels = image.reshape((-1, 3))
    else:
        pixels = np.repeat(image[:, :, None], 3, axis=2).reshape((-1, 3))
    colors = []
    for pixel in pixels:
        r, g, b = pixel.astype(int)
        colors.append(convert_rgb_to_name(r, g, b))
    counts = {}
    for color in colors:
        counts[color] = counts.get(color, 0) + 1
    return sorted(counts, key=counts.get, reverse=True)[:3]
