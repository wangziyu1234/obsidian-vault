$ErrorActionPreference = 'Stop'
$log = 'D:\obsidian\.workbuddy\tmp_render\com_log4.txt'
$src = 'C:\Users\23720\OneDrive\Word-补充自O-God'
$dst = 'D:\obsidian\.workbuddy\tmp_render'
$names = @('超前校正01','超前校正02','迟后校正01','迟后校正02','迟后校正03','迟后超前校正01','串联PID校正01','PID校正01','希望特性设计法')
$lines = @()
try {
  $word = New-Object -ComObject Word.Application
  $word.DisplayAlerts = 0
  $word.Visible = $false
  foreach ($n in $names) {
    $docPath = [string](Join-Path $src ($n + '.doc'))
    $pdfPath = [string](Join-Path $dst ($n + '.pdf'))
    if (Test-Path -LiteralPath $pdfPath) { $lines += ("SKIP " + $n); continue }
    $d = $word.Documents.Open($docPath, $false, $true)
    $d.SaveAs($pdfPath, 17)
    $d.Close($false)
    if (Test-Path -LiteralPath $pdfPath) { $lines += ("OK " + $n) } else { $lines += ("FAIL " + $n) }
  }
  $word.Quit()
} catch {
  $lines += ("ERR " + $_.Exception.Message)
}
[System.IO.File]::WriteAllLines($log, $lines)
