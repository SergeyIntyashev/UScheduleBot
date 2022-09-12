from aiogram import types


async def send_welcome(message: types.Message):
    """
    Данный хендлер вызывается, когда пользователь отправляет команду /start
    """
    await message.answer("Привет!\nЯ бот помогающий тебе не пропустить пары!\n"
                         "Я автоматически буду отправлять тебе напоминание о парах"
                         "Чтобы узнать, что я могу еще отправь /help")


async def send_help(message: types.Message):
    """
    Данный хендлер вызывается, когда пользователь отправляет команду /help
    """
    await message.answer("Расписание на текущий день /today\n"
                         "Расписание на текущую неделю /current\n"
                         "Расписание на cледующую неделю /next\n")
