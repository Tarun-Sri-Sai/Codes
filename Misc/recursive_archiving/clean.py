from argparse import ArgumentParser
from shutil import rmtree


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


def main():
    rmtree((dest_folder := read_dest()))
    print(f'Cleaned {dest_folder}')


if __name__ == '__main__':
    main()
