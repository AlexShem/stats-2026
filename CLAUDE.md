# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Materials for the **seminar (exercise-session) half** of a probability and
statistics course at MEPhI, autumn semester 2026. Someone else lectures; Alex
runs the seminars. Everything rendered from this repo is **for students**: a
Quarto book (course guide with solutions and Python examples) and a printable
PDF handout per seminar.

**All student-facing and document content is in Russian.** Prose, task
statements, figure labels, axis titles, and captions are Russian. Code
identifiers, file names, and directory slugs stay in Latin script. Comments in
code are Russian, matching the surrounding style.

Schedule: 16 seminars, Tuesdays, 2026-09-01 through 2026-12-15 (seminar 1 was
moved to Thursday 2026-09-03). The dates are generated, not hand-maintained —
see `src/mephi_stats/schedule.py`.

## `gmurman.pdf` — NEVER open this file

`gmurman.pdf` in the repo root is Гмурман, "Руководство к решению задач по теории
вероятностей и математической статистике" (Высшая школа, 1979), the book seminar
problems are drawn from.

**Do not read it, ever — with any tool.** Not `Read`, not `pdftotext`, not page
extraction, not a subagent. It is a 16 MB scan: the pages are images with no text
layer, so every attempt returns nothing usable and burns a large amount of
context. It is gitignored and stays local.

Two machine-readable substitutes exist, and both should be checked before asking
Alex for anything:

- **`gmurman-contents.md`** — the full table of contents with page numbers, plus
  a seminar-to-paragraph mapping table. Use it to work out *which pages to ask
  for*.
- **`problems/`** — the problem bank: pages Alex has already transcribed, with
  statements, solutions and answers in plain Markdown. If a problem is in there,
  it is already available; do not ask for it again. See `problems/README.md`.

**When a seminar needs problems the bank does not yet cover, stop and ask Alex.**
Name the
chapter, paragraph and page range from `gmurman-contents.md`, and ask him to open
the PDF there and paste the statements (and the answers from «Ответы», p. 373).
Never invent a problem and attribute it to Гмурман, and never guess a problem
number. Problems Alex pastes are transcribed verbatim, keeping the book's
numbering; problems written from scratch are marked as such — see the source
convention below.

Keep the mapping table at the bottom of `gmurman-contents.md` up to date as
seminars are planned.

## The one architectural idea: one source, book + handout

Each seminar is a single file `seminars/NN-slug/seminar-NN.qmd` that is both a
**chapter of the book** and the source of **that seminar's handout**. Both
outputs are read by students.

- **Book** — HTML, the default render. `_quarto.yml` has `project: type: book`
  and lists every chapter under `book.chapters`. Output: `_output/book/`.
- **Handout** — PDF, one per seminar: summary, problem statements, homework;
  no solutions, no code. Produced by the profile `handout`
  (`_quarto-handout.yml`), which switches the project type to `default` so each
  chapter renders as its own PDF. Output: `_output/handouts/`.

Book-only content is wrapped like this:

```markdown
::: {.content-hidden when-profile="handout"}
::: {.callout-tip collapse="true" title="Решение"}
Выкладка, ответ, проверка на Python.

::: {.callout-warning title="Типичная ошибка"}
…
:::
:::
:::
```

- Every solution is a **collapsed** `callout-tip` titled «Решение», so
  students try the problem first. Homework answers use the same callout titled
  «Ответы».
- `callout-warning` «Типичная ошибка» goes *inside* the solution (it usually
  gives the answer away), only where the mistake is common and short to state.
  `callout-note` «Для самопроверки» offers a twin problem with its answer.
- The «Код для этой главы» section with the setup cell is also wrapped, so the
  handout does not show an empty heading.

The wrapper, not the callout, is what hides content from the handout. After
adding a solution, render the handout and confirm the answer is absent.

Formats merge across profiles, so the handout render must pass `--to pdf`
explicitly. The Makefile targets already do.

## Commands

```bash
uv sync                                       # environment (Python 3.14)

make book                                     # book HTML → _output/book/
make preview                                  # book with live reload
make handout N=01                             # one student PDF
make handouts                                 # all student PDFs
make all                                      # book + all handouts
make new N=03 SLUG=random-variables           # scaffold from _templates/seminar.qmd
make test                                     # pytest (incl. chapter rules)
make lint                                     # ruff check + format --check
make clean                                    # drop _output, .quarto, _freeze
uv run pytest tests/test_schedule.py::test_format_ru   # a single test
```

`make new` does not touch `_quarto.yml`: add the new chapter to
`book.chapters` by hand (`tests/test_chapters.py` fails until you do).

Quarto must run inside the project venv so the `jupyter` engine finds the
dependencies: always `uv run quarto render …`, never bare `quarto render`.
PDF goes through LuaLaTeX from Quarto's TinyTeX.

## Writing for students

**Voice.** The reader is a student opening the book on their own. Write
straight to the point: what the scheme is, the derivation, the answer, the
check. No classroom directions («к доске», «даю условие и жду»), no timing
plans, no notes addressed to the seminar leader, no repo paths
(`problems/…`). Preparation notes for Alex do not live in this repo's
rendered files.

**Explicit Python.** Everything a chapter's code uses must be visible at the
top of that chapter:

- The first `{python}` cell (under «Код для этой главы», `echo: true`) holds
  **all** imports, the matplotlib `rcParams` setup, `rng`, and **every**
  `def`. Each function gets a short Russian docstring.
- Later cells contain no `import`, `def` or `lambda` — move them up.
- Chapters do not import from `mephi_stats`. Shared plotting code is copied
  into each chapter on purpose, so every chapter reads on its own.
- Before a check cell, one sentence says what the code verifies
  («Проверка: полный перебор 216 исходов.»).

`tests/test_chapters.py` enforces the cell rule, the absence of
`teacher-note`/`when-profile="prep"`/`mephi_stats`/`include: false` in
chapters, label uniqueness, and that every chapter is listed in the book.

## Conventions that are easy to get wrong

**Heading levels.** Chapter title comes from YAML `title`. In the body:
`##` for «Код для этой главы», «Краткая сводка», blocks and homework; `###` for
tasks. A body `#` would be numbered as a separate chapter. The handout profile
sets `shift-heading-level-by: -1`.

**Labels are unique across the whole book.** Prefix every label with the
seminar: `sec-s02-t5`, `fig-s02-t5`, `eq-s02-poisson`, `s02-t5-check`. Follow
Quarto cross-reference prefixes (`fig-`, `tbl-`, `sec-`, `eq-`); a plot cell
without a `fig-` label and `fig-cap` will not be referenceable. Refer to other
tasks in prose («задача 4») when the text also appears in the handout.

**Math macros are defined twice.** `\E`, `\Var`, `\Prob`, `\Cov`, `\indep`
live in the MathJax `include-in-header` of `_quarto.yml` *and* in the LaTeX
`include-in-header` of `_quarto-handout.yml`. Adding one means editing both
files, or it silently renders as literal text in one of the two outputs.

**Plots.** The setup cell sets a Cyrillic-capable font (matplotlib's default
has no Cyrillic — labels become boxes) and a palette that survives greyscale
printing. Copy that block from `_templates/seminar.qmd`.

**Randomness must be reproducible.** Seed with
`rng = np.random.default_rng(2026)` and never call the global `np.random`
functions. Where a simulation checks an analytic answer, print both side by
side so a drifting result is visible.

**Problem provenance.** Every task carries its source in the heading, so it is
always clear what may be re-derived and what was transcribed:
`### Задача 3 (Гмурман, гл. 2 § 1, № 24)` for a book problem,
`### Задача 3` alone for one written for this course. Never attach a Гмурман
number to a problem Alex did not paste from the book.

**`freeze: auto`** is on. Cell output is cached in `_freeze/` and reused until
the `.qmd` changes; after editing only `src/mephi_stats/`, run `make clean` or
touch the `.qmd`.

## `problems/`

The transcribed problem bank — `problems/gmurman/ch<NN>-<S>.md`, one file per
book paragraph, currently гл. 2 §§ 1–2 (problems 46–88). Each entry has the
statement verbatim, a type/difficulty line, a solution, and the answer.

Solutions are labelled by origin and the distinction matters:

- **Решение книжное** — printed in the book, transcribed as-is. Do not rewrite it
  into a slicker form; it is the reference for what students may have seen.
- **Решение наше** — the book leaves the problem for self-study, so the solution
  was written here.

**A book answer is not evidence on its own.** The book is assumed to contain
typos, so every answer — the book's included — gets recomputed independently
before it is trusted. That verdict lives in each problem's **Статус** field:
✅ сверено (book answer on p. 373, matched our computation), ✅ проверено (no
p. 373 entry, our recomputation confirmed the printed derivation),
⚠️ расхождение, or ❔ не проверено. Never use an answer marked ❔, and never
raise a status without actually running the check. `problems/README.md` lists
what each check consisted of.

Chapter `.qmd` files do **not** include these files — they restate the problems
they use. The duplication is deliberate: a seminar may trim or reorder a
statement, while the bank keeps the book's original.

Adding a paragraph Alex has pasted: create the file, keep the book's numbering
and `{#gNN}` anchors, recompute every answer with a scratch Python calculation
and record the verdict in **Статус** before committing, then update the table in
`problems/README.md` and the mapping table in `gmurman-contents.md`.
`problems/gmurman/answers-p373.md` already holds the answers for problems 90–109
(§§ 3–4), so those need no new request.

## `lectures/`

Lecture notes from the course lecturer land here as they arrive, named
`NN-topic.*` to line up with seminar numbers. When preparing a seminar, check
the matching lecture first — notation and the order of results in the exercises
should follow the lecture, not a textbook's own conventions.

## `src/mephi_stats/`

Build-side Python, installed as an editable package by `uv sync`:
`schedule.py` (semester dates, used by the schedule table in `index.qmd`).
It is **not** for chapter code — chapters define their helpers inline (see
«Explicit Python»).
