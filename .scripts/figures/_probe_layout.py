# 标注落点探针：打印绘图脚本里所有标注/图例的**数据坐标** bbox（配合 _check_fig_layout.py）。
# 用法：D:\miniconda3\python.exe _probe_layout.py ch5-h-inf.py [更多脚本...]
"""改标注位置前先看数，别用眼睛估。

`sanity check 排布` 的三件套：① 本脚本 → 标注现在落在数据坐标的哪块矩形；
② `_check_fig_layout.py` → 跑出 [压线]/[压字]/[越界]；③ 命中就换落点再跑①。

注意 annotate 的 `get_window_extent()` 会把**箭头**也算进去，这里用
`Text.get_window_extent()` 只量文字本体（与 _check_fig_layout 的口径一致）。
"""
import importlib.util
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.figure

FG = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(FG))
import figures_style as fs                                    # noqa: E402

for arg in sys.argv[1:]:
    figs = {}

    def fake_save(fig, name, transparent=False):
        figs.setdefault(id(fig), (pathlib.Path(name).name, fig))
        return name

    # 有的脚本直接 fig.savefig（_nyquist_style.finish），两个都拦，顺便别真写盘
    orig_savefig = matplotlib.figure.Figure.savefig

    def fake_savefig(self, fname, *a, **kw):
        figs.setdefault(id(self), (pathlib.Path(str(fname)).name, self))
        return None

    fs.save = fake_save
    matplotlib.figure.Figure.savefig = fake_savefig
    spec = importlib.util.spec_from_file_location("__main__", FG / arg)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    finally:
        matplotlib.figure.Figure.savefig = orig_savefig
    matplotlib.pyplot.close("all")

    for _, (name, fig) in figs.items():
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        FigureCanvasAgg(fig)
        fig.canvas.draw()
        r = fig.canvas.get_renderer()
        print(f"== {name}  ({fig.bbox.width:.0f}x{fig.bbox.height:.0f}px)")
        for i, ax in enumerate(fig.axes):
            print(f"  ax{i}: xlim={ax.get_xlim()} ylim={ax.get_ylim()} "
                  f"axesbox={ax.bbox.bounds}")
            inv = ax.transData.inverted()

            def box(bb):
                (x0, y0) = inv.transform((bb.x0, bb.y0))
                (x1, y1) = inv.transform((bb.x1, bb.y1))
                return f"x {x0:+.3f}~{x1:+.3f}  y {y0:+.3f}~{y1:+.3f}"

            leg = ax.get_legend()
            if leg is not None:
                print(f"    图例框: {box(leg.get_frame().get_window_extent(renderer=r))}")
            for j, t in enumerate(ax.texts):
                # annotate 的 get_window_extent 会把箭头算进去，只量文字本体
                from matplotlib.text import Annotation, Text
                if isinstance(t, Annotation):
                    bb = Text.get_window_extent(t, renderer=r)
                    kind = "annot"
                else:
                    bb = t.get_window_extent(renderer=r)
                    kind = "text "
                print(f"    {kind}[{j}] {t.get_text()[:22]!r}: {box(bb)}")
        for j, t in enumerate(fig.texts):
            print(f"    fig.text[{j}] {t.get_text()[:18]!r}: "
                  f"px x {t.get_window_extent(renderer=r).x0:.0f}~"
                  f"{t.get_window_extent(renderer=r).x1:.0f}")
