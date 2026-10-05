from pathlib import Path
import re
b=Path(__file__).with_name('errata.bin').read_bytes()
def vi(b,p):
    v=0;s=0
    while True:
        x=b[p];p+=1;v|=(x&127)<<s
        if x<128:return v,p
        s+=7
        if s>70:raise ValueError
def fields(b):
    p=0;out=[]
    while p<len(b):
        k,p=vi(b,p);n,w=k>>3,k&7
        if not n:raise ValueError
        if w==0:v,p=vi(b,p)
        elif w==2:
            l,p=vi(b,p);v=b[p:p+l];p+=l
            if p>len(b):raise ValueError
        elif w in (1,5):l=8 if w==1 else 4;v=b[p:p+l];p+=l
        else:raise ValueError
        out.append((n,w,v))
    return out
def walk(b,path=''):
    try: fs=fields(b)
    except:return
    for i,(n,w,v) in enumerate(fs):
        if w!=2:continue
        p=f'{path}/{n}:{i}'
        if b'https://docimg' in v and len(v)<2500:
            print('IMAGE',p,repr(v[:140]), re.findall(rb'https://docimg[^\x00-\x20\x7f-\xff]+',v))
        try:
            t=v.decode('utf8')
            if '基础8-33' in t:
                Path(__file__).with_name('errata_body.txt').write_text(t,encoding='utf8');print('BODY',p,len(t),t[:t.index('基础8-33')].count(chr(8)))
        except:pass
        walk(v,p)
walk(b)
