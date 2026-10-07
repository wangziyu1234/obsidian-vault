from pathlib import Path
import re
root=Path('D:/obsidian/控制理论/青岛大学825真题')
source=(root/'_导出工具/export-pdf.cjs').read_text(encoding='utf8')
source=source.replace("const notesDir = path.join(base, 'Markdown笔记');", "const project = path.join(base, '777改编模拟卷');\nconst notesDir = path.join(project, 'Markdown笔记');")
source=source.replace("const dest = path.join(base, '模拟卷PDF');", "const dest = path.join(project, 'PDF');")
source=source.replace("const htmlDir = path.join(base, '_导出工具/html');", "const htmlDir = path.join(base, '_导出工具/mock-html');")
start=source.index('function makeHeader(');end=source.index('async function make(',start)
source=source[:start]+'''function makeHeader(year, solution) {
 const id=String(year).padStart(2,'0');
 return `<h1>青大825模拟卷 · 第 ${id} 套</h1><div class="subtitle">${solution?'答案与解析':'试题与答题留白'} · 777题型改编 · 150分 / 180分钟</div>` + (solution?'<div class="instructions">选择题45分钟、综合题120分钟、检查15分钟。题源及评分参考列在各题解析后；模型按题设独立求解。</div>':'<div class="meta"><span>姓名：____________</span><span>日期：____________</span><span>用时：____________</span></div><div class="instructions">第1—12题：单项选择，每题5分；第13—17题：综合题，每题18分。不得使用计算器。除另有说明外均按零初始条件计算；MATLAB代码用于读取模型，仍须手算。</div>');
}
function cleanQuestion(year,q) { return q.body; }
''' +source[end:]
source=source.replace("`${year}年青岛大学825${solution?'答案与解析':'试题'}.md`", "`${String(year).padStart(2,'0')} 青大825模拟卷（${solution?'答案与解析':'试题'}）.md`")
source=source.replace("const name=`${year}年青岛大学825${solution?'答案与解析':'模拟卷'}.pdf`;", "const name=`${String(year).padStart(2,'0')} 青大825模拟卷（${solution?'答案与解析':'试题'}）.pdf`;")
source=source.replace("/^20\\d\\d$/", "/^[1-5]$/")
source=source.replace('Array.from({length:20},(_,i)=>2006+i)','Array.from({length:5},(_,i)=>i+1)')
source=source.replace('${year} 青岛大学 ·', '第${year}套 · 青大825 ·')
# Sources may contain longer material; keep formula blocks and code together.
(root/'_导出工具/export-mocks.cjs').write_text(source,encoding='utf8')
print('Mock PDF exporter ready')
