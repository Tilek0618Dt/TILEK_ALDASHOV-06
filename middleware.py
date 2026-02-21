from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from app.config import REQUIRED_CHANNEL, CHANNEL_URL
from aiogram.enums import ChatMemberStatus

def _is_channel_id(val: str) -> bool:
    return val.strip().lstrip("-").isdigit()

class ChannelGateMiddleware(BaseMiddleware):
    async def call(self, handler, event, data):
        bot = data["bot"]

        user_id = None
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id

        # эгер канал коюлбаса — өткөрө беребиз
        if not REQUIRED_CHANNEL or not user_id:
            return await handler(event, data)

        try:
            chat = int(REQUIRED_CHANNEL) if _is_channel_id(REQUIRED_CHANNEL) else REQUIRED_CHANNEL
            member = await bot.get_chat_member(chat_id=chat, user_id=user_id)
            if member.status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
                return await handler(event, data)
        except TelegramBadRequest:
            pass

        text = (
            "🚪 Досум, биринчи каналга каттал!\n\n"
            f"👉 {CHANNEL_URL or REQUIRED_CHANNEL}\n\n"
            "Катталгандан кийин кайра /start бас 😎"
        )
        if isinstance(event, Message):
            await event.answer(text)
        else:
            await event.message.answer(text)
        return
