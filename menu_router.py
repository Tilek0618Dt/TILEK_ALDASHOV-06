from aiogram import Router
from app.handlers import start, menu, chat, premium, referral, support, history, admin, vip

def get_router() -> Router:
    r = Router()
    r.include_router(start.router)
    r.include_router(menu.router)
    r.include_router(history.router)
    r.include_router(support.router)
    r.include_router(referral.router)
    r.include_router(premium.router)
    r.include_router(vip.router)
    r.include_router(chat.router)
    r.include_router(admin.router)
    return r
