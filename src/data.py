import json5 as json
from typing import Any
from pydantic import BaseModel


class VocalData(BaseModel):
    musicId: int
    vocals: list[int]


class GameData(BaseModel):
    initialPlayerName: str
    initialFreeCards: list[int] = []
    initialMusics: list[int] = []
    initialMusicsVocals: list[VocalData] = []
    initialStamps: list[int] = []
    initialAvailableCostumes: list[int] = []
    initialSaleCostumes: list[int] = []
    userHomeBanners: list = []


def load_data(path: str = "./data.jsonc") -> GameData:
    with open(path, "r") as f:
        data = json.load(f)
    return GameData(**data)

# Only load data if the file exists and is not empty
try:
    game_data = load_data()
except (FileNotFoundError, json.JSONDecodeError):
    print("\033[31mInvalid or missing data.jsonc\033[0m")
    exit(-1)