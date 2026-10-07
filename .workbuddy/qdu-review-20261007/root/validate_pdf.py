from pathlib import Path
import json,re,zipfile
import pymupdf as fitz

base=Path('D:/obsidian/控制理论/青岛大学825真题')
out=base/'模拟卷PDF'
report=[]
for year in range(2006,2026):
    for kind in ['模拟卷','答案与解析']:
        p=out/f'{year}年青岛大学825{kind}.pdf'
        source=base/'Markdown笔记'/f'{year}年青岛大学825{"试题" if kind=="模拟卷" else kind}.md'
        expected=re.findall(r'^## ((?:选择|计算)?第\d+题)\s*$',source.read_text(encoding='utf-8-sig'),re.M)
        doc=fitz.open(p)
        seen=[];toc=[];outside=[];bad=[];blanks=[];multi=[]
        for pi,page in enumerate(doc):
            text=page.get_text()
            if '\ufffd' in text or '\uffff' in text:bad.append((pi+1,'replacement glyph'))
            if re.search(r'flowchart LR|xychart-beta|MATHPLACEHOLDER|<svg',text):bad.append((pi+1,'unrendered source'))
            headings=re.findall(r'(?m)^((?:选择|计算)?第\d+题)(?:\s*·\s*(续答))?\s*$',text)
            actual=[q for q,cont in headings if not cont]
            if kind=='模拟卷':
                if len(actual)>1:multi.append((pi+1,actual))
                seen+=actual
                if not actual and not any(c for _,c in headings):blanks.append(pi+1)
                if re.search(r'查看本题解析|返回本题题目|\*\*|\[!tip\]',text):bad.append((pi+1,'markup/navigation leaked'))
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines',[]):
                    label=''.join(span['text'] for span in line['spans']).strip()
                    if label in expected and max((span['size'] for span in line['spans']),default=0)>=11.7:
                        if label not in [x[1] for x in toc]:toc.append([1,label,pi+1])
                    for span in line['spans']:
                        x0,y0,x1,y1=span['bbox']
                        if x0<-.5 or y0<-.5 or x1>page.rect.width+.5 or y1>page.rect.height+.5:outside.append((pi+1,span['text']))
        assert not outside,(p.name,'outside',outside[:5])
        assert not bad,(p.name,bad)
        assert not multi,(p.name,'multiple questions on a page',multi)
        if kind=='模拟卷':assert seen==expected,(p.name,seen,expected)
        assert len(toc)==len(expected),(p.name,'bookmarks',len(toc),len(expected))
        doc.set_toc(toc)
        doc.set_metadata({'title':f'{year}年青岛大学自动控制理论{kind}','author':'个人复习整理','subject':'回忆版独立复核；每年独立模拟卷与答案册','keywords':'青岛大学,控制理论,一页一道,平板练习'})
        doc.saveIncr()
        report.append({'file':p.name,'pages':len(doc),'questions':len(expected),'bookmarks':len(toc),'overflow':len(outside),'cover_only_pages':blanks})
        doc.close()
Path(__file__).with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'files':len(report),'pages':sum(x['pages'] for x in report),'question_count':sum(x['questions'] for x in report if '模拟卷' in x['file']),'all_passed':True},ensure_ascii=False))
