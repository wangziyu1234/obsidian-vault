# 项目约定（D:\obsidian 知识库）【精简版 2026-09-30；细节见 AGENTS.md / .workbuddy 日志 / 笔记本体】

## 例题来源规则（用户明确）
- 优先级：教材例题 > 教材习题 > 习题册 > 讲例题 ≫ 自编；不典型、凑不出出处的自编题不留。顺序永远是「先找源 → 再决定改标/换数/删」，勿凭印象判 trivial（实测翻过车）。
- 核出处快路：`教材OCR/分章/自控-第0N章.txt` grep（书内页 = PDF 页 − 8）；习题册渲染 jpg 再读。
- 「习题5-N」两套编号：教材 5-1—5-29 vs 777 习题册 5-1—5-40；习题册的写成「习题5-N（学校 年份）」。**777 配图用原图**，不自己画结构图/流图。

## 错题本（数学/错题本/）
- `数学\错题本\YYYY\YYYY-NN 关键词.md`，一题一篇，模板 `templates\错题模板.md`，60~80 行；「我卡在哪」永不删，原题与完整推导不抄，答案留 abstract。
- 复习三处联动：正文勾框 + frontmatter `review` 删日期 + `mastery` 调档（0 跳过→1 刚错→2 会做不熟→3 稳；0 档 review 空进「跳过挂起」）。小失误（漏 +C）不算复发 ⟹ 提到 2、日期不动；原错因复发才退 1 重排（明天/+3/+7）。
- 弃题判据：可弃=自造辅助函数/反证的技巧型证明；慎弃=零点定理/变上限积分求导/保序性/单调性外壳；弃题也要写到"免费的那一步"。
- 用户口吻「2003.12 选的 b」→ 自取原题判对错：首错按 `01 错题本使用规范` 建卡（review 排当天/次日/+3/+7/+30）→ 解析页加 `> 错题：[[…]]` 行 → 挂讲次与同型真题链接 → `check-mistake-cards.py` + check-notes.ps1 → commit；复述复习结果则改三处。
- 估分「第一次错了就是错了」，首次/复盘后两个数字并列；2002 年前数二满分 100（×1.5 折算）。

## 校验与提交
- 改完两个都跑：`check-notes.ps1`（**唯一正路 = pwsh 7 子进程**：`& "C:\Program Files\PowerShell\7\pwsh.exe" -NoProfile -File <脚本> -Root "D:\obsidian" [-File <单文件>] *> 落盘` + `$LASTEXITCODE` 落盘再读；宿主直调被脚本末尾 `exit` 杀丢输出、PS 5.1 解析无 BOM UTF-8 报 ParserError；详见 skill `obsidian-check-notes-run`）+ `check-math-format.py --path 控制理论`。渲染级必修、排版按需。
- 每批尽快 commit+push；信息写 `.workbuddy/_msgNN.txt` 再 `commit -F`；只 add 自己的路径，禁 add -A。
- 行尾**随文件家族**：数学/ 页面工作区是 LF、777 页面是 CRLF，blob 统一归一 LF（`core.autocrlf=true`）——写前先看原文件行尾并保持一致，防混入异类行尾；numstat 0/0=行尾幽灵直接 checkout。
- agent 环境 git 走 SSH（HTTPS 必败）；~/.gitconfig 硬编码 Clash 代理 7897，代理挂则 HTTPS 全挂、SSH 不受影响。**严禁把凭据值打印到会话**（输出脱敏）。

## 批量脚本与表格
- 禁止 `文本.replace('\n', 变量)`；按行组装 `'\r\n'.join(lines)`，写前断言、写后复核；bash 双引号包 Python 单行吃反斜杠 → 脚本写 `.workbuddy/_x.py` 再跑，脚本可重跑（命中就 SKIP）。
- **插入 callout/段落的锚点坑**：以「下一题标题」为锚点会插到标题之后，必须插在标题**之前**；收尾必查 `^## ` 重号与空标题。
- 表格一律紧凑：`| a | b |` + `| :-- |`，不按列宽补空格（Obsidian 自动对齐被编辑过的表；`.scripts\normalize-md-tables.py --check` 只报告）。全库 18 个历史宽表未动（用户未决定）。

## 看图与绘图（关键教训）
- ⚠️ Read 图片不可靠（看不见会脑补，777 翻过车）：转录用 `.workbuddy/_ocr_page.py`（RapidOCR）；公式密集处放大复核；要数值用 control/sympy 重算。
- 裁图 `_crop_fig.py`（阈值 170 去水印+断言），成图必须预览核验边缘，包围盒用 `_probe_band.py` 定；两套 dpi 渲染坐标不同源，量墨迹必须同 PROBE_PREFIX。
- 自绘图走 `.scripts\figures\`（mathtext `\mathrm{j}\omega` 带空格）+ `_check_fig_layout.py` 归零；tight_layout 对 GridSpec 失效 → subplots_adjust；sharex 不自动藏刻度 → tick_params(labelbottom=False)。

## 777 习题集（三册全部录完 2026-09-30；细节见 777习题集目录.md + 各 HANDOVER 文件 + git log）
- 基础 300 题 8 章、现控 200 题 5 章、强化 300 题 8 章全部收官：题目页+答案页+图+速查表，勘误对照官方摘录落实，sympy 复算留档（判原书错前必须先回查题目册原题）。
- 官方勘误文档：现控册 `DSUdRak9ZRXFvU3d4`、基础/强化册 `DSVFReWxzU29ia1R5`；get_content 只回文字层，124 张勘误配图已核（dop-api→docimg 带 Referer 下载→RapidOCR）。仍为原错标 ⚠️，印刷版已吸收的不标。
- SOP：渲染 PDF → 读题/答案 → 裁图 → 题目页+答案页（CRLF、双校验）→ 目录更新 → commit+push。页码偏移：基础+现控册 PDF 页 = 书内页+6；强化册 = 书内页+5。超长答案页单次 Write 会失败（>60KB）→ 分 partA/B 再脚本拼 CRLF。
- MIMO 能观标准型 B_o：分子系数矩阵低次块在上 vstack，不是 C_c^T（现控 3-27 踩坑）。

## 频域特征点速算（用户明确口径）
- 三频率：$\omega_0=1/\sqrt{T_1T_2}$ 落轴点；$\omega_g$ 穿越频率（$\varphi=-180°$，教材记 $\omega_x$ 同一量）；$\omega_c$ 截止频率（$|G|=1$）。一律 $K,T_1,T_2,\tau$ 直写，只留 $\tau_c=\frac{T_1T_2}{T_1+T_2}$。
- 门限：双惯性 $\tau_c$（Ⅰ型有无穿越点）与 $T_1+T_2$（Ⅱ型可稳需 $\tau>T_1+T_2$）；单惯性 $\tau\ne T$ 永不落轴 → 无 $\omega_g$、$h=\infty$，ν=2 判稳 ⟺ $\tau>T$；典型Ⅰ型 $KT=0.5$ → $\zeta=0.707$、$\omega_c\approx0.455/T$、$\gamma\approx65.5°$。777 的 $\omega_c$ 是渐近值，引用注明。分页：05-3-8 / 05-3-9 / 附录 z变换与离散化速查。

## 笔记体例与资料源
- 方法页自足、同型题不重复补例；>250 行按主题拆，但附录/单题(single-exercise)/整卷(exam-paper|exam-solutions)/统计页(long-form)/目录页(type: index)豁免。新页收尾：`$$` 奇偶【致命】必查；插链接前先看邻页行数（250 上限会被顶爆）。
- OneDrive 课件 38 份已全核完（2026-09-26），结论在 `12 资料索引（OneDrive）.md`，不必再翻原 Word；旧 .doc 用 Word COM SaveAs，.ppt 用文本框记录头法。825 真题材料本地专用不进 git。
- 题卡 LaTeX：`.tex` 已入库（生成物排除）；试题卡 `gen.py`、答案卡 `.scripts\build-answer-cards.py`——**改解析只改 md，再跑一次脚本**。
