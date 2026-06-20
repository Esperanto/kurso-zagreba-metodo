.PHONY: help venv install check html md

LINGVO ?= en
VENV ?= venv
SYSTEM_PYTHON ?= python3
PYTHON ?= $(VENV)/bin/python
TMPDIR ?= /tmp
TMP_ROOT := $(patsubst %/,%,$(TMPDIR))
MD_OUT ?= $(TMP_ROOT)/leo-$(LINGVO).md

help:
	@printf '%s\n' \
		'Targets:' \
		'  make venv            Create venv, default VENV=venv' \
		'  make install         Create venv and install requirements' \
		'  make check           Run the safe smoke test, default LINGVO=en' \
		'  make html LINGVO=en  Generate HTML for one language' \
		'  make md LINGVO=en    Generate Markdown for one language'

venv:
	@if [ ! -x "$(PYTHON)" ]; then \
		"$(SYSTEM_PYTHON)" -m venv "$(VENV)"; \
	fi

install: venv
	@"$(PYTHON)" -m pip install -r requirements.txt

check:
	@test -x "$(PYTHON)" || { printf '%s\n' 'Missing $(PYTHON). Run `make install` first or set VENV=/path/to/venv.' >&2; exit 1; }
	@"$(PYTHON)" -c 'import yaml, jinja2, chevron, mistune'
	@"$(PYTHON)" generate.py --lingvo "$(LINGVO)" --eligformo md >"$(MD_OUT)"
	@printf 'OK: generated Markdown for %s at %s\n' "$(LINGVO)" "$(MD_OUT)"

html:
	@"$(PYTHON)" generate.py --lingvo "$(LINGVO)" --eligformo html

md:
	@"$(PYTHON)" generate.py --lingvo "$(LINGVO)" --eligformo md
