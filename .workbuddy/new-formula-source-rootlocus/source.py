from pathlib import Path
import re
import sys
import fitz

ROOT = Path('D:/obsidian')
OUT = Path(__file__).resolve().parent
if len(sys.argv) > 1:
    pdf = fitz.open(next(ROOT.glob('自动控制原理（第八版）*.pdf')))
    for arg in sys.argv[1:]:
        book = int(arg)
        page = pdf[book + 7]
        path = OUT / f'book-{book:03d}-pdf-{book+8:03d}.png'
        page.get_pixmap(matrix=fitz.Matrix(1.8, 1.8), alpha=False).save(path)
        print(path)
else:
    ocr = (ROOT / '教材OCR/胡寿松自动控制原理-第八版.txt').read_text(encoding='utf-8-sig')
    for pdf_page, text in re.findall(r'=== Page (\d+) ===(.*?)(?==== Page |\Z)', ocr, re.S):
        n = int(pdf_page)
        if n > 210:
            continue
        hits = [line for line in text.splitlines() if re.search('梅森增益公式记为|方框的反馈连接|二阶.*稳定|三阶.*稳定|劳斯表|渐近线|分离点|幅值条件|相角条件|出射角', line)]
        if hits:
            print(f'book {n-8} / PDF {n}: ' + ' | '.join(hits[:8]))
