import json
import os
from ..config import config
from ..services.logger import logger

mastersuite = {}

def _load_split(fileName):
    global mastersuite
    with open(f"suitemasterfile/{fileName}", "r") as f:
        j = json.load(f)
        mastersuite = {
            **mastersuite,
            **j
        }

def _load_suite():
    for fileName in os.listdir('suitemasterfile'):
        _load_split(fileName)
        logger.info(f"Loaded master file split {fileName}")
    logger.info("Loaded master file successfully.")

_load_suite()

def get_difficulty(difficulty_id: int):
    difficulty = next((diff for diff in mastersuite['musicDifficulties'] if diff['id'] == difficulty_id), None)
    return difficulty