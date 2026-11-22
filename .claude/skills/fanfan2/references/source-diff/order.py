"""读 anchor.py 的输出，给出两样东西：
1) 讲述顺序：稿件里被原声锚定的原片时间，按稿件顺序排，标出往回跳（↶）和往前跳过 5 分钟以上（⤳）的地方；
2) 篇幅：原片每 10 分钟，稿件大约花了多少行（每行稿子归到它前面最近一个锚点的时间）。
用法: python3 anchor.py 稿 字幕 > a.txt ; python3 order.py a.txt
"""
import sys, re

def secs(t):
    p = [int(x) for x in t.split(":")]
    return p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2]

rows = []
total = 0
for line in open(sys.argv[1], encoding="utf-8"):
    parts = line.rstrip("\n").split("\t")
    if len(parts) < 2:
        continue
    total += 1
    n, t = parts[0], parts[1]
    if re.match(r"^\d+:\d+", t.strip()):
        rows.append((int(n), secs(t.strip()), t.strip()))

# 去掉孤立的离群锚点（和前后两个都差 20 分钟以上的，多半是误配）
clean = []
for i, r in enumerate(rows):
    prev = rows[i - 1][1] if i > 0 else r[1]
    nxt = rows[i + 1][1] if i + 1 < len(rows) else r[1]
    if abs(r[1] - prev) > 1200 and abs(r[1] - nxt) > 1200:
        continue
    clean.append(r)

print("== 讲述顺序（稿件行:原片时间）==")
out = []
last = None
for n, s, t in clean:
    mark = ""
    if last is not None:
        if s < last - 120:
            mark = "↶"
        elif s > last + 300:
            mark = "⤳"
    out.append(f"{mark}{n}:{t}")
    last = s
print(" ".join(out))

print("\n== 篇幅（原片每10分钟 → 稿件行数）==")
buckets = {}
if clean:
    idx = 0
    cur = clean[0][1]
    for ln in range(1, total + 1):
        while idx < len(clean) and clean[idx][0] <= ln:
            cur = clean[idx][1]
            idx += 1
        b = cur // 600
        buckets[b] = buckets.get(b, 0) + 1
for b in sorted(buckets):
    print(f"{b*10:>3}-{b*10+10:<3}分  {'█' * (buckets[b] // 5)} {buckets[b]}")
