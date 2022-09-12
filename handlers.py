from aiogram import types
from aiogram.types import ParseMode

import services
from models import Week


async def send_welcome(message: types.Message):
    """
    Данный хендлер вызывается, когда пользователь отправляет команду /start
    Отправляет сообщение-приветствие
    """
    await message.answer("Привет!\n"
                         "Я бот помогающий тебе не пропустить пары :)\n"
                         "Я автоматически буду отправлять тебе напоминание "
                         "о парах. \n"
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

    schedule = await services.get_schedule_today()

    await message.answer(schedule, parse_mode=ParseMode.HTML)


async def send_current_week_schedule(message: types.Message):
    """
    Хендлер вызывается, когда пользователь отправляет команду /current
    Отправляет сообщение с расписанием на текущую неделю
    """

    schedule = await services.get_week_schedule(Week.CURRENT)

    await message.answer(schedule, parse_mode=ParseMode.HTML)


async def send_next_week_schedule(message: types.Message):
    """
    Хендлер вызывается, когда пользователь отправляет команду /next
    Отправляет сообщение с расписанием на следующую неделю
    """

    schedule = await services.get_week_schedule(Week.NEXT)

    await message.answer(schedule, parse_mode=ParseMode.HTML)


async def handle_message(message: types.Message):
    """
    Хендлер вызывается, когда пользователь отправляет боту сообщение
    """

    await message.reply('Извините, такую команду я не могу обработать :(\n'
                        'Список доступных команд можно посмотреть '
                        'отправив /help')
