import enum

from pydantic import BaseModel


class Week(enum.Enum):
    CURRENT: str = 'CURRENT'
    NEXT: str = 'NEXT'


class Header(BaseModel):
    text: str
    align: str
    sortable: bool
    value: str


class Discipline(BaseModel):
    id: int
    name: str
    codeOneC: str
    fullName: str


class LessonTypes(BaseModel):
    id: int
    name: str


class Group(BaseModel):
    id: int
    name: str
    course: str
    direction: str
    directionCode: int | None
    faculty: str
    formOfTraining: str
    groupCode: str
    numberOfStudents: str
    program: str
    trainingPeriod: str | None
    scheduleType: int
    typesEducation: str


class HalfYear(BaseModel):
    id: int
    name: str
    current: int


class YearOfStudy(BaseModel):
    id: int
    name: str
    current: int
    yearStart: int
    yearEnd: int


class WorkPlan(BaseModel):
    id: int | None
    hours: int | None
    discipline: Discipline | None
    lessonTypes: LessonTypes | None
    group: Group | None
    halfYear: HalfYear | None
    yearOfStudy: YearOfStudy | None
    practic: bool | None


class Audience(BaseModel):
    id: int
    name: str


class TeacherInfo(BaseModel):
    id: int
    teacher: str
    fio: str


class Subject(BaseModel):
    name: str | None
    link: str | None
    subGroups: str | None
    invitationCode: str | None
    audiences: list[Audience]
    replacementTeachers: list[TeacherInfo]


class ScheduleDay(BaseModel):
    workPlan: WorkPlan
    subject: list[Subject]


class WeekTime(BaseModel):
    name: str
    WEDNESDAY: ScheduleDay
    MONDAY: ScheduleDay
    THURSDAY: ScheduleDay
    TUESDAY: ScheduleDay
    FRIDAY: ScheduleDay
    SATURDAY: ScheduleDay
    FRIDAY: ScheduleDay


class ScheduleInfo(BaseModel):
    week: str
    headers: list[Header]
    body: list[WeekTime]


class ClassInfo(BaseModel):
    date: str
    time: str
    lessonType: str
    disciplineName: str
    teacherFIO: str
    audiencePointNumber: str
    numberDayOfWeek: int

    def __str__(self):
        return f'<b>{self.date} в {self.time}</b>\n' \
               f'Предмет <em><u>{self.disciplineName}</u></em>\n' \
               f'Тип занятия <em><u>{self.lessonType}</u></em>\n' \
               f'Аудитория <em><u>{self.audiencePointNumber}</u></em>\n' \
               f'Преподаватель <em><u>{self.teacherFIO}</u></em>\n'
