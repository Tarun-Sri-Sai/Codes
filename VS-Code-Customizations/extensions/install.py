from os import system


def main():
    extensions = []
    with open('extensions.txt', 'r', encoding='utf-8', errors='replace') as f:
        extensions = f.read().rstrip().split('\n')
    for ext in extensions:
        system(f'code --install-extension {ext}')


if __name__ == '__main__':
    main()
