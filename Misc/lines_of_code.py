from os.path import join, isdir
from os import listdir


def recur_count(folder):
    lines_of_code = 0
    for item in listdir(folder):
        item_path = join(folder, item)
        if isdir(item_path):
            lines_of_code += recur_count(item_path)
        else:
            file_loc = len(open(item_path, 'r', encoding='utf-8').readlines())
            print(f'{item_path} lines of code: {file_loc}')
            lines_of_code += file_loc
    return lines_of_code


def main():
    lines_of_code = 0
    while len(folder := input()) > 0:
        lines_of_code += recur_count(folder)
        print()
    print(f'Total lines of code: {lines_of_code}')


if __name__ == '__main__':
    main()
