from pathlib import Path
import re,json
from PIL import Image,ImageOps,ImageDraw,ImageFont
root=Path('D:/obsidian'); files=sorted((root/'控制理论/自动控制原理').glob('05-[34]*.md'))
names=sorted(set(n for p in files for n in re.findall(r'!\[\[([^|\]]+)',p.read_text(encoding='utf-8-sig'))))
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18)
for start in range(0,len(names),8):
    canvas=Image.new('RGB',(1600,1200),'white'); draw=ImageDraw.Draw(canvas)
    for i,name in enumerate(names[start:start+8]):
        im=Image.open(root/'附件'/name); im.thumbnail((790,255))
        x=(i%2)*800;y=(i//2)*300
        canvas.paste(im,(x+(800-im.width)//2,y+35));draw.text((x+8,y+4),f'{start+i}: {name}',font=font,fill='black')
    canvas.save(root/f'.workbuddy/extend-05b-sheet-{start//8}.png')
(root/'.workbuddy/extend-05b-images.json').write_text(json.dumps(names,ensure_ascii=False),encoding='utf-8')
print(len(names))
