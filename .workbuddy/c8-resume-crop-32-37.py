from pathlib import Path
import json
import pymupdf

ROOT = Path('D:/obsidian/.workbuddy/c8-resume-crops')
ROOT.mkdir(parents=True, exist_ok=True)
PDF = next(p for p in Path('E:/BaiduNetdiskDownload/777真诚27考研习题集').glob('*.pdf') if p.name.endswith(' 777习题集300题.pdf'))
doc = pymupdf.open(PDF)
entries = {
    '8-34': (166, (215, 170, 532, 295)),
    '8-35': (166, (252, 459, 532, 575)),
    '8-36': (167, (207, 154, 513, 293)),
    '8-37': (167, (188, 562, 514, 696)),
}
manifest = []
for question, (page_number, rect) in entries.items():
    page = doc[page_number - 1]
    output = ROOT / (question + '-structure.png')
    page.get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=pymupdf.Rect(rect), alpha=False).save(output)
    manifest.append({'question': question, 'pdf_page': page_number, 'page_size': [page.rect.width, page.rect.height], 'rect_points': rect, 'rect_normalized': [rect[0]/page.rect.width, rect[1]/page.rect.height, rect[2]/page.rect.width, rect[3]/page.rect.height], 'png': str(output)})
(ROOT / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(manifest, ensure_ascii=True, indent=2))
