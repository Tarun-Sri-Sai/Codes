from typing import List, Dict, Tuple
from collections import defaultdict


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
    for token, freq in vocab.items():
        sub_tokens = token.strip().split()
        length = len(sub_tokens)
        for i in range(length - 1):
            pairs[(sub_tokens[i], sub_tokens[i + 1])] += freq

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



def bpe(corpus: List[str], iterations: int) -> Dict[str, int]:
    vocab: Dict[str, int] = get_vocab(corpus)
    for i in range(1, iterations + 1):
        print(f"\nVocabulary before iteration {i}:", *vocab.items(), sep="\n")
        pairs: Dict[Tuple[str, str], int] = get_pairs(vocab)
        best_pair: Tuple[str, str] = max(pairs, key=pairs.get) if pairs else None
        vocab = merge_vocab(vocab, best_pair)

    return vocab



def main():
    corpus: List[str] = ["big cat small cat digs for figs in a tall tin"]
    print("\nFinal vocabulary:", *bpe(corpus, 20).items(), sep="\n")


if __name__ == "__main__":
    main()