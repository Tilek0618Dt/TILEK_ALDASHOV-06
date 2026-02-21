from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select

from app.db import SessionLocal
from app.models import User

router = Router()

@router.callback_query(F.data == "m:video")
async def video_entry(call: CallbackQuery):
    await call.message.answer("🎥 Досум, видео үчүн тема жаз:\nМисал: *ат минген адам, кыргыз тоолору, кино стил эмес* 😎")
    await call.answer()

@router.callback_query(F.data == "m:music")
async def music_entry(call: CallbackQuery):
    await call.message.answer("🪉 Досум, музыка үчүн тема жаз:\nМисал: *романтик эмес, бизнес мотивация beats* 😈")
    await call.answer()

# Бул жерде сен өзүң /video жана /music command кылып кеңейтсең болот.
# Азыр UX skeleton: VIP кредит болсо — иштет, болбосо Premium/VIP сунуш.
