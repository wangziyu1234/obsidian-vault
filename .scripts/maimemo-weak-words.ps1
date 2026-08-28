<#
.SYNOPSIS
  从墨墨开放 API「学习记录」挖掘薄弱词，生成 英语\墨墨弱词清单.md。

.DESCRIPTION
  - 调 POST /open/api/v1/memo/study/query_study_records，按下次复习日期游标翻页
    （该接口无 offset，每页上限 1000；只能取到可调度记录，非全量）
  - 对每词取 学习次数 / 上次反馈 / 下次复习，按三类分桶：
      顽固 STICKING（标签）、易忘 FORGET（上次反馈）、模糊 VAGUE（上次反馈）
  - 全量重生成 英语\墨墨弱词清单.md（自动生成仪表盘，勿手改正文）

.PARAMETER TokenFile  token 文件（默认 .maimemo_token）
.PARAMETER NotePath   弱词清单 md（默认 .\英语\墨墨弱词清单.md）
.PARAMETER BaseUrl    API 基址（默认 https://open.maimemo.com/open）

.EXAMPLE
  .\maimemo-weak-words.ps1

.NOTES
  token 只在内存中使用，绝不写入任何入库文件。
  词汇量受 API 分页限制，笔记内会标注「非全量」。
#>
param(
  [string]$TokenFile = (Join-Path (Get-Location) '.maimemo_token'),
  [string]$NotePath  = (Join-Path (Get-Location) '英语\墨墨弱词清单.md'),
  [string]$BaseUrl   = 'https://open.maimemo.com/open'
)
$ErrorActionPreference = 'Stop'

if (-not (Test-Path $TokenFile)) { throw "缺少 token 文件: $TokenFile" }
$token = (Get-Content $TokenFile -Raw).Trim()
if (-not $token) { throw 'token 为空' }
$headers = @{ Authorization = "Bearer $token"; Accept = 'application/json' }
$url = "$BaseUrl/api/v1/memo/study/query_study_records"

# ---- 下载（游标翻页 + 按 voc_id 去重）----
$seen = @{}
$cursor = $null
$maxPages = 30
$pages = 0
while ($pages -lt $maxPages) {
  $pages++
  if ($cursor) { $body = @{ limit = 1000; next_study_date = @{ start = $cursor } } | ConvertTo-Json -Depth 6 }
  else         { $body = @{ limit = 1000 } | ConvertTo-Json }
  $r = Invoke-RestMethod -Uri $url -Headers $headers -ContentType 'application/json' -Method Post -Body $body -TimeoutSec 30
  $recs = $r.data.records
  if (-not $recs -or $recs.Count -eq 0) { break }
  foreach ($rec in $recs) { if ($rec.voc_id) { $seen[$rec.voc_id] = $rec } }
  $maxDate = ($recs | ForEach-Object { $_.next_study_date } | Where-Object { $_ } | Sort-Object | Select-Object -Last 1)
  if (-not $maxDate -or $maxDate -eq $cursor) { break }
  $cursor = $maxDate
  Start-Sleep -Milliseconds 250
}
$all = @($seen.Values)
if (-not $all) { throw '未取到学习记录' }

# ---- 分桶 ----
$sticking = @($all | Where-Object { $_.tags -contains 'STICKING' })
$forget   = @($all | Where-Object { $_.last_response -eq 'FORGET' })
$vague    = @($all | Where-Object { $_.last_response -eq 'VAGUE' })
$union    = @{}
$sticking + $forget + $vague | ForEach-Object { $union[$_.voc_id] = $true }

function RespCn($v) {
  switch ($v) {
    'FAMILIAR' { '认识' } 'VAGUE' { '模糊' } 'FORGET' { '忘记' }
    'WELL_FAMILIAR' { '熟知' } default { $v }
  }
}
function NextDate($s) {
  if (-not $s) { return '—' }
  try { return ([datetimeoffset]::Parse($s).ToOffset([timespan]::FromHours(8))).ToString('yyyy-MM-dd') }
  catch { return $s.Substring(0, [Math]::Min(10, $s.Length)) }
}

# ---- 渲染 ----
$today = (Get-Date).ToString('yyyy-MM-dd')
$sb = New-Object System.Text.StringBuilder
function AddLine([string]$s) { [void]$sb.AppendLine($s) }

AddLine '---'
AddLine ("create: " + $today)
AddLine ("modify: " + $today)
AddLine 'tags: [英语, 墨墨, 单词]'
AddLine '---'
AddLine ''
AddLine '> 返回目录：[[英语]]'
AddLine ''
AddLine '# 墨墨弱词清单'
AddLine ''
AddLine '> [!abstract]'
AddLine '> 考研词汇专项复盘：从墨墨开放 API 学习记录里挖出的「顽固 / 易忘 / 模糊」词，按学习次数排序。每天运行一次 `.scripts\maimemo-weak-words.ps1` 重新生成。'
AddLine '>'
AddLine ("> 当前覆盖 **{0}** 个独立弱词、**{1}** 个词的学习历史；三类合计 {2} 条，其中 **{3}** 个词既是顽固又是易忘。受墨墨 API 每页 1000 上限约束，此为**非全量**。" -f $union.Count, $all.Count, ($sticking.Count + $forget.Count + $vague.Count), (@($sticking | Where-Object { $_.last_response -eq 'FORGET' }).Count))
AddLine ''

function EmitSection($title, $records) {
  AddLine ('## {0}' -f $title)
  AddLine ''
  AddLine '| 单词 | 次数 | 上次反馈 | 下次复习 |'
  AddLine '| --- | --- | --- | --- |'
  foreach ($rec in ($records | Sort-Object study_count -Descending)) {
    AddLine ('| {0} | {1} | {2} | {3} |' -f $rec.voc_spelling, $rec.study_count, (RespCn $rec.last_response), (NextDate $rec.next_study_date))
  }
  AddLine ''
}

EmitSection '🚩 顽固词（STICKING）' $sticking
EmitSection '🥲 易忘词（当前反馈 FORGET）' $forget
EmitSection '🌫️ 模糊词（当前反馈 VAGUE）' $vague

# ---- 写文件（UTF-8 无 BOM）----
$dir = Split-Path $NotePath -Parent
if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
[System.IO.File]::WriteAllText($NotePath, $sb.ToString(), (New-Object System.Text.UTF8Encoding($false)))

Write-Host ("弱词清单已更新: {0}" -f $NotePath)
Write-Host ("  独立弱词 {0} / 全量 {1} 词" -f $union.Count, $all.Count)
Write-Host ("  三类: 顽固 {0} 易忘 {1} 模糊 {2}" -f $sticking.Count, $forget.Count, $vague.Count)
