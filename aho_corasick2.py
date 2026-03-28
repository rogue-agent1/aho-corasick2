#!/usr/bin/env python3
"""aho_corasick2 - Aho-Corasick multi-pattern string search."""
import argparse
from collections import deque

class AhoCorasick:
    def __init__(self):
        self.goto = [{}]
        self.fail = [0]
        self.output = [[]]
    
    def add_pattern(self, pattern: str, idx: int = 0):
        state = 0
        for c in pattern:
            if c not in self.goto[state]:
                self.goto[state][c] = len(self.goto)
                self.goto.append({}); self.fail.append(0); self.output.append([])
            state = self.goto[state][c]
        self.output[state].append((idx, pattern))
    
    def build(self):
        queue = deque()
        for c, s in self.goto[0].items():
            queue.append(s)
        while queue:
            r = queue.popleft()
            for c, s in self.goto[r].items():
                queue.append(s)
                state = self.fail[r]
                while state and c not in self.goto[state]:
                    state = self.fail[state]
                self.fail[s] = self.goto[state].get(c, 0)
                if self.fail[s] == s: self.fail[s] = 0
                self.output[s] = self.output[s] + self.output[self.fail[s]]
    
    def search(self, text: str) -> list:
        state, results = 0, []
        for i, c in enumerate(text):
            while state and c not in self.goto[state]:
                state = self.fail[state]
            state = self.goto[state].get(c, 0)
            for idx, pat in self.output[state]:
                results.append((i - len(pat) + 1, pat))
        return results

def main():
    p = argparse.ArgumentParser(description="Aho-Corasick search")
    p.add_argument("text"); p.add_argument("-p", "--patterns", nargs="+", required=True)
    args = p.parse_args()
    ac = AhoCorasick()
    for i, pat in enumerate(args.patterns):
        ac.add_pattern(pat, i)
    ac.build()
    for pos, pat in ac.search(args.text):
        print(f"  '{pat}' at position {pos}")

if __name__ == "__main__":
    main()
