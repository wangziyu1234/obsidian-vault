from pathlib import Path
import json
import re

import pymupdf

root = Path(__file__).resolve().parents[1]
pdf = root / "数学/考研数学二/习题册/2006年考研数学二答案与解析.pdf"
out = root / ".workbuddy/math2006-pdf-review"
out.mkdir(parents=True, exist_ok=True)
doc = pymupdf.open(pdf)
starts = {}
for index, page in enumerate(doc):
    text = re.sub(r"\s+", "", page.get_text())
    for match in re.finditer(r"(\d+)\.（2006\.(\d+)）", text):
        if match[1] == match[2]:
            starts[int(match[1])] = index
assert set(starts) == set(range(1, 24)), starts
rendered = []
for question in (12, 15, 20):
    for index in range(starts[question], starts[question + 1]):
        name = out / f"q{question}-p{index + 1}.png"
        doc[index].get_pixmap(dpi=135).save(name)
        rendered.append(str(name))
flat = re.sub(r"\s+", "", "".join(page.get_text() for page in doc))
for phrase in (
    "补充例：由约束消元求最小值",
    "只展开到二阶",
    "先读懂下标",
    "相加时，平方和与二阶偏导和分别怎样化简",
    "为什么最后不用反代",
):
    assert phrase in flat, phrase
assert "\uffff" not in flat, "Missing glyph in PDF text"
outside = []
for index, page in enumerate(doc):
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                box = pymupdf.Rect(span["bbox"])
                if box.x0 < 0 or box.y0 < 0 or box.x1 > page.rect.width or box.y1 > page.rect.height:
                    outside.append((index + 1, span["text"], list(box)))
assert not outside, outside
report = {"pages": len(doc), "question_pages": {q: p + 1 for q, p in starts.items()}, "rendered": rendered, "out_of_page_spans": outside}
(out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, indent=2))
