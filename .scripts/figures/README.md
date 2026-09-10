# 绘图工具链

笔记插图的统一入口。**规范见仓库根 `AGENTS.md`「绘图规范」**，这里只说怎么用。

## 快速上手

```powershell
cd .scripts\figures

.\build.ps1 -File .\circuit-RC-eq.tex        # 单张验证
.\build.ps1 -Dir .                            # 本目录全部
.\build.ps1 -All -Dpi 600                     # 同上，显式指定分辨率
.\build.ps1 -File .\circuit-RC-eq.tex -NoPdf  # 只看 PDF，不栅格化
```

成图写到 `..\..\附件\<中文名>.png`。**文件名由源码首行的注释决定**：

```latex
% figure: 频域-RC电路.png      ← .tex
```
```python
# figure: 频域-一阶低通Bode.png  ← .py
```

源码文件用 ASCII 名（避免编码问题），附件名按仓库中文命名规范。

## 文件

| 文件 | 作用 |
|:--|:--|
| `build.ps1` | 构建入口：`.tex` 走 xelatex → pdftocairo；`.py` 直接运行 |
| `list-labels.ps1` | 列出源码里所有文字节点与线段坐标，人工核对"标签是否压在线上" |
| `figures_style.py` | matplotlib 公共样式：字体、配色、`new_bode_axes()`、`tidy()`、`save()` |
| `circuit-RC-eq.tex` | 电路图模板（circuitikz）：正弦源 + R + C，含直箭头电压标注 |
| `geom-alpha-triangle.tex` | 几何图模板（TikZ）：辅助直角三角形，含角弧/旋转标签/图例 |
| `block-*.tex` | 结构图模板（TikZ）：反馈环 / 扰动 / 顺馈 / PID / 状态空间 / 死区 / 等效变换六规则 |
| `sfg-mason.tex` | 信号流图与梅森公式标注 |
| `bode-first-order.py` | 曲线图模板（control + matplotlib）：一阶低通伯德图 |
| `bode-typical-links.py` | 一次生成 8 张典型环节伯德图（05-1-2 §5.2 表格用） |
| `ch5-nyquist.py` | 第5章例题补图：奈氏图 4 张（三张自编例 + 例5-8 条件稳定示意） |
| `ch5-bode-examples.py` | 第5章例题补图：伯德/时域 7 张（例5-6、5-7、5-13、5-14、5-17、5-18、渐近线反算例） |
| `block-2nd-order.tex` | 结构图模板（TikZ）：典型二阶系统（05-3-b-2 例5-13） |
| `ch5-three-plots.py` | 三种图示法对照（05-1-1 §5.1.4）：同一 RC 系统的奈氏图/伯德图/尼科尔斯图 |

构建产物（一律单图，不做多子图拼版）：

- 第5章典型环节：`附件\频域-典型环节-*Bode.png`（8 张）、`附件\频域-典型环节-*Nyquist.png`（8 张）
- 第5章例题补图：`附件\频域-奈氏-*.png`（4 张）、`附件\频域-例5*.png`（11 张）、`附件\频域-算例-渐近线反求.png`
- 第5章图示法：`附件\频域-图示法-幅相曲线.png`、`-伯德图.png`、`-尼科尔斯图.png`
- 其他：`附件\频域-RC电路.png`、`附件\频域-一阶正弦响应.png`、`附件\频域-一阶低通Bode.png`、
  `附件\自控-典型二阶系统结构图.png`（TikZ）

> `频域-一阶低通Bode.png` 目前是**范例产物**，未嵌入任何笔记——它是曲线类插图的
> 可运行样例。不需要时把 `bode-first-order.py` 和这张图一起删掉即可。

## 已验证的环境

- TeX Live 2026（`xelatex`）、`pdftocairo`（随 TeX Live）
- Python 3.13 + `control` / `matplotlib` / `numpy` / `sympy`

## 踩过的坑（省得再踩）

1. **`pdftocairo` 不支持非 ASCII 输出路径**——`Error opening output file`，exit 2。
   `build.ps1` 已改为先渲到 `%TEMP%` 的 ASCII 临时名再搬到 `附件\`。
2. **`pdftocairo` 会给输出名追加 `.png`**：传 `foo.png` 得到 `foo.png.png`，要传不带扩展名的前缀。
3. **图内中文会变方框**：两处坑——① `font.family` 必须写成字体列表，
   `= "serif"` 这种别名不会逐字形回退；② **同一条字符串里不要混中文和 `$…$`**，
   mathtext 会接管整串并套 CM 字体集，中文随即掉字形。标题写两行：
   `"惯性环节\n$1/(Ts+1)$"`。
4. **`control` 的 rcParams 不注册进 matplotlib**：`plt.rcParams["control.grid"]` 抛 `KeyError`。
   推荐用 `ct.frequency_response()` 取数据自己画，样式完全可控。
5. **控制台中文乱码**：`build.ps1` 已设 `[Console]::OutputEncoding` 与 `PYTHONIOENCODING=utf-8`；
   直接跑 `.py` 时若乱码，先设这两个环境变量。
6. **文字压在线上**：标注样式统一加 `fill=white` 即可自动遮断底下的线，
   **但 `fill=white` 必须写在 `font=`/`color=` 之后**，否则整个节点被填成实心块、文字消失。
7. **不要尝试自动检测中文压线**：`pdftotext -bbox` 对纯中文返回 "no word list"；
   压线时文字与线连通，连通域法必然失败；开运算又会吃掉笔画（300 dpi 下笔画仅 2~4px）。
   用 `list-labels.ps1` 列出坐标人工核对，比图像启发式快且准。
