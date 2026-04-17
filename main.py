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

load_dotenv()

TOKEN = getenv('BOT_TOKEN')

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_helder( message: Message):
    await message.delete()
    buttons=["🥗 Menyu","👤 Profilim","🛒 Savat","📜 Buyurtmalarim"]
    size=[2,2]
    markup = create_reply_buttons(buttons=buttons,size=size,resize_keyboard=True)
    await message.answer(f"Assalomu Alaykom, {message.from_user.first_name}\n",reply_markup=markup)


@dp.message(F.text == "🥗 Menyu")
async def command_menu(message: Message):
    await message.answer(f"Assalomu Alaykom, {message.from_user.first_name}\nBugungi menyuyimiz")


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