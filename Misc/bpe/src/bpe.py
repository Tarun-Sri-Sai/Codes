import os
from typing import List, Dict, Tuple, Set
from collections import defaultdict
import time


def process_corpus(corpus: List[str]):
    corpus = [line.strip() for line in corpus]
    word_lengths: List[int] = []
    for line in corpus:
        word_lengths.extend([len(word) for word in line.split()])

    iterations = int(input("Iterations: "))
    start_time: float = time.perf_counter()
    _, tokens = bpe(corpus, iterations)
    end_time: float = time.perf_counter()
    print(f"Time taken: {(end_time - start_time):.2f} seconds")
    output_path = input("Token file path: ")
    if output_path == "":
        return
    with open(output_path, "w") as token_out:
        token_out.write("Tokens:\n")
        for token in sorted(tokens):
            token_out.write(token.replace("</t>", "_") + "\n")


def tokenize(vocab: Dict[str, int]) -> List[str]:
    tokens: List[str] = []
    for token_seq in vocab:
        tokens.extend(token for token in token_seq.split())

    tokens = list(set(tokens))
    return tokens


def get_vocab(corpus: List[str]) -> Dict[str, int]:
    vocab: defaultdict[str, int] = defaultdict(int)
    for sentence in corpus:
        token: str = ""
        for char in sentence:
            token += (char + "</t>")

        token += ("</s>")
        vocab[token] += 1

    vocab: Dict[str, int] = dict(vocab)
    return vocab


def get_pairs(vocab: Dict[str, int]) -> Dict[Tuple[str, str], int]:
    pairs: defaultdict[Tuple[str, str], int] = defaultdict(int)
    for token_seq, freq in vocab.items():
        tokens = token_seq.strip().split("</t>")
        length = len(tokens)
        for i in range(length - 1):
            pairs[(tokens[i], tokens[i + 1])] += freq

    pairs: Dict[Tuple[str, str], int] = dict(pairs)
    return pairs


def merge_vocab(vocab_in: Dict[str, int], pair: Tuple[str, str]) -> Dict[str, int]:
    if pair == None:
        return vocab_in

    vocab_out: Dict[str, int] = {}
    bigram: str = "</t>".join(pair)
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
    print(f"Cwd: {os.getcwd()}")
    input_path: str = input("Corpus file path: ")
    with open(input_path, "r") as file_in:
        process_corpus(file_in.readlines())


if __name__ == "__main__":
    main()
