#!/usr/bin/env python3
"""Aho-Corasick multi-pattern string matching."""
import sys
from collections import deque

class AhoCorasick:
    def __init__(self):
        self.goto = [{}]
        self.fail = [0]
        self.output = [[]]
    def add(self, pattern):
        state = 0
        for ch in pattern:
            if ch not in self.goto[state]:
                self.goto[state][ch] = len(self.goto)
                self.goto.append({})
                self.fail.append(0)
                self.output.append([])
            state = self.goto[state][ch]
        self.output[state].append(pattern)
    def build(self):
        q = deque()
        for ch, s in self.goto[0].items():
            q.append(s)
        while q:
            r = q.popleft()
            for ch, s in self.goto[r].items():
                q.append(s)
                state = self.fail[r]
                while state and ch not in self.goto[state]:
                    state = self.fail[state]
                self.fail[s] = self.goto[state].get(ch, 0)
                if self.fail[s] == s:
                    self.fail[s] = 0
                self.output[s] = self.output[s] + self.output[self.fail[s]]
    def search(self, text):
        state, results = 0, []
        for i, ch in enumerate(text):
            while state and ch not in self.goto[state]:
                state = self.fail[state]
            state = self.goto[state].get(ch, 0)
            for pat in self.output[state]:
                results.append((i - len(pat) + 1, pat))
        return results

def test():
    ac = AhoCorasick()
    for p in ["he", "she", "his", "hers"]:
        ac.add(p)
    ac.build()
    r = ac.search("ahishers")
    found = {(pos, pat) for pos, pat in r}
    assert (1, "his") in found
    assert (3, "she") in found
    assert (4, "he") in found
    assert (4, "hers") in found
    print("  aho_corasick2: ALL TESTS PASSED")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Aho-Corasick multi-pattern matcher")
