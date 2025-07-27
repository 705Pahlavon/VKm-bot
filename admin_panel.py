from aiogram import types
from config import ADMIN_ID, CHANNELS

async def handle_admin(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ Bu buyruq faqat admin uchun!")

    return await message.answer(
        f"🔧 Admin panelga xush kelibsiz!\n\n"
        f"Hozirgi kanal: {CHANNELS[0]}\n"
        f"Yangi kanalni quyidagicha yuboring:\n\n"
        f"`/kanal @yangi_kanal`"
    )

async def update_channel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    if message.text.startswith("/kanal "):
        kanal = message.text.split(maxsplit=1)[1].strip()
        from config import CHANNELS
        CHANNELS[0] = kanal
        await message.answer(f"✅ Yangi kanal o‘rnatildi: {kanal}")
