"""Единое оформление графиков: кириллица, читаемые размеры, спокойная палитра."""

from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt

#: Палитра, различимая при печати в градациях серого и при дальтонизме.
PALETTE = ["#0b5394", "#b45309", "#2e7d32", "#7b1fa2", "#c62828", "#00838f"]

#: Шрифты с кириллицей, доступные в системе (первый найденный побеждает).
CYRILLIC_FONTS = ["DejaVu Sans", "Liberation Sans", "Noto Sans", "sans-serif"]


def setup_matplotlib(scale: float = 1.0) -> None:
    """Применить оформление по умолчанию ко всем последующим графикам.

    Вызывается один раз в начале .qmd-документа. ``scale`` увеличивает все
    размеры шрифтов — удобно для проектора (``scale=1.3``).
    """
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": CYRILLIC_FONTS,
            "axes.unicode_minus": False,
            "font.size": 11 * scale,
            "axes.titlesize": 13 * scale,
            "axes.labelsize": 11 * scale,
            "legend.fontsize": 10 * scale,
            "xtick.labelsize": 10 * scale,
            "ytick.labelsize": 10 * scale,
            "axes.prop_cycle": mpl.cycler(color=PALETTE),
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.3,
            "grid.linewidth": 0.6,
            "figure.dpi": 110,
            "savefig.bbox": "tight",
            "figure.constrained_layout.use": True,
        }
    )


def annotate_prob(ax: plt.Axes, text: str, xy: tuple[float, float]) -> None:
    """Подписать область на графике (например, вероятность хвоста)."""
    ax.annotate(
        text,
        xy=xy,
        xycoords="axes fraction",
        fontsize=mpl.rcParams["font.size"],
        bbox={"boxstyle": "round,pad=0.35", "fc": "white", "ec": "#999", "alpha": 0.85},
    )
