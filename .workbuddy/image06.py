from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import re,json
names=sorted(set(n for p in Path('控制理论/自动控制原理').glob('06*.md') for n in re.findall(r'!\[\[([^|\]]+)',p.read_text(encoding='utf-8-sig'))))
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',17)
for k in range(0,len(names),12):
 batch=names[k:k+12];out=Image.new('RGB',(1200,400*((len(batch)+2)//3)),'#eeeeee');d=ImageDraw.Draw(out)
 for j,n in enumerate(batch):
  im=Image.open(Path('附件')/n).convert('RGB');im.thumbnail((390,340));x=(j%3)*400;y=(j//3)*400;out.paste(im,(x+(400-im.width)//2,y));d.text((x+5,y+345),str(k+j)+' '+n[:21],font=font,fill='black')
 out.save(f'.workbuddy/contact06-{k//12}.png')
Path('.workbuddy/images06.json').write_text(json.dumps(names,ensure_ascii=False),encoding='utf-8')
print(len(names))
