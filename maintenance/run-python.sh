#!/usr/bin/env sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$script_dir/.."

python_bin=${PYTHON:-}

if [ -z "$python_bin" ]; then
	if [ -x venv/bin/python ]; then
		python_bin=venv/bin/python
	elif [ -x .venv/bin/python ]; then
		python_bin=.venv/bin/python
	elif command -v python3 >/dev/null 2>&1; then
		python_bin=$(command -v python3)
	elif command -v python >/dev/null 2>&1; then
		python_bin=$(command -v python)
	else
		printf '%s\n' 'No Python interpreter found. Create venv/ or set PYTHON=/path/to/python.' >&2
		exit 1
	fi
fi

exec "$python_bin" "$@"
