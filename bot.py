from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio
import google.generativeai as genai
import os
from aiohttp import web

SYSTEM_PROMPT = """
You are Bakbakasur — ek witty, savage aur entertaining Hinglish Telegram bot.

Rules:
- Sirf Hinglish mein baat karna (Hindi + English mix)
- Witty, sarcastic, playful aur thoda arrogant tone rakhna
- Sirf "bc" aur "fk" jaise mild short words use kar sakta hai — wo bhi kabhi-kabhi, har sentence mein nahi
- Kabhi bhi yeh words use mat karna: bkl, mc, bsdk, chutiye, randi, lund, madarchd ya koi bhi heavy gaali
- Roast karna hai toh smart aur funny way mein, gaali se nahi
- Polite mat banna, lekin abusive bhi mat banna — balance rakhna
- Common style: "Arre bc", "Haha bc", "Kya scene hai", "Bhai sun", "Oye", "Bata na"
- Goal: User ko hasana, thoda tease karna, aur entertaining baat karna
"""

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)

bot = Bot(
    token=os.environ["BOT_TOKEN"],
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
chat_history = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply("Arre bc! Finally aa gaya kya? 😂\nBata kya scene hai.")

@dp.message(F.text)
async def bakbak(message: types.Message):
    chat_id = message.chat.id
    if chat_id not in chat_history:
        chat_history[chat_id] = []
    chat_history[chat_id].append({"role": "user", "parts": [message.text]})
    try:
        response = model.generate_content(
            chat_history[chat_id],
            generation_config=genai.types.GenerationConfig(
                temperature=0.85, max_output_tokens=220,
            )
        )
        reply = response.text
        chat_history[chat_id].append({"role": "model", "parts": [reply]})
        if len(chat_history[chat_id]) > 16:
            chat_history[chat_id] = chat_history[chat_id][-16:]
        await message.reply(reply)
    except Exception as e:
        print(f"Error: {e}")
        await message.reply("Bc thoda ruk, dimag fry ho gaya 🔥")

async def handle(request):
    return web.Response(text="Bakbakasur is alive bc!")

async def main():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get('PORT', 8080)))
    await site.start()
    print("Bakbakasur is LIVE...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
