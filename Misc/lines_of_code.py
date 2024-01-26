from argparse import ArgumentParser
from os import listdir
from os.path import join, isdir, splitext
from re import fullmatch


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

    def _is_match(self, argument_key: str, string: str) -> bool:
        pattern = self._arguments[argument_key]
        return pattern and fullmatch(pattern, string) is not None

    def _get_lines_of_code(self, folder: str, indent: str) -> int:
        lines_of_code = 0

        try:
            items = listdir(folder)
        except Exception:
            return 0

        n_items = len(items)

        for i, item in enumerate(items):
            item_path = join(folder, item)

            is_last = i == n_items - 1
            prefix = '└───' if is_last else '├───'
            next_indent = '    ' if is_last else '│   '

            if isdir(item_path):
                if self._is_match('exclude_dirs', item):
                    continue

                print(f'{indent}{prefix}{item}')

                lines_of_code += self._get_lines_of_code(
                    item_path, indent + next_indent)
                continue

            if self._is_match('exclude_exts', splitext(item)[1]):
                continue
            if self._is_match('exclude_files', item):
                continue

            try:
                with open(item_path, 'r', encoding='utf-8') as f:
                    file_lines_of_code = len(f.readlines())
            except Exception:
                continue

            print(f'{indent}{prefix}{item}: {file_lines_of_code} '
                  'lines of code')

            lines_of_code += file_lines_of_code

        return lines_of_code

    def get(self):
        loc = self._get_lines_of_code(self._arguments['path'], '')
        print(f'\nTotal {loc} lines of code')


def main():
    loc = LinesOfCode()

    loc.parse_arguments()
    loc.get()


if __name__ == '__main__':
    main()
