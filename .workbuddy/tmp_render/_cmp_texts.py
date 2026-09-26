# -*- coding: utf-8 -*-
"""全文提取 23 份 PDF 到 txt，并对疑似重复组做 difflib 相似度比对"""
import fitz, os, difflib, re

ROOT = r"D:\obsidian\.workbuddy\tmp_render"
TXT  = os.path.join(ROOT, "txts")
os.makedirs(TXT, exist_ok=True)

keys = ["ch2ex","ch3s1","ch3sum","ch4sum","ch5ex","ch5ex4","ch5s1","ch5sum",
        "comp","df01","dg","disc","hoc0","hoc1","hstep","sampex",
        "sec2d","sec2i","sfde","sfdr","sol2","t123","tlink"]

texts = {}
for k in keys:
    doc = fitz.open(os.path.join(ROOT, k + ".pdf"))
    t = "\n".join(p.get_text() for p in doc)
    doc.close()
    # 清理多余空白行
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    texts[k] = t
    with open(os.path.join(TXT, k + ".txt"), "w", encoding="utf-8") as f:
        f.write(t)

print("=== 字符数 ===")
for k in keys:
    print(f"{k:8s} {len(texts[k]):6d}")

def ratio(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

groups = [
    ("ch3sum", "ch3s1"),
    ("ch5sum", "ch5s1"),
    ("hoc0", "hoc1"),
    ("hoc0", "sec2i"),
    ("hoc1", "sec2i"),
    ("sec2d", "sec2i"),
    ("sfde", "sfdr"),
    ("ch5ex", "ch5ex4"),
    ("ch2ex", "sol2"),
    ("ch5ex", "comp"),
    ("disc", "sampex"),
    ("t123", "tlink"),
]
print("\n=== 疑似组相似度 ===")
for a, b in groups:
    r = ratio(texts[a], texts[b])
    print(f"{a:8s} vs {b:8s}  ratio={r:.3f}")

# 找出每份的开头 80 字符（去空白）便于识别主题
print("\n=== 各份开头 ===")
for k in keys:
    head = re.sub(r"\s+", " ", texts[k])[:80]
    print(f"[{k}] {head}")
