from dataclasses import dataclass

BLOCK_HOURS_FREE = 6
FREE_DAILY_QUESTIONS = 10  # FREE: күнүнө 10 суроо
REF_BONUS_USD = 3.0
REF_FREE_PLUS_DAYS = 7
REF_FREE_PLUS_MIN_PAID_USD = 5.0  # $5+ болсо 7 күн PLUS

@dataclass(frozen=True)
class Plan:
    code: str
    title: str
    price_usd: float
    monthly_chat: int
    monthly_video: int
    monthly_music: int
    monthly_image: int
    monthly_voice: int
    monthly_doc: int

PLANS = {
    "FREE": Plan("FREE", "FREE", 0.0, 0, 0, 0, 0, 0, 0),
    "PLUS": Plan("PLUS", "PLUS", 12.0, 750, 3, 3, 15, 5, 5),
    "PRO":  Plan("PRO",  "PRO",  28.0, 1500, 6, 3, 30, 15, 15),
}

VIP_VIDEO_PACKS = {1: 14.99, 3: 35.99, 5: 55.99}
VIP_MUSIC_PACKS_MINUTES = {1: 14.99, 3: 29.99, 5: 49.99}  # минуталык пакет
