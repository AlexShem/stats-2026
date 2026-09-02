# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Materials for the **seminar (exercise-session) half** of a probability and
statistics course at MEPhI, autumn semester 2026. Someone else lectures; this
repo is the seminar leader's own preparation plus the handouts given to
students.

**All student-facing and document content is in Russian.** Prose, task
statements, figure labels, axis titles, and captions are Russian. Code
identifiers, file names, and directory slugs stay in Latin script. Comments in
`src/mephi_stats/` are Russian, matching the surrounding style.

Schedule: 16 seminars, Thursdays, 2026-09-03 through 2026-12-17. The dates are
generated, not hand-maintained — see `src/mephi_stats/schedule.py`.

## `gmurman.pdf` — NEVER open this file

`gmurman.pdf` in the repo root is Гмурман, "Руководство к решению задач по теории
вероятностей и математической статистике" (Высшая школа, 1979), the book seminar
problems are drawn from.

**Do not read it, ever — with any tool.** Not `Read`, not `pdftotext`, not page
extraction, not a subagent. It is a 16 MB scan: the pages are images with no text
layer, so every attempt returns nothing usable and burns a large amount of
context. It is gitignored and stays local.

The machine-readable substitute is **`gmurman-contents.md`** — the full table of
contents with page numbers, plus a seminar-to-paragraph mapping table. Use it to
work out *which pages to ask for*.

**When a seminar needs problems from the book, stop and ask Alex.** Name the
chapter, paragraph and page range from `gmurman-contents.md`, and ask him to open
the PDF there and paste the statements (and the answers from «Ответы», p. 373).
Never invent a problem and attribute it to Гмурман, and never guess a problem
number. Problems Alex pastes are transcribed verbatim, keeping the book's
numbering; problems written from scratch are marked as such — see the source
convention below.

Keep the mapping table at the bottom of `gmurman-contents.md` up to date as
seminars are planned.

## The one architectural idea: one source, two audiences

Each seminar is a single file `seminars/NN-slug/seminar-NN.qmd` that renders two
different documents. This is the thing to understand before editing anything.

- **Student handout** — PDF, problem statements only, meant to be printed.
  This is the default render (`format: pdf` in `_quarto.yml`).
- **Preparation notes** — HTML, with worked solutions, derivations, executed
  Python, and teaching notes. Produced by the Quarto profile `prep`
  (`_quarto-prep.yml`).

Content is routed to the prep version by wrapping it:

```markdown
::: {.content-visible when-profile="prep"}
::: {.solution}
Разбор решения.
:::
:::
```

Two div classes carry styling from `prep.scss`, which auto-labels them via
`::before` — do not write a "Решение" heading by hand:

- `.solution` — the worked answer to the preceding task.
- `.teacher-note` — timing plan, common student mistakes; never shown to anyone
  but the seminar leader.

Both **must** sit inside a `content-visible when-profile="prep"` div. The div
classes alone do not hide anything; the profile does. After adding a solution,
render the PDF and confirm the answer is absent.

The `prep` profile does not disable the base `pdf` format, so the prep render
must pass `--to html` explicitly. The Makefile targets already do.

## Commands

```bash
uv sync                                       # environment (Python 3.14)

make prep N=01                                # prep HTML with solutions
make handout N=01                             # student PDF
make all                                      # whole project: all PDFs + index.html
make new N=02 SLUG=conditional-probability    # scaffold from _templates/seminar.qmd
make test                                     # pytest
make lint                                     # ruff check + format --check
make clean                                    # drop _output, .quarto, _freeze
uv run pytest tests/test_schedule.py::test_format_ru   # a single test
```

Quarto must run inside the project venv so the `jupyter` engine finds the
dependencies: always `uv run quarto render …`, never bare `quarto render`.
PDF goes through LuaLaTeX from Quarto's TinyTeX.

## Conventions that are easy to get wrong

**Math macros are defined twice.** `\E`, `\Var`, `\Prob`, `\Cov`, `\indep` live
in the LaTeX `include-in-header` of `_quarto.yml` *and* in the MathJax `macros`
block of `_quarto-prep.yml`. Adding one means editing both files, or it silently
renders as literal text in one of the two outputs.

**Plots.** Call `setup_matplotlib()` from `mephi_stats` in the setup cell of
every seminar before plotting. It selects a Cyrillic-capable font
(matplotlib's default has no Cyrillic — labels become boxes) and a palette that
survives greyscale printing, which matters because handouts get printed.

**Randomness must be reproducible.** Simulations appear in printed handouts, so
seed with `rng = np.random.default_rng(2026)` and never call the global
`np.random` functions. Where a simulation checks an analytic answer, print both
side by side so a drifting result is visible.

**Problem provenance.** Every task carries its source in the heading, so it is
always clear what may be re-derived and what was transcribed:
`## Задача 3 (Гмурман, гл. 2 § 1, № 24)` for a book problem,
`## Задача 3` alone for one written for this course. Never attach a Гмурман
number to a problem Alex did not paste from the book.

**Cell labels.** Follow Quarto cross-reference prefixes (`fig-`, `tbl-`,
`sec-`); a plot cell without a `fig-` label and `fig-cap` will not be
referenceable from the text.

**`freeze: auto`** is on. Cell output is cached in `_freeze/` and reused until
the `.qmd` changes; if a figure looks stale after editing only Python in
`src/mephi_stats/`, run `make clean` or touch the `.qmd`.

## `lectures/`

Lecture notes from the course lecturer land here as they arrive, named
`NN-topic.*` to line up with seminar numbers. When preparing a seminar, check
the matching lecture first — notation and the order of results in the exercises
should follow the lecture, not a textbook's own conventions.

## `src/mephi_stats/`

Shared helpers imported by the `.qmd` files, installed as an editable package by
`uv sync`. Keep anything reused across two or more seminars here rather than
copying setup code between documents: `plots.py` (figure styling), `schedule.py`
(semester dates, used to generate the schedule table in `index.qmd`).
