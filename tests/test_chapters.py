"""Проверки глав книги: явный код, отсутствие преподавательских заметок, уникальные метки."""

import re
from collections import Counter
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = sorted(ROOT.glob("seminars/*/seminar-*.qmd"))

CELL = re.compile(r"^```\{python\}\n(.*?)^```", re.DOTALL | re.MULTILINE)
# import, from … import, def и lambda-выражение (но не слово lambda в строке или в LaTeX)
DEFINITION = re.compile(
    r"^\s*(import |from \S+ import |def )|(?<![\\\w\"])lambda\b[^:\n\"]*:", re.MULTILINE
)
LABEL = re.compile(r"\{#((?:sec|fig|tbl|eq)-[\w-]+)")


def test_chapters_exist():
    assert CHAPTERS


@pytest.mark.parametrize("path", CHAPTERS, ids=lambda p: p.name)
def test_imports_and_functions_only_in_first_cell(path):
    cells = CELL.findall(path.read_text(encoding="utf-8"))
    assert cells, "в главе нет ячеек с кодом"
    for number, cell in enumerate(cells[1:], start=2):
        hits = [m.group(0).strip() for m in DEFINITION.finditer(cell)]
        assert not hits, f"ячейка {number}: {hits} — перенесите в первую ячейку"


@pytest.mark.parametrize("path", CHAPTERS, ids=lambda p: p.name)
def test_no_teacher_only_content(path):
    text = path.read_text(encoding="utf-8")
    for marker in ("teacher-note", 'when-profile="prep"', "mephi_stats", "include: false"):
        assert marker not in text


def test_labels_unique_across_book():
    labels = Counter()
    for path in CHAPTERS:
        labels.update(LABEL.findall(path.read_text(encoding="utf-8")))
    duplicates = [label for label, count in labels.items() if count > 1]
    assert not duplicates


def test_every_chapter_listed_in_book():
    config = yaml.safe_load((ROOT / "_quarto.yml").read_text(encoding="utf-8"))
    listed = set(config["book"]["chapters"])
    missing = [str(p.relative_to(ROOT)) for p in CHAPTERS if str(p.relative_to(ROOT)) not in listed]
    assert not missing
