from pathlib import Path
import re,fitz
root=Path('D:/obsidian'); base=root/'控制理论/777习题集'
for ch in [1,5]:
    qp=next(base.glob(f'现控200题基础 第{ch}章*（题目）.md'))
    ap=next(base.glob(f'现控200题基础 第{ch}章*（答案与解析）.md'))
    for p in [qp,ap]:
        raw=p.read_bytes();t=raw.decode('utf-8-sig').replace('\r\n','\n')
        if p==qp:
            def backlink(m):
                num=m[1]; after=t[m.end():m.end()+250]
                if f'{ap.stem}#✏️ {num}　解析' in after:return m[0]
                return m[0]+f'\n\n[[{ap.stem}#✏️ {num}　解析|查看解析]]'
            t=re.sub(rf'^#### ✏️ ({ch}-\d+)　题目$',backlink,t,flags=re.M)
            if '## 🔎 题号直达' not in t:
                count=27 if ch==1 else 34
                nav=['## 🔎 题号直达','','| 题号范围 | 直达题目 |','| :-- | :-- |']
                for st in range(1,count+1,5):
                    en=min(st+4,count)
                    nav.append(f'| {ch}-{st}～{ch}-{en} | '+' · '.join(f'[[#✏️ {ch}-{i}　题目\\|{ch}-{i}]]' for i in range(st,en+1))+' |')
                first=re.search(r'^## ',t,re.M).start()
                t=t[:first]+'\n'.join(nav)+'\n\n'+t[first:]
        t='\n'.join(line.rstrip() for line in t.split('\n'))
        p.write_bytes(t.replace('\n','\r\n' if b'\r\n' in raw else '\n').encode('utf-8'))
pdf=next(Path('E:/BaiduNetdiskDownload/777现控200题➕答案').glob('*现控200题【题目册】.pdf'))
doc=fitz.open(pdf); page=doc[19]; w,h=page.rect.width,page.rect.height
page.get_pixmap(dpi=220,clip=fitz.Rect(.34*w,.22*h,.80*w,.268*h)).save(root/'附件/现控1-24-串联系统图.png')
