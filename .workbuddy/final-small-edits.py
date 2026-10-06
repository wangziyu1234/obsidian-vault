from pathlib import Path
root=Path('控制理论/自动控制原理')
p=root/'06-1-d 频率法滞后校正例题（卢京潮讲义）.md'
b=p.read_bytes(); t=b.decode('utf-8'); nl='\r\n' if '\r\n' in t else '\n'; lines=t.splitlines()
out=[]; skip=False
for line in lines:
    if line.startswith('> [!note] 例2 的精确复核'): skip=True; continue
    if skip:
        if not line: skip=False
        continue
    out.append(line.replace('h>h^*=10',r'h(\mathrm{dB})>10'))
p.write_bytes((nl.join(out)+nl).encode('utf-8'))
p=root/'06-3-b 滞后-超前频率法图解例题（卢京潮讲义）.md';t=p.read_bytes().decode('utf-8');nl='\r\n' if '\r\n' in t else '\n';lines=t.splitlines()
for i,line in enumerate(lines):
    if line.startswith('> 极点由**低频幅值平衡**定：'):
        lines[i]=r'> 极点由**幅值平衡**定：在目标 $\omega_c$ 处，原 $-40$ 段渐近幅值为 $\omega_{c0}^2/\omega_c^2$。记 $\omega_0=\omega_{c0}^2/\omega_c$，叠加网络后要求该处总幅值为1，得到 $\omega_0\omega_F=\omega_D\omega_E$：'
p.write_bytes((nl.join(lines)+nl).encode('utf-8'))
