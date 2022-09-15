import asyncio

import aioschedule
from aiogram import Dispatcher, Bot

from services import check_tomorrow_schedule


async def scheduler(bot: Bot):
    """
    Устанавливает и запускает расписание отправки
    """
    aioschedule.every().day.at('20:00').do(check_tomorrow_schedule, bot=bot)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dp: Dispatcher):
    """
    Создает задачу для отправки напоминаний о парах
    """
    asyncio.create_task(scheduler(dp.bot))
