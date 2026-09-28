from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import create_session
from app.puzzles.generator import generate_puzzle_graph
from app.vision.inference import analyze_image


def run_demo() -> None:
    puzzles = generate_puzzle_graph(seed=42, count=5)
    print("Generated puzzle graph:", [p["id"] for p in puzzles])
    sample = Path(__file__).resolve().parents[1] / "data" / "sample_clues" / "00_fire.png"
    if sample.exists():
        result = analyze_image(str(sample))
        print("Symbol inference:", result["symbol"], result["confidence"])
    print("Demo complete: offline inference and puzzle generation succeeded.")


if __name__ == "__main__":
    run_demo()
