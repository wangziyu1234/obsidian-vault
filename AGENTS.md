# AGENTS.md — 给 AI 助手看的操作规范与方法技巧

> 本文件是仓库的「操作手册」。任何会话编辑本库笔记前，请先通读「笔记规范总纲」与「检查与修改流程」。本文只保留**规范、方法技巧与注意事项**，不记历史过程（细节见 git log）。本文件自身不参与笔记检查。

## 仓库概况位置

仓库概况、目录结构与**扫描边界（目录地图）**见 [[README]]；本文只保留规范与方法技巧，不重复仓库概况。

## 笔记规范总纲

### 文件命名
- 章节/讲次：`NN 第N章（第N讲） 描述.md`，前缀两位数字连续
- 附录：不带数字前缀，直接 `附录 XXX.md`；自控、现控的课程附录集中在 `控制理论/附录/`，与两门课程目录同级，入口为 [[控制理论/附录/附录目录]]
- 专题拆分件：`NN-x 描述.md`，与总览同目录平铺（前缀排序相邻）

### 文件头部（强制顺序）
1. frontmatter：`create` / `modify` / `tags`
2. `> 返回目录：[[目录]]`（专题件为 `> 返回：[[总览文件名]] | 返回目录：[[目录]]`）
3. `# H1`
4. `> [!abstract] 本讲定位`

- 笔记文件**有且仅有一个 H1**；讲义内部细分可用 `###`，**附录不用 H3**
- 既有稳定风格勿改：高数 05–12 讲文件名无破折号、H1 含 `——`；15 讲 H1 为「微分方程（常微分方程）」

### 小节标题
- 章节小节：`## 图标 X.Y 标题`（图标沿用各章现有样式，X 章号、Y 小节号，**连续不重号**）；每章末 `## X.N 解题套路`
- 附录方法序列可用 `## (n) 名称`；两大块式附录参考 `附录 变形技巧.md`

### wikilink 与图片
- 跨文引用一律 `[[ ]]`；跨目录优先 `[[控制理论/现代控制理论/01 状态空间表达式/01 状态空间表达式|别名]]` 短路径，**不用 `../`**；引用附录写 `[[附录 XXX]]`
- wikilink **不要放进 `$$…$$`**（MathJax 不解析）
- 图片：`![[文件名.png|尺寸]]`，正文 `|430`、速查大图 `|520`、宽高比 ≥2 的宽图也用 `|520`
- **表格单元格内**的链接管道与图片尺寸必须转义：`[[目标\|别名]]`、`![[图.png\|220]]`（`\|` 是表格转义，**不是 bug，勿改**）
- 附件图片统一 .png；待删素材先确认再删

### LaTeX
- 行内 `$…$`、块级 `$$…$$`；**`$$` 必须成对**
- `\begin/\end`、`\left/\right` 必须配对；`\leftrightarrow` 会用 `\left` 子串造成 `\left/\right` 计数**误报**
- 微分方程系数下标：笔记用 $a_n$ 配最高阶 $c^{(n)}$；胡寿松教材用 $a_0$ 配最高阶（两种约定等价）
- 观测器极点倍数统一「2~5 倍」；MATLAB 用函数句柄 `@fun`
- 跨章主线符号一致：$r(t)$ 参考输入、$e=r-b$ 偏差、$\zeta$ 阻尼比、$\omega_n$ 自然频率、$A^T$ 转置、$E$ 单位阵、$r(A)$ 秩
- **频域符号按教材原文（长期遵守，胡寿松第八版）**：$\omega_c$ 截止频率、**$\omega_x$ 穿越频率**（课本全章不用 $\omega_g$，部分资料与 825 真题写 $\omega_g$ 是同一个量，笔记统一写 $\omega_x$）、$\omega_r$ 谐振频率、$\omega_b$ 带宽频率、$\omega_d$ 阻尼自然频率、$\gamma$ 相角裕度、$h$ 幅值裕度、$M(\omega)$ 闭环幅频、$M_r$ 谐振峰值。分贝值课本写作 **$h(\mathrm{dB})$、$M_r(\mathrm{dB})$**（不写 $h_{\mathrm{dB}}$）；**$h$ 是倍率且恒为正**，正负只出现在 dB 形式上。
- **公式符号一律以教材原 PDF 为准**：`教材OCR\` 的 OCR 文字层对数学符号有系统性丢失（分数线、下标、单字符变量），凡涉及符号口径或公式细节，**必须把对应页渲染出来看原文**，不要凭 OCR 片段裁定。**页码偏移各书不同，别套用 +8**：自控（胡寿松）**+8**、现控（刘豹）**+8**、张宇高数 **+6**、张宇线代 **−7**，一律以 `教材OCR\README.md` 的表为准。渲染原页的现成脚本在 `.workbuddy\`（如 `_ocr_batch_qh*.py` 里的 PyMuPDF 渲染段、`tmp_render\_render_all.py`；该目录被 `check-notes.ps1` 排除、不入库）。
- **真题/真题解析不参与符号统一（长期遵守，用户 2026-09-17 明确）**：`控制理论\青岛大学825真题\` 里的 $\omega_x$ / $\omega_g$、$h_{\mathrm{dB}}$ 等写法**保持试卷与解析原样**，不要为了让全库一致去改真题；真题内部各年份本来就不统一，这是刻意保留的。符号统一只作用于笔记类文件。
- **下标统一用 `\mathrm{}`，不写 `_{\rm xx}`**：`\rm` 会泄漏作用域（`\Phi_{\rm r}x` 会把 $x$ 也变成正体），多字母下标写 `t_{\mathrm{on}}`、`k_{\mathrm{eq}}`、$T_{\mathrm{exact}}$。
- **行内公式含 `^*` 上标（$\omega_c^*$、$h^*$、$e^*(t)$、$\zeta^*$ 这类）时，禁止放进 `*…*` 斜体或 `**…**` 加粗包裹**：Markdown 会先把公式里的 `*` 当定界符吃掉，公式残成 `$\omega_c^=…$` 裸奔、后续 `$` 配对全错位（06-1-c 例1(II) 题注实测，2026-09-28 修）。包裹内一律写 `^{\ast}`（MathJax 渲染 ∗，与 `*` 视觉无差）；无包裹的正文可照常写 `^*`

### 拆分约定（笔记 >250 行时）
- **单题完整性优先（长期遵守）**：同一道题的题目、配图、推导、补充说明与多种解法保持在同一篇笔记中，**不因超过 250 行而拆分**；不要为了压行数挤密公式。250 行拆分规则适用于可独立阅读的多主题或多道题。
- 完整单题笔记在 frontmatter 的 `tags` 之后标记 `single-exercise: true`，供校验脚本豁免篇幅告警；此标记只豁免行数，其他结构、公式和链接仍须检查。
- **整卷真题与解析不拆分（长期遵守）**：`type: exam-paper`（试题）与 `type: exam-solutions`（答案与解析）按整卷保留，一套卷多题同篇是刻意设计，**不适用 250 行拆分规则**；校验脚本据 frontmatter 的 `type` 自动豁免篇幅告警，对没有 frontmatter 的整卷（如 `数学\考研数学二\2000年考研数学二答案与解析.md`）按文件名 `NNNN年…试题 / NNNN年…答案与解析` 兜底识别（如 [[控制理论/青岛大学825真题/Markdown笔记/2009年青岛大学825试题|青岛大学825真题]]系列）。目录/索引页另有「目录/索引页不拆分」一条单独豁免。
- **`附录 *` 速查表不拆分（长期遵守）**：速查附录的价值在于**一页查完**，长表本身就是它的形态，**不适用 250 行拆分规则**；校验脚本按文件名前缀 `附录` 自动豁免篇幅告警。但附录同样要守可读性：公式放前面、每个公式独立 `$$` 块、不留 200+ 字符的密集长行。目录/索引页另有「目录/索引页不拆分」一条单独豁免。
- **统计·策略页不拆分（长期遵守，2026-09-25 用户明确「这种的可以不拆」）**：题型分析、考频统计、应试清单这类"一页查完"的统计与策略页，**长就是它的形态**，不适用 250 行拆分规则——统计结论与执行清单放同一页反而更好用，不要为了压行数另开一篇。做法：frontmatter 标 `long-form: true`，校验脚本据此把篇幅告警降为提示（其他结构、公式与链接照常检查）；这类页仍要守可读性（结论在前、表格紧凑、不留密集长行）。目录/索引页另有「目录/索引页不拆分」一条单独豁免。
- **目录/索引页不拆分（长期遵守，2026-09-29 用户明确「豁免」）**：`type: index` 的目录、索引、总览入口与勘误汇总这类"一页查完"的导航页，**长就是它的形态**（如 `数学\考研数学二目录.md` 收录 12 专题 39 类题型的全部题号表、`控制理论\777习题集\777习题集官方勘误摘录.md` 汇总三册勘误），不适用 250 行拆分规则——拆了反而打断大量跨页引用；校验脚本据 frontmatter 的 `type: index` 把篇幅告警降为提示，其他结构、公式与链接照常检查。这类页仍要守可读性（一页查完、表格紧凑、不留密集长行），也不要把真正的正文塞进索引页——正文多主题超长仍按 `NN-x` 拆分。
- **入口模式**：原文件保留为总览入口（文件名不变、现有链接不断），正文移入同目录 `NN-x` 专题文件
- 总览样式：frontmatter + 返回行 + H1 + abstract（注明「已拆分…总览入口」）+ `## 🗂️ 分章导航` 表格 +（可选）解题流程；专题件头部 `> 返回：[[总览文件名]] | 返回目录：[[目录]]`
- 已按内容拆为主题件：第 3/5/6/7 章、高数与线代多数讲次（`NN-x`）；教材章节若整章过长，按教材目录拆为 `NN-x`
- 拆分脚本坑：`## 图标 X.Y` 带 emoji，正则取编号 `(\d+\.\d+)`；函数内取外层变量需传参；PowerShell 5 无三元运算符；`Measure-Object -Line` 会少算行数，用 `(Get-Content).Count`

### 排版与可读性规范
- **控制理论速查附录**：以公式、参数定义、适用条件和必要解题步骤为主，不保留长段解释、完整推导与完整例题；幅相等图谱可保留查形状必需的图。目录和教材对照页保留导航用途。
- **手算考试的数值口径（长期遵守，2026-10-05 用户明确）**：目标学校禁止使用计算器，整理答案以手算可完成为准。$\mathrm e$、$\pi$ 的幂、根式、对数及其组合保留精确形式，不自行展开为小数，也不罗列不同舍入版本或要求手工复现机器算出的多位小数。可令 $q=\mathrm e^{-T}$ 等缩短公式，但须在该题内明确定义；能代数化简的仍应化简。题目直接给定的小数属于原始数据，照常保留，不能擅自反向替换成指数；题目明确提供的近似值可用于手算比较或按题要求代入，正文仍优先给出精确关系。工具可用于内部复核，但交付的推导和答案应适合无计算器考试。
- **用户排版偏好（长期遵守）：纵向空间不吝啬、横向空间要珍惜、公式不要密集**——每个公式独立 `$$` 块且块间留空行；表格单元格/行内公式用 `\frac` 压扁；禁止把多个算式或长推导挤进同一行
- 例题格式统一 `#### ✏️`（或 callout 内 `> [!example] ✏️`），每步独立 `$$` 块
- 长块公式（>170 字符）统一 `\begin{aligned}` + `&=` 对齐 + `\\` 断行（单纯源码换行 MathJax 只当空格，仍横向溢出）
- **callout 颜色使用规范（长期遵守）**：`[!example] ✏️`=例题（紫）、`[!tip]`=提示/口诀/技巧（绿）、`[!note]`=说明/注意/辨析（灰蓝）、`[!derivation]`=推导/证明（青，自定义，见 `.obsidian\snippets\callouts.css`；`!info` 蓝与灰蓝太接近勿用）、`[!warning]`=易错/警告（橙）、`[!abstract]`=本讲定位（浅蓝）。**推导/证明一律用 `[!derivation]`**；「提示口诀」用 `[!tip]`、「解释提醒」用 `[!note]`
- **callout 相邻分隔（长期遵守）**：两个相邻的独立 callout 之间必须用**真空行**（真正空行，无 `>`）隔开，不得只用同一 callout 流内的 `>` 空行相连；对应地，同一 callout **内部**空行用 `>`。口诀：「callout 内用 `>`、callout 间用真空行」

## 检查与修改流程

### 检查清单（收到「检查笔记」任务时逐项执行）
1. 先 `git status` + `git log` 看增量；扫描边界见 [[README]]「目录地图」
2. **断链**：所有 `[[ ]]` 与 `![[ ]]` 目标必须命中（按 basename / 短路径解析；表格内 `\|` 先拆转义再解析）
3. **LaTeX**：`$$` 成对、`\begin/\end` 配对、`\left/\right` 配对（剔除 `\leftrightarrow`）
4. **编号**：`## X.Y` 小节号无重复；无 TODO/FIXME/待补/`??`；无空链接 `[[]]`
5. **结构**：唯一 H1、`> [!abstract]` 在 H1 之后、附录无 H3；>250 行按拆分约定处理，**`附录 *` 速查表、完整单题（`single-exercise: true`）、整卷真题/解析（`type: exam-paper` / `exam-solutions`）、统计·策略页（`long-form: true`）与目录/索引页（`type: index`）豁免拆分**
6. 检查脚本注意：`read` 工具 `limit` 上限 **2000**；输出中文注意 UTF-8 编码
7. **数学内容深度核对**：按科目分 7 组并行派子代理逐条推导复核，主代理对每一条报告**重新推导确认**后再修改，宁缺毋滥

### 已知误报与豁免（不要重复报告）
- `05 第5章` 表格内 `![[…png\|220]]`：转义正确，勿改
- `\leftrightarrow` → `\left/\right` 计数误报
- `copilot\copilot-custom-prompts\*.md` 无 H1 正常；`AGENTS.md` 自身、环境目录（`.venv\`、`D:\envs\` 等，若存在）不参与检查
- 表格内 `![[…png\|220]]` 与 README/AGENTS 的占位示例不算「图片缺失」
- >250 行的 `type: index` 目录/索引页、`附录 *` 速查表与 `long-form: true` 统计页**只报「提示」不列待修**，别再当缺陷报

### 修改流程
- **同型题不重复补例（长期遵守）**：新来的题若与已有例题**同型、同解法、同结论**（只换了数字或字母），不要再写一遍——只在既有例题处补一句"换数后结论照抄 ××"，或干脆不加。用户明确要求过："一样的话就不用了。"
- 修改/重命名前先 `grep` 检查跨文件引用，避免断链；重命名用 PowerShell `Move-Item -LiteralPath`（路径含中文与括号）
- 每次修改完主动 commit + push（中文提交信息，前缀见 [[README]]「Git 同步」）
- **自绘图**：一律走 `.scripts\figures\` 工具链（见「绘图规范」），源码入库、图入 `附件\`；不要再新增 GDI+ 手绘脚本
- **git push 与沙箱**：受限沙箱下 `git push` 会因 ssh.exe 无法创建 signal pipe 而失败（Win32 error 5）。优先直接执行；只有沙箱拦截且会话允许带权限重试（审批策略不是 never）时，才用 `sandbox_permissions` 重试同一条命令；**审批策略为 never 时不要设置 `sandbox_permissions`**，改为在回复中说明失败原因

## 方法技巧与注意事项

### Python 环境（长期遵守，2026-10-09 起 conda 已退役）

**本机 miniconda 已卸载**，Python 统一由 uv 管理。原则：**按用途用独立环境，不要往共享环境里装包**——原 conda base 就是因为被 `pip install --system` 反复灌入 311 个包，才出现"环境不一致 + 26 个包文件缺失 + 解算器无解"。

| 用途 | 解释器 | 环境内已有 |
|:--|:--|:--|
| 笔记绘图（图源 `.py`） | `D:\envs\figures\Scripts\python.exe` | numpy · scipy · matplotlib · **control** · **slycot** · sympy · pillow（**`build.ps1` 会自动选它**，无需手工指定） |
| 文档 / OCR / PDF / Office | `D:\envs\docs\Scripts\python.exe` | python-docx · python-pptx · openpyxl · XlsxWriter · pymupdf · pdfplumber · pypdf · pdf2docx · img2table · markitdown · rapidocr-onnxruntime · opencv（三变体共存，见下）· onnxruntime · shapely · pyclipper · pandas · numpy · **scipy** · matplotlib · seaborn · statsmodels · scikit-learn · reportlab · tabula-py |
| 动画（manim） | `D:\envs\manim\Scripts\python.exe` | manim 0.22.0 · manimpango（自带 cairo/pango）· numpy · scipy · pillow；**渲染依赖 ffmpeg**（本机 Gyan.FFmpeg 9.0.2 已在 PATH） |
| 交互看板（streamlit） | `D:\envs\web\Scripts\python.exe` | streamlit 1.65.0 · pandas 3.0.6 · pyarrow · altair |
| 语音转写（视频课/录音） | `D:\envs\asr\Scripts\python.exe` | faster-whisper 1.2.1 + ctranslate2 4.8.2（**不需要 torch**）；模型走 HF 镜像缓存在 `~\.cache\huggingface` |
| 深度学习（GPU） | `D:\envs\dl\Scripts\python.exe` | **torch 2.14.1+cu130** · torchvision 0.29.1+cu130 · ultralytics 8.4.174 · **pix2text 1.1.7** · transformers **4.57.6**（被 pix2text 降级，见下）· accelerate · sentence-transformers 6.1.0 · pix2tex 0.1.4 · timm（128 包 / 4.06 GB） |
| 临时脚本、不想建环境 | DSH 自带：`C:\Users\23720\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe` | numpy · pandas · python-docx/pptx · openpyxl · Pillow · lxml · XlsxWriter |

- **装包**：`uv pip install --python D:\envs\<env>\Scripts\python.exe <包>`；新项目用 `uv venv <目录> --python 3.12` 再 `uv add`。**禁止 `pip install --system` / `uv pip install --system`** 指向共享环境——这正是把原 conda base 写脏的元凶。临时依赖用 `uv run --with <包> 脚本.py`（落在 uv 缓存，不污染环境，实测 137 ms 装好 5 个包）；一次性工具用 `uvx <工具>`（实测 `uvx ruff` 秒下秒跑、不装进任何环境）。
- **slycot 已装**（figures，2026-10-10）：`control.slycot_check()` 返回 True；`balred`（模型降阶）、`h2syn`/`hinfsyn`/`mixsyn`（H2/H∞ 综合）、`minimal_realization` 这些**需要 slycot 子程序**的函数现在可用。不需要 slycot 的 `lqr`/`lqe`/`care`/`dare`/`dlqr`/`place`/`acker`/`ctrb`/`obsv`/频域/根轨迹/`margin` 一直可用。⚠ `hinfsyn` 在病态或随机对象上 γ 迭代可能极慢（实测烧了 590 s CPU），复核时先给合理对象或限时。
- **pdf2docx / pypdf / img2table / seaborn 已装**（docs，2026-10-10）：`pdf2docx.Converter(pdf).convert(docx)`（实测 1 页 → 36 KB DOCX、文字正确）；`pypdf.PdfReader(pdf)`（实测读出 `习题册\2007…pdf` 35 页，与 xelatex 输出一致）；`seaborn` 出图正常；`img2table` 能检出表格**结构**，但**取文字需外挂 OCR 后端**（Tesseract 虽已装但中文质量差、PaddleOCR/EasyOCR 未装，见下两条）——**有文字层的 PDF 直接用 `pdfplumber.extract_tables()` 就够**。
- **statsmodels / scikit-learn / reportlab / tabula-py 已装**（docs，2026-10-10，本批同时带进 **scipy 1.18.1**、jpype1，docs 环境 500.9 → **720.1 MB**）：`statsmodels` OLS 实测（斜率 2.000、R²=0.998）、`sklearn` LinearRegression + KMeans 实测通过；`reportlab` 生成 PDF、`tabula-py` 从 PDF 回读表格（3×3 中文表**往返全对**）。⚠ 两个实测坑：① **reportlab 默认字体（Helvetica）没有 CJK 字形**，中文会画成方块（实测 tabula 读回来就是 `■■`，PDF 只有 1936 字节）——必须 `pdfmetrics.registerFont(TTFont("CJK", r"C:\Windows\Fonts\msyh.ttc"))` 并给 `ParagraphStyle`/`TableStyle` 指定该字体（注册后同一份 PDF 29685 字节）；② **tabula-py 依赖 Java**（本机 `D:\jdk-17.0.20+8`，已在 PATH），首选桥 `jpype1` 已装，否则每次都会打 `Failed to import jpype dependencies. Fallback to subprocess`。
- **manim / streamlit 已装**（各自独立环境，2026-10-10）：`D:\envs\manim`（manim 0.22.0 + manimpango，**渲染依赖 ffmpeg**，本机 Gyan.FFmpeg 9.0.2 已在 PATH；实测 `manim -ql` 渲出 h264 854×480 / 1.47 s 的 mp4）；`D:\envs\web`（streamlit 1.65.0，实测 headless 起服务 → HTTP 200、`/_stcore/health` 返回 `ok`、可正常停止）。⚠ manim 的 `Square` 参数是 `side_length`（写 `side` 报 `Mobject.__init__() got an unexpected keyword argument 'side'`）。
- **Tesseract 5.4 已装，但中文识别明显不如 RapidOCR**（2026-10-10 实测）：winget 装 `UB-Mannheim.TesseractOCR` → `C:\Program Files\Tesseract-OCR`（237.9 MB，默认只有 `eng`+`osd`）；`chi_sim` 因 Program Files **无写权限**改装到 **`D:\envs\tessdata\`**（连 eng/osd 一并复制），用前须设 **`TESSDATA_PREFIX=D:\envs\tessdata\`**。**同页对比（张宇线代 PDF 第 60 页扫描）**：RapidOCR 出 516 个汉字且语句通顺（"总结矩阵的加减法需要是同型矩阵…"），Tesseract 只出 318 个汉字且**整行退化成 Latin 乱码**（`SRHDREBELA GEM, RARER AER ASAT RL`）⇒ **中文扫描件继续用 RapidOCR**；Tesseract 只留给西文/数字/干净印刷体（它在干净合成中文表上能读对"分段函数积分/中值定理"）。
- ⚠ **img2table 的表格结构检测不可靠**（2026-10-10 实测）：合成中文表 + 真实扫描页、`borderless_tables`×`implicit_rows` 共 8 种组合**全部检出 0 张表**；`min_confidence=0` 还会被拒（`ValidationError: must be a positive int`）。它读文字必须外挂 OCR 后端（Tesseract/PaddleOCR/EasyOCR），中文场景下这些后端要么是重量级 paddle、要么质量不如 RapidOCR ⇒ **别指望 img2table 抽中文表**：有文字层的 PDF 用 `pdfplumber.extract_tables()`，扫描表格走视觉或人工。
- **笔记工程小件已装**（docs，2026-10-10，本批后 docs 共 **108 包 / 841.5 MB**）：`python-frontmatter`（读 `777习题集目录.md` 得 create/modify/tags/type/aliases/cssclasses ✓ —— **批量改 frontmatter 优先用它，别再手写正则**）、`pylatexenc`（`\omega_x`→`ω_x`、`\mathrm{Re}\,G(j\omega)`→`Re G(jω)`；反向 `unicode_to_latex` 会加 `\ensuremath{}` 外壳，当心）、`cn2an`（⚠ 混合串要用 **`cn2an.transform("第五章","cn2an")`→`第5章`**，直接 `cn2an("第五章")` 报 `ValueError`；纯数字串才用 `cn2an("五","smart")`）、`img2pdf`（2 张扫描 → 2 页无损 PDF ✓）、`genanki`（错题卡 → `.apkg`，内含 `collection.anki2`+`media` ✓）、`rich`+`tabulate`（报告表格 ✓）、`networkx`（知识结构图出 PNG ✓；⚠ 走 graphviz 布局要装 **`pydot`** 并用 `nx.nx_pydot.graphviz_layout(G, prog="dot")`，**不是** pygraphviz——那个要编译、本机装不上）
- **`jieba` 考频统计**（docs）：对 `05 第5章 线性系统的频域分析法.md`（16636 字符）实测 top 词：例题93 / 教材64 / 稳定60 / 反求57 / 频域49 / 裕度48 / 频率特性43 / 伯德图42 / 判据40 / 判稳39 / 闭环39。⚠ 首次运行会打两条 `SyntaxWarning`（jieba 自身正则，无害）；统计前要**自备停用词表**滤掉"例题/教材/习题"这类噪声
- **`cvxpy` 1.9.3 凸优化**（docs，带 clarabel/osqp/scs/highs 四个解算器）：实测 `min (x−3)² s.t. x≥1 → x=3.0`；**LMI `P≻0, A'P+PA≺0` 可行性求解 optimal**（A 特征值 −2.5±1.936j，确实稳定）⇒ 做 H∞/LMI 综合时与 `control`+`slycot` 互补
- **pandoc 3.12.1**（winget，用户级 `C:\Users\23720\AppData\Local\Pandoc`，**225.1 MB**）：实测 `pandoc "05 第5章….md" -o out.docx --from gfm --toc` → 27 KB DOCX、python-docx 可读（77 段 / 9 个标题段）⇒ **笔记→docx 走它**（题卡的 md→tex→pdf 老路不动）；另有 `--pdf-engine=xelatex` 可直出 PDF
- **Graphviz 16.1.0**（winget，`C:\Program Files\Graphviz`，20.7 MB）+ `graphviz`/`pydot` Python 包装：`dot -V` ✓、`dot -Tpng` 渲染 ✓、networkx 走 dot 布局 ✓。⚠ **安装器没写 PATH**，已手工把 `C:\Program Files\Graphviz\bin` 追加到**用户 PATH**（新开终端才生效）
- **faster-whisper 1.2.1**（独立环境 `D:\envs\asr`，245.6 MB / 25 包，**不需要 torch**）：CPU 实测 5.2 s 中文语音（SAPI 合成）→ **0.6 s 转写 = 8.6× 实时**，语言判定 zh 0.99。⚠ **两个坑**：① **`av` 必须降到 `<14`**（现装 13.1.0）——faster-whisper 1.2.1 调 `av.open(..., metadata_errors=…)`，`av 19.0.1` 不接受该参数、报 `TypeError`；② 模型下载走 **`HF_ENDPOINT=https://hf-mirror.com`**（tiny 141 s 下完，缓存 74.7 MB 在 `~\.cache\huggingface`）。**精度提醒**：`tiny` 会听错专有名词（"奈氏判据"→"那是判聚"、"裕度"→"遇度"）且倾向输出繁体 ⇒ 课程转写至少 `base`/`small`，tiny 只当草稿。
- **GPU 栈已装**（独立环境 `D:\envs\dl`，**3.79 GB / 83 包**，2026-10-10）：**torch 2.14.1+cu130** + torchvision 0.29.1+cu130。⚠ **装法很关键**：PyPI（含清华镜像）上的 Win 轮子只有 **118 MB = CPU 版**，CUDA 版必须走 pytorch 专用索引；本机走的是**阿里云镜像** `--find-links https://mirrors.aliyun.com/pytorch-wheels/cu130/`，装 `torch==2.14.1+cu130`（1.9 GB，实测 **14 MB/s、2m18s 下完**；官方 download.pytorch.org 境内慢且 HEAD 返回 403）。实测：`cuda_available=True`、RTX 3060 Laptop 6.0 GB / capability 8.6 / 30 SM、**fp16 4096³ 矩阵乘 ×20 = 0.14 s ≈ 19.3 TFLOPS**。
- **ultralytics 8.4.174**（dl）：`YOLO("yolov8n.pt")`（权重 6.2 MB 从 GitHub 下、约 1 MB/s）**GPU 推理 0.89 s** ✓ —— 用途：把整页扫描件自动切成题目/图形。
- **sentence-transformers 6.1.0**（dl）：`BAAI/bge-small-zh-v1.5`（95 MB，走 hf-mirror）实测两句"稳定性题"相似度 **0.829**、与"线代特征值题"仅 **0.549/0.545** ⇒ **相似题检索 / 笔记语义搜索可用**。
- ⚠ **pix2tex 0.1.4（公式图→LaTeX）实测命中 2/8，不要依赖**：8 条典型自控公式里只有最简分式对（`\frac{K}{s(Ts+1)}`→`\frac{K}{s(T s+1)}` ✅、`\frac{1}{Ts+1}` ✅），凡带 `=`、根式、`\lg`、希腊字母组合的**全崩**（`\omega_n=\sqrt{K/T}` → `\begin{array}{c c}{{\phi\quad\underline{{{K}…`）；整页扫描页完全乱码。⇒ **只适合"已裁好的单条最简公式"**；全页混排另找 texify/marker/nougat，或直接用视觉 `read_image`（零安装、本机已可用）。使用要点：权重 97 MB 从 GitHub 下（~350 KB/s）；**必须用默认 `resize=True`**（传 `resize=False` 输出纯乱码）。
- ✅ **公式 / 中文混排 OCR 用 `pix2text` 1.1.7（dl），实测胜出**：同一批公式图 **4/4 全对**（pix2tex 在同图集只对 2/8），真实扫描教材页输出通顺中文 + 行内公式（`|AB|=|A||B|`、`(A'A)'=A'(A')'=A'A` 均正确）。⚠ **两个必需的固定**：① **`rapidocr` 必须钉 `==3.9.2`** —— `cnstd 1.2.8` 用了 `rapidocr.utils.model_resolver.resolve_model_key`，而 `rapidocr 3.10.0` 删掉了该符号（声明范围没跟着收紧），不钉就 `ImportError`；② **必须 `Pix2Text.from_config(device="cpu")`** —— 默认要用 ONNX Runtime 的 `CUDAExecutionProvider`，而本机 onnxruntime 是 CPU 版，会 `ValueError`。**副作用（已知、可接受）**：它把 dl 环境的 `transformers` 降到 4.57.6、`huggingface-hub` 降到 0.36.2，于是 `uv pip check` 报 `sentence-transformers 6.1 requires huggingface-hub>=1.3` 的冲突 —— 但**实测 SentenceTransformer 加载+编码正常**（相似度 0.670）、ultralytics 也正常，属"警告级"；若将来真咬人，就把 pix2text 单开一个环境（代价是再复制一份 1.9 GB 的 torch）。
- 🔑 **线代 / 矩阵 OCR 的实测结论（2026-10-10，张宇线代第 60 页真题页）**：**必须用 `p2t.recognize(页图)`（整页版面 + 公式检测，CPU 37 s/页），不要用 `p2t.recognize_text()`** —— 后者走纯文本路径会把矩阵压成孤立数字（同页 RapidOCR 也一样，矩阵只剩 `A / aml / a / 53`）。`recognize()` 实测：3×3 矩阵 ⇒ `$A=\left[\begin{matrix}{1}&{-2}&{1}\\{-2}&{0}&{3}\\{1}&{3}&{-1}\\\end{matrix}\right]$` ✓，行内公式 `$|AB|=|A||B|$`、`$a_{ij}=0$`、`$kEA=AkE$` 均正确。**但文字仍有少量错字**（"数乘"→"数秉"、"交换"→"麦换"、"元素"→"无素"）、相邻条目会串行、对角矩阵与分块矩阵未完全出成 LaTeX ⇒ **结构可用、文字必须校对**。单块公式质量更高（手工裁图后 `recognize_formula`：裁准的 3×3 矩阵完全正确），但**裁块位置错了会整段幻觉**（实测裁到空白/箭头时输出英文乱码与 `\frac{\partial\Pi\Pi…`）——所以宁可让 `recognize()` 自己切。
- ⚡ **pix2text 走 GPU：`onnxruntime-gpu` 已装（dl），整页识别 37.8 s → 14.1 s（2.7×）**（2026-10-10 实测，输出与 CPU **逐字一致**）。装法：`uv pip uninstall onnxruntime` 后 `uv pip install onnxruntime-gpu==1.31.0`（160 MB），EP 变为 `['TensorrtExecutionProvider','CUDAExecutionProvider','CPUExecutionProvider']`。⚠ **关键前提：运行前必须把 `D:\envs\dl\Lib\site-packages\torch\lib` 加进 PATH** —— ORT 1.31 直接吃 torch 的 **cu13** 库（`cudart64_13.dll` / `cublas64_13.dll` / `cudnn64_9.dll`），**不需要**再装 CUDA 12 的 `nvidia-*` pip 包；不加 PATH 时 CUDA EP 不会出现在 `get_available_providers()` 里。用法：`Pix2Text.from_config(device="cuda")`。按此速度，213 页线代教材整本约 **50 分钟**（CPU 要 2.2 小时）。
- ⚠ **docs 里有三个 opencv 变体共存**：`opencv-python`（rapidocr 要）· `opencv-python-headless`（pdf2docx 要）· `opencv-contrib-python`（img2table 要），同版本 5.0.0.93、共用同一个 `cv2` 模块目录。实测 `cv2 5.0.0` 导入正常、contrib 模块（`ximgproc`/`aruco`/`face`）在位、rapidocr 与 pdf2docx 均正常、`uv pip check` 报 63 个包全兼容——因为安装顺序上 contrib 最后、文件覆盖在最上层（超集）。**风险**：将来单独重装/升级 `opencv-python` 或 `opencv-python-headless` 会把 contrib 的文件盖掉，可能让 img2table 失效；**要动 opencv 就三个一起升**，或改用 `opencv-contrib-python-headless` 单一变体（需接受另两个包的元数据依赖不再满足）。
- **别信赖 PATH 里的 `python`**：现在它解析到 Windows 商店的 0 字节占位符（执行返回 9009）。一律写全路径，或交给 `build.ps1` 自动选。
- **PyPI 走清华镜像**（已写入 `%APPDATA%\uv\uv.toml`）：实测官方 `files.pythonhosted.org` 只有 **8 KB/s**，镜像 **4586 KB/s**；镜像尚未同步的新包临时加 `--index-url https://pypi.org/simple`。
- uv 本体由 winget 管理（`astral-sh.uv`，0.12.24）；迁移与回滚方案见 `D:\backup\uv-migration\uv迁移方案-20261009.md`，旧 base 的包清单见 `D:\backup\conda-base-backup-20261009-203913\`。

### 通用处理技巧
- **CRLF 陷阱**：PowerShell 正则 `^---\n` 匹配不了 CRLF 文件，frontmatter 批量处理必须行级（`Get-Content` 数组 + 保留行尾）
- **$$ 配对状态机**：行 trim 为 `$$` 翻转块内状态，块内空行删、块间与关闭符后保留
- **图片引用扫描**：取内文后用 `-replace '\\\|','|' -split '\|'` 取首段再 `-replace '\\$',''`，才能处理表格内 `\|` 转义
- **检查脚本阈值经验**：callout 内 `> $$…$$` ≤170 字符、正文长块公式 >120 字符、单句 150~200 字符均为折中豁免线
- **批量改 wikilink 用「先长后短」替换顺序**（防嵌套路径误替换）；写入脚本保留 BOM/行尾状态（`UTF8Encoding($false)` vs 原 BOM），避免全文件 diff

### 子代理与数学核对
- **子代理预验证推导也会错**：主代理必须「重新推导 + 回查原题」，子代理「自己验算 + 标注疑点」机制保留
- **「主代理重推」是过滤错误的核心**：并行数学子代理时对每条报告重新推导确认，约 30% 的 A 类发现经复推后修正或否决
- 子代理引文可能凭印象拼接，凡 `grep` 不中的 A 类一律丢弃
- 子代理处理大文件（>3000 行）需较长时间，可先发消息要部分结果

### 教材 OCR 与裁定
- 教材提取存 `教材OCR\`（不入库；索引 README 入库）：`张宇基础30讲-高数/线代 2027`、`胡寿松自动控制原理-第八版`、`刘豹现代控制理论-第三版`。**页码偏移各书不同**（自控 +8、现控 +8、高数 +6、线代 −7），一律以 `教材OCR\README.md` 的表为准，**别套用 +8**
- **三通道分工（长期遵守，2026-10-10 定）**：① **有文字层的 PDF → `pymupdf.get_text()`**（零 OCR 误差、秒级、带页码；胡寿松那本 692 页就是这样提取的，**不是 OCR**）；② **纯扫描/图片 → RapidOCR 批量**（产出可 grep、可入库、可引页码的语料；张宇、刘豹属此类）；③ **手绘/图形/版式 → 视觉 `read_image`**（OCR 读不了拓扑与版式，如 825 手绘原卷）。**OCR 只负责"批量产出可检索文本"，不当公式权威**
- OCR 文本有系统性丢字符（分数线、撇号、下标、单字符变量），凡引用例题须用答案反推校验
- OCR 路线：旧 .doc/.ppt 二进制含公式图片 → Word COM `SaveAs(FileFormat=17)` 转 PDF → PyMuPDF 渲染 → RapidOCR；中文路径用 `os.listdir` 枚举；控制台 GBK 打印 emoji/✓ 报错 → 写 UTF-8 文件或纯 ASCII；装包统一用 `uv pip install --python D:\envs\docs\Scripts\python.exe …`（**清华镜像已在 `%APPDATA%\uv\uv.toml` 全局配好**，不必再手写 `-i`）
- RapidOCR v1.4.4 传参用 `RapidOCR(params={...})`（dict 形式，旧 kwargs 不再适用）
- **旧 `.doc`/`.ppt` 怎么读**（2026-09-18 实测，**2026-10-10 校正路径**）：资料根目录在 **`C:\Users\23720\OneDrive\自动控制原理\`** 下 —— `…\自动控制原理\按章节-原视频和PPT\`（第5章 = 控制88-17~28）与 `…\自动控制原理\Word-补充自O-God\`（`第五章小结例4.doc` 就在这里）；不在这两个目录里找旧讲义。⚠ 原先记录的 `OneDrive\按章节-原视频和PPT\` 直挂路径**已不存在**（整体下移了一层）。
  - `.doc` → Word COM `SaveAs([ref]$out,[ref]2)`（FileFormat=2 为纯文本）可读；**公式是图片**，只能拿到文字骨架，`第五章小结例4.doc` 这类文档要配合渲染看。
  - `.ppt` → **PowerPoint COM 在本机一律失败**（`Presentations.Open` 报 `Unexpected HRESULT`，换 `MsoTriState`、传整数参、先复制到 `%TEMP%` 都无效）。改用**按文本框记录头定位**：文本以 UTF-16LE 明文存放在 `TextCharsAtom`(0x0FA0) / `TextBytesAtom`(0x0FA8) 里，`data.find(b'\x00\x00\xa0\x0f')` 命中后，紧跟的 4 字节是**小端长度**，按长度切片解 UTF-16LE 即得整段文字（`.a8\x0f` 同理，按 GBK 解）。12 份第 5 章 PPT 用此法抽出 2238 行干净文本；**不要**直接对整文件按 UTF-16 扫描——那会产出 59 万行垃圾，无法读。

### 绘图规范（长期遵守）

**工具选择**：按图的性质选，不要在 GDI+ 里手调像素（历史上反复返工）。三者都是纯文本源码，可复现、可版本管理。

| 图的性质 | 工具 | 说明 |
|:--|:--|:--|
| 电路图 | **circuitikz**（TeX Live 已含） | 元件形状/线宽/字号由包统一，期刊标准；`voltages=straight` 出直箭头电压标注 |
| 频域曲线、时域响应、根轨迹、相平面 | **Python `control` + matplotlib** | 数据由库算，不手算采样点 |
| 几何示意、结构图、角弧标注 | **TikZ** | 弧线、旋转标签、直角标记都有现成写法 |

**目录与构建**：
- 源码与样式模块放 `.scripts\figures\`（ASCII 文件名），成图落 `附件\<中文名>.png`
- 源文件首行用注释声明输出名：`.tex` 写 `% figure: 频域-xxx.png`，`.py` 写 `# figure: 频域-xxx.png`——源码保持 ASCII，附件名沿用仓库中文命名规范
- 构建：`.scripts\figures\build.ps1 -File .\xxx.tex`（或 `-Dir` / `-All`，`-Dpi` 默认 600）；`.tex` 走 xelatex → pdftocairo，`.py` 由脚本自己写 `$env:FIGURE_OUT`
- **新图先 `-File` 单独构建验证，再批量**
- **成图核验（脚本 + 视觉两道并用）**：① **脚本自检** —— `.scripts\figures\_check_fig_layout.py` 批量筛查可量化的问题，跑一遍绘图脚本（拦 `figures_style.save` 与 `Figure.savefig` 两份出口拿到 fig），用 renderer 量三类问题：
  - `[压字]` 文字白框两两重叠（图例框天然包住自己的文字，已豁免）；
  - `[越界]` 文字跑出画布；
  - `[压线]` **文字白框/图例框压住曲线或参考线**——把每条 Line2D 的数据点（`step*` 按 drawstyle 展开、`axhline/axvline` 按 2px 加密）投到像素后，看有没有落进框里；框按「半个线宽」外扩再内缩 1px，防边界擦边误报。
  用法：`D:\envs\figures\Scripts\python.exe _check_fig_layout.py <脚本.py> [...]`（内部把 spec 名取 `__main__`，否则脚本的 `if __name__ == "__main__"` 不执行）。**改完任何图的标注位置都要跑**，目标 0 处；配套 `_probe_layout.py` 打印每个标注的**数据坐标 bbox**，用来挑落点（改标注前先跑它，别用眼睛估）。两个脚本都会**拦截存图**，跑完不改动 `附件\`，可放心跑。图源解释器统一用 uv 环境 `D:\envs\figures`（2026-10-09 起，渲染结果与原 conda 环境逐字节一致）；`build.ps1` 已自动选用它，手工调用时才需写全路径，并自行设 `$env:PYTHONIOENCODING='utf-8'`（否则含 `⟹` 的打印会在 GBK 控制台崩）。② **视觉复核** —— `read_image` 逐张看观感（刻度被压、页脚被裁、标注遮挡），脚本查不出"好不好看"；**两道都要走**。
- **标注不许贴曲线放（长期遵守，2026-09-24 用户指出「遮挡还挺厉害的」后定）**：带白底 `bbox` 的标注一旦压在曲线上，等于把曲线咬掉一块。落点优先级：① 该曲线**够不到的空区**（如相频 < −90° 以下的世界、Bode 幅频上方的留白）；② 三条曲线挤在一起时，**改用图例**（图例框放空白区，颜色对号）；③ 曲线斜穿整个象限时，把标注**下移/上抬到曲线之外**再拉一条细引线（`arrowstyle="-"`）连回目标点。竖线（`axvline`）上的刻度标签要摆在**竖线旁边**（`ha="left"` 且 `x = kc*1.08`），不要骑在线上。
- **825 真题材料是本地专用，不进 git**：`.git/info/exclude` 里已有两条规则（`/控制理论/青岛大学825真题/`、`/附件/青大825-*.png`），它们**从未被 git 跟踪过任何文件**，全靠 remotely-save 多端同步。因此：
  - 对 825 的笔记改动**不要 `git add`**（会被拒；`-f` 强制入库是错的，会把本地专用材料泄漏到版本库）；
  - 出现「只改了 825 笔记」的会话，正常收尾就是**没有 git 提交**（改动由云同步带走），不要为了"有提交"而强行入库；
  - 825 原卷扫描件多为手绘，**拓扑以解答方程为准，布局无法仅凭方程还原**；若确需重画，必须照原图逐线描，不能"从方程反推着画"

**必踩的坑（已实测）**：
- **`pdftocairo` 打不开非 ASCII 输出路径**（报 `Error opening output file`，exit 2）→ build.ps1 已改为先渲到 `%TEMP%` 的 ASCII 临时名再 `Move-Item` 过去，别绕开这一步
- **`pdftocairo` 会给输出名追加 `.png`**：传 `foo.png` 会得到 `foo.png.png`。传不带扩展名的前缀
- **中文字体**：matplotlib 的 `font.family` 必须写成**字体列表**（`= "serif"` 这种别名写法不会逐字形回退，Cambria 缺 CJK 字形就画方框）；`figures_style.py` 已配好 `["Cambria", "Times New Roman", "Microsoft YaHei", "SimHei"]`
- **同一字符串里不要混中文和 `$…$`**：mathtext 会接管整串并套 CM 字体集，中文随即变方框（纯中文、纯公式、中文+西文都正常）。标题写两行：`"惯性环节\n$1/(Ts+1)$"`
- **图内中文的可用写法（已实测，按可靠度排序）**：
  1. **汉字包进 `$\mathrm{…}$`，且整串要"先数学、后中文"**：`r"$K=4$：$\mathrm{不包围}\ (-1,0)$，稳定"` ✅；反过来写成 `r"不包围 $(-1,0)$"` 会让段首汉字变方框 ❌。
  2. **纯中文段用字体族**：`plt.text(..., family=["Microsoft YaHei", "SimHei"])` ✅（不掺 `$…$` 时 `figures_style` 的回退链本来就够用）。
  3. `figures_style.use_style()` 已把 `mathtext.fontset` 设为 `custom` 并把 `mathtext.rm` 指向 `Microsoft YaHei`，这样 `\mathrm{}` 里的汉字有字形。⚠ `mathtext.*` 只接受**单个** fontconfig 模式，写 `"Cambria, Microsoft YaHei"` 会 `ParseException`。
- **`\mathrm` 后面不能跟空格**：`\mathrm j`、`\mathrm{Re}\,G` 这类写法在 custom 字体集下直接 `ParseFatalException: Unknown symbol: \mathrm`（这才是"本机 mathtext 对 `\mathrm` 报错"的真正机制）。改成 `j`、`\mathrm{j}` 或 `\mathrm{Re}` 都正常。`\sqrt3` 同样要写成 `\sqrt{3}`。
- **`tight_layout()` 遇到 GridSpec 双面板会静默拒绝执行**：只打一条 `UserWarning: ... Axes that are not compatible with tight_layout`，布局**一点不动**，图级 `fig.text` 就压在轴标签上。多面板图用 `fig.subplots_adjust(left=…, right=…, top=…, bottom=…)` 显式排版，别依赖 tight_layout。
- **`add_subplot(…, sharex=…)` 不会自动隐藏上面板的刻度标签**：共享横轴的双面板要显式写 `ax.tick_params(labelbottom=False)`，否则上一条面板的刻度文字正好落在下面板的标题上。
- **视觉可用（2026-10-10 复核，此前"读不了 PNG"的记录作废）**：本机 `read_image` 能直接读图并判读内容；**看图与脚本断言并用**——断言管数值（相角最低值、交点个数、穿轴位置），视觉管观感（刻度被压、页脚被裁、标注遮挡），两者都不能省。举反例踩过一次形式坑：`(s+0.01)²` 的极点在 ω=0.01，写成 `(0.01s+1)²` 极点就在 ω=100，画出来的相角只到 −89.9°（这类错只有断言能拦）。
- **`control` 的 rcParams 不在 matplotlib 里**：`plt.rcParams["control.grid"]` 会 `KeyError`。与其和它的默认样式搏斗，不如用 `ct.frequency_response()` 取数据自己画
- **`from matplotlib.path import Path` 与 `pathlib.Path` 撞名**：绘图脚本里同时用到两者时，把前者 `as MplPath`，否则 `fig.savefig(Path(...))` 会抛 `float() argument must be … not 'WindowsPath'`
- **不要用 PowerShell 管道改含中文的源码**：`python -c "...read/write..."` 经管道会按 GBK 写回，注释成乱码，且 git 不易察觉。改笔记/脚本一律走编辑工具的定点替换
- **控制台中文乱码**：build.ps1 已设 `[Console]::OutputEncoding` 与 `PYTHONIOENCODING=utf-8`

**曲线动态范围大时怎么画（奈氏/伯德，长期遵守）**：频率特性常有 3–4 个数量级的纵向跨度（如 $1/[s(s+5)]$ 的 $\operatorname{Im}G$ 在 $\omega\to0^+$ 处到 $-\infty$），线性纵轴会把曲线压成一条线。四条经验：
- **纵轴用 symlog 并显式设刻度**：`ax.set_yscale("symlog", linthresh=…)` 之后**必须** `set_yticks` + `set_yticklabels`，matplotlib 自带的 symlog 刻度格式器会把 $-10^1,-10^2,-10^3$ 全压成 "10"（实测）
- **采样要取到两端极限**，让两支自然贴轴闭合成环；端点若超出视野，用文字或小箭头标"还要继续伸向无穷远"，不要留下看起来像被截断的断头
- **形状比数值更重要时，先换增益**：同一个"对任意 $k>0$ 稳定"的结论，取 $k=2$ 画出的环宽高比远好于 $k=10$（后者扁成一条）
- **先做多画法对比再定稿**：临时脚本一次画 2×2（symlog / 有界倒数坐标 / 局部放大 / 双对数）存一张 PNG，肉眼挑完再写正式脚本，比反复改正式脚本快得多
- **成图必须自己看图**：`read_image` 逐张确认，别只看"脚本没报错"（2026-10-10 起本机视觉可用，这条**真能执行**了）。历史上多次出现刻度被压、页脚被裁、插图压线而脚本"完全正常"

**MATLAB 作为独立复核（环境已装 R2026a）**：不要求用，但**核对容易算错的解析式时值得跑**（见「子代理与数学核对」）。三个已实测的调用坑：
- **`.m` 文件必须纯 ASCII**：`matlab -batch` 按系统 ANSI 读文件，含中文注释直接报"文本字符无效"，把 `%` 注释写成英文即可
- **从含中文的路径 `run()` 会失败**（`D:\obsidian\...` 实测报字符错误）→ 把临时 `.m` 复制到 `%TEMP%` 再跑，用完即删
- **`s = tf('s')` 之后再 `syms s` 会冲突**（`无法从 tf 转换为 sym`）→ 符号段单独 `clear` 并重新 `syms`
- **`nyquist()` 的自动量程会被 $s=0$ 极点拉到 $10^{19}$**，糊成直线 → 给频率范围 `nyquist(G, {wmin, wmax})`，或干脆自己取 `freqresp` 数据画


**与云同步抢文件（长期遵守）**：Remotely Save 现配置为 onedrive / 双向 / **每 10 分钟自动同步**（`autoRunEveryMilliseconds: 600000`，2026-09-17 由 60 秒改来；启动后 10 秒触发一次，`syncOnSave` 延迟 1 秒）、`conflictAction: keep_newer`、`protectModifyPercentage: 50`、V3 算法、`concurrency: 20`。**另一个客户端（手机等）会把附件改名成 `xxx_1789228415866.png`**，本机插件在下次同步时照做「远端改名」：原名当场消失、`![[原名]]` 断链，随后 git 自动备份还把改名结果一并提交（`af63ca6`、`8368f51` 两次同因复发）。**注意：这不是本机的冲突处理，也不是 `conflictAction`/`protectModifyPercentage` 能管的事**（详见下条实证）。
- **实测事实**（别再重新摸索，直接照做）：① **内容没丢**——改名副本与被删原名逐字节相同（`奈氏-例01` SHA256 前后一致），改回名即可，**不必重画**；② 后缀值是**改名时刻**的 epoch 毫秒，不是文件修改时间，所以同批文件的 mtime 可以早好几天（2026-09-17 01:44:46 那批，mtime 跨 9/11–9/16）；③ 每批 8~11 个文件、集中在 200 ms~4 s 内落盘，重灾区正是 `.scripts\figures\` 产出的成图；④ 到 2026-09-17 已复发四次（`af63ca6`、`8368f51`、`4850b59`、本次）。
- **真凶不在本机（2026-09-17 已坐实，推翻此前"改插件/暂停同步"的假设）**：这批改名发生在 **01:44:46**，而本机 **00:13:44 已关机（Kernel-Power 109）、14:04:07 才开机（EventLog 6005）**；`fsutil usn readjournal D:` 在 9/17 的 01 时段**一条记录都没有**（桶直接从 00 跳到 14）。14:06:49（开机后 Remotely Save 首次同步）发生的动作是**本机照做云端指令**：`奈氏-例01.png` → 重命名进回收站（`$R6CHHID.png`，130111 B = 原名那份），14:06:54 再落盘 `奈氏-例01_1789580686386.png`。**⇒ 改名是 OneDrive 云端由同一账号的另一个客户端（手机/另一台设备）做的，本机插件只是把「远端已改名」下载成本地**，所以**暂停本机同步、改 `conflictAction`、改 `ignorePaths` 都防不住**。
- **本机三处都已排除**（代码实测，别再查一遍）：Remotely Save 0.5.25 的冲突去重一律是 **`.dup` 后缀**（`getFileRenameForDup()` → `${name}.dup.${ext}`，PRO 的 `smart_conflict` 对非 md 文件也走这条）；Obsidian 本体 `obsidian.asar` 里 `Date.now()` 202 处、**没有任何按时间造文件名的代码**；每晚 git 备份只做 `git add -A` + commit + push。
- **真凶画像（2026-09-17 16:00 定案，手机/平板截图直接坐实）**：**外部 App 在给附件"留版本历史"**——每次有新版本写入，就把旧版改名成 `<原名>_<写入时刻毫秒>` 归档。截图里 `伯德-例512` 一个名字底下挂着 PNG+JPG 共 18 个版本，时间戳从 `1788501354200`(8/26) 排到 `1789630964180`(9/17)，**每个都精确等于我们写那张图的时刻**（9/8 晚绘图、9/12 22:07、9/13 23:00、9/15 22:00、9/17 01:44 各对应一个后缀值）。这解释了全部现象：① 每批 8~11 个、时间戳只差 200 ms~4 s——那是 `.scripts\figures\` 连续写图的节奏；② `.jpg` 孪生（旧世代 jpg，后统一 png）；③ `校正-例64超前_1788888780292_1789018182803` 这种二次后缀；④ **那 12 张"热图"正是绘图工具链每次会话都会重画的**（奈氏-例01/59/512、伯德-例512/515、校正-例64超前、根轨迹-041-例42b/042-例44/042-例46/044-s012/044-s2s1），各攒 8~17 个历史副本；⑤ 手机侧 1,273 个文件 vs 本库 292 个，多出来的全是它们。
  ⇒ **不是冲突处理、不是 Remotely Save 的锅**：它只是把云端已有的改名照做下来。**修的地方在那台设备上**：把 Obsidian 库目录**从那个 App 的同步/备份范围里排除**（或关掉它的"版本历史 / 自动备份旧版"）。开着"保留历史版本"的云盘/文件管理器 + 指向库目录 = 必然复发。
- **云端清场（2026-09-17 已做，可复用）**：`%USERPROFILE%\OneDrive\Apps\remotely-save\obsidian\附件\` 是 OneDrive 客户端维护的**云端镜像**（文件名明文），它一度被灌进 **205 个**历史副本。清法：逐组按 `原名_<毫秒>` 归组、确认本库有同名原件且内容一致后从镜像删除（删镜像 = 删云端）；本库无对应原件的先查内容（当时只有 4 个 `校正-例64超前_*.jpg` 是早期 jpg 世代、4 份互相同内容，留一份到 `.trash\云端历史副本-20260917\`）。清完镜像 205→0，本库无损。
- **下次怎么一眼确认是"外面干的"**：`check-notes.ps1` 会顺带查**云端镜像** `%USERPROFILE%\OneDrive\Apps\remotely-save\obsidian\附件\`（OneDrive 客户端维护的云上副本、文件名明文），判据是「**镜像里的后缀名有没有对应的原名陪着**」（两边都被改名时，旧的"本库有没有同名"判据会漏报）；只要出现孤儿后缀名就报"改名由外部客户端发起"。想持续盯，就在后台每 30 秒采样一次「本库后缀数 / 镜像后缀数」——**数量一起涨 = 外部 App 又在归档版本**。
- **修法（常驻工具）**：`.scripts\fix-attachment-conflicts.ps1`（默认只预览，`-Apply` 才落盘）。原名已存在时按 SHA256 判定：相同→删多余副本；不同→留修改时间较新的那份，另一份入 `.trash\附件冲突修复-<时间戳>\`。校验时直接 `check-notes.ps1 -Fix`，会先修复再查断链。
- **两道自动保险**：`build.ps1` 构建前后各扫一次成图目录，构建前自动修复、构建后仍冒冲突就报警（`fix-attachment-conflicts.ps1` 挂在 `figures\` 上一层，用相对路径调用）；`check-notes.ps1` 既报「附件带冲突后缀」，也把**笔记直接引用冲突副本名**列为致命项（那种引用当下能命中、下次同步必断，必须改回原名）。
- **批量重画图的注意点**：既然改名来自外部客户端，**暂停本机同步并不能防它**（9/17 那批就是 PC 关机时被改的）；把间隔放宽到 10 分钟只是让本机"别在别人改名时正好也在动同一批文件"。真·批量重画时仍可暂停 Remotely Save，让成图一次落地、一次记账——这是为了省事，不是防线。
- **不要把自控成图放进 `ignorePaths`**：手机端要靠云同步看图，排除了等于图上不了手机。图的正确保障是**可重建**（源码都在 `.scripts/figures/` 且入库，`build.ps1 -File/-All` 随时重生成），加上改名副本内容无损，所以这属于"断链"而非"图丢了"。
- **留证据的办法**：改名只发生在云上、本机只是执行者，所以本机日志（`logToDB`）只能看到 `remote_is_created_then_pull` + `remote_is_deleted_thus_also_delete_local`，看不到"改名"动作本身。真要抓现行，就盯云端镜像目录（见上条）——**PC 关机期间镜像里带后缀的名字冒出来**即可定案；`fsutil usn readjournal D:` 与事件日志（Kernel-Power 109 / EventLog 6005）可用来证明本机当时根本没开机。`data.json` 在 `.obsidian/plugins/remotely-save/.gitignore` 里（**不进版本库、无历史可比**），且是**混淆存储**的（`d` 字段 = base64 反转 → 逐字节反转 → UTF-8 JSON）；要看设置**只在内存里解码打印，不要手改这个文件**（含凭据，插件会自动重写），要改设置走插件设置界面。

**多端同步的方向策略（2026-09-17 血的教训，长期遵守）**：这套库的正确形态是「**PC 唯一作者 + 其他端只读**」。Remotely Save 的「同步方向」（设置里叫「同步方向（实验性）」）才是真正的安全阀——**`protectModifyPercentage` 只是熔断器，管不了方向**：

| 选项值 | 界面名 | 用途 |
|:--|:--|:--|
| `bidirectional` | 双向（默认） | 只有 PC 用；多端同时双向 = 一台设备的误删/改名会广播给所有端 |
| `incremental_push_only` | 仅上传（备份模式） | PC 专用：批量回填云端、恢复事故时用 |
| **`incremental_pull_only`** | **仅下载** | **手机/平板等只读端必须用这个**：只接收，永不上传 |
| `incremental_push_and_delete_only` | 仅上传并删除 | 会广播删除，别给非作者端 |
| `incremental_pull_and_delete_only` | 仅下载并删除 | 会跟随云端删除，慎用 |

- **为什么必须这样**：双向同步下，"删除"是一种**会被广播的指令**。2026-09-17 的实测：平板端删掉 `附件` 文件夹 → 云端被清空（只剩 1 个文件）→ 只差一步就删到 PC（PC 当时没在同步才幸免）。而外部 App 生成的 900 多个历史副本，在双向下也会被一遍遍推上云端。
- **只读端要改内容怎么办**：一律"在 PC 上改，让只读端同步"。反过来在只读端写、又指望它同步出去，就是把上面那个事故重演一遍。
- **事故恢复的推回法**（云端被误删、PC 完好时）：PC 端 `syncDirection` 改 `incremental_push_only`，`protectModifyPercentage` 临时改 `100`（批量上传不受熔断阻断），手动同步把本机推回云端，完事**立刻把方向改回 `bidirectional`、阈值改回 `50`**。2026-09-17 用它把 306 个附件从 1 个恢复到 306 个。
- **动库结构前先让非作者端停手**：要删目录、批量改名、挪文件夹时，先暂停其它端的同步；PC 同步也先暂停更稳妥。

**风格约定**：
- 与正文 MathJax 一致：`unicode-math` + `Cambria Math`（TikZ/circuitikz）；matplotlib 侧 `figures_style.py` 用 `mathtext.fontset="custom"`（数学符号走 Cambria、`\mathrm{}` 里的汉字走 Microsoft YaHei，理由见上）
- 统一配色：图线 `#1E2228`、强调/相频 `#B23020`、幅频 `#1F3D7A`、次要文字 `#606874`、填充 `#E8EFF8`
- 输出 600 dpi 起（`pdftocairo -r 600` / `dpi=300` 配高 figsize），白底或透明底，直接可嵌
- 命名沿用 `自控-xxx.png` / `频域-xxx.png` / `高数-xxx.png`，嵌入尺寸按「wikilink 与图片」节
- **文字压线一律加白底遮罩，不要靠反复挪坐标**：写在信号线上的标注样式（`sig`/`lbl`/`gain`/`sub`/`figcap`）统一加 `fill=white`，文字会把底下的线自动遮断；方框内的文字（`blk`/`sum`）不要加——方框已有填充。
  ⚠ **`fill=white` 必须放在 `font=`、`color=` 之后**——写在样式最前面会把整个节点填成实心块、文字被吞掉（实测：`{fill=white, font=\small, color=figink}` 出黑块，`{font=\small, color=figink, fill=white}` 正常）
- **不要指望自动检测"中文压线"**：三种判据都不稳——`pdftotext -bbox` 对纯中文返回 "no word list"（只认西文/数字）；压线时文字与线互相连通，连通域法必然把两者并成一个巨块；开运算在 300 dpi 下会把汉字笔画一并吃掉。**改用 `list-labels.ps1` 列出所有文字节点坐标与线段坐标，人工对照**——源码级核对比图像启发式快且准

### git 检出与恢复（同步覆盖事故）
- **行尾符差异**会让 status 报 M 而正文无差，用 `git diff --ignore-space-at-eol` 鉴别后 `git restore` 归一
- **云同步被静默回退**：环境允许 remotely-save 保留（多端同步主力），git 作版本兜底。检出法：无图笔记看 `git status` + 抽查近期改动文件的内容 marker（回退 diff 常是原提交的镜像符号）；有图笔记看孤儿附件；用 `git hash-object` 磁盘文件比对历史 blob，判定「旧版覆盖」还是「本地新编辑」再动手
- **恢复对象一律用 `HEAD`**（=远程已确认状态），不要用更老的提交；并行会话期间提交只 `git add` 自己的路径，禁用 `add -A` 扫入对方未完成改动

### 例题编号（长期遵守）
- **统一用章内连续号 `例N.M`**：跨教师、跨章节引用时才不会重号。自控第 5 章的编号规则、例题总表见 `05 第5章 线性系统的频域分析法.md` §⑤，格式为 `例5.12（教材例5-12）` 或 `例5.10〔自编·判稳〕`；正文引用一律用 `例5.N`，教材号只作补充信息。
- **自编题不占例题号（长期遵守）**：编号只给**有明确出处**的题（教材例题、教材习题、课程讲例题）。自编或改写自编的算例**不进编号表**，写成"补充算例"小节即可；用户明确要求过"自编题删掉就行，我会补充类似的"。教材原文里的定义性举例（如 §5-3 的 $\frac{K}{s^2(Ts+1)}$ 结构不稳定）按"教材原文例子"收录，但不占号。
- **插入新例题的三条规则**：① 插在末尾→直接取下一号（首选）；② 插在两例之间→用小数细分号 `例5.9.1`、`例5.9.2`（保序、不重号、不动旧号）；③ 同一位置到第 4 道→跑一次整章重排。
- **重排工具**：`.scripts\renumber-examples.ps1`（常驻）。不带参数只体检（列编号、查重复/缺号）；`-Map "旧=新,..."` 先预览待改文件；加 `-Apply` 才写回。**替换是两段式**（先打标记再落号），避免 `17→14` 之后又被 `14→11` 级联命中。改完要同步索引页的例题总表。
- 引用时写"编号 + 所在篇"（如"见 [[05-4-a 奈氏特殊情形与条件稳定]] 例5.13"），重排后仍能对上。

### 一次性脚本不沉淀
- 拆分/提取/清理脚本用完即删，`.scripts/` 只留常驻工具：`check-notes.ps1`（对标 AGENTS 清单的全库校验，`-Fix` 时先修同步冲突改名）、`fix-attachment-conflicts.ps1`（把 `xxx_1789228415866.png` 改回原名并清理冗余副本，见「与云同步抢文件」）、`renumber-examples.ps1`（例题编号重排）、`build-answer-cards.py`（考研数学二答案题卡，见下条）、`figures\` 绘图工具链（源码入库，属长期设施，不删）

### 考研数学二 题卡（md → LaTeX → PDF，长期遵守）
- **三形态分工**：`数学\考研数学二\YYYY年考研数学二答案与解析.md` 是**唯一真源**（改解析只改它）；`_题卡LaTeX源\YYYY年考研数学二答案与解析.tex` 与 `习题册\YYYY年考研数学二答案与解析.pdf` 都是生成物，由脚本从 md 重排。
- **答案卡**：`D:\envs\docs\Scripts\python.exe .scripts\build-answer-cards.py 2003`（写 tex → xelatex×2 → 覆盖 `习题册\` 的 PDF）；`--all` 只写 tex，`--all --pdf` 才批量编译；`--check` 写进 scratch 并与归档 tex 逐行比对，用于确认转换器没跑偏（归档 27 份 tex 应 0 差异）。脚本本身是纯 stdlib，任何 Python 都能跑，写解释器全路径是为了 conda 退役后仍然可用。
- **试题卡**：`_题卡LaTeX源\gen.py YYYY …`（`YYYY年考研数学二试题.md` → `YYYY.tex`，一题一页 240×200mm，页数必须等于题数）。
- **入库口径**（2026-09-29 用户确认）：`_题卡LaTeX源\*.tex`（答案卡 + 试题卡）与 `gen.py` **进 git**；同目录 `*.pdf`、`*.aux`、`*.log` 由 `.git/info/exclude` 排除，不重复入库（答案 pdf 的正本在 `习题册\`）。
- 写解析要守转换器的输入语法：`**N.（yyyy.N；原卷X）答案：…**` 起题、`## 一、…` 分节、`> 错题：[[…]]`、`> [!note]` / `> [!tip]`、`- ` 列表、`$$…$$`；**别在解析页里用表格/图片/H4**（归档里没有这些形态，转换器未覆盖）。新建年份的 md 同样照此写，`--all` 会自动带上。

