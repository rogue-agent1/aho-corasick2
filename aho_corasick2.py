#!/usr/bin/env python3
"""Aho-Corasick — multi-pattern string matching automaton."""
from collections import deque
import sys

class AhoCorasick:
    def __init__(self):
        self.goto = [{}]; self.fail = [0]; self.output = [[]]
    def add_pattern(self, pattern):
        state = 0
        for c in pattern:
            if c not in self.goto[state]:
                self.goto[state][c] = len(self.goto)
                self.goto.append({}); self.fail.append(0); self.output.append([])
            state = self.goto[state][c]
        self.output[state].append(pattern)
    def build(self):
        q = deque()
        for c, s in self.goto[0].items(): q.append(s)
        while q:
            r = q.popleft()
            for c, s in self.goto[r].items():
                q.append(s)
                state = self.fail[r]
                while state and c not in self.goto[state]: state = self.fail[state]
                self.fail[s] = self.goto[state].get(c, 0)
                if self.fail[s] == s: self.fail[s] = 0
                self.output[s] = self.output[s] + self.output[self.fail[s]]
    def search(self, text):
        state = 0; results = []
        for i, c in enumerate(text):
            while state and c not in self.goto[state]: state = self.fail[state]
            state = self.goto[state].get(c, 0)
            for pattern in self.output[state]:
                results.append((i - len(pattern) + 1, pattern))
        return results

if __name__ == "__main__":
    ac = AhoCorasick()
    for p in ["he", "she", "his", "hers"]: ac.add_pattern(p)
    ac.build()
    text = "ahishers"
    matches = ac.search(text)
    print(f"Text: '{text}'")
    for pos, pat in matches: print(f"  Found '{pat}' at position {pos}")
