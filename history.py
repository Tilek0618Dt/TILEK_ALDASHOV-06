from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data == "m:history")
async def history(call: CallbackQuery):
    text = (
        "😎 Tilek ким?\n\n"
        "Tilek — сенин Telegram’деги AI досуң:\n"
        "😂 2 сүйлөм күлдүрөт\n"
        "😈 1 сүйлөм “катуу” кылат\n"
        "🧠 Анан мээңди ойготот\n\n"
        "💡 Факт: Tilek — “акча эмес, система” деп үйрөтөт.\n"
        "🔥 Максат: сени күчтөндүрүү + ишиңди жеңилдетүү.\n\n"
        "Досум, суроо бер — көрөсүң 😎🤲🏻"
    )
    await call.message.answer(text)
    await call.answer()
