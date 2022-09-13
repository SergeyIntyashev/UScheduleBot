from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

today_button = KeyboardButton('Расписание на текущий день')
current_week_button = KeyboardButton('Расписание на текущую неделю')
next_week_button = KeyboardButton('Расписание на следующую неделю')
remind_button = KeyboardButton('Напоминать о парах')
not_remind_button = KeyboardButton('Не напоминать о парах')

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_client. \
    add(today_button). \
    add(current_week_button). \
    add(next_week_button). \
    add(remind_button). \
    add(not_remind_button)
