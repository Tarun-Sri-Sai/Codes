from numpy import random, array
from typing import List, Tuple, Dict


def split_sentence(sen: str) -> List[str]:
    sen = sen.strip()
    for spaced in ".,?!;:/&\'\"+-*%=()[]{}_@$#`~<>^":
        sen = sen.replace(spaced, f" {spaced} ")

    return sen.replace("[\n\t ]+", " ").split()


def get_k_seqs(tokens: str, k: int) -> List[Tuple[str, ...]]:
    tokens_len: int = len(tokens)
    result: List[Tuple[str, ...]] = []
    for i in range(tokens_len - k):
        result.append(tuple(tokens[i: i + k]))

    return result


def make_sentence(tokens: List[str]) -> str:
    result: str = ""
    for token in tokens:
        if token in ".,?!;:\%\'\"":
            result += (token)
        else:
            result += (" " + token)

    return result.strip()


def weighted_choice(options: List[str], probabilities: List[float]) -> str:
    probabilities = array(probabilities)
    probabilities /= probabilities.sum()

    index = random.choice(len(options), p=probabilities)
    return options[index]


def split_choice(possibilities: Dict[str, float]) -> str:
    words: List[str] = []
    likelihoods: List[float] = []
    for key, value in possibilities.items():
        words.append(key)
        likelihoods.append(value)

    return weighted_choice(words, likelihoods)


def choice(matrix: Dict[Tuple[str, ...], Dict[str, int]], k_seq_counts: Dict[Tuple[str, ...], int], k_seq: Tuple[str, ...]) -> str:
    words_dict: Dict[str, int] = matrix[k_seq]
    possibilities: Dict[str, float] = {}
    total: int = k_seq_counts[k_seq]
    for word, freq in words_dict.items():
        possibilities[word] = freq / total

    return split_choice(possibilities)



def chain(seed: str, length: int, matrix: Dict[Tuple[str, ...], Dict[str, int]], k_seq_counts: Dict[Tuple[str, ...], int], k: int) -> str:
    seed_tuple: Tuple[str, ...] = tuple(split_sentence(seed))
    seed_tuple_len: int = len(seed_tuple)
    if seed_tuple_len != k:
        raise ValueError(f"Expected {k} tokens as seed, got {seed_tuple_len}")
    
    sentence: List[str] = []
    k_seq: Tuple[str, ...] = seed_tuple
    sentence.append(make_sentence(list(seed_tuple)))
    for _ in range(length):
        best_word = choice(matrix, k_seq_counts, k_seq)
        sentence.append(best_word)
        k_seq = tuple(list(k_seq[1 :]) + [best_word])

    return make_sentence(sentence)


def main() -> None:
    # corpus_path: str = input("Corpus path: ")
    corpus_path: str = "txt/train.txt"
    corpus: str = ""
    with open(corpus_path, "r") as f:
        corpus += f.read()

    corpus_words: List[str] = split_sentence(corpus)
    corpus_len = len(corpus_words)
    k: int = 4
    #k = int(input("Enter k: "))
    k_seqs: List[Tuple[str, ...]] = get_k_seqs(corpus_words, k)
    matrix: Dict[Tuple[str, ...], Dict[str, int]] = {}
    for i, k_seq in enumerate(k_seqs):
        if i + k >= corpus_len:
            break

        next_word: str = corpus_words[i + k]
        matrix[k_seq] = matrix.get(k_seq, {})
        matrix[k_seq][next_word] = matrix[k_seq].get(next_word, 0) + 1

    k_seq_counts: Dict[Tuple[str, ...], int] = {}
    for k_seq, next_words in matrix.items():
        for _, freq in next_words.items():
            k_seq_counts[k_seq] = k_seq_counts.get(k_seq, 0) + freq

    # seed: str = input("Seed: ")
    seed: str = make_sentence(k_seqs[random.randint(0, len(k_seqs) - 1)])
    # length: int = int(input("Chain length: "))
    length: int = 200
    print(chain(seed, length, matrix, k_seq_counts, k))


if __name__ == "__main__":
    main()
