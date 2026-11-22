"""把凡凡稿里的英文原声行，对到原片字幕的时间码上。
用法: python3 anchor.py 稿件路径 字幕txt路径(subs/ 下 time zh|en 格式)
输出: 稿件行号  时间码(或 -)  稿件原文
"""
import re, sys, difflib

def norm(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9' ]+", " ", s)
    return [w for w in s.split() if w]

script = open(sys.argv[1], encoding="utf-8").read().splitlines()
subs = []
for line in open(sys.argv[2], encoding="utf-8"):
    line = line.rstrip("\n")
    m = re.match(r"(\d+:\d+(?::\d+)?) (.*)", line)
    if not m:
        continue
    t, rest = m.groups()
    en = rest.split("|", 1)[1] if "|" in rest else ""
    zh = rest.split("|", 1)[0]
    subs.append((t, norm(en), zh.strip()))

# 用滑动窗口(连续3条字幕拼起来)提高长句命中
win = []
for i in range(len(subs)):
    words = []
    for j in range(i, min(i + 3, len(subs))):
        words += subs[j][1]
    win.append((subs[i][0], words, subs[i][2]))

last = 0
for n, line in enumerate(script, 1):
    ascii_ratio = sum(c.isascii() and c.isalpha() for c in line) / max(1, len(line))
    w = norm(line)
    if ascii_ratio < 0.5 or len(w) < 2:
        print(f"{n}\t \t{line}")
        continue
    best, bt, bzh, bi = 0, "-", "", last
    for i, (t, ww, zh) in enumerate(win):
        if not ww:
            continue
        r = difflib.SequenceMatcher(None, w, ww[: len(w) + 4]).ratio()
        # 稍微偏向就近(原声多按顺序出现)，但允许跳
        if r > best:
            best, bt, bzh, bi = r, t, zh, i
    if best >= 0.45:
        last = bi
        print(f"{n}\t{bt}\t{line}\t〔{bzh}〕")
    else:
        print(f"{n}\t?\t{line}")
