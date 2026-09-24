# 无视觉核验时的排版自检：跑一遍绘图脚本，检查图内文字是否互相压字 / 压住曲线 / 跑出画布。
# 用法：D:\miniconda3\python.exe _check_fig_layout.py ch5-ex530-krange.py [...]
"""代替肉眼看图。

本机 `Read` 读 PNG 会返回 "current model does not support images"，成图无法目视核对。
这个脚本 monkeypatch 掉 figures_style.save 拿到 fig 对象，用 renderer 量：
  (1) 每个文字 artist 的窗口 bbox → 两两重叠（[压字]）、越出画布（[越界]）；
  (2) 每条 Line2D 的数据点投影到像素 → 落在文字白框/legend 框里（[压线]）。

[压线] 是 2026-09-24 用户指出的老毛病：标注带着白色 facecolor 的 bbox 摆在曲线必经之处，
把曲线「咬掉」一块。原理上是「框内不许有曲线点」，所以量的是 bbox patch 的窗口范围
（比文字本体大一个 pad），不是文字本体的 extent。

已知误报与默认豁免：
  * Annotation 的 window extent 含箭头 patch —— 改用 Text.get_window_extent 只量字；
  * 同一 artist 既是 fig.texts[i] 又是 fig._suptitle —— 按 id 去重；
  * 落在坐标范围之外、被裁掉的刻度标签（如 xlim=-1.45 却有 -1.5 刻度）—— 跳过；
  * legend 框已按整框量，框内文字不再单独拿去比曲线（否则一条线报两遍）；
  * 曲线自身的 lw 有粗细：判定时把框按「半个线宽」外扩，再内缩 1px 防边界擦边误报。
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.figure
import matplotlib.pyplot as plt
from matplotlib.text import Annotation, Text

import figures_style as fs

HERE = pathlib.Path(__file__).resolve().parent


def collect(fig):
    """收集 (label, artist, 越界算不算问题, 要不要拿去比曲线, 要不要参与压字两两比对)。"""
    items = []
    seen = set()

    def add(label, art, outside_ok, vs_line=True, in_pair=True):
        if id(art) in seen:
            return
        seen.add(id(art))
        items.append((label, art, outside_ok, vs_line, in_pair))

    for i, ax in enumerate(fig.axes):
        for j, t in enumerate(ax.texts):
            add(f"ax{i}.text[{j}]:{t.get_text()[:14]!r}", t, False)
        add(f"ax{i}.title:{ax.title.get_text()[:14]!r}", ax.title, True)
        add(f"ax{i}.xlabel:{ax.xaxis.label.get_text()[:14]!r}", ax.xaxis.label, True)
        add(f"ax{i}.ylabel:{ax.yaxis.label.get_text()[:14]!r}", ax.yaxis.label, True)

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
            # 图例框天然包住自己的文字 ⟹ 不参与压字比对，但拿它去比曲线（框会挡住线）
            add(f"ax{i}.legend框", leg.get_frame(), False, vs_line=True, in_pair=False)
            for j, t in enumerate(leg.get_texts()):
                add(f"ax{i}.legend[{j}]:{t.get_text()[:14]!r}", t, False, vs_line=False)

    for j, t in enumerate(fig.texts):
        add(f"fig.text[{j}]:{t.get_text()[:14]!r}", t, False)
    if fig._suptitle is not None:
        add(f"suptitle:{fig._suptitle.get_text()[:14]!r}", fig._suptitle, True)
    return items


def bbox_of(art, renderer, *, as_occluder=False):
    """as_occluder=True 时优先取白底 patch 的范围——那才是真正遮住曲线的那块。"""
    try:
        if as_occluder and isinstance(art, Text):
            patch = art.get_bbox_patch()
            if patch is not None:
                bb = patch.get_window_extent(renderer=renderer)
                if bb.width > 0 and bb.height > 0:
                    return bb
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


def stepped(pts, style):
    """按 drawstyle 把数据点展开成**实际画出来**的折线（step 图的数据点不是折线本身）。

    不处理的话，ax.step() 只有 5 个原始点，加密插值会连成对角线 —— 纯粹是假象。
    """
    if not style.startswith("steps"):
        return pts
    post = style == "steps-post"
    out = []
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        if post:
            out += [(x0, y0), (x1, y0), (x1, y1)]
        else:                                   # pre / mid 按各段端点取值即可
            out += [(x0, y0), (x0, y1), (x1, y1)]
    out.append(tuple(pts[-1]))
    return np.asarray(out, dtype=float)


def densify(pts, step=2.0):
    """把折线按 ~step 像素加密：axhline/axvline 只有 2 个端点，不加密会漏掉横穿白框的线。"""
    if len(pts) < 2:
        return pts
    seg = np.hypot(np.diff(pts[:, 0]), np.diff(pts[:, 1]))
    n = np.maximum((seg / step).astype(int) + 1, 1)
    if n.sum() > 200000:                    # 兜底，别把内存吃爆
        return pts
    out = [pts[:1]]
    for i, k in enumerate(n):
        t = np.linspace(0.0, 1.0, k + 1)[1:, None]
        out.append(pts[i] + t * (pts[i + 1] - pts[i]))
    return np.vstack(out)


def line_overlaps(fig, occluders):
    """[压线]：每条 Line2D 的数据点投到像素后，有没有落进某个框里。"""
    hits = []
    for i, ax in enumerate(fig.axes):
        for k, ln in enumerate(ax.lines):
            xy = np.asarray(ln.get_xydata(), dtype=float)
            if xy.size == 0 or not np.isfinite(xy).all():
                xy = xy[np.isfinite(xy).all(axis=1)]
            if len(xy) == 0:
                continue
            try:
                pts = ln.get_transform().transform(stepped(xy, ln.get_drawstyle()))
            except Exception:                                   # pragma: no cover
                continue
            keep = np.isfinite(pts).all(axis=1)
            pts = pts[keep]
            if len(pts) == 0:
                continue
            if ln.get_clip_on():
                # 曲线跑出坐标轴的部分在图上根本看不见（被轴裁掉），别拿来判压线
                ab = ax.bbox
                keep = ((pts[:, 0] >= ab.x0 - 1) & (pts[:, 0] <= ab.x1 + 1)
                        & (pts[:, 1] >= ab.y0 - 1) & (pts[:, 1] <= ab.y1 + 1))
                pts = pts[keep]
                if len(pts) == 0:
                    continue
            pts = densify(pts)
            half = ln.get_linewidth() / 72.0 * fig.dpi / 2.0    # 线有粗细
            tag = f"ax{i}.line[{k}]{ln.get_linestyle()}"
            for lb, bb in occluders:
                x0, y0 = bb.x0 + 1 - half, bb.y0 + 1 - half
                x1, y1 = bb.x1 - 1 + half, bb.y1 - 1 + half
                if x1 <= x0 or y1 <= y0:
                    continue
                # 先按包围盒粗筛，再逐点判
                if (pts[:, 0].max() < x0 or pts[:, 0].min() > x1
                        or pts[:, 1].max() < y0 or pts[:, 1].min() > y1):
                    continue
                inside = ((pts[:, 0] > x0) & (pts[:, 0] < x1)
                          & (pts[:, 1] > y0) & (pts[:, 1] < y1))
                n = int(inside.sum())
                if n:
                    hits.append((tag, lb, n, x0, y0, x1, y1))
    return hits


def check(path: pathlib.Path) -> None:
    print(f"\n===== {path.name} =====")
    captured = {}

    def fake_save(fig, name, transparent=False):
        captured.setdefault(id(fig), (pathlib.Path(name).name, fig))
        return str(HERE / ".." / ".." / "附件" / name)

    # 有的脚本走 figures_style.save，有的（_nyquist_style.finish）直接 fig.savefig ⟹ 两个都拦
    orig_savefig = matplotlib.figure.Figure.savefig

    def fake_savefig(self, fname, *args, **kwargs):
        captured.setdefault(id(self), (pathlib.Path(str(fname)).name, self))
        return None

    fs.save = fake_save
    matplotlib.figure.Figure.savefig = fake_savefig
    # 名字必须是 __main__，脚本里的 if __name__ == "__main__" 才会跑起来
    spec = importlib.util.spec_from_file_location("__main__", path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    finally:
        matplotlib.figure.Figure.savefig = orig_savefig
        plt.close("all")

    for _, (name, fig) in captured.items():
        # 脚本里 plt.figure() 可能挂的是 FigureCanvasBase，量 bbox 需要真的 Agg 画布
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        FigureCanvasAgg(fig)
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        fbb = fig.bbox
        raw = collect(fig)
        items = [(lb, bbox_of(a, renderer), ok, vs, inp)
                 for lb, a, ok, vs, inp in raw]
        items = [(lb, bb, ok, vs, inp) for lb, bb, ok, vs, inp in items if bb is not None]
        pairables = [(lb, bb) for lb, bb, ok, vs, inp in items if inp]
        occluders = [(lb, bbox_of(a, renderer, as_occluder=True))
                     for lb, a, ok, vs, inp in raw if vs]
        occluders = [(lb, bb) for lb, bb in occluders if bb is not None]

        bad = 0
        for lb, bb, ok, vs, inp in items:
            if not ok:
                continue
            if (bb.x0 < fbb.x0 - 1 or bb.x1 > fbb.x1 + 1
                    or bb.y0 < fbb.y0 - 1 or bb.y1 > fbb.y1 + 1):
                print(f"  [越界] {lb}  bbox=({bb.x0:.0f},{bb.y0:.0f})-({bb.x1:.0f},{bb.y1:.0f})"
                      f"  画布={fbb.width:.0f}x{fbb.height:.0f}")
                bad += 1
        for i in range(len(pairables)):
            for j in range(i + 1, len(pairables)):
                a, b = pairables[i][1], pairables[j][1]
                ov_w = min(a.x1, b.x1) - max(a.x0, b.x0)
                ov_h = min(a.y1, b.y1) - max(a.y0, b.y0)
                if ov_w > 2.0 and ov_h > 2.0:
                    print(f"  [压字 {ov_w:.0f}x{ov_h:.0f}px] "
                          f"{pairables[i][0]}  ×  {pairables[j][0]}")
                    bad += 1
        for tag, lb, n, x0, y0, x1, y1 in line_overlaps(fig, occluders):
            print(f"  [压线 {n}点] {lb}  ×  {tag}"
                  f"  框内像素 ({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f})")
            bad += 1
        print(f"  {name}: 文字 {len(items)} 个，问题 {bad} 处，"
              f"画布 {fbb.width:.0f}x{fbb.height:.0f}px")


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        check((HERE / arg).resolve())
