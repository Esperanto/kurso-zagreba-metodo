#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fonto.py.normaligu_yaml import main


if __name__ == '__main__':
    main()
