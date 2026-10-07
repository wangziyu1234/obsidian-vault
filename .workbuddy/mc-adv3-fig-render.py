from pathlib import Path
import pymupdf as fitz
from PIL import Image, ImageDraw

root=Path('D:/obsidian')
src=Path('E:/BaiduNetdiskDownload/777现控200题➕答案')
out=root/'.workbuddy/mc-adv3-fig-source'
out.mkdir(exist_ok=True)
for tag,pattern,first,last in [('q','*题目册*.pdf',106,123),('a','*答案册*.pdf',156,191)]:
    doc=fitz.open(next(src.glob(pattern)))
    last=min(last,len(doc))
    images=[]
    for n in range(first,last+1):
        dst=out/f'{tag}{n}.png'
        if not dst.exists():
            doc[n-1].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(dst)
        im=Image.open(dst).convert('RGB');im.thumbnail((310,438));images.append((n,im))
    for start in range(0,len(images),12):
        chunk=images[start:start+12]
        sheet=Image.new('RGB',(310*4,465*3),'white');d=ImageDraw.Draw(sheet)
        for k,(n,im) in enumerate(chunk):
            x=(k%4)*310;y=(k//4)*465
            sheet.paste(im,(x,y+24));d.text((x+15,y+5),f'{tag} PDF {n}',fill='black')
        sheet.save(out/f'{tag}-contact-{start}.png')
print(out)
