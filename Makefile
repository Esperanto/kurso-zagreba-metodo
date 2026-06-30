.PHONY: help venv install install-ui pip-tools lock lock-upgrade check check-ui check-pwa html html-all md serve clean

LINGVO ?= en
HTML_LINGVOJ ?= ar ca cs da de el en es fa fr frp ga he hi hr hu id it ja kk km ko lo mg ms my nl pl pt ro ru sk sl sv sw th tok tr uk ur vi yo zh zh-tw
HOST ?= 127.0.0.1
PORT ?= 8000
OUTPUT_DIR ?= eligo/retejo
NODE_MODULES ?= node_modules
NPM ?= npm
VENV ?= venv
SYSTEM_PYTHON ?= python3
PYTHON ?= $(VENV)/bin/python
PIP_TOOLS ?= pip-tools==7.5.3
CHECK_LINGVO := en
MD_OUT ?= eligo/md/$(CHECK_LINGVO).md

help:
	@printf '%s\n' \
		'Celoj:' \
		'  make venv            Kreas venv-on, defaŭlte VENV=venv' \
		'  make install         Kreas venv-on kaj instalas Python- kaj npm-dependecojn' \
		'  make install-ui      Instalas Chromium por Playwright-testoj' \
		'  make lock            Rekreas requirements.txt el requirements.in' \
		'  make lock-upgrade    Ĝisdatigas ĉiujn ŝlositajn Python-dependecojn' \
		'  make check           Purigas kaj kontrolas anglan Markdown-, HTML- kaj Anki-eligon' \
		'  make check-ui        Kontrolas anglajn UI-interagojn per Playwright' \
		'  make check-pwa       Kontrolas PWA-manifeston kaj kompletan offline-liston' \
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
	@"$(NPM)" ci --ignore-scripts

install-ui:
	@"$(NPM)" exec -- playwright install chromium

pip-tools: venv
	@"$(PYTHON)" -m pip install "$(PIP_TOOLS)"

lock: pip-tools
	@"$(PYTHON)" -m piptools compile --strip-extras --output-file requirements.txt requirements.in

lock-upgrade: pip-tools
	@"$(PYTHON)" -m piptools compile --upgrade --strip-extras --output-file requirements.txt requirements.in

check:
	@test -x "$(PYTHON)" || { printf '%s\n' 'Mankas $(PYTHON). Rulu `make install` unue aŭ agordu VENV=/path/to/venv.' >&2; exit 1; }
	@test -f "$(NODE_MODULES)/bootstrap/dist/css/bootstrap.min.css" \
		&& test -f "$(NODE_MODULES)/bootstrap/dist/js/bootstrap.bundle.min.js" \
		&& test -f "$(NODE_MODULES)/jquery/dist/jquery.min.js" \
		&& test -f "$(NODE_MODULES)/jquery-ui-dist/jquery-ui.min.js" \
		&& test -f "$(NODE_MODULES)/typeahead.js/dist/typeahead.bundle.min.js" || { printf '%s\n' 'Mankas npm-dependecoj en $(NODE_MODULES). Rulu `make install` unue.' >&2; exit 1; }
	@"$(PYTHON)" -c 'import yaml, jinja2, chevron, mistune, genanki'
	@"$(PYTHON)" -m fonto.py.kontrolu_yaml
	@$(MAKE) --no-print-directory clean
	@mkdir -p "$(dir $(MD_OUT))"
	@$(MAKE) --no-print-directory md LINGVO="$(CHECK_LINGVO)" >"$(MD_OUT)"
	@$(MAKE) --no-print-directory html LINGVO="$(CHECK_LINGVO)"
	@"$(PYTHON)" -m fonto.py.kontrolu_eligon --lingvo "$(CHECK_LINGVO)" --md-out "$(MD_OUT)" --output-dir "$(OUTPUT_DIR)"

check-ui:
	@test -x "$(PYTHON)" || { printf '%s\n' 'Mankas $(PYTHON). Rulu `make install` unue aŭ agordu VENV=/path/to/venv.' >&2; exit 1; }
	@test -f "$(NODE_MODULES)/.bin/playwright" || { printf '%s\n' 'Mankas Playwright en $(NODE_MODULES). Rulu `make install` unue.' >&2; exit 1; }
	@$(MAKE) --no-print-directory clean
	@$(MAKE) --no-print-directory html LINGVO="$(CHECK_LINGVO)"
	@"$(NPM)" exec -- playwright test

check-pwa:
	@"$(PYTHON)" -m fonto.py.kontrolu_pwa --output-dir "$(OUTPUT_DIR)" --lingvoj $(HTML_LINGVOJ)

html:
	@"$(PYTHON)" -m fonto.py.generu --lingvo "$(LINGVO)" --eligformo html

html-all:
	@"$(PYTHON)" -m fonto.py.generu --lingvoj $(HTML_LINGVOJ) --eligformo html

md:
	@"$(PYTHON)" -m fonto.py.generu --lingvo "$(LINGVO)" --eligformo md

serve:
	@"$(PYTHON)" -m http.server "$(PORT)" --bind "$(HOST)" --directory "$(OUTPUT_DIR)"

clean:
	@test -n "$(OUTPUT_DIR)" && test "$(OUTPUT_DIR)" != "/" || { printf '%s\n' 'OUTPUT_DIR estas nesekura por forigo.' >&2; exit 1; }
	@rm -rf "$(OUTPUT_DIR)"
	@printf 'Forigis %s\n' "$(OUTPUT_DIR)"
