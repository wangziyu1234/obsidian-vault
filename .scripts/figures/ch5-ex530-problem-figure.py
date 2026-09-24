# figure: 自控-频域-例530-题图.png
"""例5.30（习题5-31 燕山大学2018）的**原题图**：从手机照片里裁出并去水印。

来源是用户拍的书页照片（QQ 接收目录），不是矢量源码，所以这张图只能裁不能画。
处理三步：
  1. 按暗像素包围盒定位题图区域（照片里题图在页面下半部靠右）；
  2. 灰度阈值 150 二值化 —— 这一步顺带把页面上的**粉色水印**去掉（水印比线条浅）；
  3. 抹掉孤立黑点（水印残渣、纸张噪点）。

之所以要单独留这份脚本：照片路径在系统临时目录里，日后重出图或换清晰照片时，
裁剪框与阈值都得有据可查；`crop_box` 是按包围盒实测的，换照片后要重测。

Build: ..\\build.ps1 -File .\\ch5-ex530-problem-figure.py
"""
from __future__ import annotations

import os
import pathlib

import numpy as np
from PIL import Image

SRC = pathlib.Path(r"D:\ProgramData\tx\qq"
                   r"\Screenshot_2026-09-24-16-28-01-368_com.onyx.gala..jpg")
CROP_BOX = (1707, 1035, 2597, 1761)      # 原图像素；= 暗像素包围盒 (1721,1049,2583,1747) 外扩 14
THRESHOLD = 150                          # <150 记黑，粉水印（约 170~200）被滤掉
SPECK_MAX_NEIGHBOURS = 1                 # 3x3 邻域里黑点少于等于此值 → 当噪点抹掉
REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]


def build() -> np.ndarray:
    assert SRC.exists(), f"找不到源照片：{SRC}"
    grey = Image.open(SRC).convert("L").crop(CROP_BOX)
    a = np.asarray(grey)
    out = np.where(a < THRESHOLD, 0, 255).astype("uint8")

    # 定位自检：题图左右两端应当分别落在 −10 刻度左侧、+1 刻度右侧的空白里
    ink = out == 0
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    assert ink.mean() > 0.02, f"黑像素太少（{ink.mean():.3f}），阈值可能过高"
    assert rows.min() > 0 and rows.max() < out.shape[0] - 1, "题图被上下切到，裁剪框要放大"
    assert cols.min() > 0 and cols.max() < out.shape[1] - 1, "题图被左右切到，裁剪框要放大"

    # 抹孤立黑点
    b = ink.astype(np.uint8)
    nb = sum(np.roll(np.roll(b, dy, 0), dx, 1)
             for dy in (-1, 0, 1) for dx in (-1, 0, 1)) - b
    out[(b == 1) & (nb <= SPECK_MAX_NEIGHBOURS)] = 255
    print(f"crop {out.shape[1]}x{out.shape[0]}，黑像素 "
          f"{(out == 0).mean() * 100:.2f}%（去噪前 {ink.mean() * 100:.2f}%）")
    return out


def main() -> None:
    out = build()
    dst = pathlib.Path(os.environ.get("FIGURE_OUT")
                       or (REPO_ROOT / "附件" / "自控-频域-例530-题图.png"))
    Image.fromarray(out).save(dst)
    print(f"saved {dst}")


if __name__ == "__main__":
    main()
