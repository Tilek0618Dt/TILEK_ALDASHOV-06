from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from app.db import SessionLocal
from app.models import User
from app.keyboards import kb_main
from app.utils import day_key_utc
from app.constants import PLANS
from app.data.countries import COUNTRIES, DEFAULT_LANG  # сенин 100+ файл

router = Router()

async def _get_or_create_user(tg_id: int, username: str | None, ref: int | None) -> User:
    async with SessionLocal() as s:
        res = await s.execute(select(User).where(User.tg_id == tg_id))
        u = res.scalar_one_or_none()
        if u:
            return u

        u = User(
            tg_id=tg_id,
            username=username,
            language=DEFAULT_LANG,
            plan="FREE",
            free_day_key=day_key_utc(),
        )
        if ref and ref != tg_id:
            u.referrer_tg_id = ref
        s.add(u)
        await s.commit()
        await s.refresh(u)
        return u

def _countries_page(page: int, per: int = 12):
    items = list(COUNTRIES.items())
    start = page * per
    return items[start:start+per], len(items)

@router.message(F.text.startswith("/start"))
async def start_cmd(message: Message):
    parts = message.text.split()
    ref = None
    if len(parts) > 1 and parts[1].isdigit():
        ref = int(parts[1])

    u = await _get_or_create_user(message.from_user.id, message.from_user.username, ref)

    # language select first time
    await message.answer("🌍 Досум, өлкөңдү танда! (100+) 😎")
    # show page 0
    await show_lang_page(message, page=0)

async def show_lang_page(message_or_call, page: int):
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    chunk, total = _countries_page(page)
    kb = []
    row = []
    for code, info in chunk:
        row.append(InlineKeyboardButton(text=f"{info['flag']} {info['name']}", callback_data=f"lang:{code}:{page}"))
        if len(row) == 2:
            kb.append(row); row = []
    if row: kb.append(row)

    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="⬅️", callback_data=f"langpage:{page-1}"))
    if (page+1)*12 < total:
        nav.append(InlineKeyboardButton(text="➡️", callback_data=f"langpage:{page+1}"))
    if nav:
        kb.append(nav)

    markup = InlineKeyboardMarkup(inline_keyboard=kb)

    if isinstance(message_or_call, Message):
        await message_or_call.answer("🌐 Тил/өлкө тандоо:", reply_markup=markup)
    else:
        await message_or_call.message.edit_text("🌐 Тил/өлкө тандоо:", reply_markup=markup)

@router.callback_query(F.data.startswith("langpage:"))
async def lang_page(call: CallbackQuery):
    page = int(call.data.split(":")[1])
    await show_lang_page(call, page)

@router.callback_query(F.data.startswith("lang:"))
async def lang_choose(call: CallbackQuery):
    _, code, page = call.data.split(":")
    info = COUNTRIES.get(code)
    if not info:
        await call.answer("Ката 😅")
        return

    async with SessionLocal() as s:
        res = await s.execute(select(User).where(User.tg_id == call.from_user.id))
        u = res.scalar_one()
        u.country_code = code
        u.language = info.get("lang", "ky")
        await s.commit()

    await call.message.answer(f"✅ Тандалды: {info['flag']} {info['name']}\n\n🤖 Tilek AI даяр! Суроо бер, досум 😎", reply_markup=kb_main())
    await call.answer()
