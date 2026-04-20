import json
from pathlib import Path
from cryptography.fernet import Fernet
from config.config import *
from object.others.logger import logger

SECRET_KEY = b'r-h6ZS1saE2ecNk_dw4_-mFmHDSeMerH_r9XmXWTp-M='
cipher = Fernet(SECRET_KEY)

class save_load():
    def __init__(self, file):
        self.file = file

    def save_data(file, data=False):
        if data != False:
            content = json.dumps(data, indent=4, ensure_ascii=False).encode()
            encrypted = cipher.encrypt(content)
            with open(ACCOUNT_LOCATION / f'{file}', 'wb') as f:  # ← 'wb' binaire
                f.write(encrypted)
        else:
            logger.info(f"Data Erreur : {data}")
            return False

    def load_data(file):
        with open(ACCOUNT_LOCATION / f'{file}', 'rb') as f:  # ← 'rb' binaire
            encrypted = f.read()
        content = cipher.decrypt(encrypted)
        return json.loads(content.decode())

    def build_data(file, pseudo="null", money=-1, inventory=None):
        if inventory is None:
            inventory = {"energy": 1, "pression": 1}
        return {"pseudo": pseudo, "money": money, "inventory": inventory}