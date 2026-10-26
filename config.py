import os

from dotenv import load_dotenv

load_dotenv()


def _ids(raw: str) -> set[int]:
    return {int(part) for part in raw.replace(" ", "").split(",") if part}


BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
CHANNEL_URL = os.getenv("CHANNEL_URL", "").strip()
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID") or 0) or None
ADMIN_IDS = _ids(os.getenv("ADMIN_IDS", ""))
DB_PATH = os.getenv("DB_PATH", "leads.db")
