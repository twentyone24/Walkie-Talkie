import os
from dotenv import load_dotenv

SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SETTINGS_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'DataModels')

# Discord Conf
TOKEN = os.getenv("DISCORD_TOKEN", False)
