from __future__ import annotations

import random
from pathlib import Path

import cv2
import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFilter

from app.vision.cnn import MODEL_PATH, SymbolCNN, SYMBOLS


def make_symbol_image(symbol: str, size: int = 224, rng: random.Random | None = None) -> np.ndarray:
    rng = rng or random.Random(42)
    image = Image.new("L", (size, size), 255)
    draw = ImageDraw.Draw(image)
    cx, cy = size // 2, size // 2
    radius = size * 0.32
    if symbol == "fire":
        points = [(cx, cy - radius), (cx + radius * 0.8, cy + radius), (cx - radius * 0.8, cy + radius)]
        draw.polygon(points, fill=0)
    elif symbol == "water":
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=0, width=12)
        draw.arc((cx - radius * 0.6, cy - radius * 0.6, cx + radius * 0.6, cy + radius * 0.6), 0, 180, fill=0, width=10)
    elif symbol == "moon":
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=0, width=10)
        draw.pieslice((cx - radius, cy - radius, cx + radius, cy + radius), 90, 270, fill=255)
    elif symbol == "sun":
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=0, width=10)
        for i in range(12):
            angle = i * 30
            x1 = cx + int((radius + 18) * np.cos(np.deg2rad(angle)))
            y1 = cy + int((radius + 18) * np.sin(np.deg2rad(angle)))
            x2 = cx + int((radius + 30) * np.cos(np.deg2rad(angle)))
            y2 = cy + int((radius + 30) * np.sin(np.deg2rad(angle)))
            draw.line((x1, y1, x2, y2), fill=0, width=4)
    elif symbol == "key":
        draw.arc((cx - radius, cy - radius, cx + radius, cy + radius), 190, 350, fill=0, width=10)
        draw.rectangle((cx + radius * 0.2, cy - radius * 0.2, cx + radius * 0.8, cy + radius * 0.8), outline=0, width=8)
        draw.line((cx + radius * 0.5, cy - radius * 0.5, cx + radius * 0.7, cy - radius * 0.9), fill=0, width=8)
    elif symbol == "eye":
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=0, width=8)
        draw.ellipse((cx - radius * 0.5, cy - radius * 0.5, cx + radius * 0.5, cy + radius * 0.5), fill=255)
        draw.ellipse((cx - radius * 0.15, cy - radius * 0.15, cx + radius * 0.15, cy + radius * 0.15), fill=0)
    elif symbol == "star":
        pts = []
        for i in range(10):
            angle = -np.pi/2 + i * (np.pi/5)
            dist = radius if i % 2 == 0 else radius * 0.5
            x = cx + dist * np.cos(angle)
            y = cy + dist * np.sin(angle)
            pts.append((int(x), int(y)))
        draw.polygon(pts, outline=0, width=8)
    elif symbol == "triangle":
        draw.polygon([(cx, cy - radius), (cx + radius, cy + radius), (cx - radius, cy + radius)], fill=0)
    elif symbol == "spiral":
        for r in range(20, 0, -10):
            draw.arc((cx - r, cy - r, cx + r, cy + r), 0, 270, fill=0, width=6)
    elif symbol == "skull":
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=0, width=8)
        draw.ellipse((cx - radius * 0.5, cy - radius * 0.8, cx - radius * 0.15, cy - radius * 0.3), fill=0)
        draw.ellipse((cx + radius * 0.15, cy - radius * 0.8, cx + radius * 0.5, cy - radius * 0.3), fill=0)
        draw.arc((cx - radius * 0.4, cy - radius * 0.1, cx + radius * 0.4, cy + radius * 0.5), 180, 360, fill=0, width=8)
    elif symbol == "leaf":
        draw.ellipse((cx - radius * 0.7, cy - radius * 0.7, cx + radius * 0.7, cy + radius * 0.7), outline=0, width=8)
        draw.line((cx, cy - radius, cx, cy + radius), fill=0, width=6)
    elif symbol == "lock":
        draw.rounded_rectangle((cx - radius * 0.7, cy - radius * 0.6, cx + radius * 0.7, cy + radius * 0.8), radius=18, outline=0, width=10)
        draw.ellipse((cx - radius * 0.18, cy - radius * 0.18, cx + radius * 0.18, cy + radius * 0.18), fill=0)

    image = image.rotate(rng.randint(-30, 30), expand=True)
    image = image.filter(ImageFilter.GaussianBlur(rng.uniform(0.0, 1.2)))
    image = image.resize((224, 224), Image.Resampling.BILINEAR)
    arr = np.asarray(image).astype(np.uint8)
    arr = cv2.GaussianBlur(arr, (3, 3), 0)
    return arr


def build_dataset(output_dir: Path, count_per_symbol: int = 100) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(42)
    for symbol in SYMBOLS:
        klass_dir = output_dir / symbol
        klass_dir.mkdir(parents=True, exist_ok=True)
        for idx in range(count_per_symbol):
            arr = make_symbol_image(symbol, rng=rng)
            image_path = klass_dir / f"{idx}.png"
            Image.fromarray(arr).save(image_path)


def train_model(data_dir: Path, epochs: int = 4) -> None:
    device = torch.device("cpu")
    model = SymbolCNN().to(device)
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    xs, ys = [], []
    for klass_idx, symbol in enumerate(SYMBOLS):
        for image_path in sorted((data_dir / symbol).glob("*.png")):
            img = Image.open(image_path).convert("L")
            arr = np.asarray(img, dtype=np.float32) / 255.0
            xs.append(arr)
            ys.append(klass_idx)
    dataset = [(torch.tensor(x).unsqueeze(0).unsqueeze(0), torch.tensor(y)) for x, y in zip(xs, ys)]
    for _ in range(epochs):
        model.train()
        for x, y in dataset:
            optimizer.zero_grad()
            logits = model(x.to(device))
            loss = criterion(logits, y.unsqueeze(0).to(device))
            loss.backward()
            optimizer.step()
    torch.save(model.state_dict(), MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    dataset_dir = Path(__file__).resolve().parents[1] / "data" / "symbol_dataset"
    build_dataset(dataset_dir)
    train_model(dataset_dir)
