from string import printable


def main():
    with open("txt/train_ascii.txt", "w") as f_write:
        with open("txt/train.txt", "r", encoding="utf-8") as f_read:
            f_write.write(
                "".join(filter(lambda ch: ch in printable, f_read.read())))


if __name__ == "__main__":
    main()
