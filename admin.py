from aiogram import Router
from aiogram.types import Message
from sqlalchemy import select, func

from app.config import ADMIN_IDS
from app.db import SessionLocal
from app.models import User, Invoice

router = Router()

def _is_admin(tg_id: int) -> bool:
    return tg_id in ADMIN_IDS

@router.message(lambda m: m.text and m.text.startswith("/stats"))
async def stats(message: Message):
    if not _is_admin(message.from_user.id):
        return
    async with SessionLocal() as s:
        total_users = (await s.execute(select(func.count(User.id)))).scalar_one()
        paid = (await s.execute(select(func.count(Invoice.id)).where(Invoice.status == "paid"))).scalar_one()
    await message.answer(f"📊 Users: {total_users}\n✅ Paid invoices: {paid}")
