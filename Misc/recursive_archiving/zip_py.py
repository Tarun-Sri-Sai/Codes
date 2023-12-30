from argparse import ArgumentParser
from sys import exit
from os import path, makedirs
from shutil import rmtree, make_archive


MAX_FOLDERS = 53
MAX_FILES = 1000
MAX_CHARS = 10000


def exit_on_failure(parser):
    parser.print_help()
    exit()


def read_args():
    parser = ArgumentParser(
        description='ZipPy -- Recursive Zipper --')

    parser.add_argument(
        '-d',
        dest='dest_folder', type=str,
        help='Destination folder path')
    parser.add_argument(
        '-r',
        dest='num_folders', type=int,
        help=f'Number of nested folders (< {MAX_FOLDERS})')
    parser.add_argument(
        '-f',
        dest='num_files', type=int,
        help=f'Number of files in each folder (< {MAX_FILES})')
    parser.add_argument(
        '-c',
        dest='num_chars', type=int,
        help=f"Number of '0' characters in each file (< {MAX_CHARS})")
    
    args = parser.parse_args()
    result = [args.dest_folder, args.num_folders, args.num_files, 
              args.num_chars]
    
    if any(x is None or x <= 0 for x in result[1:]):
        exit_on_failure(parser)
    if result[1] >= MAX_FOLDERS or result[2] >= MAX_FILES or result[3] >= MAX_CHARS:
        exit_on_failure(parser)
    return result


def make_new_folder(folder_path):
    if path.isdir(folder_path):
        rmtree(folder_path)
    makedirs(folder_path)


def create_files(folder_path, num_files, num_chars):
    for i in range(num_files):
        file_path = path.join(folder_path, f'f{i + 1:0>3}.txt')
        with open(file_path, 'w') as f:
            f.write('0' * num_chars)


def zip_folder(folder_path, parent_path, zip_name):
    zip_path = path.join(parent_path, zip_name)
    make_archive(zip_path, 'zip', folder_path)


def recursive_zip(num_folders, num_files, num_chars, parent_path):
    if num_folders == 0:
        return
    
    folder_name = f'd{num_folders:0>2}'
    folder_path = path.join(parent_path, folder_name)
    
    make_new_folder(folder_path)
    
    recursive_zip(num_folders - 1, num_files, num_chars, folder_path)

    create_files(folder_path, num_files, num_chars)
    zip_folder(folder_path, parent_path, folder_name)
    print(f'Zipped {folder_name}', end='\r')

    rmtree(folder_path)


def create_and_zip(dest_folder, num_folders, num_files, num_chars):
    recursive_zip(num_folders, num_files, num_chars, dest_folder)
    print(f'Zipped {num_folders} folders')


def main():
    create_and_zip(*read_args())


if __name__ == '__main__':
    main()
