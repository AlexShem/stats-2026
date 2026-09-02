import datetime as dt

import pytest

from mephi_stats.schedule import SEMINAR_DATES, format_ru, seminar_date


def test_semester_has_sixteen_thursdays():
    assert len(SEMINAR_DATES) == 16
    assert all(d.weekday() == 3 for d in SEMINAR_DATES)


def test_semester_boundaries():
    assert SEMINAR_DATES[0] == dt.date(2026, 9, 3)
    assert SEMINAR_DATES[-1] == dt.date(2026, 12, 17)


def test_seminar_date_is_one_indexed():
    assert seminar_date(1) == SEMINAR_DATES[0]
    with pytest.raises(ValueError):
        seminar_date(0)
    with pytest.raises(ValueError):
        seminar_date(17)


def test_format_ru():
    assert format_ru(dt.date(2026, 9, 3)) == "3 сентября 2026"
