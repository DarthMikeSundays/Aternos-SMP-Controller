import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
ATERNOS_ACCOUNT = {
    "password": os.getenv("ATERNOS_ACCOUNT_PASSWORD"),
    "username": os.getenv("ATERNOS_ACCOUNT_USERNAME")
}
