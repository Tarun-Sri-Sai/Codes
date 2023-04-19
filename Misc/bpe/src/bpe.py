import json
import os
import re
from typing import List, Dict, Tuple
from collections import  Counter
from itertools import tee
import time


class BPE:
    def __init__(self, corpus: List[str], vocab_path: str, iterations: int) -> None:
        self.vocab_json_path: str = vocab_path
        self.vocab: Dict[str, int] = {}
        try:
            with open(self.vocab_json_path, "r") as vocab_reader:
                self.vocab = json.load(vocab_reader)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            pass

        for sentence in corpus:
            sentence = re.sub("[ ]+", "_", sentence.strip())
            sentence += "^"
            key = self.characterize_tokens(sentence)
            self.vocab[key] = self.vocab.get(key, 0) + 1

        print()
        for i in range(iterations):
            self.rank_pairs()
            best_pair: Tuple[str, str] = max(self.pairs, key=self.pairs.get)
            self.merge_vocab(best_pair)
            print(f"Best pair in iteration {i + 1}: {best_pair}")

        with open(self.vocab_json_path, "w") as json_writer:
            json.dump(self.vocab, json_writer, indent=4)

    def characterize_tokens(self, string: str) -> str:
        return " ".join(ch for ch in string)

    def get_tokens(self) -> List[str]:
        tokens: List[str] = []
        for token_seq in self.vocab:
            tokens.extend(token_seq.split())
        return list(set(tokens))

    def pairwise(self, iterable):
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

    def rank_pairs(self) -> None:
        pairs: Counter = Counter()
        for token_seq in self.vocab:
            tokens = token_seq.split()
            pairs.update(self.pairwise(tokens))

        self.pairs: Dict[Tuple[str, str], int] = dict(pairs)

    def merge_vocab(self, best_pair: Tuple[str, str]) -> None:
        vocab: Dict[str, int] = {}
        bigram_key: str = " ".join(best_pair)
        repl: str = "".join(best_pair)
        for token_seq, freq in self.vocab.items():
            new_token_seq = token_seq.replace(bigram_key, repl)
            vocab[new_token_seq] = freq

        self.vocab = vocab


def main() -> None:
    print(f"CWD: {os.getcwd()}")
    corpus_path: str = input("Corpus .txt path: ")
    vocab_path: str = input("Vocab .json path: ")
    iterations: int = int(input("Iterations: "))
    tokens_path: str = input("Tokens .txt path: ")
    with open(tokens_path, "w") as t_out:
        with open(corpus_path, "r") as c_in:
            start_time = time.perf_counter()
            bpe = BPE(c_in.readlines(), vocab_path, iterations)
            tokens = bpe.get_tokens()
            end_time = time.perf_counter()
            print(f"Time taken: {end_time - start_time:.3f} seconds")
            for token in tokens:
                t_out.write(token + "\n")


if __name__ == "__main__":
    main()
