import datetime as dt
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select

from app.db import SessionLocal
from app.models import User
from app.constants import FREE_DAILY_QUESTIONS, BLOCK_HOURS_FREE
from app.style_engine import tilek_wrap, limit_ad_text
from app.services.grok import grok_chat

router = Router()

async def _load_user(tg_id: int) -> User:
    async with SessionLocal() as s:
        res = await s.execute(select(User).where(User.tg_id == tg_id))
        return res.scalar_one()

@router.callback_query(F.data == "m:chat")
async def ask_chat(call: CallbackQuery):
    await call.message.answer("✍️ Досум, сурооңду жазчы (чатка жибер) 😎")
    await call.answer()

@router.message(F.text)
async def on_text(message: Message):
    async with SessionLocal() as s:
        res = await s.execute(select(User).where(User.tg_id == message.from_user.id))
        u = res.scalar_one_or_none()
        if not u:
            # /start баспай туруп жазса — түзөбүз
            u = User(tg_id=message.from_user.id, username=message.from_user.username)
            s.add(u)
            await s.commit()
            await s.refresh(u)

        now = dt.datetime.utcnow()

        # блок текшерүү
        if u.blocked_until and now < u.blocked_until:
            left = int((u.blocked_until - now).total_seconds() // 60)
            await message.answer(f"⛔ Досум, FREE блок активдүү 😭\nКалганы: {left} мүнөт\n\n{limit_ad_text()}")
            return

        # PREMIUM monthly chat
        if u.plan in ("PLUS", "PRO"):
            if u.chat_left <= 0:
                await message.answer("🚫 Айлык чат лимит бүттү 😭\nКийинки reset 30 күндө.\n\n💎 VIP пакеттер лимитке кирбейт 😎")
                return
            u.chat_left -= 1
            is_pro = (u.plan == "PRO")
        else:
            # FREE daily
            if u.free_today_count >= FREE_DAILY_QUESTIONS:
                u.blocked_until = now + dt.timedelta(hours=BLOCK_HOURS_FREE)
                await s.commit()
                await message.answer(limit_ad_text())
                return
            u.free_today_count += 1
            is_pro = False

        # AI жооп
        ai = await grok_chat(message.text, lang=u.language or "ky", is_pro=is_pro)
        styled = tilek_wrap(u, ai)

        await s.commit()
        await message.answer(styled)
