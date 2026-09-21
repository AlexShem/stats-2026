# Сборка материалов. Переменная N — номер семинара, например: make handout N=01

VENV := uv run
SEM  := $(wildcard seminars/$(N)-*/seminar-$(N).qmd)

.PHONY: help book preview handout handouts all publish clean lint test new

help:  ## показать список целей
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*##/\t/' | expand -t 12

book:  ## книга для студентов (HTML): _output/book/
	$(VENV) quarto render

preview:  ## книга с автообновлением в браузере
	$(VENV) quarto preview

handout:  ## PDF-раздатка одного семинара: make handout N=01
	@test -n "$(SEM)" || { echo "Нет семинара с N=$(N)"; exit 1; }
	$(VENV) quarto render $(SEM) --profile handout --to pdf

handouts:  ## PDF-раздатки всех семинаров: _output/handouts/
	$(VENV) quarto render --profile handout --to pdf

all: book handouts  ## книга и все раздатки

publish: all  ## собрать всё и выложить на GitHub Pages (ветка gh-pages)
	rm -rf _output/book/handouts
	cp -r _output/handouts _output/book/handouts
	$(VENV) quarto publish gh-pages --no-render --no-prompt

new:  ## новый семинар из шаблона: make new N=03 SLUG=random-variables
	@test -n "$(N)" && test -n "$(SLUG)" || { echo "Нужны N и SLUG"; exit 1; }
	mkdir -p seminars/$(N)-$(SLUG)
	sed -e "s/Семинар NN/Семинар $$(expr $(N) + 0)/" -e "s/sNN-/s$(N)-/g" _templates/seminar.qmd \
	  > seminars/$(N)-$(SLUG)/seminar-$(N).qmd
	@echo "Создан seminars/$(N)-$(SLUG)/seminar-$(N).qmd — впишите тему и дату"
	@echo "и добавьте его в book.chapters в _quarto.yml"

lint:  ## проверить python-код
	$(VENV) ruff check .
	$(VENV) ruff format --check .

test:  ## прогнать тесты
	$(VENV) pytest

clean:  ## удалить сборку и кеш freeze
	rm -rf _output .quarto _freeze
