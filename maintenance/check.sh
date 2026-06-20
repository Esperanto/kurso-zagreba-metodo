#!/usr/bin/env sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$script_dir/.."

language=${1:-${LINGVO:-en}}
tmp_dir=${TMPDIR:-/tmp}
md_out="$tmp_dir/leo-${language}.md"

maintenance/run-python.sh -c 'import yaml, jinja2, chevron, mistune'
maintenance/run-python.sh generate.py --lingvo "$language" --eligformo md >"$md_out"

printf 'OK: generated Markdown for %s at %s\n' "$language" "$md_out"
