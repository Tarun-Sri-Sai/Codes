import argparse
import typing
import re
import os


def fetch_args() -> tuple[dict[str, typing.Any], typing.Callable]:
    parser = argparse.ArgumentParser(
        description='Get the largest files and directories')
    parser.add_argument('path', type=str,
                        help='Path to a file or a directory')
    parser.add_argument('-t', '--top',
                        type=int,
                        dest='num_results',
                        help='Number of results')
    parser.add_argument('-x', '--exclude',
                        type=str,
                        dest='exclude_regex',
                        help='Regex pattern to exclude')
    parser.add_argument('-r', '--human-readable',
                        dest='human_readable',
                        action='store_true',
                        help='Convert bytes to human readable format')
    return vars(parser.parse_args()), parser.print_help


def bytes_to_human_readable(size: int) -> str:
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    index = 0
    while size >= 1024 and index < len(suffixes) - 1:
        size /= 1024
        index += 1
    return f"{size:.2f} {suffixes[index]}"


def find_all_sizes(path: str,
                   exclude_regex: str = None) -> list[tuple[str, int]]:
    result = []
    if not os.path.exists(path):
        raise ValueError('Path does not exist')

    if exclude_regex is not None:
        try:
            if re.search(exclude_regex, path):
                return result
        except Exception as e:
            raise ValueError(f'Invalid regex, {e}')

    if os.path.isfile(path):
        result.append((os.path.relpath(path), os.path.getsize(path)))
        return result

    total = 0
    for item in os.listdir(path):
        full_path = os.path.join(path, item)

        next_result = find_all_sizes(full_path, exclude_regex)
        result += next_result

        total += sum(x[1] for x in next_result)

    result.append((os.path.relpath(path), total))
    return result


def get_ranking(path: str,
                num_results: int = None,
                exclude_regex: str = None,
                human_readable: bool = False) -> list[tuple[str, int | str]]:
    if num_results is None:
        num_results = 10

    if num_results <= 0:
        raise ValueError('Number of results is not positive')

    result = sorted(find_all_sizes(path, exclude_regex),
                    key=lambda x: x[1], reverse=True)[:num_results]
    if human_readable:
        return [(x[0], bytes_to_human_readable(x[1]))
                for x in result]
    return result


def main():
    args, print_help = fetch_args()
    try:
        results = get_ranking(**args)

        max_path_len = max(len(x[0]) for x in results)
        max_index_len = len(str(len(results)))

        print('\n'.join(f'{i + 1:>{max_index_len}}: '
                        f'{x[0]:<{max_path_len}} - {x[1]}'
                        for i, x in enumerate(results)))
    except Exception as e:
        print(f'Exited due to error {e}')
        print_help()
        raise


if __name__ == '__main__':
    main()
