#!/usr/bin/env python3
"""Migrate duplicate review dates to one Tasks due date; preview by default.

Completed lines are never rewritten. Old schedules stay in a folded, non-task
note, and --apply saves the original bytes under the ignored .trash directory.
"""
from __future__ import annotations

import argparse
from datetime import date, datetime
import hashlib
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SECTION = "#### ⏱️ 复习记录"
DATE = r"\d{4}-\d{2}-\d{2}"
STAGES = ("当天", "次日", "第 3 天", "第 7 天", "第 30 天")


def stage_of(text: str) -> str:
    for value in reversed(STAGES):
        if value in text:
            return value
    if "明天" in text:
        return "次日"
    match = re.search(r"\+(1|3|7|30)(?!\d)", text)
    if match:
        return {"1": "次日", "3": "第 3 天", "7": "第 7 天", "30": "第 30 天"}[match[1]]
    raise ValueError(f"Unknown review stage: {text}")


def migrate(raw: bytes, today: str) -> tuple[bytes, dict]:
    date.fromisoformat(today)
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    eol = "\r\n" if "\r\n" in text else "\n"
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("Missing frontmatter")
    end = lines.index("---", 1)
    fm = lines[1:end]
    if "type: mistake" not in fm:
        raise ValueError("Not a mistake card")
    keys = [i for i, line in enumerate(fm) if line.startswith("review:")]
    if not keys:
        return raw, {"changed": False}
    if len(keys) != 1:
        raise ValueError("Duplicate review fields")
    mastery = int(next(line.split(":", 1)[1].strip() for line in fm if line.startswith("mastery:")))
    start = keys[0]
    stop = start + 1
    while stop < len(fm) and (not fm[stop].strip() or fm[stop][0].isspace()):
        stop += 1
    old_dates = re.findall(DATE, "\n".join(fm[start:stop]))
    for value in old_dates:
        date.fromisoformat(value)
    section = lines.index(SECTION, end)
    section_end = next((i for i in range(section + 1, len(lines)) if re.match(r"^#{1,4} ", lines[i])), len(lines))
    pending = []
    completed_dates = set()
    for i in range(section + 1, section_end):
        line = lines[i]
        if re.match(r"^- \[[xX]\] ", line):
            match = re.match(rf"^- \[[xX]\] ({DATE})", line)
            if match:
                completed_dates.add(match[1])
        match = re.match(r"^- \[ \] (.+)$", line)
        if match:
            value = re.match(DATE, match[1])
            pending.append({"index": i, "old": match[1], "date": value[0] if value else None, "stage": stage_of(match[1])})
    known = {x["date"] for x in pending if x["date"]} | completed_dates
    missing = [x for x in pending if not x["date"]]
    available = sorted(set(old_dates) - known)
    if missing:
        if len(missing) != 1 or len(available) != 1:
            raise ValueError("Cannot unambiguously recover an undated task")
        missing[0]["date"] = available[0]
    for item in pending:
        date.fromisoformat(item["date"])
    unresolved = set(old_dates) - {x["date"] for x in pending} - completed_dates
    if mastery in (1, 2) and unresolved:
        raise ValueError(f"Orphan review dates: {sorted(unresolved)}")
    if mastery in (1, 2) and not pending:
        raise ValueError("Active card has no pending task")
    if mastery in (0, 3) and pending:
        raise ValueError("Inactive card still has pending tasks")
    nearest = min(pending, key=lambda x: x["date"]) if pending else None
    replacement = f"- [ ] 错题复习（{nearest['stage']}） 📅 {nearest['date']}" if nearest else None
    old_completed = [line for line in lines if re.match(r"^- \[[xX]\] ", line)]
    # Keep old schedules as plain prose, never as task checkboxes.
    archive = []
    if old_dates or pending:
        archive = ["", "> [!note]- 旧复习计划（迁移留存）", "> 以下是迁移前的排期快照，后续日期只看上方的「错题复习」待办。"]
        if pending:
            archive += ["> 原未完成计划："] + ["> - " + x["old"] for x in pending]
        if old_dates:
            archive += ["> 原属性中的日期：" + "、".join(old_dates) + "。"]
        if missing:
            archive += ["> 原待办缺少日期，已由唯一对应的原属性日期补回。"]
        task_dates = {x["date"] for x in pending}
        if mastery in (1, 2) and task_dates != set(old_dates):
            archive += ["> 原任务与属性曾不一致：保留已完成勾选；未勾任务仍按待复习处理。"]
    indices = {x["index"] for x in pending}
    new_section = []
    for i in range(section + 1, section_end):
        if i in indices:
            if i == pending[0]["index"] and replacement:
                new_section.append(replacement)
        else:
            new_section.append(lines[i])
    # Update only obsolete workflow instructions inside the review section.
    new_section = [line.replace("哪天决定要这 6 分：把 `mastery` 改成 1，从当天起排「当天 / 次日 / +3 / +7 / +30」五个节点，它就转入正常复习流程。", "哪天决定要这 6 分：重做本题后运行「记录本次复习」，按本次表现恢复排期。")
                   .replace("若二刷时同类错再犯，按规范把 `mastery` 退回 1、从当天起重排明天 / +3 / +7。", "若二刷时同类错再犯，运行「记录本次复习」，选择本次表现即可恢复排期。")
                   for line in new_section]
    while new_section and not new_section[-1]:
        new_section.pop()
    lines[section + 1:section_end] = new_section + archive + ([""] if section_end < len(lines) else [])
    fm[start:stop] = []
    fm = ["modify: " + today if line.startswith("modify:") else line for line in fm]
    lines[1:end] = fm
    assert old_completed == [line for line in lines if re.match(r"^- \[[xX]\] ", line)]
    result = ("\ufeff" if bom else "") + eol.join(lines) + (eol if text.endswith(("\n", "\r")) else "")
    result_raw = result.encode("utf-8")
    return result_raw, {"changed": True, "mastery": mastery, "completed": len(old_completed), "next": nearest["date"] if nearest else None,
                        "old_pending": len(pending), "recovered_date": bool(missing),
                        "drift": mastery in (1, 2) and {x["date"] for x in pending} != set(old_dates)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--date", default=date.today().isoformat())
    args = parser.parse_args()
    plans = []
    for path in sorted((ROOT / "数学" / "错题本").glob("*/*.md")):
        original = path.read_bytes()
        updated, report = migrate(original, args.date)
        if report["changed"]:
            plans.append((path, original, updated, report))
            print(path.name, report)
    print(f"{'Apply' if args.apply else 'Preview'}: {len(plans)} cards; completed lines preserved: {sum(x[3]['completed'] for x in plans)}")
    if args.apply and plans:
        backup = ROOT / ".trash" / ("review-migration-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
        # All transforms have already passed before the first mutation.
        for path, original, updated, report in plans:
            if path.read_bytes() != original:
                raise RuntimeError(f"File changed concurrently: {path}")
            saved = backup / path.relative_to(ROOT)
            saved.parent.mkdir(parents=True, exist_ok=True)
            saved.write_bytes(original)
        for path, original, updated, report in plans:
            if path.read_bytes() != original:
                raise RuntimeError(f"File changed concurrently; backup at {backup}: {path}")
            path.write_bytes(updated)
            assert path.read_bytes() == updated
        print(f"Original bytes backed up: {backup}")
        print("SHA256 of original card bytes: " + hashlib.sha256(b"".join(x[1] for x in plans)).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
