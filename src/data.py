import json5 as json
from typing import Any
from pydantic import BaseModel


class VocalData(BaseModel):
    musicId: int
    vocals: list[int]


class GameData(BaseModel):
    initialPlayerName: str
    initialFreeCards: list[int]
    initialMusics: list[int]
    initialMusicsVocals: list[VocalData] = []
    initialStamps: list[int] = []


def load_data(path: str = "./data.jsonc") -> GameData:
    with open(path, "r") as f:
        data = json.load(f)
    return GameData(**data)

# Only load data if the file exists and is not empty
try:
    game_data = load_data()
except (FileNotFoundError, json.JSONDecodeError):
    # Provide default values if data.json doesn't exist or is invalid
    game_data = GameData(
        initialPlayerName="SEKAI Player",
        initialFreeCards=[81, 89, 93, 97, 101, 105],
        initialMusics=[1, 2, 10, 26, 41, 50, 51, 54, 57, 60, 67, 76, 77, 82],
        initialMusicsVocals=[],
        initialStamps=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    )
