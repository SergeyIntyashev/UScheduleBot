from aiogram import types
import traceback


def log_errors(func):
    async def wrapper(message: types.Message):
        try:
            return await func(message)
        except Exception as ex:
            print('Произошла ошибка в работе - ', traceback.format_exc())
            await message.answer('Упс, что-то пошло не так. '
                                 'Попробуйте запросить расписание позже')

    return wrapper
