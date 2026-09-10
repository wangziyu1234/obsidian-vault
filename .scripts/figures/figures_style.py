# -*- coding: utf-8 -*-
"""笔记插图统一风格（matplotlib）。

用法：
    import figures_style as fs
    fig, axs = fs.new_bode_axes()
    ...绘图...
    fs.save(fig, "频域-一阶低通Bode.png")

约定：
  * 字体用 Cambria（正文系统字体），数学用 `cm`，与笔记里 MathJax 的
    Computer Modern 观感一致；中文如需出现在图内，请另设中文字体。
  * 幅频线 = 深蓝，相频线 = 赭红，参考线/网格 = 浅灰，均与
    circuitikz/TikZ 模板的配色保持一致。
  * save() 优先读取环境变量 FIGURE_OUT（由 ..\\build.ps1 注入），
    在命令行直接跑脚本时也把图写到同一个 附件\\ 下。
"""
from __future__ import annotations

import os
import pathlib
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# 仓库根 = .scripts/figures/figures_style.py 上溯三级
REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
ATTACH_DIR = REPO_ROOT / "附件"

INK = "#1E2228"      # 主文字/轴线
MAG = "#1F3D7A"      # 幅频曲线（深蓝）
PHA = "#B23020"      # 相频曲线、强调（赭红）
SUB = "#606874"      # 次要文字
GRID = "#C9D0DA"     # 网格
FILL = "#E8EFF8"     # 浅填充

DPI = 300


def use_style() -> None:
    """套用笔记插图统一风格。每个脚本开头调用一次即可。"""
    plt.rcParams.update({
        # 必须给「字体列表」而不是 'serif' 这个别名：matplotlib 只在 font.family
        # 是列表时逐字形回退，别名写法遇到 Cambria 缺字（CJK）直接画方框。
        # font.serif 也要设成同一列表——否则它自己的默认值会盖掉回退链。
        "font.family": ["Cambria", "Times New Roman", "Microsoft YaHei", "SimHei"],
        "font.serif": ["Cambria", "Times New Roman", "Microsoft YaHei", "SimHei"],
        "mathtext.fontset": "cm",
        "font.size": 13,
        "axes.titlesize": 14,
        "axes.labelsize": 14,
        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "axes.linewidth": 0.9,
        "axes.unicode_minus": False,
        "xtick.color": INK,
        "ytick.color": INK,
        "text.color": INK,
        "legend.frameon": False,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
    })
    warnings.filterwarnings("ignore", category=FutureWarning)


def new_bode_axes(figsize=(7.4, 5.6)):
    """返回 (fig, (ax_mag, ax_phase))：上下两栏共享横轴的伯德图。"""
    fig, axs = plt.subplots(2, 1, figsize=figsize, sharex=True)
    axs[0].set_ylabel(r"$L(\omega)$ / dB")
    axs[1].set_ylabel(r"$\varphi(\omega)$ / $^\circ$")
    axs[1].set_xlabel(r"$\omega$ / (rad/s)")
    return fig, (axs[0], axs[1])


def tidy(ax, turn_freqs=(), which="both") -> None:
    """统一网格、去顶右边框；turn_freqs 画转折频率竖虚线。"""
    ax.grid(True, which=which, color=GRID, linewidth=0.6, alpha=0.9)
    for x in turn_freqs:
        ax.axvline(x, color=SUB, linewidth=1.0, linestyle=(0, (4, 3)))
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


def save(fig, name: str, transparent: bool = False) -> str:
    """保存到 附件\\<name>；name 必须与笔记里的 ![[name]] 完全一致。"""
    if not name.lower().endswith(".png"):
        name += ".png"
    out = os.environ.get("FIGURE_OUT") or str(ATTACH_DIR / name)
    path = pathlib.Path(out)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=DPI, transparent=transparent)
    print(f"saved {path}")
    return str(path)
