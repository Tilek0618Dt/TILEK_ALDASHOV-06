import uuid
from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import select

from app.db import SessionLocal
from app.models import User, Invoice
from app.constants import PLANS, VIP_VIDEO_PACKS, VIP_MUSIC_PACKS_MINUTES
from app.services.cryptomus import create_invoice
from app.config import PUBLIC_BASE_URL

router = Router()

async def _mk_invoice(call: CallbackQuery, kind: str, amount: float) -> str:
    order_id = f"{kind}-{call.from_user.id}-{uuid.uuid4().hex[:10]}"
    callback_url = f"{PUBLIC_BASE_URL}/cryptomus/webhook"
    data = await create_invoice(amount, order_id, callback_url)

    # cryptomus жооп структурасы ар кандай болушу мүмкүн; көбүнчө result.url бар
    pay_url = None
    if isinstance(data, dict):
        pay_url = (data.get("result") or {}).get("url") or (data.get("result") or {}).get("pay_url")

    async with SessionLocal() as s:
        inv = Invoice(order_id=order_id, tg_id=call.from_user.id, kind=kind, amount_usd=amount, payment_url=pay_url)
        s.add(inv)
        await s.commit()

    return pay_url or "⚠️ payment_url табылган жок (Cryptomus response өзгөргөн болушу мүмкүн)."

@router.callback_query(F.data.startswith("buy:plan:"))
async def buy_plan(call: CallbackQuery):
    plan_code = call.data.split(":")[2]
    plan = PLANS[plan_code]
    pay_url = await _mk_invoice(call, f"PLAN_{plan_code}", plan.price_usd)

    await call.message.answer(
        f"💳 {plan.title} сатып алуу\n\n"
        f"Баа: ${plan.price_usd:.2f}\n"
        f"Төлөм линк: {pay_url}\n\n"
        "Төлөгөндөн кийин автомат актив болот 😎",
        disable_web_page_preview=True
    )
    await call.answer()

@router.callback_query(F.data.startswith("buy:vip_video:"))
async def buy_vip_video(call: CallbackQuery):
    n = int(call.data.split(":")[2])
    amount = VIP_VIDEO_PACKS[n]
    pay_url = await _mk_invoice(call, f"VIP_VIDEO_{n}", amount)
    await call.message.answer(f"🎥 VIP VIDEO пакет: {n}\nБаа: ${amount:.2f}\nЛинк: {pay_url}", disable_web_page_preview=True)
    await call.answer()

@router.callback_query(F.data.startswith("buy:vip_music:"))
async def buy_vip_music(call: CallbackQuery):
    minutes = int(call.data.split(":")[2])
    amount = VIP_MUSIC_PACKS_MINUTES[minutes]
    pay_url = await _mk_invoice(call, f"VIP_MUSIC_{minutes}", amount)
    await call.message.answer(f"🪉 VIP MUSIC: {minutes} мин\nБаа: ${amount:.2f}\nЛинк: {pay_url}", disable_web_page_preview=True)
    await call.answer()
