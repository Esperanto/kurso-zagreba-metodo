.PHONY: help venv install install-ui pip-tools lock lock-upgrade bundle check check-yaml check-yaml-normalized check-md-normalized check-ui check-pwa html html-all md normalize-yaml normalize-md serve clean

LINGVO_ORIGIN := $(origin LINGVO)
LINGVO ?= en
HOST ?= 127.0.0.1
PORT ?= 8000
OUTPUT_DIR ?= eligo/retejo
NODE_MODULES ?= node_modules
NPM ?= npm
VENV ?= venv
SYSTEM_PYTHON ?= python3
PYTHON ?= $(VENV)/bin/python
YAML_SCHEMA_LINTER ?= $(VENV)/bin/check-jsonschema
TRADUKENDA_SCHEMA_DIR ?= skemoj/tradukenda
PIP_TOOLS ?= pip-tools==7.5.3
REQUESTED_LINGVO := $(if $(filter command line,$(LINGVO_ORIGIN)),$(LINGVO),)
CHECK_FORMAT_LINGVO ?= $(REQUESTED_LINGVO)
CHECK_FORMAT_PATH := $(if $(CHECK_FORMAT_LINGVO),enhavo/tradukenda/$(CHECK_FORMAT_LINGVO),enhavo)
CHECK_YAML_LINGVO ?= $(REQUESTED_LINGVO)
CHECK_YAML_TRADUKENDA_GLOB := enhavo/tradukenda/$(if $(CHECK_YAML_LINGVO),$(CHECK_YAML_LINGVO),*)
CHECK_YAML_TRADUKENDA_FIND_ROOT := $(if $(CHECK_YAML_LINGVO),enhavo/tradukenda/$(CHECK_YAML_LINGVO),enhavo/tradukenda)
CHECK_YAML_SUCCESS := $(if $(CHECK_YAML_LINGVO),Sukcesis: kontrolis YAML-dosierojn por $(CHECK_YAML_LINGVO),Sukcesis: kontrolis YAML-dosierojn)
CHECK_PWA_LINGVO ?= $(REQUESTED_LINGVO)
CHECK_PWA_ARGS := $(if $(CHECK_PWA_LINGVO),--lingvo $(CHECK_PWA_LINGVO),)
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
		'  make check           Kontrolas anglan Markdown-, HTML- kaj Anki-eligon' \
		'  make check-yaml      Kontrolas YAML-dosierojn per sekura legado kaj skemoj; kun LINGVO=de nur unu lingvon' \
		'  make check-yaml-normalized  Kontrolas YAML-formaton sub enhavo/; kun LINGVO=de nur unu lingvon' \
		'  make check-md-normalized    Kontrolas Markdown-formaton sub enhavo/; kun LINGVO=de nur unu lingvon' \
		'  make check-ui        Kontrolas anglajn UI-interagojn per Playwright' \
		'  make check-pwa       Kontrolas PWA-manifeston kaj kompletan offline-liston; kun LINGVO=de nur unu lingvon' \
		'  make html LINGVO=en  Generas HTML por unu lingvo' \
		'  make html-all        Generas HTML por publikaj kaj testaj lingvoj' \
		'  make md LINGVO=en    Generas Markdown por unu lingvo' \
		'  make normalize-yaml  Normaligas YAML-dosierojn sub enhavo/' \
		'  make normalize-md    Normaligas Markdown-dosierojn sub enhavo/' \
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
		&& test -f "$(NODE_MODULES)/typeahead.js/dist/typeahead.bundle.min.js" || { printf '%s\n' 'Mankas npm-dependecoj en $(NODE_MODULES). Rulu `make install` unue.' >&2; exit 1; }
	@"$(PYTHON)" -c 'import yaml, jinja2, chevron, mistune, genanki'
	@$(MAKE) --no-print-directory clean
	@mkdir -p "$(dir $(MD_OUT))"
	@$(MAKE) --no-print-directory md LINGVO="$(CHECK_LINGVO)" >"$(MD_OUT)"
	@$(MAKE) --no-print-directory html LINGVO="$(CHECK_LINGVO)"
	@"$(PYTHON)" -m fonto.py.kontrolu_eligon --lingvo "$(CHECK_LINGVO)" --md-out "$(MD_OUT)" --output-dir "$(OUTPUT_DIR)"

check-yaml:
	@test -x "$(PYTHON)" || { printf '%s\n' 'Mankas $(PYTHON). Rulu `make install` unue aŭ agordu VENV=/path/to/venv.' >&2; exit 1; }
	@test -z "$(CHECK_YAML_LINGVO)" || test -d "$(CHECK_YAML_TRADUKENDA_FIND_ROOT)" || { printf '%s\n' 'Nekonata lingvo por YAML-kontrolo: $(CHECK_YAML_LINGVO)' >&2; exit 1; }
	@"$(PYTHON)" -m fonto.py.kontrolu_yaml
	@test -x "$(YAML_SCHEMA_LINTER)" || { printf '%s\n' 'Mankas $(YAML_SCHEMA_LINTER). Rulu `make install` unue.' >&2; exit 1; }
	@printf '%s' 'startis fasado-skemoj... '
	@eligo=$$("$(YAML_SCHEMA_LINTER)" --schemafile "$(TRADUKENDA_SCHEMA_DIR)/fasado.schema.yml" $(CHECK_YAML_TRADUKENDA_GLOB)/fasado/*.yml 2>&1) || { printf '\n%s\n' "$$eligo"; exit 1; }
	@printf '%s\n' 'bone'
	@printf '%s' 'startis vortaro-skemoj... '
	@eligo=$$("$(YAML_SCHEMA_LINTER)" --schemafile "$(TRADUKENDA_SCHEMA_DIR)/vortaro.schema.yml" $(CHECK_YAML_TRADUKENDA_GLOB)/vortaro/*.yml 2>&1) || { printf '\n%s\n' "$$eligo"; exit 1; }
	@printf '%s\n' 'bone'
	@printf '%s' 'startis specifaj vortaro-skemoj... '
	@for dosiero in $(CHECK_YAML_TRADUKENDA_GLOB)/vortaro/*.yml; do \
		nomo=$$(basename "$$dosiero" .yml); \
		skemo="$(TRADUKENDA_SCHEMA_DIR)/vortaro/$${nomo}.schema.yml"; \
		test -f "$$skemo" || { printf '\nMankas vortaro-skemo por %s: %s\n' "$$dosiero" "$$skemo"; exit 1; }; \
	done
	@for skemo in "$(TRADUKENDA_SCHEMA_DIR)"/vortaro/*.schema.yml; do \
		nomo=$$(basename "$$skemo" .schema.yml); \
		dosieroj=$$(find "$(CHECK_YAML_TRADUKENDA_FIND_ROOT)" -path "*/vortaro/$${nomo}.yml" -type f | sort); \
		test -n "$$dosieroj" || continue; \
		eligo=$$("$(YAML_SCHEMA_LINTER)" --schemafile "$$skemo" $$dosieroj 2>&1) || { printf '\n%s\n' "$$eligo"; exit 1; }; \
	done
	@printf '%s\n' 'bone'
	@printf '%s' 'startis traduku-skemoj... '
	@for leciono in 01 02 03 04 05 06 07 08 09 10 11 12; do \
		eligo=$$("$(YAML_SCHEMA_LINTER)" --schemafile "$(TRADUKENDA_SCHEMA_DIR)/traduku/$${leciono}.schema.yml" $(CHECK_YAML_TRADUKENDA_GLOB)/ekzercoj/traduku/$${leciono}.yml 2>&1) || { printf '\n%s\n' "$$eligo"; exit 1; }; \
	done
	@printf '%s\n' 'bone'
	@printf '%s' 'startis traduku-kaj-respondu-skemoj... '
	@for leciono in 01 02 03 04 05 06 07 08 09 10 11 12; do \
		eligo=$$("$(YAML_SCHEMA_LINTER)" --schemafile "$(TRADUKENDA_SCHEMA_DIR)/traduku-kaj-respondu/$${leciono}.schema.yml" $(CHECK_YAML_TRADUKENDA_GLOB)/ekzercoj/traduku-kaj-respondu/$${leciono}.yml 2>&1) || { printf '\n%s\n' "$$eligo"; exit 1; }; \
	done
	@printf '%s\n' 'bone'
	@printf '%s\n' '$(CHECK_YAML_SUCCESS)'

check-yaml-normalized:
	@test -x "$(PYTHON)" || { printf '%s\n' 'Mankas $(PYTHON). Rulu `make install` unue aŭ agordu VENV=/path/to/venv.' >&2; exit 1; }
	@test -z "$(CHECK_FORMAT_LINGVO)" || test -d "$(CHECK_FORMAT_PATH)" || { printf '%s\n' 'Nekonata lingvo por YAML-formata kontrolo: $(CHECK_FORMAT_LINGVO)' >&2; exit 1; }
	@"$(PYTHON)" -m fonto.py.normaligu_yaml --kontrolu "$(CHECK_FORMAT_PATH)"

check-md-normalized:
	@test -x "$(PYTHON)" || { printf '%s\n' 'Mankas $(PYTHON). Rulu `make install` unue aŭ agordu VENV=/path/to/venv.' >&2; exit 1; }
	@test -z "$(CHECK_FORMAT_LINGVO)" || test -d "$(CHECK_FORMAT_PATH)" || { printf '%s\n' 'Nekonata lingvo por Markdown-formata kontrolo: $(CHECK_FORMAT_LINGVO)' >&2; exit 1; }
	@"$(PYTHON)" -m fonto.py.normaligu_md --kontrolu "$(CHECK_FORMAT_PATH)"

check-ui:
	@test -x "$(PYTHON)" || { printf '%s\n' 'Mankas $(PYTHON). Rulu `make install` unue aŭ agordu VENV=/path/to/venv.' >&2; exit 1; }
	@test -f "$(NODE_MODULES)/.bin/playwright" || { printf '%s\n' 'Mankas Playwright en $(NODE_MODULES). Rulu `make install` unue.' >&2; exit 1; }
	@$(MAKE) --no-print-directory clean
	@$(MAKE) --no-print-directory html LINGVO="$(CHECK_LINGVO)"
	@$(MAKE) --no-print-directory html LINGVO="no"
	@"$(NPM)" exec -- playwright test

check-pwa:
	@"$(PYTHON)" -m fonto.py.kontrolu_pwa --output-dir "$(OUTPUT_DIR)" $(CHECK_PWA_ARGS)

bundle:
	@test -d "$(NODE_MODULES)/esbuild" || { printf '%s\n' 'Mankas esbuild en $(NODE_MODULES). Rulu `make install` unue.' >&2; exit 1; }
	@"$(NPM)" run --silent bundle

html: bundle
	@"$(PYTHON)" -m fonto.py.generu --lingvo "$(LINGVO)" --eligformo html

html-all: bundle
	@"$(PYTHON)" -m fonto.py.generu --cxiuj-lingvoj --eligformo html

md:
	@"$(PYTHON)" -m fonto.py.generu --lingvo "$(LINGVO)" --eligformo md

normalize-yaml:
	@test -x "$(PYTHON)" || { printf '%s\n' 'Mankas $(PYTHON). Rulu `make install` unue aŭ agordu VENV=/path/to/venv.' >&2; exit 1; }
	@"$(PYTHON)" -m fonto.py.normaligu_yaml enhavo

normalize-md:
	@test -x "$(PYTHON)" || { printf '%s\n' 'Mankas $(PYTHON). Rulu `make install` unue aŭ agordu VENV=/path/to/venv.' >&2; exit 1; }
	@"$(PYTHON)" -m fonto.py.normaligu_md enhavo

serve:
	@"$(PYTHON)" -m http.server "$(PORT)" --bind "$(HOST)" --directory "$(OUTPUT_DIR)"

clean:
	@test -n "$(OUTPUT_DIR)" && test "$(OUTPUT_DIR)" != "/" || { printf '%s\n' 'OUTPUT_DIR estas nesekura por forigo.' >&2; exit 1; }
	@rm -rf "$(OUTPUT_DIR)"
	@printf 'Forigis %s\n' "$(OUTPUT_DIR)"
