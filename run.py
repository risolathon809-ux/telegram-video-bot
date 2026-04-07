import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN not set")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Salom! Menga Instagram, TikTok yoki YouTube Shorts havolasini yuboring.")

@dp.message()
async def download_video(message: types.Message):
    url = message.text.strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        await message.answer("Iltimos, to‘g‘ri havola yuboring.")
        return
    
    await message.answer("Video yuklanmoqda, biroz kuting...")
    
    import yt_dlp
    
    ydl_opts = {
        'format': 'best[height<=720]',
        'outtmpl': '/tmp/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if not os.path.exists(filename):
                import glob
                files = glob.glob(f"/tmp/{info['id']}.*")
                if files:
                    filename = files[0]
                else:
                    raise Exception("Fayl topilmadi")
        
        with open(filename, 'rb') as f:
            await message.answer_video(f, caption="✅ Yuklab olindi!")
        
        os.remove(filename)
    except Exception as e:
        await message.answer(f"Xatolik: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
