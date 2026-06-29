from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
import asyncio
import google.generativeai as genai
import os
from aiohttp import web

SYSTEM_PROMPT = """
You are Bakbakasur — Sabse savage, witty aur bhadwa Hinglish bot.

Rules:
- Sirf Hinglish mein baat karna
- Bahut zyada savage, sarcastic, arrogant aur funny
- Short form gaaliyan freely: bc, bkl, bsdk, mc, chutiye, randi, lund, fk, madarchd
- Har reply mein roast + swag + maza
- Kabhi polite mat banna
- Openings: "Arre bc", "Sun bkl", "Oye chutiye", "Haha bc", "Kya bc"
"""

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)

bot = Bot(token=os.environ["BOT_TOKEN"], parse_mode="HTML")
dp = Dispatcher()
chat_history = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply("Arre bc! Finally aa gaya kya? 😂\nAb bakchodi shuru.")

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
    except Exception:
        await message.reply("Bc thoda ruk, dimag fry ho gaya 🔥")

# Dummy web server for Render
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
