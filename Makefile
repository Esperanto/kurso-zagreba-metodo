.PHONY: help check html md

LINGVO ?= en

help:
	@printf '%s\n' \
		'Targets:' \
		'  make check          Run the safe smoke test, default LINGVO=en' \
		'  make html LINGVO=en Generate HTML for one language' \
		'  make md LINGVO=en   Generate Markdown for one language'

check:
	@maintenance/check.sh "$(LINGVO)"

html:
	@maintenance/run-python.sh generate.py --lingvo "$(LINGVO)" --eligformo html

md:
	@maintenance/run-python.sh generate.py --lingvo "$(LINGVO)" --eligformo md
