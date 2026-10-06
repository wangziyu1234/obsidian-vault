from pathlib import Path
import pymupdf
from PIL import Image
import numpy as np
import sys
sys.path.insert(0,str(Path(__file__).parent))
from _pdf_render import find_pdf
pdf=pymupdf.open(find_pdf('现控200题【答案册】'))
page=pdf[50];r=page.rect
# PDF 51: full original diagram, including top input branch and lowest gain box.
clip=pymupdf.Rect(r.width*190/1281,r.height*380/1813,r.width*1015/1281,r.height*760/1813)
pix=page.get_pixmap(dpi=300,clip=clip)
im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples).convert('L')
a=np.array(im);a=np.where(a<170,0,255).astype('uint8')
im=Image.fromarray(a)
out=Path('D:/obsidian/附件/现控3-17-对偶系统模拟结构图.png')
assert a[:15].min()==255 and a[-15:].min()==255
assert a[:,:15].min()==255 and a[:,-15:].min()==255
im.save(out)
print('PDF51 crop',im.size,'white margins pass')
