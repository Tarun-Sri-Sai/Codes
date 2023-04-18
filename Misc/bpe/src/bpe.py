import json
import os
import re
from typing import List, Dict, Tuple, DefaultDict
from collections import defaultdict


class BPE:

    def __init__(self, corpus: List[str], iterations: int) -> None:
        self.vocab_json_path: str = "json/vocab.json"
        self.vocab: Dict[str, int] = {}
        with open(self.vocab_json_path, "r") as vocab_reader:
            try:
                self.vocab = json.load(vocab_reader)
            except json.decoder.JSONDecodeError:
                pass

        for sentence in corpus:
            sentence = re.sub("[ ]+", "_", sentence.strip())
            sentence += "^"
            key = self.characterize_tokens(sentence)
            self.vocab[key] = 1 if key not in self.vocab else self.vocab[key] + 1

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
            tokens.extend(token for token in token_seq.split())
        return list(set(tokens))
    
    def rank_pairs(self) -> None:
        pairs: DefaultDict[Tuple[str, str], int] = defaultdict(int)
        for token_seq, freq in self.vocab.items():
            tokens = token_seq.split()
            for i in range(0, len(tokens) - 1):
                pairs[tokens[i], tokens[i + 1]] += freq

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
    corpus_path: str = input("Corpus path: ")
    iterations: int = int(input("Iterations: "))
    tokens_path: str = input("Tokens path: ")
    with open(tokens_path, "w") as t_out:
        with open(corpus_path, "r") as c_in:
            bpe = BPE(c_in.readlines(), iterations)
            for token in bpe.get_tokens():
                t_out.write(token + "\n")


if __name__ == "__main__":
    main()
