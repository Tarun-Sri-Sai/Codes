from serializer import serialize
from sample import build


def main():
    build()
    print(serialize('tree.json'))


if __name__ == '__main__':
    main()
