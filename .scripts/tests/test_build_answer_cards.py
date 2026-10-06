"""Regression checks for headings and display math in answer PDF conversion."""

import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "build-answer-cards.py"
SPEC = importlib.util.spec_from_file_location("build_answer_cards", SCRIPT)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class AnswerCardConversionTests(unittest.TestCase):
    def test_numbered_heading_keeps_existing_question_pagination(self):
        prefix = "# Answers\n\n## Section\n\nEarlier content.\n\n"
        bold = BUILDER.convert(prefix + "**12.(2006.12) Answer: D.**\n")
        heading = BUILDER.convert(prefix + "### 12.(2006.12) Answer: D.\n")
        self.assertEqual(bold, heading)
        self.assertIn(r"\clearpage", heading)

    def test_example_heading_has_no_markdown_or_unsupported_pencil(self):
        result = BUILDER.convert("# Answers\n\n#### ✏️ Worked example\n")
        self.assertIn(r"{\bfseries Worked example\par}", result)
        self.assertNotIn("✏", result)
        self.assertNotIn(r"\#", result)

    def test_callout_preserves_one_contiguous_display_math_block(self):
        source = r"""# Answers

> [!derivation] Chain rule
> Before.
>
> $$
> \begin{aligned}
> z_{xx}&=f''(u)u_x^2\\
>
> &\quad+f'(u)u_{xx}.
> \end{aligned}
> $$
>
> After.
"""
        result = BUILDER.convert(source).replace("\r\n", "\n")
        display = result.split("$$")[1]
        self.assertNotIn("\n\n", display)
        self.assertIn(r"z_{xx}&=", display)
        self.assertIn(r"\begin{aligned}", display)
        self.assertIn(r"\end{aligned}", display)
        self.assertIn("Before.\n\n$$", result)
        self.assertIn("$$\n\nAfter.", result)

    def test_callout_step_heading_reserves_space_for_its_formula(self):
        source = "# Answers\n\n> [!derivation] Derivatives\n> **Step 2.** Differentiate.\n>\n> $$\n> u_y=y/u.\n> $$\n"
        result = BUILDER.convert(source)
        self.assertIn(r"\Needspace{9\baselineskip}\textbf{Step 2.}", result)


if __name__ == "__main__":
    unittest.main()
