import os
from collections import namedtuple
from datetime import datetime
from functools import lru_cache

import aiohttp
from dotenv import load_dotenv

from models import ScheduleInfo, ClassInfo, ScheduleDay, Header

load_dotenv()

DayOfWeek = namedtuple('DayOfWeek', ('name', 'number'))

SCHEDULE_URL = os.environ.get('SCHEDULE_URL')
GROUP_ID = os.environ.get('GROUP_ID')


@lru_cache
def get_days_of_week() -> list[DayOfWeek]:
    """Возвращает список дней недели и порядковый номер"""

    return [
        DayOfWeek('MONDAY', 1),
        DayOfWeek('TUESDAY', 2),
        DayOfWeek('WEDNESDAY', 3),
        DayOfWeek('THURSDAY', 4),
        DayOfWeek('FRIDAY', 5),
        DayOfWeek('SATURDAY', 6)
    ]


def get_week_schedule_days(schedule_info: ScheduleInfo) -> list[ClassInfo]:
    """Возвращает список информации о занятиях за неделю"""

    result = []
    headers = schedule_info.headers

    days_of_week = get_days_of_week()

    for week_time in schedule_info.body:
        for day_of_week in days_of_week:
            schedule_day = getattr(week_time, day_of_week.name)
            if schedule_day.workPlan.id is not None:
                class_info = get_schedule_day_info(
                    schedule_day=schedule_day,
                    headers=headers,
                    time=week_time.name,
                    week_day=day_of_week
                )
                result.append(class_info)

    result.sort(key=lambda obj: obj.numberDayOfWeek)

    return result


def get_date_of_lesson(headers: list[Header], week_day: DayOfWeek) -> str:
    """Возвращет дату и день недели занятия"""

    return next(filter(lambda obj: obj.value == week_day, headers)).text


def get_schedule_day_info(schedule_day: ScheduleDay,
                          headers: list[Header],
                          time: str,
                          week_day: DayOfWeek) -> ClassInfo:
    """Возвращает информацию о занятии"""

    lesson_type = schedule_day.workPlan.lessonTypes.name
    discipline_name = schedule_day.workPlan.discipline.fullName
    audience_point_number = ''
    teacher_fio = ''

    if schedule_day.subject:
        subject = schedule_day.subject[0]

        if subject.audiences:
            audience = subject.audiences[0]
            audience_point_number = audience.accessPointName

        if subject.replacementTeachers:
            replacement_teacher = subject.replacementTeachers[0]
            teacher_fio = replacement_teacher.fio

    return ClassInfo(
        time=time,
        date=get_date_of_lesson(headers=headers, week_day=week_day.name),
        lessonType=lesson_type,
        disciplineName=discipline_name,
        teacherFIO=teacher_fio,
        audiencePointNumber=audience_point_number,
        numberDayOfWeek=week_day.number
    )


def get_query_params(schedule_week: str) -> str:
    """Возвращает параметры запроса для получения расписания"""

    return f"groupId={GROUP_ID}&scheduleWeek={schedule_week}&date="


def get_schedule_message(schedule_info: list[ClassInfo]) -> str:
    """Возвращает расписание на неделю строкой"""

    return '\n'.join([str(class_info) for class_info in schedule_info])


async def get_week_schedule(week: str) -> list[ClassInfo] | None:
    """Возвращает расписание на неделю"""

    query_params = get_query_params(week)
    url = f"{SCHEDULE_URL}?{query_params}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None

            body = await response.text()
            schedule_info = ScheduleInfo.parse_raw(body)

            return get_week_schedule_days(schedule_info)


def get_schedule_today(classes_info: list[ClassInfo]) -> str:
    """Возвращает занятия на текущий день"""

    result = []
    now = datetime.now()
    week_day = datetime.isoweekday(now)

    cur_class_info = filter(lambda obj: obj.numberDayOfWeek == week_day,
                            classes_info)

    while next(cur_class_info):
        result.append(str(cur_class_info))

    if not result:
        return 'Сегодня занятий нет'

    return '\n'.join(result)
