from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keyboards import kb_main, kb_premium, kb_vip_video, kb_vip_music

router = Router()

@router.callback_query(F.data == "m:back")
async def back(call: CallbackQuery):
    await call.message.edit_text("🏠 Башкы меню:", reply_markup=kb_main())
    await call.answer()

@router.callback_query(F.data == "m:premium")
async def premium(call: CallbackQuery):
    await call.message.edit_text("💎 Премиум пландарды танда, досум 😎", reply_markup=kb_premium())
    await call.answer()

@router.callback_query(F.data == "m:vip_video")
async def vip_video(call: CallbackQuery):
    await call.message.edit_text("🎥 VIP VIDEO пакет танда:", reply_markup=kb_vip_video())
    await call.answer()

@router.callback_query(F.data == "m:vip_music")
async def vip_music(call: CallbackQuery):
    await call.message.edit_text("🪉 VIP MUSIC минут пакет танда:", reply_markup=kb_vip_music())
    await call.answer()
