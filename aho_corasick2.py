#!/usr/bin/env python3
"""aho_corasick2 - Multi-pattern string matching."""
import sys
from collections import deque,defaultdict
class AhoCorasick:
    def __init__(s):s.goto=defaultdict(dict);s.fail={};s.output=defaultdict(list);s.states=0
    def add(s,pattern):
        state=0
        for c in pattern:
            if c not in s.goto[state]:s.states+=1;s.goto[state][c]=s.states
            state=s.goto[state][c]
        s.output[state].append(pattern)
    def build(s):
        q=deque()
        for c,st in s.goto[0].items():s.fail[st]=0;q.append(st)
        while q:
            r=q.popleft()
            for c,st in s.goto[r].items():
                q.append(st);state=s.fail[r]
                while state and c not in s.goto[state]:state=s.fail.get(state,0)
                s.fail[st]=s.goto[state].get(c,0)
                if s.fail[st]==st:s.fail[st]=0
                s.output[st]=s.output[st]+s.output[s.fail[st]]
    def search(s,text):
        state=0;results=[]
        for i,c in enumerate(text):
            while state and c not in s.goto[state]:state=s.fail.get(state,0)
            state=s.goto[state].get(c,0)
            for pat in s.output[state]:results.append((i-len(pat)+1,pat))
        return results
if __name__=="__main__":
    ac=AhoCorasick();patterns=sys.argv[1].split(",")
    for p in patterns:ac.add(p)
    ac.build();text=sys.argv[2] if len(sys.argv)>2 else sys.stdin.read()
    for pos,pat in ac.search(text):print(f"  '{pat}' at position {pos}")
