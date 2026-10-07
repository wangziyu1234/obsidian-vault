from pathlib import Path
import pymupdf as fitz
root=Path('D:/obsidian')
pdf=next(Path('E:/BaiduNetdiskDownload/777现控200题➕答案').glob('*题目册*.pdf'))
page=fitz.open(pdf)[77]
w,h=page.rect.width,page.rect.height
clip=fitz.Rect(445*w/900,740*h/1275,864*w/900,1006*h/1275)
page.get_pixmap(dpi=400,clip=clip).save(root/'附件/现控强化1-7-结构图.png')
