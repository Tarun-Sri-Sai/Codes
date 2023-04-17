import os
import codecs


def main():
    print(f"Cwd: {os.getcwd()}")
    input_csv_path = input("Input .txt file path: ")
    output_txt_path = input("Output .csv file path: ")
    with open(output_txt_path, "w") as txt_out:
        csv_in = codecs.open(input_csv_path, "r", encoding="ascii", errors="ignore")
        for line in csv_in:
            txt_out.write(line + "\n")


if __name__ == "__main__":
    main()