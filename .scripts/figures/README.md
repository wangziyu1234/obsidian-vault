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
| `figures_style.py` | matplotlib 公共样式：字体、配色、`new_bode_axes()`、`tidy()`、`save()` |
| `circuit-RC-eq.tex` | 电路图模板（circuitikz）：正弦源 + R + C，含直箭头电压标注 |
| `geom-alpha-triangle.tex` | 几何图模板（TikZ）：辅助直角三角形，含角弧/旋转标签/图例 |
| `bode-first-order.py` | 曲线图模板（control + matplotlib）：一阶低通伯德图 |

构建产物：`附件\频域-RC电路.png`、`附件\频域-一阶正弦响应.png`、`附件\频域-一阶低通Bode.png`。

> `频域-一阶低通Bode.png` 目前是**范例产物**，未嵌入任何笔记——它是曲线类插图的
> 可运行样例。不需要时把 `bode-first-order.py` 和这张图一起删掉即可。

## 已验证的环境

- TeX Live 2026（`xelatex`）、`pdftocairo`（随 TeX Live）
- Python 3.13 + `control` / `matplotlib` / `numpy` / `sympy`

## 踩过的坑（省得再踩）

1. **`pdftocairo` 不支持非 ASCII 输出路径**——`Error opening output file`，exit 2。
   `build.ps1` 已改为先渲到 `%TEMP%` 的 ASCII 临时名再搬到 `附件\`。
2. **`pdftocairo` 会给输出名追加 `.png`**：传 `foo.png` 得到 `foo.png.png`，要传不带扩展名的前缀。
3. **图内中文会变方框**：Cambria / Times 无 CJK 字形。标注优先用数学符号
   （`$L(\omega)$`）；确需中文时把字体族改成 `["Microsoft YaHei", "SimHei"]`。
4. **`control` 的 rcParams 不注册进 matplotlib**：`plt.rcParams["control.grid"]` 抛 `KeyError`。
   推荐用 `ct.frequency_response()` 取数据自己画，样式完全可控。
5. **控制台中文乱码**：`build.ps1` 已设 `[Console]::OutputEncoding` 与 `PYTHONIOENCODING=utf-8`；
   直接跑 `.py` 时若乱码，先设这两个环境变量。
