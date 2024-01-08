from argparse import ArgumentParser
from os import listdir
from os.path import join, isdir, splitext
from re import search


class LinesOfCode:
    def __init__(self):
        self._arguments = {}

    def parse_arguments(self):
        parser = ArgumentParser(
            description='Get lines of code in a project')

        parser.add_argument(
            'path',
            type=str,
            help='Specify the project path')
        parser.add_argument(
            '-f',
            dest='exclude_files',
            type=str,
            help='Specify the exclude pattern for files')
        parser.add_argument(
            '-x',
            dest='exclude_exts',
            type=str,
            help='Specify the exclude pattern for file extensions')
        parser.add_argument(
            '-d',
            dest='exclude_dirs',
            type=str,
            help='Specify the exclude pattern for directories')

        args = parser.parse_args()
        self._arguments = {
            'path': args.path,
            'exclude_files': args.exclude_files or '',
            'exclude_exts': args.exclude_exts or '',
            'exclude_dirs': args.exclude_dirs or ''
        }

    def _is_match(self, argument_key, string):
        pattern = self._arguments[argument_key]
        return pattern and search(pattern, string)

    def _get_loc(self, folder: str, indent: str) -> tuple[int, list[str]]:
        logs = []

        lines_of_code = 0

        items = listdir(folder)
        n_items = len(items)

        for i, item in enumerate(items):
            item_path = join(folder, item)

            is_last = i == n_items - 1
            prefix = '└───' if is_last else '├───'
            next_indent = '    ' if is_last else '│   '

            if isdir(item_path):
                if self._is_match('exclude_dirs', item_path):
                    continue

                logs.append(f'{indent}{prefix}{item}')

                next_lines_of_code, next_logs = self._get_loc(
                    item_path, indent + next_indent)
                lines_of_code += next_lines_of_code
                logs += next_logs
                continue

            if self._is_match('exclude_exts', splitext(item)[1]):
                continue
            if self._is_match('exclude_files', item_path):
                continue

            with open(item_path, encoding='utf-8', errors='ignore') as f:
                file_lines_of_code = len(f.readlines())

            logs.append(f'{indent}{prefix}{item}: {file_lines_of_code} '
                        'lines of code')

            lines_of_code += file_lines_of_code

        return lines_of_code, logs

    def get(self) -> int:
        loc, logs = self._get_loc(self._arguments['path'], '')
        return [*logs, f'\nTotal: {loc} lines of code']


def main():
    loc = LinesOfCode()

    loc.parse_arguments()
    logs = loc.get()
    print('\n'.join(logs))


if __name__ == '__main__':
    main()
