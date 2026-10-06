$ErrorActionPreference='Stop'
$taskRoot='D:\obsidian'
$base=Join-Path $taskRoot '控制理论\自动控制原理'
$names=@('附录 自控常用公式总表.md','附录 非线性系统速查.md','自动控制原理.md','08 第8章 非线性控制系统分析.md','附录 教材对照与复习索引.md')
$failed=0
$logs=[System.Collections.Generic.List[string]]::new()
foreach($name in $names){
    $out=& 'C:\Program Files\PowerShell\7\pwsh.exe' -NoProfile -File (Join-Path $taskRoot '.scripts\check-notes.ps1') -Root $taskRoot -File (Join-Path $base $name) 2>&1
    $code=$LASTEXITCODE
    $str=$out -join "`n"
    $logs.Add($name+"`n"+$str)
    if($code -ne 0 -or $str -match '【待修】'){$failed++;Write-Output $str}
}
[IO.File]::WriteAllText((Join-Path $taskRoot '.workbuddy\new-control-appendices-check-20261006.txt'),($logs -join "`n`n"),[Text.UTF8Encoding]::new($false))
Write-Output "Checked $($names.Count) notes; failures/warnings: $failed"
if($failed){exit 1}
