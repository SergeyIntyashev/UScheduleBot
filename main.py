import os

from aiogram import Bot, Dispatcher, executor
from dotenv import load_dotenv

import handlers

load_dotenv()

API_TOKEN = os.environ.get('API_TOKEN')

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)

dp.register_message_handler(handlers.send_welcome, commands=["start"])

dp.register_message_handler(handlers.send_help, commands=["help"])

dp.register_message_handler(handlers.send_today_schedule, commands=["today"])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
