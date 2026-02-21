from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import select

from app.db import SessionLocal
from app.models import User
from app.config import CHANNEL_URL

router = Router()

@router.callback_query(F.data == "m:ref")
async def ref(call: CallbackQuery):
    async with SessionLocal() as s:
        res = await s.execute(select(User).where(User.tg_id == call.from_user.id))
        u = res.scalar_one()

    link = f"https://t.me/{call.bot.username}?start={call.from_user.id}"
    text = (
        "🎁 Реферал\n\n"
        f"Сенин ссылкаң:\n{link}\n\n"
        f"Баланс: ${u.ref_balance_usd:.2f}\n\n"
        "Эреже:\n"
        "✅ Досуң PLUS сатып алса → $3 баланс\n"
        "✅ Досуң $5+ төлөсө → 7 күн PLUS бекер\n"
        "❌ PRO бекер берилбейт (банкрот болбойлу 😅)\n\n"
        f"Канал: {CHANNEL_URL}"
    )
    await call.message.answer(text, disable_web_page_preview=True)
    await call.answer()
