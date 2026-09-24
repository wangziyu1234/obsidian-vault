# Shared schematic curve for 例5.30 (习题5-31). No standalone output.
"""习题5-31 奈氏图的**形状示意**曲线（横坐标按题目给定的三个交点摆放）。

题目只给了图形、没给传递函数，所以曲线是示意：控制点按「ν=1 从 (0,-∞) 进入 →
第三个象限上扫 → 交负实轴于 -10（自下而上）→ 第二象限大弧（顶点约 -7.9）→
交 -5（自上而下）→ 下沉到谷底约 (-2.6,-0.8) → 过 (-0.8,-0.6)（恰在单位圆上，
0.8²+0.6²=1）→ 交 -0.2（自下而上）→ 收于原点」设计，样条插值保证光滑。

坐标全部是 **K = 5** 那一张图的数据；其他增益只需把整条曲线按 K/5 缩放
（交点随之线性缩放，见 05-4-a 例5.13）。
"""
from __future__ import annotations

import numpy as np
from scipy.interpolate import splprep, splev

K_REF = 5.0          # 控制点对应的开环增益
CROSSINGS = (-10.0, -5.0, -0.2)   # 负实轴上的三个交点（K = 5）
UNIT_POINT = (-0.8, -0.6)         # 曲线与单位圆的交点（题目给定）

_CONTROL = [
    (0.05, -7.2), (-0.8, -5.0), (-2.6, -3.2), (-5.6, -1.8), (-8.6, -1.05),
    (-10.0, 0.00),                       # 交点 ①（ω1，自下而上 = 负穿越）
    (-9.75, 0.85), (-8.9, 1.95), (-7.9, 2.30), (-6.9, 1.80), (-5.8, 0.75),
    (-5.0, 0.00),                        # 交点 ②（ω2，自上而下 = 正穿越）
    (-3.9, -0.58), (-2.6, -0.82), (-1.5, -0.76), (-0.8, -0.6), (-0.42, -0.28),
    (-0.2, 0.00),                        # 交点 ③（ω3，自下而上 = 负穿越）
    (-0.05, 0.11), (0.0, 0.0),
]


def curve(scale: float = 1.0, n: int = 1600):
    """返回 (x, y)：示意曲线；scale = K / K_REF 时即该增益下的奈氏曲线。"""
    pts = np.asarray(_CONTROL, dtype=float)
    tck, _ = splprep([pts[:, 0], pts[:, 1]], s=0.0, k=3)
    u = np.linspace(0.0, 1.0, n)
    x, y = splev(u, tck)
    return scale * np.asarray(x), scale * np.asarray(y)


def check() -> None:
    """自检：三个交点与单位圆交点确实被曲线穿过（示意曲线不能自己走偏）。"""
    x, y = curve()
    idx = np.where(y[:-1] * y[1:] < 0)[0]          # 曲线穿实轴的位置
    assert len(idx) == len(CROSSINGS), idx
    hits = [0.5 * (x[i] + x[i + 1]) for i in idx]
    for got, target in zip(sorted(hits), CROSSINGS):
        assert abs(got - target) < 0.15, (got, target)
    px, py = UNIT_POINT
    r = np.hypot(x - px, y - py)
    assert r.min() < 0.02, r.min()
    print("curve check ok: 穿实轴于 %s（应为 %s）、过单位圆交点 %s" %
          ([round(h, 2) for h in sorted(hits)], CROSSINGS, UNIT_POINT))


if __name__ == "__main__":
    check()
