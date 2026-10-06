from pathlib import Path
import fitz
root = Path('D:/obsidian')
doc = fitz.open(next(root.glob('自动控制原理（第八版）*.pdf')))
out = root / '.workbuddy/new-control-formula-source-20261006'
out.mkdir(exist_ok=True)
for lo, hi, terms in [(258,266,['6-14','6-18','6-12']), (346,358,['位置误差系数','朱利','7-110','7-105']), (447,485,['传递函数矩阵','状态转移矩阵','可控性判别']), (518,527,['观测器','反馈矩阵'])]:
    for book in range(lo, hi+1):
        t=doc[book+7].get_text()
        matches=[q for q in terms if q in t]
        if matches: print(book, '|'.join(matches))
for book in (260,265,266,351,356,461,462,466,481,518,526):
    doc[book+7].get_pixmap(matrix=fitz.Matrix(1.35,1.35)).save(out / f'p{book}.png')
print('Rendered candidate pages.')
