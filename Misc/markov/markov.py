from numpy import random, array
from json import load, dump
from time import perf_counter


def tokenize(text):
    symbols = [".", ",", "\'", "\"", "“", "”", "?", "!",
               "[", "]", "{", "}", "(", ")", "-", ":", ";"]
    text = text.strip()
    for symbol in symbols:
        text = text.replace(symbol, f" {symbol} ")

    return text.replace("[\n\t ]+", " ").split()


def get_k_seqs(tokens, k):
    tokens_len = len(tokens)
    result = []
    for i in range(tokens_len - k):
        result.append(tuple(tokens[i: i + k]))

    return result


def detokenize(tokens):
    text = []
    no_space_symbols = ["\'"]
    post_space_symbols = [".", ",", "?", "!", ":", ";", "”", "]", "}", ")"]
    pre_space_symbols = ["“", "[", "{", "("]
    for token in tokens:
        if token in no_space_symbols or token in post_space_symbols:
            if len(text) > 0 and text[-1] == " ":
                text = text[:-1]

            text.append(token)
            if token in post_space_symbols:
                text.append(" ")

        else:
            if len(text) > 0 and text[-1] != " " and text[-1] not in pre_space_symbols:
                text.append(" ")
            text.append(token)
            if token not in pre_space_symbols:
                text.append(" ")

    return "".join(text)


def weighted_choice(options, probabilities):
    probabilities = array(probabilities)
    probabilities /= probabilities.sum()

    index = random.choice(len(options), p=probabilities)
    return options[index]


def choice(matrix, k_seq_counts, k_seq):
    words_dict = matrix[to_str(k_seq)]
    total = k_seq_counts[to_str(k_seq)]
    words = []
    likelihoods = []
    for word, freq in words_dict.items():
        words.append(word)
        likelihoods.append(freq / total)

    return weighted_choice(words, likelihoods)


def chain(seed, length, matrix, k_seq_counts, k):
    seed_tuple = tuple(tokenize(seed))
    seed_tuple_len = len(seed_tuple)
    if seed_tuple_len != k:
        raise ValueError(f"Expected {k} tokens as seed, got {seed_tuple_len}")

    sentence = []
    k_seq = seed_tuple
    sentence.append(detokenize(list(seed_tuple)))
    for _ in range(length):
        best_word = choice(matrix, k_seq_counts, k_seq)
        sentence.append(best_word)
        k_seq = tuple(list(k_seq[1:]) + [best_word])

    return detokenize(sentence)


def get_cache(cache_path):
    with open(cache_path, "r") as c_read:
        return load(c_read)


def to_str(tuple):
    return "".join(["(", ", ".join(tuple), ")"])


def main():
    corpus_path = "txt/ice_and_fire.txt"
    # corpus_path = input("Corpus path: ")
    k = 3
    # k = int(input("k value: "))
    start_time = perf_counter()
    cache = get_cache("json/cache.json")
    if corpus_path in cache and str(k) in cache[corpus_path]:
        print("Reading from cache...")
        cached_data = cache[corpus_path][str(k)]
        k_seqs = cached_data["k_seqs"]
        k_seq_counts = cached_data["k_seq_counts"]
        matrix = cached_data["matrix"]
    else:
        print("Writing into cache...")
        corpus = ""
        with open(corpus_path, "r", encoding="utf-8") as f:
            corpus += f.read()

        corpus_words = tokenize(corpus)
        corpus_len = len(corpus_words)
        k_seqs = get_k_seqs(corpus_words, k)
        matrix = {}
        for i, k_seq in enumerate(k_seqs):
            if i + k >= corpus_len:
                break

            next_word = corpus_words[i + k]
            matrix[to_str(k_seq)] = matrix.get(to_str(k_seq), {})
            matrix[to_str(k_seq)][next_word] = matrix[to_str(
                k_seq)].get(next_word, 0) + 1

        k_seq_counts = {}
        for k_seq_as_str, next_words in matrix.items():
            for _, freq in next_words.items():
                k_seq_counts[k_seq_as_str] = k_seq_counts.get(
                    k_seq_as_str, 0) + freq

        cache = {}
        cache[corpus_path] = {}
        cache[corpus_path][k] = {}
        cached_data = cache[corpus_path][k]
        cached_data["k_seqs"] = k_seqs
        cached_data["k_seq_counts"] = k_seq_counts
        cached_data["matrix"] = matrix
        with open("json/cache.json", "w") as c_write:
            dump(cache, c_write)

    end_time = perf_counter()
    print(
        f"Time taken to process dataset: {end_time - start_time:.2f} seconds")
    seed = detokenize(k_seqs[random.randint(0, len(k_seqs) - 1)])
    # seed = input("Seed: ")
    length = 200
    # length = int(input("Chain length: "))
    print(chain(seed, length, matrix, k_seq_counts, k))


if __name__ == "__main__":
    main()
