import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from config.config import *
from object.others.logger import logger

class save_load():
    def __init__(self, file="player.json"):
        self.file = file

    def save_data(data=False, file="player.json"):
        if data!=False:
            with open(f'{ROOT}/config/{file}', 'w', encoding='utf-8') as fichier_json:
                json.dump(data, fichier_json, indent=4, ensure_ascii=False)
        else:
            logger.info(f"Data Erreur : {data}")
            return False
    
    def load_data(file="player.json"):
        with open(f'{ROOT}/config/accounts/{file}', 'r', encoding='utf-8') as data:
            return json.load(data)
