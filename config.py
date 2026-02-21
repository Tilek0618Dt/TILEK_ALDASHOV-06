import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

GROK_API_KEY = os.getenv("GROK_API_KEY", "").strip()

CRYPTOMUS_API_KEY = os.getenv("CRYPTOMUS_API_KEY", "").strip()
CRYPTOMUS_MERCHANT_ID = os.getenv("CRYPTOMUS_MERCHANT_ID", "").strip()
CRYPTOMUS_WEBHOOK_SECRET = os.getenv("CRYPTOMUS_WEBHOOK_SECRET", "").strip()  # optional

REQUIRED_CHANNEL = os.getenv("REQUIRED_CHANNEL", "").strip()  # @channel OR -100id
CHANNEL_URL = os.getenv("CHANNEL_URL", "").strip()           # https://t.me/...

PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "").strip()   # https://xxx.onrender.com

ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()]
SUPPORT_ADMINS = [x.strip() for x in os.getenv("SUPPORT_ADMINS", "").split(",") if x.strip()]

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN жок, досум 😭")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL жок, досум 😭")
if not PUBLIC_BASE_URL:
    raise RuntimeError("PUBLIC_BASE_URL жок, webhook иштебей калат 😅")
