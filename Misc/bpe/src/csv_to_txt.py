from os.path import join
from pandas import read_csv
from re import sub


def main() -> None:
    train_csv_path = join('..', 'csv', 'train.csv')
    train_df = read_csv(train_csv_path)
    train_txt = '\n'.join(train_df['text'].apply(
        lambda x: x.replace('<br />', '\n')))
    train_txt_path = join('..', 'txt', 'train.txt')
    with open(train_txt_path, 'w', encoding='utf-8') as f:
        f.write(sub('[\n]+', '\n', train_txt))

    test_csv_path = join('..', 'csv', 'test.csv')
    test_df = read_csv(test_csv_path)
    test_txt = '\n'.join(test_df['text'].apply(
        lambda x: x.replace('<br />', '\n')))
    test_txt_path = join('..', 'txt', 'test.txt')
    with open(test_txt_path, 'w', encoding='utf-8') as f:
        f.write(sub('[\n]+', '\n', test_txt))


if __name__ == "__main__":
    main()
