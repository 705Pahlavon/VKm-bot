from aiogram import Bot, types
from config import CHANNELS

async def check_subscription(user_id: int, bot: Bot):
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["member", "creator", "administrator"]:
                return False
        except:
            return False
    return True

async def force_subscribe_message():
    text = "⛔ Botdan foydalanish uchun quyidagi kanalga obuna bo‘ling:\n\n"
    for ch in CHANNELS:
        text += f"👉 {ch}\n"
    text += "\n✅ Obuna bo‘lib, qayta urinib ko‘ring."
    return text
