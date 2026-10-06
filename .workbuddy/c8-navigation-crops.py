from pathlib import Path
import fitz
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont

root = Path('D:/obsidian')
folder = Path('E:/BaiduNetdiskDownload/777真诚27考研习题集')
answer = fitz.open(next(p for p in folder.glob('*.pdf') if '基础' in p.name))
question = fitz.open(next(p for p in folder.glob('*.pdf') if p.name.endswith('300题.pdf')))
out = root / '附件'
scratch = root / '.workbuddy/c8-navigation-crops'
scratch.mkdir(exist_ok=True)

def crop(doc, page, rect):
    pg = doc[page-1]
    w, h = pg.rect.width, pg.rect.height
    clip = fitz.Rect(rect[0]*w, rect[1]*h, rect[2]*w, rect[3]*h)
    pix = pg.get_pixmap(dpi=300, clip=clip, alpha=False)
    im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    arr = np.asarray(im).astype(float)
    keep = (np.max(arr, axis=2)-np.min(arr, axis=2) < 38) & (arr.mean(axis=2) < 170)
    im = Image.fromarray(np.where(keep, 0, 255).astype('uint8'))
    return ImageOps.expand(im, border=20, fill=255)

six_specs = [
    (204, (.49, .245, .75, .427)),
    (204, (.50, .483, .75, .660)),
    (204, (.48, .702, .75, .876)),
    (205, (.45, .088, .72, .260)),
    (205, (.46, .297, .72, .484)),
    (205, (.47, .521, .73, .681)),
]
canvas = Image.new('L', (1100, 1500), 255)
draw = ImageDraw.Draw(canvas)
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 26)
for i, spec in enumerate(six_specs):
    im = crop(answer, *spec)
    im.thumbnail((490, 440))
    px, py = (i%2)*550, (i//2)*500
    canvas.paste(im, (px+(550-im.width)//2, py+45+(440-im.height)//2))
    draw.text((px+22, py+12), f'({i+1})', fill=0, font=font)
canvas.save(out / '777-基础8-4-六类相轨迹原解.png')

specs = [
    ('777-基础8-5-局部相轨迹原解.png', answer, 206, (.332,.378,.792,.539)),
    ('777-基础8-10-相轨迹原解.png', answer, 210, (.357,.411,.720,.576)),
    ('777-基础8-12-相轨迹原解.png', answer, 212, (.430,.405,.714,.578)),
    ('777-基础8-13-相轨迹原解.png', answer, 213, (.366,.363,.635,.492)),
    ('777-8-29-结构图.png', question, 163, (.412,.566,.850,.675)),
    ('777-8-31-结构图.png', question, 164, (.535,.640,.923,.773)),
]
for name, doc, page, rect in specs:
    crop(doc,page,rect).save(out/name)
    print(name)
print('Six phase types and six individual crops saved.')
