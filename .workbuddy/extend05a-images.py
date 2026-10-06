from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import re,json
r=Path('D:/obsidian'); names=sorted(set(n for p in (r/'控制理论/自动控制原理').glob('05-[12]*.md') for n in re.findall(r'!\[\[([^|\]]+)',p.read_text(encoding='utf-8-sig'))))
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18)
for group in range((len(names)+7)//8):
 canvas=Image.new('RGB',(1600,1800),'white');d=ImageDraw.Draw(canvas)
 for k,n in enumerate(names[group*8:group*8+8]):
  im=Image.open(r/'附件'/n);im.thumbnail((770,390));x=(k%2)*800;y=(k//2)*450
  canvas.paste(im,(x+(800-im.width)//2,y));d.text((x+10,y+401),str(group*8+k)+' '+n,font=font,fill='black')
 canvas.save(r/f'.workbuddy/extend05a-contact-{group}.png')
(r/'.workbuddy/extend05a-images.json').write_text(json.dumps(names,ensure_ascii=False),encoding='utf-8')
