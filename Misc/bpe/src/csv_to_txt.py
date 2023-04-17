import os
from typing import List


def read_input_path(input_csv_path):
    result: List[str] = []
    with open(input_csv_path, "r", encoding="utf-8") as csv_in:
        for line in csv_in.readlines():
            line = line.strip()
            result.append("".join(ch for ch in line if str.isascii(ch)))

    return result


def main():
    print(f"Cwd: {os.getcwd()}")
    input_csv_path: str = input("Input .csv file path: ")
    output_txt_path: str = input("Output .txt file path: ")
    with open(output_txt_path, "w") as txt_out:
        for line in read_input_path(input_csv_path):
            txt_out.write(line + "\n")


if __name__ == "__main__":
    main()