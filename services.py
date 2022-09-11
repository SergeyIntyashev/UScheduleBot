from collections import namedtuple
from functools import lru_cache

from models import ScheduleInfo, ClassInfo, ScheduleDay, Header

DayOfWeek = namedtuple('DayOfWeek', ('name', 'number'))


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
