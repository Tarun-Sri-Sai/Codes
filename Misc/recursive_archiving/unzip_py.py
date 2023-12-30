from argparse import ArgumentParser
from os import path, listdir, remove, makedirs
from shutil import unpack_archive, rmtree


def read_dest():
    parser = ArgumentParser(
        description='UnzipPy -- Recursive Unzipper --')

    parser.add_argument(
        '-d',
        dest='dest_folder', type=str,
        help='Destination folder path')
    
    args = parser.parse_args()

    if not (result := args.dest_folder):
        parser.print_help()
        exit()
    return result


def make_new_folder(folder_path):
    if path.isdir(folder_path):
        rmtree(folder_path)
    makedirs(folder_path)


def unzip_folder(zip_path, parent_path):
    make_new_folder(parent_path)
    unpack_archive(zip_path, parent_path, 'zip')


def recursive_unzip(dest_folder):
    for item in listdir(dest_folder):
        item_path = path.join(dest_folder, item)
        if path.splitext(item_path)[1] == '.zip':
            folder_name = item[:-4]
            unzip_folder(item_path, path.join(dest_folder, folder_name))
            print(f'Unpacked {item}', end='\r')
            recursive_unzip(path.join(dest_folder, folder_name))
            remove(item_path)

def main():
    recursive_unzip((dest_folder := read_dest()))
    print(f'Unpacked all folders in {dest_folder}')


if __name__ == '__main__':
    main()
