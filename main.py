import os

from aiogram import Bot, Dispatcher, executor
from dotenv import load_dotenv

from handlers import register_handlers
from scheduler import on_startup

load_dotenv()

API_TOKEN = os.environ.get('API_TOKEN')

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)

register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
