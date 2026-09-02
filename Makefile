# Сборка материалов. Переменная N — номер семинара, например: make prep N=01

VENV := uv run
SEM  := $(wildcard seminars/$(N)-*/seminar-$(N).qmd)

.PHONY: help prep handout all clean lint test new

help:  ## показать список целей
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*##/\t/' | expand -t 12

prep:  ## HTML с решениями для подготовки: make prep N=01
	$(VENV) quarto render $(SEM) --profile prep --to html

handout:  ## PDF-раздатка для студентов: make handout N=01
	$(VENV) quarto render $(SEM) --to pdf

all:  ## собрать весь проект (PDF-раздатки + index.html)
	$(VENV) quarto render

new:  ## новый семинар из шаблона: make new N=02 SLUG=conditional-probability
	@test -n "$(N)" && test -n "$(SLUG)" || { echo "Нужны N и SLUG"; exit 1; }
	mkdir -p seminars/$(N)-$(SLUG)
	sed "s/Семинар NN/Семинар $(N)/" _templates/seminar.qmd \
	  > seminars/$(N)-$(SLUG)/seminar-$(N).qmd
	@echo "Создан seminars/$(N)-$(SLUG)/seminar-$(N).qmd — впишите тему и дату"

lint:  ## проверить python-код
	$(VENV) ruff check .
	$(VENV) ruff format --check .

test:  ## прогнать тесты
	$(VENV) pytest

clean:  ## удалить сборку и кеш freeze
	rm -rf _output .quarto _freeze
