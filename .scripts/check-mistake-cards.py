#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""错题卡结构校验（数学/错题本）。

用法：
    python .scripts/check-mistake-cards.py            # 全部卡片
    python .scripts/check-mistake-cards.py 2000-17    # 只查名字含该串的卡片

检查项：
  1. frontmatter 必备字段齐全，且 type=mistake、tags 含 #错题
  2. 唯一 H1；有「> 返回：」行；有 [!abstract] 定位块
  3. 四个必备小节齐全：❌ 我卡在哪 / ✅ 纠正的关键一步 / 🔁 同类与变式 / ⏱️ 复习记录
  4. 复习记录里的勾选项日期 与 frontmatter review 一致：
     每个未完成项必须在 review 里；已完成项(打了叉)不该留在 review 里
     （`mastery: 3` 视为已归档，跳过这一项检查）
  5. 篇幅：60~90 行为宜（>90 提示拆分，<50 提示过简）
"""
import io
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "数学", "错题本")
REQUIRED_FM = ["create", "modify", "tags", "type", "year", "no", "kind", "topic", "cause", "mastery", "review"]
SECTIONS = ["❌ 我卡在哪", "✅ 纠正的关键一步", "🔁 同类与变式", "⏱️ 复习记录"]
SKIP = {"01 错题本使用规范.md", "00 错题本总览.md"}

errors, warns = [], []


def parse_fm(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return None
    fm, order, key = {}, [], None
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if km:
            key = km.group(1)
            fm[key] = km.group(2).strip()
            order.append(key)
        elif line.strip().startswith("- ") and key:
            fm.setdefault(key + "__list", []).append(line.strip()[2:].strip())
    return fm


def check(path, rel):
    text = io.open(path, encoding="utf-8").read()
    lines = text.splitlines()
    fm = parse_fm(text)
    if not fm:
        errors.append("[%s] 缺少 frontmatter" % rel)
        return
    for k in REQUIRED_FM:
        if k not in fm:
            errors.append("[%s] frontmatter 缺字段 `%s`" % (rel, k))
    if fm.get("type") != "mistake":
        errors.append("[%s] type 应为 mistake，现为 %r" % (rel, fm.get("type")))
    if "错题" not in fm.get("tags__list", []):
        errors.append("[%s] tags 缺少 `错题`" % rel)
    if not fm.get("cause__list"):
        errors.append("[%s] cause 为空（至少要有一个错因）" % rel)
    if fm.get("mastery") not in ("1", "2", "3"):
        errors.append("[%s] mastery 应为 1/2/3，现为 %r" % (rel, fm.get("mastery")))
    if not fm.get("review__list"):
        errors.append("[%s] review 为空（没有复习节点）" % rel)

    h1 = [l for l in lines if l.startswith("# ")]
    if len(h1) != 1:
        errors.append("[%s] H1 数量应为 1，现为 %d" % (rel, len(h1)))
    if not any(l.startswith("> 返回：") for l in lines):
        errors.append("[%s] 缺少「> 返回：」行" % rel)
    if "[!abstract]" not in text:
        errors.append("[%s] 缺少 [!abstract] 定位块" % rel)

    for s in SECTIONS:
        if s not in text:
            errors.append("[%s] 缺少小节 `#### %s`" % (rel, s))

    review_dates = set(fm.get("review__list", []))
    boxes = re.findall(r"^- \[([ xX])\]\s*(\d{4}-\d{2}-\d{2})", text, re.M)
    archived = fm.get("mastery") == "3"          # mastery 3 = 归档，不再排复习节点
    if not archived:
        for state, d in boxes:
            if state == " " and d not in review_dates:
                errors.append("[%s] 未完成项 %s 不在 frontmatter review 里" % (rel, d))
            if state.lower() == "x" and d in review_dates:
                errors.append("[%s] %s 已勾选，但仍留在 review 里（应删掉该日期）" % (rel, d))
        if not boxes and "review__list" in fm:
            warns.append("[%s] ⏱️ 复习记录 里没有可勾选的日期项" % rel)

    n = len(lines)
    if n > 90:
        warns.append("[%s] %d 行，超过 90 行——按规范考虑拆分/精简" % (rel, n))
    elif n < 50:
        warns.append("[%s] %d 行，偏简——检查「我卡在哪」是否写清" % (rel, n))


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else ""
    hits = 0
    for dirpath, _, files in os.walk(ROOT):
        if os.path.basename(dirpath) == "templates":
            continue
        for f in sorted(files):
            if not f.endswith(".md") or f in SKIP:
                continue
            if target and target not in f:
                continue
            hits += 1
            check(os.path.join(dirpath, f), os.path.relpath(os.path.join(dirpath, f), ROOT))

    print("检查 %d 个文件" % hits)
    for w in warns:
        print("  ⚠️  " + w)
    for e in errors:
        print("  ❌  " + e)
    print("结论：%d 个错误，%d 个提示" % (len(errors), len(warns)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
