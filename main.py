import asyncio
import logging
import sys
from os import getenv

from aiofiles import os
from aiogram import Bot,Dispatcher,html,F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.orm import Session
from buttons import create_inline_buttons, create_reply_buttons
from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv

from example.alchemy import session, User

load_dotenv()

TOKEN = getenv('BOT_TOKEN')

dp = Dispatcher()


def save_user_to_db(user_id: int, first_name: str, last_name: str = None):
    # Foydalanuvchi bazada bor yoki yo'qligini tekshiramiz
    existing_user = session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()

    if not existing_user:
        # Agar yo'q bo'lsa, yangi user yaratamiz
        new_user = User(id=user_id, name=first_name, fullname=last_name)
        session.add(new_user)
        session.commit()
        print(f"Yangi foydalanuvchi saqlandi: {first_name}")
    else:
        print(f"Foydalanuvchi bazada mavjud: {first_name}")


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    # 1. Bazaga saqlash funksiyasini chaqiramiz
    save_user_to_db(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    # 2. Tugmalarni chiqarish
    buttons = ["🥗 Menyu", "👤 Profilim", "🛒 Savat", "📜 Buyurtmalarim"]
    size = [2, 2]
    markup = create_reply_buttons(buttons=buttons, size=size, resize_keyboard=True)

    await message.answer(
        f"Assalomu Alaykom, {html.bold(message.from_user.first_name)}!\nMa'lumotlaringiz bazaga saqlandi.",
        reply_markup=markup
    )


async def main():
    bot = Bot(token=TOKEN,default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    port = int(os.environ.get("PORT", 5000)) #
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,stream=sys.stdout)
    asyncio.run(main())