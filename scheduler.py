import datetime as dt
from sqlalchemy import select
from app.db import SessionLocal
from app.models import User
from app.utils import day_key_utc
from app.constants import PLANS

async def ensure_resets():
    """
    - FREE daily reset (UTC day key)
    - Monthly reset every 30 days for PLUS/PRO (plan limits refill)
    """
    now = dt.datetime.utcnow()
    today_key = day_key_utc()

    async with SessionLocal() as s:
        res = await s.execute(select(User))
        users = res.scalars().all()

        for u in users:
            # daily reset for free counter
            if u.free_day_key != today_key:
                u.free_day_key = today_key
                u.free_today_count = 0

            # unblock if time passed
            if u.blocked_until and now >= u.blocked_until:
                u.blocked_until = None

            # monthly refill if 30 days passed
            if (now - u.last_monthly_reset).days >= 30:
                if u.plan in ("PLUS", "PRO"):
                    p = PLANS[u.plan]
                    u.chat_left = p.monthly_chat
                    u.video_left = p.monthly_video
                    u.music_left = p.monthly_music
                    u.image_left = p.monthly_image
                    u.voice_left = p.monthly_voice
                    u.doc_left = p.monthly_doc
                u.last_monthly_reset = now

        await s.commit()
