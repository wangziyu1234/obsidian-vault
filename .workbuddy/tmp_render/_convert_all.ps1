$ErrorActionPreference = 'Stop'
$log = 'D:\obsidian\.workbuddy\tmp_render\com_log7.txt'
$src = 'C:\Users\23720\OneDrive\Word-补充自O-God'
$dst = 'D:\obsidian\.workbuddy\tmp_render'
$pairs = @(
  'ch2ex|第二章例02.doc',
  'ch3sum|第三章小结.doc',
  'ch3s1|第三章小结01.doc',
  'ch4sum|第四章小结.doc',
  'ch5sum|第五章小结.doc',
  'ch5s1|第五章小结1.doc',
  'ch5ex|第五章例题01.DOC',
  'ch5ex4|第五章小结例4.doc',
  't123|自动控制原理1～3章测验题.doc',
  'comp|控制系统元件.doc',
  'tlink|典型环节及其传递函数.doc',
  'sfdr|结构图等效变换规则.doc',
  'sfde|结构图等效变换举例.doc',
  'sec2d|二阶欠阻尼动态性能.doc',
  'sec2i|二阶系统性能改善及稳定性.doc',
  'hstep|高阶系统的阶跃响应及动态性能.doc',
  'hoc0|高阶系统性能计算0.doc',
  'hoc1|高阶系统性能计算1.doc',
  'sol2|解2：.doc',
  'disc|离散系统的稳定性.doc',
  'sampex|例3 采样系统结构图.doc',
  'df01|典型非线性特性的描述函数01.doc',
  'dg|自控大纲.doc'
)
$lines = @()
try {
  $word = New-Object -ComObject Word.Application
  $word.DisplayAlerts = 0
  $word.Visible = $false
  foreach ($p in $pairs) {
    $kv = $p.Split('|')
    $n = $kv[1]
    $docPath = [string](Join-Path $src $n)
    $pdfPath = [string](Join-Path $dst ($kv[0] + '.pdf'))
    if (Test-Path -LiteralPath $pdfPath) { $lines += ("SKIP " + $kv[0]); continue }
    if (-not (Test-Path -LiteralPath $docPath)) { $lines += ("MISS " + $n); continue }
    $d = $word.Documents.Open($docPath, $false, $true)
    $d.SaveAs($pdfPath, 17)
    $d.Close($false)
    if (Test-Path -LiteralPath $pdfPath) { $lines += ("OK " + $kv[0] + " " + $n) } else { $lines += ("FAIL " + $n) }
  }
  $word.Quit()
} catch {
  $lines += ("ERR " + $_.Exception.Message)
}
[System.IO.File]::WriteAllLines($log, $lines)
