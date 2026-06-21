.PHONY: help venv install check html html-all md serve clean

LINGVO ?= en
HTML_LINGVOJ ?= ar ca cs da de el en es fa fr frp ga he hi hr hu id it ja kk km ko lo mg ms my nl pl pt ro ru sk sl sv sw th tr uk ur vi yo zh zh-tw
HOST ?= 127.0.0.1
PORT ?= 8000
OUTPUT_DIR ?= eligo/retejo
VENV ?= venv
SYSTEM_PYTHON ?= python3
PYTHON ?= $(VENV)/bin/python
TMPDIR ?= /tmp
TMP_ROOT := $(patsubst %/,%,$(TMPDIR))
MD_OUT ?= $(TMP_ROOT)/leo-$(LINGVO).md

help:
	@printf '%s\n' \
		'Celoj:' \
		'  make venv            Kreas venv-on, defaŭlte VENV=venv' \
		'  make install         Kreas venv-on kaj instalas requirements' \
		'  make check           Rulas sekuran provan kontrolon, defaŭlte LINGVO=en' \
		'  make html LINGVO=en  Generas HTML por unu lingvo' \
		'  make html-all        Generas HTML por ĉiuj produktadaj lingvoj' \
		'  make md LINGVO=en    Generas Markdown por unu lingvo' \
		'  make serve           Servas HTML loke ĉe http://127.0.0.1:8000' \
		'  make clean           Forigas generitan HTML-eligon'

venv:
	@if [ ! -x "$(PYTHON)" ]; then \
		"$(SYSTEM_PYTHON)" -m venv "$(VENV)"; \
	fi

install: venv
	@"$(PYTHON)" -m pip install -r requirements.txt

check:
	@test -x "$(PYTHON)" || { printf '%s\n' 'Mankas $(PYTHON). Rulu `make install` unue aŭ agordu VENV=/path/to/venv.' >&2; exit 1; }
	@"$(PYTHON)" -c 'import yaml, jinja2, chevron, mistune'
	@"$(PYTHON)" -m fonto.py.generu --lingvo "$(LINGVO)" --eligformo md >"$(MD_OUT)"
	@printf 'Sukcesis: generis Markdown por %s al %s\n' "$(LINGVO)" "$(MD_OUT)"

html:
	@"$(PYTHON)" -m fonto.py.generu --lingvo "$(LINGVO)" --eligformo html

html-all:
	@set -e; for lingvo in $(HTML_LINGVOJ); do \
		printf 'Generas HTML por %s\n' "$$lingvo"; \
		"$(PYTHON)" -m fonto.py.generu --lingvo "$$lingvo" --eligformo html; \
	done

md:
	@"$(PYTHON)" -m fonto.py.generu --lingvo "$(LINGVO)" --eligformo md

serve:
	@"$(PYTHON)" -m http.server "$(PORT)" --bind "$(HOST)" --directory "$(OUTPUT_DIR)"

clean:
	@test -n "$(OUTPUT_DIR)" && test "$(OUTPUT_DIR)" != "/" || { printf '%s\n' 'OUTPUT_DIR estas nesekura por forigo.' >&2; exit 1; }
	@rm -rf "$(OUTPUT_DIR)"
	@printf 'Forigis %s\n' "$(OUTPUT_DIR)"
