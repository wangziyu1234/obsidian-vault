# 项目约定（D:\obsidian 知识库）【精简版 2026-09-25；细节见 AGENTS.md / .workbuddy 日志 / 笔记本体】

## 例题来源规则（用户明确）
- 优先级：教材例题 > 教材习题 > 习题册 > 讲例题 ≫ 自编；不典型、凑不出出处的自编题不留。顺序永远是「先找源 → 再决定改标/换数/删」，勿凭印象判 trivial（实测翻过车）。
- 核出处快路：`教材OCR/分章/自控-第0N章.txt` grep（书内页 = PDF 页 − 8）；习题册渲染 jpg 再读。
- 「习题5-N」两套编号：教材 5-1—5-29 vs 777 习题册 5-1—5-40；习题册的写成「习题5-N（学校 年份）」。
- **777 配图用原图**（用户 2026-09-25 明确）：能裁原书图就用原图，不自己画 mermaid 结构图/流图。

## 错题本（数学/错题本/）
- `数学\错题本\YYYY\YYYY-NN 关键词.md`，一题一篇，模板 `templates\错题模板.md`，60~80 行；「我卡在哪」永不删，原题与完整推导不抄。
- 复习三处联动：正文勾框 + frontmatter `review` 删日期 + `mastery` 调档（0 跳过→1 刚错→2 会做不熟→3 稳；0 档 review 空进「跳过挂起」）。
- 小失误（漏 +C）不算复发 ⟹ 提到 2、日期不动；原错因复发才退 1 重排。
- 弃题判据：可弃=自造辅助函数/反证的技巧型证明；慎弃=零点定理/变上限积分求导/保序性/单调性外壳；弃题也要写到"免费的那一步"。
- 用户口吻「2000 数二第 11 题」→ 自取原题按规范改三处；估分「第一次错了就是错了」，首次/复盘后两个数字并列；2002 年前数二满分 100（×1.5 折算）。

## 校验与提交
- 改完两个都跑：`check-notes.ps1`（PowerShell 工具 `&` 调用 `*>` 落盘再读；bash 里禁 powershell.exe -Command）+ `check-math-format.py --path 控制理论`。渲染级必修、排版按需。
- 每批尽快 commit+push；信息写 `.workbuddy/_msgNN.txt` 再 `commit -F`；只 add 自己的路径，禁 add -A。
- 行尾一律 CRLF（二进制读写判断，写完查裸 LF=0）；numstat 0/0=行尾幽灵直接 checkout。
- agent 环境 git 走 SSH（HTTPS 必败）；用户真实 git 在 `D:\Program Files\Git`；~/.gitconfig 硬编码 Clash 代理 7897，代理挂则 HTTPS 全挂、SSH 不受影响。**严禁把凭据值打印到会话**（输出脱敏）。

## 批量脚本坑
- 禁止 `文本.replace('\n', 变量)`；按行组装 `'\r\n'.join(lines)`，写前断言、写后复核。行尾二进制读判断。
- bash 双引号包 Python 单行吃反斜杠 → 脚本写 `.workbuddy/_x.py` 再跑；脚本可重跑（命中就 SKIP）；PowerShell 5 无三元。

## 看图与绘图（关键教训）
- ⚠️ Read 图片能否看到取决于会话模型，不可靠，看不见时会脑补转录（777 第5章初录翻车）。转录用 `.workbuddy/_ocr_page.py`（RapidOCR）；公式密集处用 `_zoom_a2.py` 式放大复核；要数值用 control 库重算。
- 裁图 `_crop_fig.py`（分数包围盒+阈值 170 去水印+断言），成图必须预览核验边缘；包围盒用 `_probe_band.py` 定。
- 自绘图走 `.scripts\figures\`：mathtext 用 `$\mathrm{j}\omega$`（\mathrm 后带空格）；`_check_fig_layout.py` 查压字/越界/压线必跑归零；标注不贴曲线放（72 张遗留待清）。
- tight_layout 对 GridSpec 失效 → subplots_adjust；sharex 不自动藏刻度 → tick_params(labelbottom=False)；别补 set_box_aspect(1)。

## 777 习题集进度（详见 777习题集目录.md）
- 已录：第 1（ea5fa74）、5（b5bde8e）、**2 章（cf235f3，09-25）**；剩 3/4/6/7/8 → 强化 300 题、现控 200 题。
- 每章 SOP：渲染 PDF → 读题/答案 → 裁图（含答案册自绘图）→ 题目页+答案页（CRLF、双校验）→ 目录更新 → commit+push。两册 PDF 页 = 书内页 + 6。
- 勘误先查 `777习题集官方勘误摘录.md`，落实处标 ⚠️；「改图」条目提不出图须回原文档。
- 第2章复核细节存 2026-09-25 日志（2-20/2-22/2-24 拓扑定案、2-36 系数、2-39 重推、2-5 留数）。
- mermaid 反馈框图（如仍需要）：引出点画法 `G --> B((•))`，`B --> 输出` + `B --> H --> SUM`。

## 笔记体例（要点）
- 方法/知识点写方法篇自足；同型题不重复补例；题图本体随笔记落附件。
- 拆分：>250 行按主题拆（附录/single-exercise/exam-paper/exam-solutions 豁免）；三处索引同步；合并改写全部反向链接。
- `type:` 按实际标；页尾统一出口行；method 页 abstract 后 5 条考点速记；`aliases:` 顺手补。
- 高数拆分页体例（第5讲样板）：按题型切分，「知识点→配套例题」配对，小节号跨文件连续。
- 第5章入口 232 行贴上限别再加；例题编号用到 例5.30，新增插末尾。

## OneDrive 课件与 825
- 根目录 `C:\Users\23720\OneDrive\按章节-原视频和PPT\`、`Word-补充自O-God\`；旧 .doc 用 Word COM SaveAs；.ppt 用文本框记录头法（`data.find(b'\x00\x00\xa0\x0f')`）。
- 825 真题材料与 `数学\考研数学二\_题卡LaTeX源\` 本地专用不进 git。
