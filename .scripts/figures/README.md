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
| `bode-typical-links.py` | 一次生成 10 张典型环节伯德图（8 个最小相位 + 不稳定惯性/不稳定振荡），**上下两层**：上幅频、下相频 |
| `ch5-legacy-bode.py` | 把早期两张伯德图（`伯德-例512` / `伯德-例515`）重绘为同一两层风格 |
| `ch5-vector-method.py` | 矢量法 s 平面极点矢量图 + 惯性环节逐点描点图（05-1-1 §5.1.3、05-1-2 §5.2.2） |
| `ch5-bode-examples.py` | 第5章例题补图：伯德/时域 7 张（例5-6、5-7、5-13、5-14、5-17、5-18、渐近线反算例） |
| `block-2nd-order.tex` | 结构图模板（TikZ）：典型二阶系统（05-3-b-2 例5-13） |
| `ch5-three-plots.py` | 三种图示法对照（05-1-1 §5.1.4）：同一 RC 系统的奈氏图/伯德图/尼科尔斯图 |
| `openloop-nyquist.py` | 开环幅相：九类单图 + 课程例7—9的五张例题/局部放大图；`control.frequency_response` 采样，内置交点与端点断言 |
| `_nyquist_style.py` | 幅相图的等比例坐标、极限标记、按实际频响取点的方向箭头；共享模块，不单独构建 |
| `minimum-phase-comparison.py` | 惯性与不稳定惯性的同幅、反相伯德对照图 |
| `nyquist-type2-parameter.py` | 习题5-9原题幅相图；参数化Ⅱ型稳定边界、闭环根与真实绕行奈氏围线校验 |
| `freq-inverse-omega0-convention.py` | 反求口径图（05-2-b §5.11.2）：三条型别的低频延长线共过 $(1,20\lg K)$、与 0 dB 交于 $\omega_0=K^{1/\nu}$ |
| `type-family-compare.py` | 例5.4 型别对照（05-3-4）：同两惯性极点、$\nu=0,1,2,3$ 四条幅相曲线 + 三条起动射线 |
| `freq-same-mag-diff-phase.py` | 课件 §5.3.4 的最简反例（附录 §5.3.2.8）：Ⅰ 型一个零点一个极点、四种半平面组合，$L(\omega)$ 完全重合而 $\varphi(\omega)$ 四条各不相同 |
| `ch5-ex527-osc-steady.py` | 例5.27（05-1-2-c）：振荡环节的正弦稳态输出，输出幅值是输入的 3 倍、相位滞后 $T/4$ |

构建产物（一律单图，不做多子图拼版）：

- 第5章典型环节：`附件\频域-典型环节-*Bode.png`（8 张）、`附件\频域-典型环节-*Nyquist.png`（8 张）
- 第5章例题补图：`附件\频域-奈氏-*.png`（4 张）、`附件\频域-例5*.png`（12 张）、`附件\频域-算例-渐近线反求.png`
- 第5章图示法：`附件\频域-图示法-幅相曲线.png`、`-伯德图.png`、`-尼科尔斯图.png`
- 第5章反求/型别：`附件\频域-反求-低频延长线与ω0.png`、`附件\频域-幅相-四种型别对照.png`、
  `附件\频域-幅频相同相频不同.png`
- **课件截图**（从 `按章节-原视频和PPT\` 的旧 `.ppt` 里抽的原图，前缀 `自控-频域-`，与
  `自控-频域-三频段`/`中频斜率`/`最小相位`/`闭环幅频`/`伯德判稳` 同一批）：
  `附件\自控-频域-反求延长线与K.png`（05-2-b）、`附件\自控-频域-Bode折线与相频.png`（05-2-1）
- 其他：`附件\频域-RC电路.png`、`附件\频域-一阶正弦响应.png`、`附件\频域-一阶低通Bode.png`、
  `附件\自控-典型二阶系统结构图.png`（TikZ）

> `频域-一阶低通Bode.png` 目前是**范例产物**，未嵌入任何笔记——它是曲线类插图的
> 可运行样例。不需要时把 `bode-first-order.py` 和这张图一起删掉即可。
>
> **伯德图统一约定**：一律用 `figures_style.new_bode_axes()` 的**上下两层**
> （上：$L(\omega)$/dB；下：$\varphi(\omega)/^\circ$；共用横轴 $\lg\omega$），
> 不要再画「单轴左右双刻度」的变体。

## 从课件 PPT 里取原图（2026-09-18 验证）

PowerPoint COM 在本机打不开旧 `.ppt`，但**里面的图片可以裸扫出来**，不必解 OLE 目录：

1. 按签名全文件扫：PNG `\x89PNG\r\n\x1a\n` → `IEND\xaeB\x60\x82`、JPEG `\xff\xd8\xff` → `\xff\xd9`；
   EMF/WMF 另有签名（EMF 在偏移 40 处有 ` EMF`）。按签名切片直接落盘。
2. 一节课件（2–3 MB）能扫出 70–230 张 PNG，**绝大多数是公式位图**（按尺寸 ≲300 px、体积 ≲4 KB 过滤掉）。
   真正的插图是 300–800 px 那批，一节课件也就 5–10 张。
3. 筛选靠**联系表**：按墨量（灰度 <190 的像素占比）排序，缩略图 + 文件名拼成一张图，一次看几十张，
   比逐张打开快一个数量级。空白坐标纸的墨量极低，自然沉底。
4. 取回来的图**存成 `附件\自控-频域-*.png`**（与既有课件截图同名前缀），保留原始像素不要再压缩。

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
   **图例也算“文字”**：四条以上曲线时 `loc="upper right"` 常压在曲线上，
   先看曲线占满了哪块区域再放；放不下就把 `ylim` 下探留一条空白带给图例
   （见 `freq-same-mag-diff-phase.py`：下探到 $-400$）。
7. **中文字符串的 `f-string` 拼接同样中招**：`label + rf"$\ {span}$"` 里 `span` 若自带
   `$…$`，拼出来就是嵌套 `$` 直接 `ParseException`；而中文段与 `$…$` 段拼在同一条
   label 里时，汉字仍要走 `\mathrm{}`。分界点是**一条字符串里只能有一段数学**。
8. **不要尝试自动检测中文压线**：`pdftotext -bbox` 对纯中文返回 "no word list"；
   压线时文字与线连通，连通域法必然失败；开运算又会吃掉笔画（300 dpi 下笔画仅 2~4px）。
   用 `list-labels.ps1` 列出坐标人工核对，比图像启发式快且准。
