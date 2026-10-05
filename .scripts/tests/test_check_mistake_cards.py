"""Regression tests for four-round mistake-card tasks marked directly by hand."""
import importlib.util
from pathlib import Path
import tempfile
import unittest


SPEC = importlib.util.spec_from_file_location(
    "check_mistake_cards", Path(__file__).resolve().parents[1] / "check-mistake-cards.py"
)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


def card(mastery="1", records="", extra_fm=""):
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

    def test_all_mastery_values_allow_no_tasks(self):
        for mastery in ("0", "1", "2", "3"):
            with self.subTest(mastery=mastery):
                checker.errors.clear()
                self.assertEqual(self.inspect(card(mastery)), [])
                self.assertEqual(self.inspect(card(mastery, "- [x] 2026-09-30 当日")), [])

    def test_obsolete_review_properties_mean_migration_incomplete(self):
        for mastery in ("0", "1", "2", "3"):
            for extra in ("review: []\n", "review-start: 2026-10-05\n", "review-start:\n"):
                with self.subTest(mastery=mastery, extra=extra):
                    checker.errors.clear()
                    errors = self.inspect(card(mastery, extra_fm=extra))
                    self.assertTrue(any("迁移未完成" in e for e in errors))

    def test_active_cards_allow_zero_to_four_pending_rounds(self):
        rounds = ["- [ ] 错题复习（%s） 📅 %s" % pair for pair in zip(
            checker.REVIEW_STAGES, ("2026-10-06", "2026-10-08", "2026-10-12", "2026-11-04")
        )]
        for mastery in ("1", "2"):
            for count in range(5):
                with self.subTest(mastery=mastery, count=count):
                    checker.errors.clear()
                    self.assertEqual(self.inspect(card(mastery, "\n".join(rounds[:count]))), [])
        checker.errors.clear()
        self.assertEqual(self.inspect(card(records=rounds[0] + "\n" + rounds[3])), [])

    def test_invalid_calendar_dates(self):
        for invalid in ("2026-02-29", "2026-02-30", "2026-13-01", "0000-01-01"):
            with self.subTest(date=invalid):
                checker.errors.clear()
                errors = self.inspect(card(records="- [ ] 错题复习（次日） 📅 " + invalid))
                self.assertTrue(any("日期无效" in e for e in errors))
        checker.errors.clear()
        self.assertEqual(self.inspect(card(records="- [ ] 错题复习（次日） 📅 2028-02-29")), [])

    def test_duplicate_stages_or_dates_are_rejected(self):
        first = "- [ ] 错题复习（次日） 📅 2026-10-06"
        for second, message in (("- [ ] 错题复习（次日） 📅 2026-10-08", "阶段不能重复"),
                                ("- [ ] 错题复习（第 3 天） 📅 2026-10-06", "日期不能重复")):
            with self.subTest(second=second):
                checker.errors.clear()
                self.assertTrue(any(message in e for e in self.inspect(card(records=first + "\n" + second))))

    def test_stage_dates_must_increase_even_if_source_lines_are_reordered(self):
        records = "- [ ] 错题复习（第 7 天） 📅 2026-10-06\n- [ ] 错题复习（次日） 📅 2026-10-08"
        self.assertTrue(any("顺序递增" in e for e in self.inspect(card(records=records))))

    def test_archived_or_unstarted_cannot_have_pending_tasks(self):
        for mastery in ("0", "3"):
            with self.subTest(mastery=mastery):
                checker.errors.clear()
                errors = self.inspect(card(mastery, "- [ ] 错题复习（次日） 📅 2026-10-06"))
                self.assertTrue(any("不应有未完成复习任务" in e for e in errors))

    def test_today_and_malformed_pending_tasks_are_rejected(self):
        for records in ("- [ ] 错题复习（当天） 📅 2026-10-05", "- [ ] 2026-10-06 次日", "- [ ] 错题复习（次日） 📅 2026-1-06", "> - [ ] 引用中的待办", "- [/] 复习进行中"):
            with self.subTest(records=records):
                checker.errors.clear()
                self.assertTrue(any("格式应为" in e for e in self.inspect(card(records=records))))

    def test_at_most_four_pending_tasks(self):
        errors = self.inspect(card(records="\n".join(["- [ ] 错题复习（次日） 📅 2026-10-06"] * 5)))
        self.assertTrue(any("最多 4 条" in e for e in errors))

    def test_completed_history_requires_no_result_or_count(self):
        records = "\n".join(["- [x] 2026-10-01 当日", "- [X] 2026-10-02 次日", "- [x] 复习 ✅ 2026-10-05 —— 提示后做对"] * 30)
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
