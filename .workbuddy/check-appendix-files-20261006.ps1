$ErrorActionPreference = 'Stop'
$taskRoot = 'D:\obsidian'
$base = Join-Path $taskRoot '控制理论\自动控制原理'
$files = @(Get-ChildItem -LiteralPath $base -Filter '附录*.md' | Select-Object -ExpandProperty FullName)
$extra = @('自动控制原理.md', '07-1 采样与z变换.md', '07 第7章 线性离散系统的分析与校正.md', '05-3-1 幅相曲线的画法与最小相位.md', '05-3 奈氏图（幅相特性与奈氏判据）.md', '05 第5章 线性系统的频域分析法.md')
$files += @($extra | ForEach-Object { Join-Path $base $_ })
$failed = 0
$reports = [System.Collections.Generic.List[string]]::new()
foreach ($file in $files) {
    $result = & 'C:\Program Files\PowerShell\7\pwsh.exe' -NoProfile -File (Join-Path $taskRoot '.scripts\check-notes.ps1') -Root $taskRoot -File $file 2>&1
    $code = $LASTEXITCODE
    $content = $result -join "`n"
    $reports.Add($file + "`n" + $content)
    if ($code -ne 0 -or $content -match '【待修】') {
        $failed++
        Write-Output $content
    }
}
[IO.File]::WriteAllText((Join-Path $taskRoot '.workbuddy\appendix-check-report-20261006.txt'), ($reports -join "`n`n"), [Text.UTF8Encoding]::new($false))
Write-Output "Checked $($files.Count) files; failures or warnings: $failed"
if ($failed -gt 0) { exit 1 }
