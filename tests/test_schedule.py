import datetime as dt

import pytest

from mephi_stats.schedule import RESCHEDULED, SEMINAR_DATES, TUESDAYS, format_ru, seminar_date

TUESDAY = 1


def test_semester_has_sixteen_tuesdays():
    assert len(TUESDAYS) == len(SEMINAR_DATES) == 16
    assert all(d.weekday() == TUESDAY for d in TUESDAYS)


def test_only_rescheduled_dates_leave_tuesday():
    off = [d for d in SEMINAR_DATES if d.weekday() != TUESDAY]
    assert off == sorted(RESCHEDULED.values())
    assert SEMINAR_DATES == sorted(SEMINAR_DATES)


def test_seminar_06_moved_to_friday_9_october():
    assert seminar_date(6) == dt.date(2026, 10, 9)


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
        seminar_date(17)


def test_format_ru():
    assert format_ru(dt.date(2026, 9, 8)) == "8 сентября 2026"
