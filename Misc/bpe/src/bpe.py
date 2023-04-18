import os
from typing import List


def bpe(corpus: List[str], iterations: int) -> List[str]:
    #   TODO: Tokenise corpus iterations times and return as list
    return corpus


def main() -> None:
    print(f"CWD: {os.getcwd()}")
    corpus_path: str = input("Corpus path: ")
    iterations: int = int(input("Iterations: "))
    tokens_path: str = input("Tokens path: ")
    with open(tokens_path, "w") as t_out:
        with open(corpus_path, "r") as c_in:
            for token in bpe(c_in.readlines(), iterations):
                t_out.write(token + "\n")

if __name__ == "__main__":
    main()
