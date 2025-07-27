import os
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from admin_panel import handle_admin, update_channel
from check_subscription import check_subscription, force_subscribe_message
import yt_dlp

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    if not await check_subscription(message.from_user.id, bot):
        return await message.answer(await force_subscribe_message())

    await message.answer("🎵 Qaysi qo‘shiqni yuklamoqchisiz? Menga nomini yozing!")

@dp.message_handler(commands=["admin"])
async def admin_cmd(message: types.Message):
    await handle_admin(message)

@dp.message_handler(lambda msg: msg.text.startswith("/kanal "))
async def kanal_change_cmd(message: types.Message):
    await update_channel(message)

@dp.message_handler()
async def search_music(message: types.Message):
    if not await check_subscription(message.from_user.id, bot):
        return await message.answer(await force_subscribe_message())

    query = message.text
    await message.reply("🔎 Izlanmoqda...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
            filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")

        await message.reply_audio(types.InputFile(filename), title=info['title'])
        os.remove(filename)

    except Exception as e:
        await message.reply("❌ Xatolik yuz berdi. Iltimos, boshqa nom kiriting.")

if __name__ == '__main__':
    if not os.path.exists("downloads"):
        os.mkdir("downloads")
    executor.start_polling(dp)
