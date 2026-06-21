.PHONY: help venv install check html html-all md

LINGVO ?= en
HTML_LINGVOJ ?= ar ca cs da de el en es fa fr frp ga he hi hr hu id it ja kk km ko lo mg ms my nl pl pt ro ru sk sl sv sw th tr uk ur vi yo zh zh-tw
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
		'  make md LINGVO=en    Generas Markdown por unu lingvo'

venv:
	@if [ ! -x "$(PYTHON)" ]; then \
		"$(SYSTEM_PYTHON)" -m venv "$(VENV)"; \
	fi

install: venv
	@"$(PYTHON)" -m pip install -r requirements.txt

check:
	@test -x "$(PYTHON)" || { printf '%s\n' 'Mankas $(PYTHON). Rulu `make install` unue aŭ agordu VENV=/path/to/venv.' >&2; exit 1; }
	@"$(PYTHON)" -c 'import yaml, jinja2, chevron, mistune'
	@"$(PYTHON)" generate.py --lingvo "$(LINGVO)" --eligformo md >"$(MD_OUT)"
	@printf 'Sukcesis: generis Markdown por %s al %s\n' "$(LINGVO)" "$(MD_OUT)"

html:
	@"$(PYTHON)" generate.py --lingvo "$(LINGVO)" --eligformo html

html-all:
	@set -e; for lingvo in $(HTML_LINGVOJ); do \
		printf 'Generas HTML por %s\n' "$$lingvo"; \
		"$(PYTHON)" generate.py --lingvo "$$lingvo" --eligformo html; \
	done

md:
	@"$(PYTHON)" generate.py --lingvo "$(LINGVO)" --eligformo md
