from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.config import SUPPORT_ADMINS

router = Router()

@router.callback_query(F.data == "m:support")
async def support(call: CallbackQuery):
    admins = "\n".join([f"• {a}" for a in SUPPORT_ADMINS]) if SUPPORT_ADMINS else "• (админдер кошула элек 😅)"
    text = (
        "🆘 Жардам\n\n"
        "Досум, кыскача жазып жибер:\n"
        "1) Маселе эмне?\n"
        "2) Скрин болсо кош\n\n"
        "Админдер:\n"
        f"{admins}\n\n"
        "✅ Админ 2+ бар, жооп келет ✊🏻"
    )
    await call.message.answer(text)
    await call.answer()
