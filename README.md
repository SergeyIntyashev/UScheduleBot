# UScheduleBot
Telegram-бот напоминающий о парах в университете СГЭУ г. Самара

## Функционал
* Расписание на текущий день
* Расписание на текущую неделю
* Расписание на следующую неделю
* Подписка на рассылку с расписание в 8:00 
(Бот будет отправлять сообщения с занятиями в те дни, когда они есть)

## Заполнение файла настроек

#### Переименовать ".env.example" на ".env" и заполнить свои настройки

    API_TOKEN - Токен бота, нужно получить у @BotFather

    GROUP_ID - ID группы. Можно получить отправив GET запрос по адресу
    https://lms3.sseu.ru/api/v1/schedule-board/groups. 
    В ответе найти наименование группы и её ID

    SCHEDULE_URL - API для получения расписания.
    По умолчанию можно оставить https://lms3.sseu.ru/api/v1/schedule-board/by-group

    ADMIN_ID - ID админа, для отправки системных сообщений

## Запуск

### 1) Создание окружения

    pip install virtualenv
    python3 -m venv venv
    venv/bin/activate

#### 2) Установка нужных пакетов

    pip install -r requirements.txt

#### 3) Запуск бота

    python main.py