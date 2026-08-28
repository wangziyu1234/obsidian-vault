<#
.SYNOPSIS
  拉取墨墨背单词「今日学习进度」，在库内维护 英语\墨墨学习打卡.md 每日打卡页。

.DESCRIPTION
  - 从库根 .maimemo_token 读 Bearer token（该文件已在 .gitignore，不入库）
  - 调 POST /open/api/v1/memo/study/get_study_progress 取今日学习进度
  - 历史存于 .scripts\maimemo-data.json，每次只新增/覆盖「今天」一行
  - 全量重生成 英语\墨墨学习打卡.md（自动生成的仪表盘，勿手改正文）

.PARAMETER TokenFile  token 文件（默认 .maimemo_token）
.PARAMETER DataFile   历史数据 JSON（默认 .scripts\maimemo-data.json）
.PARAMETER NotePath   打卡页 md（默认 .\英语\墨墨学习打卡.md）
.PARAMETER BaseUrl    API 基址（默认 https://open.maimemo.com/open）

.EXAMPLE
  .\maimemo-daily.ps1        # 今天第一次跑；之后每天跑会更新今天那行

.NOTES
  token 只在内存中使用，绝不写入任何入库文件。
#>
param(
  [string]$TokenFile = (Join-Path (Get-Location) '.maimemo_token'),
  [string]$DataFile  = (Join-Path (Get-Location) '.scripts\maimemo-data.json'),
  [string]$NotePath  = (Join-Path (Get-Location) '英语\墨墨学习打卡.md'),
  [string]$BaseUrl   = 'https://open.maimemo.com/open'
)
$ErrorActionPreference = 'Stop'

# 1) token
if (-not (Test-Path $TokenFile)) { throw "缺少 token 文件: $TokenFile" }
$token = (Get-Content $TokenFile -Raw).Trim()
if (-not $token) { throw "token 为空" }
$headers = @{ Authorization = "Bearer $token"; Accept = 'application/json' }

# 2) 今日进度
$progress = $null
try {
  $resp = Invoke-RestMethod -Uri "$BaseUrl/api/v1/memo/study/get_study_progress" `
    -Headers $headers -ContentType 'application/json' -Method Post -Body '{}' -TimeoutSec 30
  $progress = $resp.data.progress
} catch {
  Write-Warning "API 调用失败: $($_.Exception.Message)"
  if (-not (Test-Path $NotePath)) { throw "无历史打卡页且 API 失败，无法生成" }
  Write-Host 'API 失败，保留现有打卡页。'
  return
}
if (-not $progress) { throw '响应里没取到 progress' }

$finished = [int]$progress.finished
$total = [int]$progress.total
$studyMs = [int64]$progress.study_time

# 3) 历史数据
$today = (Get-Date).ToString('yyyy-MM-dd')
$data = @{ create = ''; days = @{} }
if (Test-Path $DataFile) {
  $raw = Get-Content $DataFile -Raw
  if ($raw) {
    $p = $raw | ConvertFrom-Json
    if ($p.create) { $data.create = [string]$p.create }
    if ($p.days) {
      $data.days = @{}
      $p.days.PSObject.Properties | ForEach-Object {
        $data.days[$_.Name] = @{
          finished      = [int]$_.Value.finished
          total         = [int]$_.Value.total
          study_time_ms = [int64]$_.Value.study_time_ms
        }
      }
    }
  }
}
if (-not $data.create) { $data.create = $today }
$data.days[$today] = @{ finished = $finished; total = $total; study_time_ms = $studyMs }

# 4) 统计
$days = $data.days
$dateList = @($days.Keys | Sort-Object)
$totalMs = 0L
foreach ($d in $days.Keys) { $totalMs += [int64]$days[$d].study_time_ms }
$clockCount = $dateList.Count

function fmtMin([int64]$ms) {
  $min = $ms / 60000.0
  if ($min -lt 0.1) { return '{0} 秒' -f [math]::Round($ms / 1000.0) }
  return '{0:0.0} 分钟' -f $min
}
function fmtDuration([int64]$ms) {
  $min = $ms / 60000.0
  if ($min -lt 0.1) { return '{0} 秒' -f [math]::Round($ms / 1000.0) }
  $hh = [math]::Floor($min / 60.0)
  $mm = [math]::Round($min - $hh * 60)
  if ($hh -gt 0) { return '{0} 小时 {1} 分钟' -f $hh, $mm }
  return '{0:0.0} 分钟' -f $min
}

$todayMin = fmtMin $studyMs
$todayPct = if ($total -gt 0) { '{0:0.0}%' -f (100.0 * $finished / $total) } else { '—' }
$totalDuration = fmtDuration $totalMs

# 5) 渲染 note
$sb = New-Object System.Text.StringBuilder
function AddLine([string]$s) { [void]$sb.AppendLine($s) }

AddLine '---'
AddLine ("create: " + $data.create)
AddLine ("modify: " + $today)
AddLine 'tags: [英语, 打卡, 墨墨]'
AddLine '---'
AddLine ''
AddLine '> 返回目录：[[英语]]'
AddLine ''
AddLine '# 墨墨背单词 每日打卡'
AddLine ''
AddLine '> [!abstract]'
AddLine '> 考研英语词汇的每日打卡页（自动生成，无需手改）。数据来自墨墨开放 API 的「今日学习进度」；每天运行一次 `.scripts\maimemo-daily.ps1` 即更新今日进度。'
AddLine ''
AddLine '## 📅 今日进度'
AddLine ''
AddLine '| 项目 | 数值 |'
AddLine '| --- | --- |'
AddLine ("| 已学单词 | {0} / {1} |" -f $finished, $total)
AddLine ("| 学习时长 | {0} |" -f $todayMin)
AddLine ("| 完成率 | {0} |" -f $todayPct)
AddLine ("| 更新于 | {0} {1} |" -f $today, (Get-Date).ToString('HH:mm'))
AddLine ''
if ($total -gt 0 -and (100.0 * $finished / $total) -lt 60) { AddLine '> 今日完成率还不到 60%，加油哦 💪' }
AddLine ''
AddLine '## 🗓️ 历史记录'
AddLine ''
AddLine '| 日期 | 完成 | 计划 | 学习时长 | 完成率 |'
AddLine '| --- | --- | --- | --- | --- |'
foreach ($d in $dateList) {
  $e = $days[$d]
  $pct = if ($e.total -gt 0) { '{0:0.0}%' -f (100.0 * $e.finished / $e.total) } else { '—' }
  AddLine ("| {0} | {1} | {2} | {3} | {4} |" -f $d, $e.finished, $e.total, (fmtMin $e.study_time_ms), $pct)
}
AddLine ''
AddLine '## 📈 累计'
AddLine ''
AddLine ("- 打卡天数：{0} 天" -f $clockCount)
AddLine ("- 累计学习时长：{0}" -f $totalDuration)
AddLine ''

# 6) 写 note（UTF-8 无 BOM）
$dir = Split-Path $NotePath -Parent
if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
[System.IO.File]::WriteAllText($NotePath, $sb.ToString(), (New-Object System.Text.UTF8Encoding($false)))

# 7) 写数据
$djson = $data | ConvertTo-Json -Depth 8
[System.IO.File]::WriteAllText($DataFile, $djson, (New-Object System.Text.UTF8Encoding($false)))

Write-Host ("打卡页已更新: {0}" -f $NotePath)
Write-Host ("  今日 {0}/{1}  时长 {2}  完成率 {3}" -f $finished, $total, $todayMin, $todayPct)
Write-Host ("  累计 {0} 天  {1}" -f $clockCount, $totalDuration)
