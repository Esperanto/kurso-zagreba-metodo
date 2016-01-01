# -*- coding: utf-8 -*-

import yaml

filenames = [
    'enhavo/tradukenda/de/gramatiko/01.yml',
    'enhavo/tradukenda/de/ekzercoj/01.yml', 
    'enhavo/netradukenda/tekstoj/01.yml', 
    'enhavo/netradukenda/ekzercoj/01.yml', 
]
for filename in filenames:
    print filename 
    d = yaml.load(file(filename, 'r'))
    print d
    print
