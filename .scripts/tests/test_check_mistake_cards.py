"""Regression tests for the single-task mistake-card review workflow."""
import importlib.util
from pathlib import Path
import tempfile
import unittest


SPEC = importlib.util.spec_from_file_location(
    "check_mistake_cards", Path(__file__).resolve().parents[1] / "check-mistake-cards.py"
)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


def card(mastery="1", records="- [ ] 错题复习（次日） 📅 2026-10-06", extra_fm=""):
    return """---
create: 2026-10-05
modify: 2026-10-05
tags: [数学, 错题]
type: mistake
year: 2000
no: 17
kind: 解答
topic: 微分
cause: [概念, "条件, 检查"]
mastery: %s
%s---
> 返回：[[00 错题本总览]]

# 测试错题

> [!abstract] 本讲定位
> 测试卡片。

#### ❌ 我卡在哪

漏掉条件。

#### ✅ 纠正的关键一步

先确认条件。

#### 🔁 同类与变式

保留原题链接。

#### ⏱️ 复习记录

%s
""" % (mastery, extra_fm, records)


class MistakeCardChecks(unittest.TestCase):
    def setUp(self):
        checker.errors.clear()
        checker.warns.clear()

    def inspect(self, text):
        checker.check_text(text, "test.md")
        return checker.errors

    def test_inline_and_block_lists(self):
        self.assertEqual(self.inspect(card()), [])
        checker.errors.clear()
        text = card().replace("tags: [数学, 错题]", "tags:\n  - '数学'\n  - \"错题\"")
        text = text.replace('cause: [概念, "条件, 检查"]', "cause:\n  - 概念\n  - '条件, 检查'")
        self.assertEqual(self.inspect(text), [])
        self.assertEqual(checker.parse_fm(card())["cause__list"], ["概念", "条件, 检查"])

    def test_archived_or_unstarted_needs_no_pending_task(self):
        for mastery in ("0", "3"):
            with self.subTest(mastery=mastery):
                checker.errors.clear()
                self.assertEqual(self.inspect(card(mastery, "- [x] 2026-09-30 当日")), [])
                self.assertTrue(self.inspect(card(mastery)))

    def test_review_property_even_empty_means_migration_incomplete(self):
        for mastery in ("0", "1", "3"):
            with self.subTest(mastery=mastery):
                checker.errors.clear()
                records = "" if mastery in ("0", "3") else "- [ ] 错题复习（次日） 📅 2026-10-06"
                errors = self.inspect(card(mastery, records, "review: []\n"))
                self.assertTrue(any("迁移未完成" in e for e in errors))

    def test_invalid_calendar_dates(self):
        for invalid in ("2026-02-29", "2026-02-30", "2026-13-01", "0000-01-01"):
            with self.subTest(date=invalid):
                checker.errors.clear()
                errors = self.inspect(card(records="- [ ] 错题复习（次日） 📅 " + invalid))
                self.assertTrue(any("日期无效" in e for e in errors))
        checker.errors.clear()
        self.assertEqual(self.inspect(card(records="- [ ] 错题复习（次日） 📅 2028-02-29")), [])

    def test_active_cards_need_exactly_one_task(self):
        for mastery in ("1", "2"):
            for records in ("", "- [ ] 错题复习（次日） 📅 2026-10-06\n- [ ] 错题复习（隔三日） 📅 2026-10-08"):
                with self.subTest(mastery=mastery, records=records):
                    checker.errors.clear()
                    self.assertTrue(any("只能有一条" in e for e in self.inspect(card(mastery, records))))

    def test_legacy_pending_format_is_rejected(self):
        self.assertTrue(any("格式应为" in e for e in self.inspect(card(records="- [ ] 2026-10-06 次日"))))

    def test_completed_history_requires_no_result_or_count(self):
        records = "\n".join(["- [x] 2026-10-01 当日", "- [X] 2026-10-02 次日", "- [x] 复习 ✅ 2026-10-05 —— 提示后做对"] * 30)
        records += "\n- [ ] 错题复习（次日） 📅 2026-10-06"
        self.assertEqual(self.inspect(card("1", records)), [])
        self.assertTrue(checker.warns)
        self.assertFalse(any("拆分" in warning or "精简" in warning for warning in checker.warns))

    def test_task_scope_excludes_other_sections_and_fences(self):
        text = card().replace("漏掉条件。", "漏掉条件。\n- [ ] 其他正文待办 📅 2026-10-05")
        text += "\n````markdown\n# 示例 H1\n#### ⏱️ 复习记录\n- [ ] 2026-02-30\n```\n- [ ] 2026-02-30\n````\n"
        text += "\n~~~markdown\n- [ ] 2026-02-30\n~~~\n"
        text += "\n> ```markdown\n> - [ ] 2026-02-30\n> ```\n"
        text += "\n#### 其他小节\n- [ ] 其他小节待办\n"
        self.assertEqual(self.inspect(text), [])

    def test_code_sample_does_not_supply_missing_review_heading(self):
        text = card().replace("#### ⏱️ 复习记录", "```markdown\n#### ⏱️ 复习记录\n```")
        self.assertTrue(any("缺少小节" in e for e in self.inspect(text)))

    def test_bom_crlf_and_read_only_file_check(self):
        data = ("\ufeff" + card()).replace("\n", "\r\n").encode("utf-8")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.md"
            path.write_bytes(data)
            checker.check(path, "test.md")
            self.assertEqual(checker.errors, [])
            self.assertEqual(path.read_bytes(), data)


if __name__ == "__main__":
    unittest.main()
