from pathlib import Path
import pymupdf as fitz
from PIL import Image, ImageDraw
root=Path('D:/obsidian')
out=root/'.workbuddy/mc-adv1-review-source'
out.mkdir(exist_ok=True)
src=Path('E:/BaiduNetdiskDownload/777现控200题➕答案')
for tag,pattern,first,last in [('q','*题目册*.pdf',75,90),('a','*答案册*.pdf',106,133)]:
    doc=fitz.open(next(src.glob(pattern)))
    for page in range(first,last+1):
        dst=out/f'{tag}{page}.png'
        if not dst.exists():
            doc[page-1].get_pixmap(matrix=fitz.Matrix(1.6,1.6)).save(dst)
    for page in range(first,last+1,2):
        ps=list(range(page,min(page+2,last+1)))
        ims=[Image.open(out/f'{tag}{p}.png').convert('RGB') for p in ps]
        for im in ims: im.thumbnail((900,1275))
        sheet=Image.new('RGB',(sum(im.width for im in ims),max(im.height for im in ims)+28),'white')
        draw=ImageDraw.Draw(sheet); x=0
        for p,im in zip(ps,ims):
            sheet.paste(im,(x,28));draw.text((x+20,6),f'{tag} PDF {p}',fill='black');x+=im.width
        sheet.save(out/f'{tag}{page}-pair.png')
print(out)
