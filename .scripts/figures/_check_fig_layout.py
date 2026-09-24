# 无视觉核验时的排版自检：跑一遍绘图脚本，检查图内文字是否互相压字 / 跑出画布。
# 用法：D:\miniconda3\python.exe _check_fig_layout.py ch5-ex530-krange.py [...]
"""代替肉眼看图。

本机 `Read` 读 PNG 会返回 "current model does not support images"，成图无法目视核对。
这个脚本 monkeypatch 掉 figures_style.save 拿到 fig 对象，用 renderer 量每个文字
artist 的窗口 bbox，报告两两重叠（面积 > 2px）与越出画布的文字。

四类已知误报已排除：
  * Annotation 的 window extent 含箭头 patch —— 改用 Text.get_window_extent 只量字；
  * 同一 artist 既是 fig.texts[i] 又是 fig._suptitle —— 按 id 去重；
  * legend 的 frame 天然包住自己的文字 —— 只收 frame 里的文字；
  * 落在坐标范围之外、被裁掉的刻度标签（如 xlim=-1.45 却有 -1.5 刻度）—— 跳过。
线条与文字的交叉查不出来，但「压字」和「跑出画布」能兜住。
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.text import Annotation, Text

import figures_style as fs

HERE = pathlib.Path(__file__).resolve().parent


def collect(fig):
    """收集 (label, artist, 越界算不算问题) 列表。"""
    items = []
    seen = set()

    def add(label, art, outside_ok):
        if id(art) in seen:
            return
        seen.add(id(art))
        items.append((label, art, outside_ok))

    for i, ax in enumerate(fig.axes):
        for j, t in enumerate(ax.texts):
            add(f"ax{i}.text[{j}]:{t.get_text()[:16]!r}", t, False)
        add(f"ax{i}.title:{ax.title.get_text()[:16]!r}", ax.title, True)
        add(f"ax{i}.xlabel:{ax.xaxis.label.get_text()[:16]!r}", ax.xaxis.label, True)
        add(f"ax{i}.ylabel:{ax.yaxis.label.get_text()[:16]!r}", ax.yaxis.label, True)

        for kind, vals, lim in (("x", ax.get_xticks(), ax.get_xlim()),
                                ("y", ax.get_yticks(), ax.get_ylim())):
            lo, hi = min(lim), max(lim)
            labels = ax.get_xticklabels() if kind == "x" else ax.get_yticklabels()
            for v, t in zip(vals, labels):
                if not t.get_text() or not (lo <= v <= hi):     # 被裁掉的刻度不量
                    continue
                add(f"ax{i}.tick{kind}({v:g}):{t.get_text()!r}", t, True)

        leg = ax.get_legend()
        if leg is not None:
            for j, t in enumerate(leg.get_texts()):
                add(f"ax{i}.legend[{j}]:{t.get_text()[:16]!r}", t, False)

    for j, t in enumerate(fig.texts):
        add(f"fig.text[{j}]:{t.get_text()[:16]!r}", t, False)
    if fig._suptitle is not None:
        add(f"suptitle:{fig._suptitle.get_text()[:16]!r}", fig._suptitle, True)
    return items


def bbox_of(art, renderer):
    try:
        if isinstance(art, Annotation):       # 只要文字框，不要箭头
            bb = Text.get_window_extent(art, renderer=renderer)
        else:
            bb = art.get_window_extent(renderer=renderer)
    except Exception as exc:                  # pragma: no cover
        print(f"  ! 取不到 bbox：{exc}")
        return None
    if bb.width <= 0 or bb.height <= 0:
        return None
    return bb


def check(path: pathlib.Path) -> None:
    print(f"\n===== {path.name} =====")
    captured = {}

    def fake_save(fig, name, transparent=False):
        captured[name] = fig
        return str(HERE / ".." / ".." / "附件" / name)

    fs.save = fake_save
    # 名字必须是 __main__，脚本里的 if __name__ == "__main__" 才会跑起来
    spec = importlib.util.spec_from_file_location("__main__", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    plt.close("all")

    for name, fig in captured.items():
        # 脚本里 plt.figure() 可能挂的是 FigureCanvasBase，量 bbox 需要真的 Agg 画布
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        FigureCanvasAgg(fig)
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        fbb = fig.bbox
        items = [(lb, bbox_of(a, renderer), ok) for lb, a, ok in collect(fig)]
        items = [(lb, bb, ok) for lb, bb, ok in items if bb is not None]

        bad = 0
        for lb, bb, ok in items:
            if not ok:
                continue
            if (bb.x0 < fbb.x0 - 1 or bb.x1 > fbb.x1 + 1
                    or bb.y0 < fbb.y0 - 1 or bb.y1 > fbb.y1 + 1):
                print(f"  [越界] {lb}  bbox=({bb.x0:.0f},{bb.y0:.0f})-({bb.x1:.0f},{bb.y1:.0f})"
                      f"  画布={fbb.width:.0f}x{fbb.height:.0f}")
                bad += 1
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                a, b = items[i][1], items[j][1]
                ov_w = min(a.x1, b.x1) - max(a.x0, b.x0)
                ov_h = min(a.y1, b.y1) - max(a.y0, b.y0)
                if ov_w > 2.0 and ov_h > 2.0:
                    print(f"  [压字 {ov_w:.0f}x{ov_h:.0f}px] {items[i][0]}  ×  {items[j][0]}")
                    bad += 1
        print(f"  {name}: 文字 {len(items)} 个，问题 {bad} 处，"
              f"画布 {fbb.width:.0f}x{fbb.height:.0f}px")


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        check((HERE / arg).resolve())
