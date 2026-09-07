import datetime as dt

import pytest

from mephi_stats.schedule import SEMINAR_DATES, format_ru, seminar_date

TUESDAY = 1


def test_semester_has_sixteen_tuesdays():
    assert len(SEMINAR_DATES) == 16
    assert all(d.weekday() == TUESDAY for d in SEMINAR_DATES)


def test_semester_boundaries():
    assert SEMINAR_DATES[0] == dt.date(2026, 9, 1)
    assert SEMINAR_DATES[-1] == dt.date(2026, 12, 15)


def test_seminar_02_falls_on_8_september():
    # Дата на раздатке семинара 02; проверяем явно, потому что нумерация
    # сдвинута относительно фактического четверга первой недели.
    assert seminar_date(2) == dt.date(2026, 9, 8)


def test_seminar_date_is_one_indexed():
    assert seminar_date(1) == SEMINAR_DATES[0]
    with pytest.raises(ValueError):
        seminar_date(0)
    with pytest.raises(ValueError):
        seminar_date(17)


def test_format_ru():
    assert format_ru(dt.date(2026, 9, 8)) == "8 сентября 2026"
