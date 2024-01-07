from argparse import ArgumentParser
from os import listdir
from os.path import join, isdir, splitext
from re import match


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
        return bool(match(self._arguments[argument_key], string))

    def _get_loc(self, folder: str) -> int:
        lines_of_code = 0
        for item in listdir(folder):
            item_path = join(folder, item)
            if isdir(item_path):
                if self._is_match('exclude_dirs', item_path):
                    continue
                lines_of_code += self._get_loc(item_path)
            else:
                if self._is_match('exclude_exts', 
                                  splitext(item)[1]):
                    continue
                if self._is_match('exclude_files', item_path):
                    continue
                lines_of_code += len(
                    open(item_path, 
                         encoding='utf-8',
                         errors='ignore').readlines())          

        return lines_of_code

    def get(self) -> int:
        return self._get_loc(self._arguments['path'])


def main():
    loc = LinesOfCode()

    loc.parse_arguments()
    print(loc.get())


if __name__ == '__main__':
    main()
