from aiogram import types

import services
from models import Week


async def send_welcome(message: types.Message):
    """
    Данный хендлер вызывается, когда пользователь отправляет команду /start
    Отправляет сообщение-приветствие
    """
    await message.answer("Привет!\nЯ бот помогающий тебе не пропустить пары!\n"
                         "Я автоматически буду отправлять тебе напоминание о парах"
                         "Чтобы узнать, что я могу еще отправь /help")


async def send_help(message: types.Message):
    """
    Данный хендлер вызывается, когда пользователь отправляет команду /help
    Отправляет сообщение со списком доступных команд
    """
    await message.answer("Расписание на текущий день /today\n"
                         "Расписание на текущую неделю /current\n"
                         "Расписание на cледующую неделю /next\n")


async def send_today_schedule(message: types.Message):
    """
    Хендлер вызывается, когда пользователь отправляет команду /today
    Отправляет сообщение с расписанием на сегодняшний день
    """

    classes_info = await services.get_week_schedule(Week.CURRENT)

    schedule = services.get_schedule_today(classes_info)

    await message.answer(schedule)

