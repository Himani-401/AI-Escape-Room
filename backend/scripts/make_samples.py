from __future__ import annotations

import base64
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

OUT_DIR = Path(__file__).resolve().parents[1] / "data" / "sample_clues"
SYMBOLS = ["fire", "water", "moon", "sun", "key", "eye", "star", "triangle", "spiral", "skull", "leaf", "lock"]


def draw_symbol(symbol: str, size: int = 512):
    image = Image.new("RGB", (size, size), (18, 21, 30))
    draw = ImageDraw.Draw(image)
    cx, cy = size // 2, size // 2
    r = size * 0.28
    if symbol == "fire":
        draw.polygon([(cx, cy - r), (cx + r * 0.9, cy + r), (cx - r * 0.9, cy + r)], fill=(255, 90, 60))
    elif symbol == "water":
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(70, 130, 255), width=10)
        draw.arc((cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.7), 0, 180, fill=(70, 130, 255), width=8)
    elif symbol == "moon":
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(220, 220, 255))
        draw.pieslice((cx - r, cy - r, cx + r, cy + r), 90, 270, fill=(18, 21, 30))
    elif symbol == "sun":
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 210, 70))
        for fi in range(12):
            ang = fi * 30
            x1 = cx + int((r + 20) * np.cos(np.deg2rad(ang)))
            y1 = cy + int((r + 20) * np.sin(np.deg2rad(ang)))
            x2 = cx + int((r + 40) * np.cos(np.deg2rad(ang)))
            y2 = cy + int((r + 40) * np.sin(np.deg2rad(ang)))
            draw.line((x1, y1, x2, y2), fill=(255, 165, 0), width=5)
    elif symbol == "key":
        draw.arc((cx - r, cy - r, cx + r, cy + r), 210, 360, fill=(240, 215, 150), width=10)
        draw.rectangle((cx + r * 0.2, cy - r * 0.2, cx + r * 0.8, cy + r * 0.8), outline=(240, 215, 150), width=8)
    elif symbol == "eye":
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(160, 220, 255), width=8)
        draw.ellipse((cx - r * 0.5, cy - r * 0.5, cx + r * 0.5, cy + r * 0.5), fill=(160, 220, 255))
        draw.ellipse((cx - r * 0.15, cy - r * 0.15, cx + r * 0.15, cy + r * 0.15), fill=(18, 21, 30))
    elif symbol == "star":
        coords = []
        for i in range(10):
            ang = -np.pi / 2 + i * (np.pi / 5)
            dist = r if i % 2 == 0 else r * 0.45
            coords.append((cx + int(dist * np.cos(ang)), cy + int(dist * np.sin(ang))))
        draw.polygon(coords, fill=(255, 215, 90), outline=(255, 255, 200), width=4)
    elif symbol == "triangle":
        draw.polygon([(cx, cy - r), (cx + r, cy + r), (cx - r, cy + r)], fill=(200, 160, 255))
    elif symbol == "spiral":
        for rad in range(20, int(r), 25):
            draw.arc((cx - rad, cy - rad, cx + rad, cy + rad), 0, 270, fill=(160, 245, 180), width=5)
    elif symbol == "skull":
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(255, 140, 140), width=8)
        draw.ellipse((cx - r * 0.35, cy - r * 0.7, cx - r * 0.1, cy - r * 0.35), fill=(255, 140, 140))
        draw.ellipse((cx + r * 0.1, cy - r * 0.7, cx + r * 0.35, cy - r * 0.35), fill=(255, 140, 140))
        draw.arc((cx - r * 0.28, cy - r * 0.12, cx + r * 0.28, cy + r * 0.4), 180, 360, fill=(255, 140, 140), width=6)
    elif symbol == "leaf":
        draw.ellipse((cx - r * 0.85, cy - r * 0.6, cx + r * 0.85, cy + r * 0.6), outline=(120, 220, 150), width=8)
        draw.line((cx, cy - r, cx, cy + r), fill=(120, 220, 150), width=6)
    elif symbol == "lock":
        draw.rounded_rectangle((cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.8), radius=25, outline=(180, 210, 255), width=8)
        draw.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=(180, 210, 255))
    return image


def save_samples() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    for idx, symbol in enumerate(SYMBOLS):
        image = draw_symbol(symbol)
        path = OUT_DIR / f"{idx:02d}_{symbol}.png"
        image.save(path)
        manifest.append({"path": str(path), "symbol": symbol})
    with open(OUT_DIR / "manifest.json", "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    print(f"Created {len(manifest)} sample clue images in {OUT_DIR}")


if __name__ == "__main__":
    save_samples()
