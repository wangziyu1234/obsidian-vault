from pathlib import Path
import pymupdf as fitz
root=Path('D:/obsidian')
pdf=next(Path('E:/BaiduNetdiskDownload/777现控200题➕答案').glob('*题目册*.pdf'))
doc=fitz.open(pdf)
for num,page,box in [(1,75,(450,500,795,695)),(3,76,(480,785,850,965)),(6,78,(253,242,884,443))]:
    dst=next((root/'附件').glob(f'现控强化1-{num}-*.png'))
    p=doc[page-1]; w,h=p.rect.width,p.rect.height
    clip=fitz.Rect(box[0]*w/910,box[1]*h/1287,box[2]*w/910,box[3]*h/1287)
    p.get_pixmap(dpi=300,clip=clip).save(dst)
    print(num)
