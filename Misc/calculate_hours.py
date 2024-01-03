from argparse import ArgumentParser
from markdown import markdown
from re import findall
from sys import exit
from typing import Any


class Parser:
    def __init__(self):
        self._parser = ArgumentParser(
            description='Find watch hours in markdown watchlists')

    def get_arguments(self) -> dict[str, Any]:
        self._parser.add_argument(
            '-f',
            type=str,
            dest='md_file',
            help='Specify the markdown file containing the watchlist')
        self._parser.add_argument(
            '-t',
            type=str,
            dest='text_pattern',
            help='Specify the text pattern containing the content info')
        self._parser.add_argument(
            '-s',
            type=str,
            dest='split_pattern',
            help='Specify the pattern to split content type and value')
        self._parser.add_argument(
            '-p',
            action='store_true',
            dest='print_html',
            help='Print as HTML content')

        args = self._parser.parse_args()

        if args.md_file is None:
            self.exit_on_error('Bad md_file')

        return {
            'md_file': args.md_file,
            'text_pattern': args.text_pattern,
            'split_pattern': args.split_pattern,
            'print_html': args.print_html
        }

    def exit_on_error(self, error_string):
        print(f'error: {error_string}', end='\n\n')
        self._parser.print_help()
        exit(1)

    def exit_on_success(self):
        exit(0)


parser = Parser()


def to_html(md_text: str) -> str:
    return markdown(md_text)


def find_content_info(html_content: str, text_pattern: str) -> list[str]:
    try:
        return findall(text_pattern, html_content)
    except Exception:
        parser.exit_on_error('Bad text_pattern')


def calculate_hours(content_types: list[str], split_pattern: str) -> float:
    total_hours = 0

    try:
        multipliers = {'Episode': 1 / 3, 'Movie': 3 / 2, 'Special': 1}
        for item in content_types:
            split_words = item.split(split_pattern)
            total_hours += int(split_words[1]) * multipliers[split_words[0]]
    except Exception:
        parser.exit_on_error('Bad split_pattern argument')

    return total_hours


def format_hours(hours: float) -> str:
    minutes_string = ''
    decimal_diff = hours - int(hours)
    if decimal_diff > 1e-5:
        minutes_string = f', {int(decimal_diff * 60)} minutes'

    return f'Watch time: {int(hours)} hours{minutes_string}'


def get_watch_time(md_text: str,
                   text_pattern=None,
                   split_pattern=None) -> str:

    text_pattern = text_pattern or r'Episode \d+|Movie \d+|Special \d+'
    split_pattern = split_pattern or ' '

    html_content = to_html(md_text)
    content_info = find_content_info(html_content, text_pattern)
    hours = calculate_hours(content_info, split_pattern)

    return format_hours(hours)


def main():
    arguments = parser.get_arguments()

    with open(arguments['md_file'], 'r') as f:
        md_text = f.read()

    if arguments['print_html']:
        print(to_html(md_text))
        parser.exit_on_success()

    print(get_watch_time(md_text,
                         text_pattern=arguments['text_pattern'],
                         split_pattern=arguments['split_pattern']))


if __name__ == '__main__':
    main()
