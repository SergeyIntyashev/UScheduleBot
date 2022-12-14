from aiogram import types, Dispatcher
from aiogram.types import ParseMode

import services
from db import db_helper
from keyboards import keyboard_client
from models import Week
from utils import log_errors


async def send_welcome(message: types.Message):
    """
    Данный хендлер вызывается, когда пользователь отправляет команду /start
    Отправляет сообщение-приветствие
    """
    await message.answer("Привет!\n"
                         "Я бот помогающий тебе не пропустить пары :)\n"
                         "Я могу автоматически отправлять тебе напоминание "
                         "о парах. \n"
                         "Чтобы узнать, что я могу еще - отправь /help",
                         reply_markup=keyboard_client)


async def send_help(message: types.Message):
    """
    Данный хендлер вызывается, когда пользователь отправляет команду /help
    Отправляет сообщение со списком доступных команд
    """
    await message.answer("Расписание на текущий день /today\n"
                         "Расписание на текущую неделю /current\n"
                         "Расписание на cледующую неделю /next\n"
                         "Напоминать о парах /subscribe\n"
                         "Не напоминать о парах /unsubscribe\n"
                         )


@log_errors
async def send_today_schedule(message: types.Message):
    """
    Хендлер вызывается, когда пользователь отправляет команду /today
    Отправляет сообщение с расписанием на сегодняшний день
    """

    schedule = await services.get_schedule_for_day()

    await message.answer(schedule, parse_mode=ParseMode.HTML)


@log_errors
async def send_current_week_schedule(message: types.Message):
    """
    Хендлер вызывается, когда пользователь отправляет команду /current
    Отправляет сообщение с расписанием на текущую неделю
    """

    schedule = await services.get_week_schedule(Week.CURRENT.value)

    await message.answer(schedule, parse_mode=ParseMode.HTML)


@log_errors
async def send_next_week_schedule(message: types.Message):
    """
    Хендлер вызывается, когда пользователь отправляет команду /next
    Отправляет сообщение с расписанием на следующую неделю
    """

    schedule = await services.get_week_schedule(Week.NEXT.value)

    await message.answer(schedule, parse_mode=ParseMode.HTML)


@log_errors
async def subscribe_to_schedule(message: types.Message):
    """Добавляет пользователя в БД для отправки напоминания о парах"""

    user_id = message.from_user.id

    if db_helper.user_exist(user_id):
        return await message.answer('Вы уже добавлены в рассылку')

    db_helper.add_user(user_id)
    await message.answer('Вы добавлены в рассылку.\n'
                         'Рассылка осуществляется в 21:00 СМР '
                         'за день до занятий')


@log_errors
async def unsubscribe_from_schedule(message: types.Message):
    """Удаляет пользователя из БД, чтобы не получать напоминания о парах"""

    user_id = message.from_user.id

    if not db_helper.user_exist(user_id):
        return await message.answer('Вы не подписаны на рассылку')

    db_helper.delete_user(user_id)
    await message.answer('Вы удалены из рассылки')


@log_errors
async def handle_message(message: types.Message):
    """
    Хендлер вызывается, когда пользователь отправляет боту сообщение
    """

    match message.text:
        case 'Расписание на текущий день':
            await send_today_schedule(message)
        case 'Расписание на текущую неделю':
            await send_current_week_schedule(message)
        case 'Расписание на следующую неделю':
            await send_next_week_schedule(message)
        case 'Напоминать о парах':
            await subscribe_to_schedule(message)
        case 'Не напоминать о парах':
            await unsubscribe_from_schedule(message)
        case _:
            await message.reply('Извините, такую команду я не могу обработать '
                                ':(\n'
                                'Список доступных команд можно посмотреть '
                                'отправив /help или воспользоваться кнопками '
                                'на клавиатуре')


def register_handlers(dp: Dispatcher) -> None:
    """Регистрирует команды в диспатчере"""
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(send_help, commands=['help'])
    dp.register_message_handler(send_today_schedule, commands=['today'])
    dp.register_message_handler(send_current_week_schedule,
                                commands=['current'])
    dp.register_message_handler(send_next_week_schedule, commands=['next'])
    dp.register_message_handler(subscribe_to_schedule, commands=['subscribe'])
    dp.register_message_handler(unsubscribe_from_schedule,
                                commands=['unsubscribe'])
    dp.register_message_handler(handle_message)
