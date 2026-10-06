from pathlib import Path
import fitz

root = Path('D:/obsidian')
pdf = next(root.glob('自动控制原理（第八版）*.pdf'))
doc = fitz.open(pdf)
out = root / '.workbuddy' / 'appendix-time-source-20261006'
out.mkdir(exist_ok=True)
for book_page in (77, 78, 86, 87, 89):
    page = doc[book_page + 7]
    page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(out / f'p{book_page}.png')
    print(book_page, str(out / f'p{book_page}.png'))
