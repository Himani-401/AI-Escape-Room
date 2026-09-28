from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image, ImageOps

from app.core.config import PROJECT_ROOT

MODEL_PATH = PROJECT_ROOT / "models" / "symbol_cnn.pt"
SYMBOLS = ["fire", "water", "moon", "sun", "key", "eye", "star", "triangle", "spiral", "skull", "leaf", "lock"]


class SymbolCNN(nn.Module):
    def __init__(self, num_classes: int = len(SYMBOLS)):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.fc1 = nn.Linear(64 * 28 * 28, 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        return self.fc2(x)


def preprocess_image_for_cnn(image: Any) -> torch.Tensor:
    if isinstance(image, str):
        img = Image.open(image).convert("L")
    else:
        img = Image.fromarray(np.asarray(image)).convert("L")
    img = ImageOps.fit(img, (224, 224), Image.Resampling.LANCZOS)
    arr = np.asarray(img, dtype=np.float32) / 255.0
    tensor = torch.from_numpy(arr).unsqueeze(0).unsqueeze(0)
    return tensor


def load_model(model_path: Path | str | None = None) -> SymbolCNN:
    path = Path(model_path) if model_path is not None else MODEL_PATH
    model = SymbolCNN()
    if path.exists():
        model.load_state_dict(torch.load(path, map_location="cpu"))
    else:
        model.eval()
    return model


def predict_symbol(image: Any, model: SymbolCNN | None = None) -> tuple[str, float]:
    model = model or load_model()
    tensor = preprocess_image_for_cnn(image)
    with torch.no_grad():
        logits = model(tensor)
        probs = torch.softmax(logits, dim=1)
        idx = int(probs.argmax(dim=1).item())
        conf = float(probs[0, idx].item())
    return SYMBOLS[idx], conf
