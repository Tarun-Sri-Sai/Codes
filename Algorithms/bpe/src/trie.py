class TrieNode:
    def __init__(self):
        self.is_leaf = False
        self.children = {}

class Trie:
    def __init__(self, strings):
        self.root = TrieNode()
        for string in strings:
            temp = self.root
            i_max = len(string) - 1
            for i, ch in enumerate(string):
                temp.children[ch] = temp.children.get(ch, TrieNode())
                temp = temp.children[ch]
                if i == i_max:
                    temp.is_leaf = True
    
    def match(self, string):
        result = []
        i, length = 0, len(string)
        is_matched = [False] * length
        while i < length:
            if string[i] not in self.root.children:
                i += 1
                continue
            temp = self.root
            start = i
            while i < length and string[i] in temp.children:
                temp = temp.children[string[i]]
                i += 1
            if not temp.is_leaf:
                continue
            result.append((start, string[start:i]))
            for j in range(start, i):
                is_matched[j] = True
        i = 0
        while i < length:
            if is_matched[i]:
                i += 1
                continue
            start = i
            while i < length and not is_matched[i]:
                i += 1
            result.append((start, string[start:i]))
        return [x[1] for x in sorted(result, key=lambda x: x[0])]
