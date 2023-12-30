from argparse import ArgumentParser
from markdown import markdown
from re import findall
from sys import exit


class Parser:
    def __init__(self):
        self._parser = ArgumentParser(
            description='Find watch hours in markdown watchlists')
        
    def get_arguments(self) -> tuple[str, str | None, str | None]:
        self._parser.add_argument(
            '-f',
            type=str,
            dest='md_file',
            help='Specify the markdown file containing the watchlist')
        self._parser.add_argument(
            '-t',
            type=str,
            dest='html_pattern',
            help='Specify the HTML pattern containing the content info')
        self._parser.add_argument(
            '-s',
            type=str,
            dest='split_pattern',
            help='Pattern to split content types(Episode e, Movie m, Special s)')
        
        args = self._parser.parse_args()

        if args.md_file is None:
            self.exit_on_error('Bad md_file')

        return args.md_file, args.html_pattern, args.split_pattern
    
    def exit_on_error(self, error_string):
        print(error_string, end='\n\n')
        self._parser.print_help()
        exit(1)



parser = Parser()


def to_html(md_text: str) -> str:
    return markdown(md_text)


def find_content_info(html_content: str, html_pattern: str) -> list[str]:
    try:
        return findall(html_pattern, html_content)
    except Exception:
        parser.exit_on_error('Bad html_pattern')


def find_content_types(content_info: list[str],
                       split_pattern: str) -> list[str]:

    content_types = []
    for content in content_info:
        content_types += [s.strip() for s in content.split(split_pattern)]
    return content_types


def calculate_hours(content_types: list[str]) -> float:
    total_hours = 0

    try:
        multipliers = {'Episode': 1 / 3, 'Movie': 3 / 2, 'Special': 1}
        for item in content_types:
            split_words = item.split(' ')
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
                   html_pattern=None,
                   split_pattern=None) -> str:

    html_pattern = html_pattern or r'<em>\[(.*?)\]</em>'
    split_pattern = split_pattern or ', '

    html_content = to_html(md_text)
    content_info = find_content_info(html_content, html_pattern)
    content_types = find_content_types(content_info, split_pattern)
    hours = calculate_hours(content_types)

    return format_hours(hours)


def main():
    md_file, html_pattern, split_pattern = parser.get_arguments()

    with open(md_file, 'r') as f:
        md_text = f.read()

    print(get_watch_time(md_text,
                         html_pattern=html_pattern,
                         split_pattern=split_pattern))


if __name__ == '__main__':
    main()
