import os
from typing import List, Dict, Tuple, Set
from collections import defaultdict


def process_corpus(corpus: List[str]):
    corpus = [line.strip() for line in corpus]
    word_lengths: List[int] = []
    for line in corpus:
        word_lengths.extend([len(word) for word in line.split()])
    vocab, tokens = bpe(corpus, 100)
    max_length: int = 2 * max(word_lengths) + 5
    print("\nFinal vocabulary:")
    for pair in sorted(vocab.items()):
        print(padding(pair[0], max_length), ": ", pair[1], sep="")

    print("\nTokens:", *sorted(tokens), sep="\n")


def padding(string: str, max_length: int):
    padding_length: int = max_length - len(string)
    return string + (" " * padding_length)


def tokenize(vocab: Dict[str, int]) -> List[str]:
    tokens: Set[str] = []
    for token_seq in vocab:
        tokens.extend(token for token in token_seq.split())

    tokens: List[str] = list(set(tokens))
    return tokens


def get_vocab(corpus: List[str]) -> Dict[str, int]:
    vocab: defaultdict[str, int] = defaultdict(int)
    for sentence in corpus:
        for word in sentence.split():
            token: str = ""
            for char in word:
                token += (char + " ")

            token += ("</w>" + " ")
            vocab[token] += 1

    vocab: Dict[str, int] = dict(vocab)
    return vocab


def get_pairs(vocab: Dict[str, int]) -> Dict[Tuple[str, str], int]:
    pairs: defaultdict[Tuple[str, str], int] = defaultdict(int)
    for token_seq, freq in vocab.items():
        tokens = token_seq.strip().split()
        length = len(tokens)
        for i in range(length - 1):
            pairs[(tokens[i], tokens[i + 1])] += freq

    pairs: Dict[Tuple[str, str], int] = dict(pairs)
    return pairs


def merge_vocab(vocab_in: Dict[str, int], pair: Tuple[str, str]) -> Dict[str, int]:
    if pair == None:
        return vocab_in

    vocab_out: Dict[str, int] = {}
    bigram: str = " ".join(pair)
    for token_in in vocab_in:
        token_out = token_in.replace(bigram, "".join(pair))
        vocab_out[token_out] = vocab_in[token_in]

    return vocab_out


def bpe(corpus: List[str], iterations: int) -> Tuple[Dict[str, int], List[str]]:
    vocab: Dict[str, int] = get_vocab(corpus)
    for _ in range(1, iterations + 1):
        pairs: Dict[Tuple[str, str], int] = get_pairs(vocab)
        best_pair: Tuple[str, str] = max(
            pairs, key=pairs.get) if pairs else None
        vocab = merge_vocab(vocab, best_pair)

    return vocab, tokenize(vocab)


def main():
    input_path: str = input(f"Enter file path(Cwd {os.getcwd()}): ")
    # path: str = "Text Files/Input.txt"
    with open(input_path, "r") as file_in:
        process_corpus(file_in.readlines())


if __name__ == "__main__":
    main()
