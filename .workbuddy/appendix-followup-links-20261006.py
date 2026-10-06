from pathlib import Path
import re

base = Path('D:/obsidian/控制理论/自动控制原理')
changes = {
    '07-1 采样与z变换.md': [
        ('由 $F(s)$ 求 $F(z)$ 的换算表（20 行）、带零阶保持器的 $G(s)\\to G_d(z)$ 四行表、控制器离散化替换式与定理，见 [[附录 z变换与离散化速查]]（本节的定理也已收进该页 §(1)，便于一页查完）；拉氏表与 z 表并列版见 [[附录 拉氏变换表与z变换表]]。',
         '由 $F(s)$ 求 $F(z)$ 的常用换算、ZOH 四类公式、差分方程与判稳，见 [[附录 z变换与离散化速查]]；本节定理可直达 [[附录 z变换与离散化速查#🧮 (6) 基本定理|基本定理]]。双曲、多极点与推导在该页后部；拉氏表与 z 表并列版见 [[附录 拉氏变换表与z变换表]]。')],
    '07 第7章 线性离散系统的分析与校正.md': [
        ('**ZOH 的 $G(s)\\to G_d(z)$ 四行表**', '**ZOH 的 $G(s)\\to G_d(z)$ 四类公式**')],
    '附录 开环增益与闭环增益.md': [
        ('**根轨迹增益 $K^*$（首一标准式）**', '**根轨迹增益 $K^{\\ast}$（首一标准式）**')],
    '附录 z变换与离散化速查.md': [
        ('G_d(z)=\\left(1-z^{-1}\\right)\\mathcal Z\\left[\\frac{G(s)}{s}\\right]=\\frac{z-1}{z}\\,\\mathcal Z\\Bigl[\\mathcal L^{-1}\\Bigl\\{\\frac{G(s)}{s}\\Bigr\\}_{t=kT}\\Bigr]',
         '\\begin{aligned}\nG_d(z)&=\\left(1-z^{-1}\\right)\\mathcal Z\\left[\\frac{G(s)}{s}\\right]\\\\\n&=\\frac{z-1}{z}\\,\\mathcal Z\\Bigl[\\mathcal L^{-1}\\Bigl\\{\\frac{G(s)}{s}\\Bigr\\}_{t=kT}\\Bigr]\n\\end{aligned}')]
}
for name, pairs in changes.items():
    p = base / name
    raw = p.read_bytes()
    text = raw.decode('utf-8-sig').replace('\r\n', '\n')
    for old, new in pairs:
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new)
    text = re.sub(r'^modify: .*$', 'modify: 2026-10-06', text, count=1, flags=re.M)
    p.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'') + text.replace('\n', '\r\n' if b'\r\n' in raw else '\n').encode('utf-8'))
print('Updated dependent references and two display details.')
