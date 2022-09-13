import asyncio

import aioschedule
from aiogram import Dispatcher, Bot

from services import check_today_schedule


async def scheduler(bot: Bot):
    aioschedule.every().day.at('8:00').do(check_today_schedule, bot=bot)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dp: Dispatcher):
    asyncio.create_task(scheduler(dp.bot))
