from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

today_button = KeyboardButton('Расписание на текущий день')
current_week_button = KeyboardButton('Расписание на текущую неделю')
next_week_button = KeyboardButton('Расписание на следующую неделю')

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_client. \
    add(today_button). \
    add(current_week_button). \
    add(next_week_button)
