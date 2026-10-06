from pathlib import Path
import fitz
src=next(Path('E:/BaiduNetdiskDownload/777现控200题➕答案').glob('*现控200题【题目册】.pdf'))
doc=fitz.open(src)
crops=[
('现控1-1-结构图.png',8,(.44,.46,.96,.59)),
('现控1-2-结构图.png',9,(.30,.136,.94,.32)),
('现控1-3-结构图.png',9,(.37,.594,.91,.668)),
('现控1-4-结构图.png',10,(.42,.17,.96,.30)),
('现控1-6-电路图.png',11,(.38,.19,.90,.31)),
('现控1-7-电路图.png',11,(.48,.66,.88,.80)),
('现控1-8-机械系统图.png',12,(.44,.185,.93,.35)),
('现控1-23-并联系统图.png',19,(.62,.72,.88,.88)),
('现控1-24-串联系统图.png',20,(.34,.22,.80,.272)),
]
for name,n,box in crops:
    page=doc[n-1];w,h=page.rect.width,page.rect.height
    rect=fitz.Rect(box[0]*w,box[1]*h,box[2]*w,box[3]*h)
    page.get_pixmap(clip=rect,dpi=220).save(Path('附件')/name)
    print(name,n)
