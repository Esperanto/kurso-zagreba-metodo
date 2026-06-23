#!/usr/bin/env python

import yaml
from yaml.constructor import ConstructorError

from .generu import legi_yaml, YAML_LOADER


def fail(message):
    raise SystemExit('YAML-kontrolo malsukcesis: ' + message)


def require(condition, message):
    if not condition:
        fail(message)


def collect_values(data, key):
    if isinstance(data, dict):
        for item_key, value in data.items():
            if item_key == key:
                yield value
            yield from collect_values(value, key)
    elif isinstance(data, list):
        for item in data:
            yield from collect_values(item, key)


def check_safe_yaml_loader_blocks_python_tags():
    try:
        yaml.load('x: !!python/name:os.system\n', Loader=YAML_LOADER)
    except ConstructorError:
        return
    fail('la sekura YAML-loader akceptis Python-specifan YAML-etikedon')


def check_bool_like_scalars():
    data = yaml.load(
        (
            'yes_value: yes\n'
            'no_value: no\n'
            'on_value: on\n'
            'off_value: off\n'
            'true_value: true\n'
            'false_value: false\n'
            'quoted_no: "no"\n'
        ),
        Loader=YAML_LOADER
    )
    require(data['yes_value'] is True, 'unquoted yes ne fariĝis True')
    require(data['no_value'] is False, 'unquoted no ne fariĝis False')
    require(data['on_value'] is True, 'unquoted on ne fariĝis True')
    require(data['off_value'] is False, 'unquoted off ne fariĝis False')
    require(data['true_value'] is True, 'unquoted true ne fariĝis True')
    require(data['false_value'] is False, 'unquoted false ne fariĝis False')
    require(data['quoted_no'] == 'no', 'quoted "no" ne restis teksto')


def check_malagasy_no_values():
    checks = [
        ('enhavo/tradukenda/mg/ekzercoj/traduku-kaj-respondu/04.yml', 'estas'),
        ('enhavo/tradukenda/mg/ekzercoj/traduku-kaj-respondu/07.yml', 'estas'),
        ('enhavo/tradukenda/mg/ekzercoj/traduku-kaj-respondu/09.yml', 'havus'),
    ]
    for path, key in checks:
        values = list(collect_values(legi_yaml(path), key))
        require('no' in values, path + ' ne enhavas tekstan "no" por ' + key)
        require(False not in values, path + ' ankoraŭ enhavas bulean False por ' + key)


def main():
    check_safe_yaml_loader_blocks_python_tags()
    check_bool_like_scalars()
    check_malagasy_no_values()
    print('Sukcesis: kontrolis sekuran YAML-legadon')


if __name__ == '__main__':
    main()
