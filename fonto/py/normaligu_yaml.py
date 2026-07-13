# -*- coding: utf-8 -*-

import argparse
import difflib
from pathlib import Path
import sys

import yaml


YAML_EXTENSIONS = {'.yaml', '.yml'}


class DuplicateKeyError(ValueError):
    pass


class UniqueKeyLoader(yaml.SafeLoader):
    pass


class NormalizingDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def construct_unique_mapping(loader, node, deep=False):
    seen = {}
    for key_node, _value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in seen:
            first_mark = seen[key]
            second_mark = key_node.start_mark
            raise DuplicateKeyError(
                f'duobla ŝlosilo {key!r} en {second_mark.name}:'
                f'{second_mark.line + 1}; unua apero en linio '
                f'{first_mark.line + 1}'
            )
        seen[key] = key_node.start_mark
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


def represent_none(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:null', '')


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_unique_mapping,
)
NormalizingDumper.add_representer(type(None), represent_none)


def yaml_paths(paths):
    result = []
    for path in paths:
        path = Path(path)
        if path.is_dir():
            result.extend(
                file_path
                for file_path in path.rglob('*')
                if file_path.is_file() and file_path.suffix in YAML_EXTENSIONS
            )
        elif path.is_file() and path.suffix in YAML_EXTENSIONS:
            result.append(path)
        else:
            raise SystemExit(f'Ne estas YAML-dosiero aŭ dosierujo: {path}')
    return sorted(set(result))


def read_yaml(path):
    with path.open(encoding='utf-8-sig') as file:
        return yaml.load(file, Loader=UniqueKeyLoader)


def dump_yaml(data):
    text = yaml.dump(
        data,
        Dumper=NormalizingDumper,
        allow_unicode=True,
        default_flow_style=False,
        indent=2,
        sort_keys=False,
        width=4096,
    )
    return text if text.endswith('\n') else text + '\n'


def is_translated_vortaro_file(path):
    parts = path.parts
    for index in range(len(parts) - 4):
        if (
            parts[index] == 'enhavo'
            and parts[index + 1] == 'tradukenda'
            and parts[index + 3] == 'vortaro'
            and index + 5 == len(parts)
        ):
            return True
    return False


def sort_top_level_keys(data):
    if not isinstance(data, dict):
        return data
    return dict(sorted(data.items(), key=lambda item: (str(item[0]).casefold(), str(item[0]))))


def normalized_text(path):
    data = read_yaml(path)
    if is_translated_vortaro_file(path):
        data = sort_top_level_keys(data)
    text = dump_yaml(data)
    reparsed = yaml.load(text, Loader=UniqueKeyLoader)
    if reparsed != data:
        raise SystemExit(f'Normaligo ŝanĝus la YAML-datumojn: {path}')
    return text


def print_diff(path, old_text, new_text):
    diff = difflib.unified_diff(
        old_text.splitlines(keepends=True),
        new_text.splitlines(keepends=True),
        fromfile=str(path),
        tofile=str(path),
    )
    sys.stdout.writelines(diff)


def normalize_file(path, check=False, show_diff=False):
    old_text = path.read_text(encoding='utf-8-sig')
    new_text = normalized_text(path)
    if old_text == new_text:
        return False

    if show_diff:
        print_diff(path, old_text, new_text)

    if not check:
        path.write_text(new_text, encoding='utf-8')

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Normaligas YAML-dosierojn determinisme.'
    )
    parser.add_argument(
        'paths',
        nargs='*',
        default=['enhavo'],
        help='YAML-dosieroj aŭ dosierujoj; defaŭlte: enhavo',
    )
    parser.add_argument(
        '--kontrolu',
        '--check',
        action='store_true',
        dest='check',
        help='nur kontrolas, ĉu dosieroj jam estas normaligitaj',
    )
    parser.add_argument(
        '--diferenco',
        '--diff',
        action='store_true',
        dest='show_diff',
        help='montras unuecan diferencon por ŝanĝotaj dosieroj',
    )
    args = parser.parse_args()

    changed = []
    errors = []
    files = yaml_paths(args.paths)
    for path in files:
        try:
            if normalize_file(path, check=args.check, show_diff=args.show_diff):
                changed.append(path)
        except (DuplicateKeyError, OSError, yaml.YAMLError) as error:
            errors.append((path, error))

    if errors:
        print('Ne eblis normaligi kelkajn YAML-dosierojn:', file=sys.stderr)
        for path, error in errors:
            print(f'  {path}: {error}', file=sys.stderr)
        raise SystemExit(2)

    if args.check and changed:
        print('Nenormaligitaj YAML-dosieroj:', file=sys.stderr)
        for path in changed:
            print(f'  {path}', file=sys.stderr)
        raise SystemExit(1)

    verb = 'Ŝanĝiĝus' if args.check else 'Normaligis'
    for path in changed:
        print(f'{verb}: {path}')
    print(f'Kontrolis {len(files)} YAML-dosierojn; ŝanĝoj: {len(changed)}')


if __name__ == '__main__':
    main()
