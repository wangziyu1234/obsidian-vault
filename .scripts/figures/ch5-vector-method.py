# figure: 频域-矢量法-s平面.png
"""矢量法与惯性环节描点（05-1-1 §5.1.3、05-1-2 §5.2.2）：

  频域-矢量法-s平面.png      —— 极点矢量之比：$G(s)=2/(s+2)$ 的极点 s=-2 到 jω 的矢量
  频域-惯性环节-描点.png      —— 逐点描点：G(jω)=2/(2+jω) 的轨迹与 6 个描点

两张都是单图，不做组图。图内文字不混用中文与 `$…$`，公式用纯文本。
构建：..\\build.ps1 -File .\\ch5-vector-method.py
"""
import os

import numpy as np
import matplotlib.pyplot as plt

import figures_style as fs

fs.use_style()
OUT = os.path.join(fs.REPO_ROOT, "附件")
W = np.array([0.0, 0.6, 1.0, 2.0, 4.0, 8.0])


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.subplots_adjust(left=0.14,right=0.96,bottom=0.17,top=0.82)
    fig.savefig(path, dpi=fs.DPI)
    plt.close(fig)
    print("saved", path)


# ================================================================ (1) s 平面矢量法
fig, ax = plt.subplots(figsize=(6.4, 5.6))
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-3.2, 3.6)
ax.set_ylim(-0.6, 9.4)
ax.axhline(0, color=fs.SUB, linewidth=0.9)
ax.axvline(0, color=fs.SUB, linewidth=0.9)
ax.grid(True, color=fs.GRID, linewidth=0.5, alpha=0.8)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.set_xlabel("实轴 σ")
ax.set_ylabel("虚轴 jω")
ax.set_title("矢量法：由 s 平面的极点矢量读 A 与 φ\nG(s) = 2/(s+2)，极点在 s = −2", pad=8)

ax.plot([-2], [0], marker="x", color=fs.PHA, markersize=11, markeredgewidth=2.4, zorder=6)
ax.annotate("极点 −2", xy=(-2, 0), xytext=(-1.95, -0.42), color=fs.PHA, fontsize=11.5)

for i, w in enumerate(W[1:]):
    ax.annotate("", xy=(0, w), xytext=(-2, 0),
                arrowprops=dict(arrowstyle="-|>", color=fs.MAG, lw=1.4,
                                mutation_scale=12, shrinkA=0, shrinkB=2), zorder=4)
    ax.annotate("j%.1f" % w, xy=(0, w), xytext=(6, -3), textcoords="offset points",
                color=fs.MAG, fontsize=10.5)
# 强调 ω = 2 的那一根
ax.annotate("", xy=(0, 2), xytext=(-2, 0),
            arrowprops=dict(arrowstyle="-|>", color=fs.PHA, lw=2.2,
                            mutation_scale=14, shrinkA=0, shrinkB=2), zorder=5)
ax.annotate("|矢量| = 2√2\n∠ = 45°", xy=(-1.0, 1.0), xytext=(-3.15, 2.6),
            color=fs.PHA, fontsize=11)
ax.annotate("A(ω) = 2 / |极点矢量|\nφ(ω) = −∠(极点矢量)", xy=(1.0, 9.2),
            color=fs.INK, fontsize=11.5, ha="left", va="top")
ax.annotate("ω = 2 时：\nA = 1/√2\nφ = −45°", xy=(0.35, 6.4),
            color=fs.SUB, fontsize=10.5, ha="left", va="top")
save(fig, "频域-矢量法-s平面.png")

# ================================================================ (2) 惯性环节描点
fig, ax = plt.subplots(figsize=(6.4, 5.4))
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-0.18, 1.24)
ax.set_ylim(-0.78, 0.34)
ax.axhline(0, color=fs.SUB, linewidth=0.9)
ax.axvline(0, color=fs.SUB, linewidth=0.9)
ax.grid(True, color=fs.GRID, linewidth=0.5, alpha=0.8)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.set_xlabel("实部")
ax.set_ylabel("虚部")
ax.set_title("逐点描点：G(jω) = 2/(2+jω) 的轨迹（第四象限半圆）", pad=8)

w = np.logspace(-2, 3, 2000)
G = 2 / (2 + 1j * w)
ax.plot(G.real, G.imag, color=fs.MAG, linewidth=2.2, zorder=4)
th = np.linspace(-np.pi, 0, 300)
ax.plot(0.5 + 0.5 * np.cos(th), 0.5 * np.sin(th), color=fs.SUB,
        linewidth=0.9, linestyle=(0, (2, 3)), zorder=2)
ax.plot([0.5], [0], marker="x", color=fs.SUB, markersize=6, zorder=3)

# Frequency labels only; exact coordinates remain in the note table.
pts=[(0,(8,12)),(.6,(12,8)),(1,(12,-12)),(2,(-20,-24)),(4,(-8,-40)),(8,(-52,8))]
for wv,off in pts:
    g=2/(2+1j*wv)
    ax.plot(g.real,g.imag,'o',color=fs.PHA,ms=5)
    ax.annotate('ω = %g'%wv,(g.real,g.imag),xytext=off,textcoords='offset points',fontsize=10)
ax.annotate('ω → ∞',(0,0),xytext=(-32,12),textcoords='offset points',fontsize=10)
from _nyquist_style import curve
import control as ct
curve(ax,ct.tf([2],[1,2]),np.geomspace(1e-4,1e4,3000),arrows=(1.4,5.5))
fig.text(.5,.035,'各点的复数坐标见正文表；箭头表示频率增大。',ha='center',fontsize=10)
assert abs(2/(2+2j)-(.5-.5j))<1e-12
save(fig, "频域-惯性环节-描点.png")

# 打印核对值
for wv in W:
    g = 2 / (2 + 1j * wv) if wv > 0 else complex(1, 0)
    print("ω=%-5g |G|=%.4f  ∠=%.2f°  %.4f%+.4fj"
          % (wv, abs(g), np.degrees(np.angle(g)), g.real, g.imag))
