#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import sys


# Replace fonto/py on sys.path to avoid shadowing Python's stdlib html package.
sys.path[0] = str(Path(__file__).resolve().parents[2])

from fonto.py.normaligu_md import main


if __name__ == '__main__':
    main()
