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
  4. frontmatter 不再保留 review / review-start；复习区只安排次日、第 3 天、
     第 7 天、第 30 天四轮 Tasks 待办，直接打勾即可，不安排当天待办。
     mastery 1/2 可有 0~4 条待办，mastery 0/3 不排待办；阶段和日期不能重复，
     日期按阶段递增。
     历史已完成记录原样保留，不用次数推断掌握度；忽略代码块及其他小节待办。
  5. 篇幅仅作提示，复习历史增长不要求精简或拆分单题。

本脚本只读文件，不修改笔记。frontmatter 支持平铺字段及行内/分行字符串列表。
"""
from datetime import date
import io
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "数学", "错题本")
REQUIRED_FM = ["create", "modify", "tags", "type", "year", "no", "kind", "topic", "cause", "mastery"]
SECTIONS = ["❌ 我卡在哪", "✅ 纠正的关键一步", "🔁 同类与变式", "⏱️ 复习记录"]
REVIEW_STAGES = ("次日", "第 3 天", "第 7 天", "第 30 天")
SKIP = {"01 错题本使用规范.md", "00 错题本总览.md"}
FM_PATTERN = re.compile(r"^\ufeff?---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.S)

errors, warns = [], []


def unquote(value):
    """Read a plain or quoted scalar from the card's flat YAML fields."""
    value = value.strip()
    if value.startswith('"'):
        match = re.match(r'"(?:[^"\\]|\\.)*"', value)
        if match:
            try:
                return json.loads(match.group())
            except ValueError:
                return match.group()[1:-1]
    elif value.startswith("'"):
        match = re.match(r"'(?:[^']|'')*'", value)
        if match:
            return match.group()[1:-1].replace("''", "'")
    return re.split(r"\s+#", value, maxsplit=1)[0].strip()


def parse_fm(text):
    m = FM_PATTERN.match(text)
    if not m:
        return None
    fm, key = {}, None
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_][A-Za-z_0-9-]*):\s*(.*)$", line)
        if km:
            key = km.group(1)
            value = km.group(2).strip()
            fm[key] = unquote(value)
            sequence = re.fullmatch(r"\[(.*)\]\s*(?:#.*)?", value)
            if sequence:
                items = re.findall(r'''"(?:[^"\\]|\\.)*"|'(?:[^']|'')*'|[^,\s][^,]*''', sequence.group(1))
                fm[key + "__list"] = [unquote(item) for item in items if item.strip()]
        elif line.strip().startswith("- ") and key:
            fm.setdefault(key + "__list", []).append(unquote(line.strip()[2:]))
    return fm


def prose_lines(text):
    """Remove frontmatter and fenced examples without changing line positions."""
    m = FM_PATTERN.match(text)
    if m:
        text = "\n" * text[:m.end()].count("\n") + text[m.end():]
    result, fence = [], None
    for line in text.splitlines():
        # Callout code examples are fenced too; strip quote prefixes only for detection.
        candidate = re.sub(r"^(?: {0,3}> ?)+", "", line)
        if fence:
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + r"{" + str(len(fence)) + r",}\s*", candidate):
                fence = None
            result.append("")
        else:
            opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", candidate)
            if opening and (opening.group(1)[0] != "`" or "`" not in opening.group(2)):
                fence = opening.group(1)
                result.append("")
            else:
                result.append(line)
    return result


def review_lines(lines):
    """Yield only the review section, ending at the next peer/parent heading."""
    active = False
    for line in lines:
        heading = re.match(r"^(#{1,6})\s+(.+?)(?:\s+#+)?\s*$", line)
        if heading and len(heading.group(1)) <= 4:
            active = len(heading.group(1)) == 4 and heading.group(2) == SECTIONS[-1]
        elif active:
            yield line


def check_text(text, rel):
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
    if fm.get("mastery") not in ("0", "1", "2", "3"):
        errors.append("[%s] mastery 应为 0/1/2/3，现为 %r" % (rel, fm.get("mastery")))
    for key in ("review", "review-start"):
        if key in fm:
            errors.append("[%s] 迁移未完成：删除旧 frontmatter `%s`，日期只保留在复习任务中" % (rel, key))

    prose = prose_lines(text)
    h1 = [l for l in prose if l.startswith("# ")]
    if len(h1) != 1:
        errors.append("[%s] H1 数量应为 1，现为 %d" % (rel, len(h1)))
    if not any(l.startswith("> 返回：") for l in prose):
        errors.append("[%s] 缺少「> 返回：」行" % rel)
    if not any("[!abstract]" in l for l in prose):
        errors.append("[%s] 缺少 [!abstract] 定位块" % rel)

    for s in SECTIONS:
        if not any(re.fullmatch(r"####\s+" + re.escape(s) + r"(?:\s+#+)?\s*", l) for l in prose):
            errors.append("[%s] 缺少小节 `#### %s`" % (rel, s))

    pending = []
    for line in review_lines(prose):
        candidate = re.sub(r"^(?: {0,3}> ?)+", "", line)
        task = re.match(r"^\s*[-*+]\s+\[([^\]\r\n])\]\s*(.*)$", candidate)
        if task and task.group(1) not in ("x", "X"):
            pending.append(line)
    if pending:
        if fm.get("mastery") in ("0", "3"):
            errors.append("[%s] mastery: %s 不应有未完成复习任务，现有 %d 条" % (rel, fm["mastery"], len(pending)))
        if len(pending) > 4:
            errors.append("[%s] 未完成复习任务最多 4 条，现有 %d 条" % (rel, len(pending)))
    stages, dated = [], []
    for line in pending:
        task = re.fullmatch(r"- \[ \] 错题复习（(次日|第 3 天|第 7 天|第 30 天)） 📅 (\d{4}-\d{2}-\d{2})\s*", line)
        if not task:
            errors.append("[%s] 复习待办格式应为 `- [ ] 错题复习（次日/第 3 天/第 7 天/第 30 天） 📅 YYYY-MM-DD`，不再安排当天待办" % rel)
            continue
        stage, due = task.groups()
        stages.append(stage)
        try:
            dated.append((REVIEW_STAGES.index(stage), date.fromisoformat(due)))
        except ValueError:
            errors.append("[%s] 复习日期无效：%s" % (rel, due))
    if len(set(stages)) != len(stages):
        errors.append("[%s] 未完成复习任务的阶段不能重复" % rel)
    dates = [due for _, due in dated]
    if len(set(dates)) != len(dates):
        errors.append("[%s] 未完成复习任务的日期不能重复" % rel)
    ordered = sorted(dated)
    if any(earlier_stage < later_stage and earlier_due >= later_due
           for (earlier_stage, earlier_due), (later_stage, later_due) in zip(ordered, ordered[1:])):
        errors.append("[%s] 未完成复习任务的日期必须按次日、第 3 天、第 7 天、第 30 天顺序递增" % rel)

    n = len(lines)
    if n > 90:
        warns.append("[%s] %d 行；复习记录可随历史增长，单题保持完整（仅提示）" % (rel, n))
    elif n < 50:
        warns.append("[%s] %d 行，偏简——检查「我卡在哪」是否写清" % (rel, n))


def check(path, rel):
    with io.open(path, encoding="utf-8-sig") as handle:
        check_text(handle.read(), rel)


def main():
    errors.clear()
    warns.clear()
    target = sys.argv[1] if len(sys.argv) > 1 else ""
    hits = 0
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d != "templates"]
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
