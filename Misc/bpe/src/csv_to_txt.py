import os


def main() -> None:
    print(f"CWD: {os.getcwd()}")
    input_csv_path: str = input("Input .csv: ")
    output_txt_path: str = input("Output .txt: ")
    with open(output_txt_path, "w") as txt_out:
        with open(input_csv_path, "r", encoding="utf-8") as csv_in:
            for line in csv_in.readlines():
                line = line.strip().replace(",", " ").replace("  ", ", ")
                txt_out.write(
                    "".join(ch for ch in line if str.isascii(ch)) + "\n")


if __name__ == "__main__":
    main()
