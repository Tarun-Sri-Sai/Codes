from argparse import ArgumentParser
from os import path, walk


def read_dest():
    parser = ArgumentParser(
        description='Clean -- Clean up extracted files --')

    parser.add_argument(
        '-d',
        dest='dest_folder', type=str,
        help='Destination folder path')
    
    args = parser.parse_args()

    if not (result := args.dest_folder):
        parser.print_help()
        exit()
    return result


def get_size(folder_path):
    total_size = 0

    for dirpath, _, filenames in walk(folder_path):
        for filename in filenames:
            file_path = path.join(dirpath, filename)
            total_size += path.getsize(file_path)

    return total_size / 1024


def main():
    dest_folder = read_dest()
    print(f'Size of {dest_folder}: {get_size(dest_folder):.2f} KB')


if __name__ == '__main__':
    main()
