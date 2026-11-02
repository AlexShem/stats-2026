import datetime as dt

import pytest

from mephi_stats.schedule import (
    CLASS_DATES,
    MIDTERMS,
    RESCHEDULED,
    SEMINAR_DATES,
    TUESDAYS,
    format_ru,
    seminar_date,
)

TUESDAY = 1


def test_sixteen_classes_one_of_them_a_midterm():
    assert len(TUESDAYS) == len(CLASS_DATES) == 16
    assert all(d.weekday() == TUESDAY for d in TUESDAYS)
    assert set(MIDTERMS) <= set(CLASS_DATES)
    assert len(SEMINAR_DATES) == 16 - len(MIDTERMS) == 15


def test_only_rescheduled_dates_leave_tuesday():
    off = [d for d in CLASS_DATES if d.weekday() != TUESDAY]
    assert off == sorted(RESCHEDULED.values())
    assert SEMINAR_DATES == sorted(SEMINAR_DATES)


def test_seminar_06_moved_to_friday_9_october():
    assert seminar_date(6) == dt.date(2026, 10, 9)


def test_midterm_3_november_and_20_october_moved_to_6_november():
    # Контрольная 3 ноября номера семинара не берёт; занятие 20 октября
    # перенесено на пятницу 6 ноября и стало семинаром 8.
    assert dt.date(2026, 10, 20) not in CLASS_DATES
    assert dt.date(2026, 11, 3) in MIDTERMS
    assert seminar_date(7) == dt.date(2026, 10, 27)
    assert seminar_date(8) == dt.date(2026, 11, 6)
    assert seminar_date(9) == dt.date(2026, 11, 10)


def test_semester_boundaries():
    assert SEMINAR_DATES[0] == dt.date(2026, 9, 8)
    assert SEMINAR_DATES[-1] == dt.date(2026, 12, 22)


def test_seminar_03_falls_on_22_september():
    # Дата на раздатке семинара 03: опорная точка всей серии.
    assert seminar_date(3) == dt.date(2026, 9, 22)


def test_seminar_date_is_one_indexed():
    assert seminar_date(1) == SEMINAR_DATES[0]
    with pytest.raises(ValueError):
        seminar_date(0)
    with pytest.raises(ValueError):
        seminar_date(16)


def test_format_ru():
    assert format_ru(dt.date(2026, 9, 8)) == "8 сентября 2026"
