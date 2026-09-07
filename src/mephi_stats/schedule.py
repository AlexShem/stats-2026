"""Расписание семинаров: осенний семестр 2026, вторники."""

from __future__ import annotations

import datetime as dt

#: Первый вторник семестра. Семинар 01 фактически прошёл в четверг 3 сентября
#: (разовый перенос в первую неделю), дальше занятия идут строго по вторникам.
FIRST_SEMINAR = dt.date(2026, 9, 1)

#: Число семинаров в семестре.
SEMINAR_COUNT = 16

#: Даты всех семинаров семестра, по порядку.
SEMINAR_DATES: list[dt.date] = [FIRST_SEMINAR + dt.timedelta(weeks=i) for i in range(SEMINAR_COUNT)]


def seminar_date(number: int) -> dt.date:
    """Дата семинара по его номеру (нумерация с 1)."""
    if not 1 <= number <= len(SEMINAR_DATES):
        raise ValueError(
            f"Номер семинара должен быть от 1 до {len(SEMINAR_DATES)}, получено {number}"
        )
    return SEMINAR_DATES[number - 1]


def format_ru(date: dt.date) -> str:
    """Дата по-русски: '8 сентября 2026'."""
    months = [
        "января",
        "февраля",
        "марта",
        "апреля",
        "мая",
        "июня",
        "июля",
        "августа",
        "сентября",
        "октября",
        "ноября",
        "декабря",
    ]
    return f"{date.day} {months[date.month - 1]} {date.year}"
