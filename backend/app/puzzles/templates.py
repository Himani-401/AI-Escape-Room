from __future__ import annotations

from typing import Dict, List

PUZZLE_TEMPLATES = {
    "symbol_sequence": {
        "title": "Lantern Lock",
        "prompt": "The lock hums softly. Arrange the symbols in the order that keeps the room from falling into darkness: fire, water, moon, sun.",
        "answer": "fire, water, moon, sun",
        "hint_templates": [
            "Think about the cycle of the day and the life it protects.",
            "The clues move from heat to calm, then to night and day.",
            "The first symbol is warmth, then flow, then the night watcher, then the day star."
        ],
        "type": "symbol_sequence"
    },
    "riddle_map": {
        "title": "The Whispering Note",
        "prompt": "I am the hidden eye that watches every move. I am not a flame, but I glow in the dark. Which symbol matches my riddle?",
        "answer": "moon",
        "hint_templates": [
            "The symbol is a quiet watcher of the night.",
            "It is not the sun, and it is not a flame.",
            "Picture the pale traveler in the empty sky."
        ],
        "type": "riddle_map"
    },
    "color_order": {
        "title": "The Prism Vault",
        "prompt": "Choose the color order that unlocks the vault: red, blue, gold, green.",
        "answer": "red, blue, gold, green",
        "hint_templates": [
            "The first color is the danger signal.",
            "The second is the cool breath of the sea.",
            "The third is treasure, and the fourth is growth."
        ],
        "type": "color_order"
    },
    "cipher": {
        "title": "The Shifted Script",
        "prompt": "The basilisk's secret reads: 'JXQKJ' after Caesar shift +1. What word is hidden?",
        "answer": "iviii",
        "hint_templates": [
            "It is a word from the room, not a number.",
            "Shift back one letter at a time.",
            "The original text is a small object that opens things."
        ],
        "type": "cipher"
    }
}

SYMBOLS = ["fire", "water", "moon", "sun", "key", "eye", "star", "triangle", "spiral", "skull", "leaf", "lock"]


def build_default_templates() -> List[Dict[str, object]]:
    return [
        {
            "id": "puzzle_a",
            "title": "Lantern Lock",
            "type": "symbol_sequence",
            "prompt": "The lock hums softly. Arrange the symbols in the order that keeps the room from falling into darkness: fire, water, moon, sun.",
            "answer": "fire, water, moon, sun",
            "hint_templates": [
                "The order follows the cycle of survival.",
                "Start with heat, then flow, then night, then day.",
                "The path is warmth, rain, moonlight, sunlight."
            ],
            "depends_on": [],
            "unlocks": ["puzzle_b"],
        },
        {
            "id": "puzzle_b",
            "title": "Whispering Note",
            "type": "riddle_map",
            "prompt": "I am the hidden eye that watches every move. I am not a flame, but I glow in the dark. Which symbol matches my riddle?",
            "answer": "moon",
            "hint_templates": [
                "It is a quiet watcher in the sky.",
                "It reflects light and rules the night.",
                "A pale disc is your answer."
            ],
            "depends_on": ["puzzle_a"],
            "unlocks": ["puzzle_c"],
        },
        {
            "id": "puzzle_c",
            "title": "Prism Vault",
            "type": "color_order",
            "prompt": "Choose the color order that unlocks the vault: red, blue, gold, green.",
            "answer": "red, blue, gold, green",
            "hint_templates": [
                "The first color is danger and the second is the sea.",
                "The third reflects the treasure room.",
                "The fourth is the color of growth."
            ],
            "depends_on": ["puzzle_b"],
            "unlocks": ["puzzle_d"],
        },
        {
            "id": "puzzle_d",
            "title": "Shifted Script",
            "type": "cipher",
            "prompt": "The script reads: 'JXQKJ' after Caesar shift +1. What word is hidden?",
            "answer": "iviii",
            "hint_templates": [
                "It is a word from the room, not a number.",
                "Shift one letter backward to decode it.",
                "The answer is a small object with metal teeth."
            ],
            "depends_on": ["puzzle_c"],
            "unlocks": ["puzzle_e"],
        },
        {
            "id": "puzzle_e",
            "title": "Final Symbol Gate",
            "type": "symbol_sequence",
            "prompt": "The final gate asks for the triumvirate: key, eye, star.",
            "answer": "key, eye, star",
            "hint_templates": [
                "One symbol opens, one sees, one guides.",
                "The sequence follows trust, awareness, and guidance.",
                "Remember the objects that release a room and guide astral travelers."
            ],
            "depends_on": ["puzzle_d"],
            "unlocks": [],
        },
    ]
