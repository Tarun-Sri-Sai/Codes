from os.path import join, isdir
from pandas import read_csv
from re import sub
from os import mkdir


def convert_util(csv_path, txt_path):
    df = read_csv(csv_path)
    rows = df['text'].apply(lambda x: x.replace('<br />', '\n'))
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(sub('[\n]+', '\n', '\n'.join(rows)))


def convert(mode):
    txt_dir = join('..', 'txt')
    if not isdir(txt_dir):
        mkdir(txt_dir)

    exts = ['csv', 'txt']
    convert_util(*[join('..', ext, '.'.join([mode, ext])) for ext in exts])
