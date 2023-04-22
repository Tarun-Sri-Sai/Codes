from string import printable
from os import getcwd


def main():
    print(f"Current directory: {getcwd()}")
    file_path = input("File path: ")
    with open("".join([file_path[:-4], "_ascii.txt"]), "w") as f_write:
        with open(file_path, "r", encoding="utf-8") as f_read:
            f_write.write(
                "".join(filter(lambda ch: ch in printable, f_read.read())))


if __name__ == "__main__":
    main()
