"""Вспомогательные утилиты для семинаров по теории вероятностей и статистике."""

from mephi_stats.plots import annotate_prob, distribution_polygon, setup_matplotlib
from mephi_stats.schedule import SEMINAR_DATES, seminar_date

__all__ = [
    "SEMINAR_DATES",
    "annotate_prob",
    "distribution_polygon",
    "seminar_date",
    "setup_matplotlib",
]
