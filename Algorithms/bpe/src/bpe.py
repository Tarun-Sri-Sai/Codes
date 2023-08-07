from os.path import join, isdir
from os import mkdir
from csv_to_txt import convert
from json import dump, load
from collections import Counter
from itertools import tee
from re import sub
from trie import Trie


class BPE:
    def process(self, sentences):
        for i, sentence in enumerate(sentences):
            sentences[i] = sub(r'\s+', '_', sentence.strip()) + '^'
        return sentences

    def characterize_tokens(self, string):
        return ' '.join(ch for ch in string)

    def build_vocab(self, sentences):
        vocab = {}
        for sentence in sentences:
            key = self.characterize_tokens(sentence)
            vocab[key] = vocab.get(key, 0) + 1
        return vocab

    def pairwise(self, iterable):
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

    def rank_pairs(self, vocab):
        pairs = Counter()
        for token_seq in vocab:
            tokens = token_seq.split()
            pairs.update(self.pairwise(tokens))
        return dict(pairs)

    def merge_vocab(self, vocab, best_pair):
        new_vocab = {}
        bigram_key = ' '.join(best_pair)
        repl = ''.join(best_pair)
        for token_seq, freq in vocab.items():
            new_token_seq = token_seq.replace(bigram_key, repl)
            new_vocab[new_token_seq] = freq
        return new_vocab
    
    def index(self, items):
        return {key: i for i, key in enumerate(items)}

    def get_tokens(self, vocab):
        tokens = []
        for token_seq in vocab:
            tokens.extend(token_seq.split())
        return self.index([*set(tokens)])

    def train(self, text_path, json_path, iterations=100):
        with open(text_path, 'r', encoding='utf-8') as f:
            sentences = f.readlines()
            sentences = self.process(sentences)
            vocab = self.build_vocab(sentences)
            for _ in range(iterations):
                pairs = self.rank_pairs(vocab)
                best_pair = max(pairs, key=pairs.get)
                vocab = self.merge_vocab(vocab, best_pair)
        with open(json_path, 'w', encoding='utf-8') as f:
            dump(self.get_tokens(vocab), f, indent=4)

    def match_tokens(self, sentences, token_dict):
        trie = Trie([x for x, _ in token_dict.items()])
        result = []
        for sentence in sentences:
            result += trie.match(sentence)
        return [token_dict.get(x, x) for x in result]

    def test(self, text_path, json_path, tokens_path):
        with open(text_path, 'r', encoding='utf-8') as f:
            sentences = f.readlines()
            sentences = self.process(sentences)
        with open(json_path, 'r', encoding='utf-8') as f:
            tokens = load(f)
            tokenized = self.match_tokens(sentences, tokens)
        with open(tokens_path, 'w', encoding='utf-8') as f:
            f.write('|'.join(str(x) for x in tokenized))


def main():
    folders = {ext: join('..', ext) for ext in ['txt', 'json']}
    for _, folder in folders.items():
        if isdir(folder):
            continue
        mkdir(folder)
    modes = {'train', 'test'}
    mode = input('Enter training mode: ')
    if mode not in modes:
        print(f'Wrong mode, options: {", ".join(modes)}')
        return
    convert(mode)
    paths = {
        'txt': join(folders['txt'], '.'.join([mode, 'txt'])),
        'json': join(folders['json'], '.'.join(['tokens', 'json']))
    }
    bpe = BPE()
    if mode == 'train':
        bpe.train(paths['txt'], paths['json'])
    elif mode == 'test':
        tokens_path = join(folders['txt'], '.'.join(['tokens', 'txt']))
        bpe.test(paths['txt'], paths['json'], tokens_path)


if __name__ == '__main__':
    main()
