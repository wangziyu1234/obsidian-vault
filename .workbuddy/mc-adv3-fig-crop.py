from pathlib import Path
import pymupdf as fitz
from PIL import Image, ImageOps
root=Path('D:/obsidian')
src=Path('E:/BaiduNetdiskDownload/777现控200题➕答案')
out=root/'.workbuddy/mc-adv3-fig-source'
q=fitz.open(next(src.glob('*题目册*.pdf')))
a=fitz.open(next(src.glob('*答案册*.pdf')))
# Rectangles are selected from fresh 1.5x full-page renders, with white margins.
jobs=[(q,107,(298,387,762,563),'现控强化3-3-开环系统结构图.png'),
      (q,117,(188,167,691,526),'现控强化3-22-状态反馈系统框图.png'),
      (a,158,(254,841,780,1129),'现控强化3-5-ans-状态变量图.png')]
for doc,n,box,name in jobs:
    rect=fitz.Rect(*(v/1.5 for v in box))
    pix=doc[n-1].get_pixmap(matrix=fitz.Matrix(4,4),clip=rect)
    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    # Remove the red diagonal source watermark without altering black diagram strokes.
    import numpy as np
    ar=np.array(im)
    grey=ar[:,:,0].copy()
    grey[grey>225]=255
    im=ImageOps.expand(Image.fromarray(grey).convert('RGB'),border=25,fill='white')
    im.save(root/'附件'/name)
    print(name,im.size)
