import pathlib,re
b=pathlib.Path('D:/obsidian/.workbuddy/_qqdoc.bin').read_bytes()
i=b.find('基础8-20'.encode())
print(i,repr(b[i-100:i+500]))
urls=re.findall(rb'https?[^\x00-\x20"<>]+',b)
print('urls',len(urls))
print([u[:200] for u in urls[:5]])
t=pathlib.Path('D:/obsidian/.workbuddy/_errata_text.txt').read_text(encoding='utf-8')
i=t.find('基础8-20')
print('marker count',t[:i].count(chr(8)))
import subprocess
imgs=re.findall(rb'https://docimg[^\x00-\x20"<>]+?\.png\?w=\d+&h=\d+',b)
print('images',len(imgs))
out=pathlib.Path(__file__).parent
for j in range(106,110):
    url=imgs[j].decode().split('?')[0]
    print(j,url)
    subprocess.run(['curl.exe','-L','-s','--max-time','30','-A','Mozilla/5.0','-e','https://docs.qq.com/',url,'-o',str(out/f'errata{j}.png')],check=True)
