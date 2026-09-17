<#
.SYNOPSIS
    修复云同步冲突改名造成的附件断链（xxx_1789228415866.png → xxx.png）。

.DESCRIPTION
    Remotely Save 双向同步在「两侧都改过同一文件」时，会把本地那份改名成
    <原名>_<epoch毫秒>.<扩展名>，原文件名随即消失，笔记里的 ![[原名.png]] 当场断链。
    2026-09-12 / 09-13 / 09-15 / 09-17 已复发四次。

    本脚本把带冲突后缀的附件改回原名（内容不动）。若原名文件已存在：
      - 两份内容相同  → 删掉多余副本
      - 两份内容不同  → 保留内容修改时间较新的那份，旧的一份移入 .trash
    默认只列出将要执行的动作，加 -Apply 才真正落盘。

.PARAMETER Root
    仓库根目录（默认本脚本上两级）。

.PARAMETER Apply
    真正执行改名/移入回收站。不加则只输出计划。

.PARAMETER KeepTrash
    两份并存且内容不同时，把丢弃的那份移入 .trash\<日期>\ 而不是直接删除（默认即如此）。

.EXAMPLE
    .\.scripts\fix-attachment-conflicts.ps1          # 只看计划
.EXAMPLE
    .\.scripts\fix-attachment-conflicts.ps1 -Apply   # 执行修复
#>
[CmdletBinding()]
param(
    [string]$Root = (Split-Path $PSScriptRoot -Parent),
    [switch]$Apply
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$AttRoot = Join-Path $Root '附件'
if (-not (Test-Path -LiteralPath $AttRoot)) { throw "找不到附件目录：$AttRoot" }

$conflictPattern = '_\d{10,}$'          # 13 位 epoch 毫秒；放宽到 10 位以上
$suffixed = @(Get-ChildItem -LiteralPath $AttRoot -File -Recurse |
    Where-Object { $_.BaseName -match $conflictPattern })

if ($suffixed.Count -eq 0) {
    Write-Host '✔ 没有带同步冲突后缀的附件，无需修复。' -ForegroundColor Green
    exit 0
}

function Get-FileHashSafe([string]$Path) {
    try { return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash }
    catch { return $null }
}

$plan = New-Object System.Collections.Generic.List[object]
foreach ($f in $suffixed) {
    $origName  = ($f.BaseName -replace $conflictPattern, '') + $f.Extension
    $origPath  = Join-Path $f.DirectoryName $origName
    $origExists = Test-Path -LiteralPath $origPath

    # 只用「路径 + 动作」描述计划，落盘时再按路径操作，避免捏着已失效的 FileInfo
    $action   = ''
    $keepPath = $null       # 最终占用“原名”的那份
    $dropPath = $null       # 被丢弃的那份（移入 .trash；相同内容的直接不留）

    if (-not $origExists) {
        $action   = '改名回原名'
        $keepPath = $f.FullName
    } else {
        $h1 = Get-FileHashSafe $f.FullName
        $h2 = Get-FileHashSafe $origPath
        if ($h1 -and $h1 -eq $h2) {
            $action   = '内容相同，删副本'
            $keepPath = $origPath
            $dropPath = $f.FullName
        } else {
            $a = (Get-Item -LiteralPath $f.FullName).LastWriteTime
            $b = (Get-Item -LiteralPath $origPath).LastWriteTime
            if ($a -ge $b) { $keepPath = $f.FullName;    $dropPath = $origPath }
            else           { $keepPath = $origPath;      $dropPath = $f.FullName }
            $action = '内容不同，保留较新的一份，另一份入 .trash'
        }
    }

    $plan.Add([pscustomobject]@{
        ConflictName = $f.Name
        OrigName     = $origName
        OrigPath     = $origPath
        Action       = $action
        KeepPath     = $keepPath
        DropPath     = $dropPath
    })
}

Write-Host ''
Write-Host ("发现 {0} 个带冲突后缀的附件：" -f $plan.Count) -ForegroundColor Cyan
foreach ($p in $plan) {
    Write-Host ("  - {0}" -f $p.ConflictName)
    Write-Host ("      → {0}   [{1}]" -f $p.OrigName, $p.Action) -ForegroundColor DarkGray
}

if (-not $Apply) {
    Write-Host ''
    Write-Host '以上为预览。加 -Apply 执行修复。' -ForegroundColor Yellow
    exit 0
}

$trashDir = Join-Path $Root ('.trash\附件冲突修复-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
function Move-ToTrash([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { return }
    if (-not (Test-Path -LiteralPath $trashDir)) { New-Item -ItemType Directory -Path $trashDir -Force | Out-Null }
    $dest = Join-Path $trashDir (Split-Path $Path -Leaf)
    Move-Item -LiteralPath $Path -Destination $dest -Force
}

foreach ($p in $plan) {
    # 1) 先把要保持的那份挪到「原名」位置；原名位置若已被别人占着，先妥善处理掉
    if ($p.KeepPath -ne $p.OrigPath) {
        if (Test-Path -LiteralPath $p.OrigPath) {
            if ($p.DropPath -eq $p.OrigPath) {
                # 原名叫那份正是被淘汰的那份：移入 .trash，然后清空 drop 免得再动一次
                Move-ToTrash $p.OrigPath
                $p.DropPath = $null
            } else {
                Remove-Item -LiteralPath $p.OrigPath -Force
            }
        }
        Move-Item -LiteralPath $p.KeepPath -Destination $p.OrigPath -Force
    }
    # 2) 淘汰的那份（若还没处理过）移入 .trash
    if ($p.DropPath -and (Test-Path -LiteralPath $p.DropPath)) { Move-ToTrash $p.DropPath }
    Write-Host ("  ✔ {0}" -f $p.OrigName) -ForegroundColor Green
}

Write-Host ''
Write-Host ("修复完成：{0} 个附件已恢复原名。" -f $plan.Count) -ForegroundColor Green
if (Test-Path -LiteralPath $trashDir) {
    Write-Host ("冗余副本已移入：{0}" -f $trashDir) -ForegroundColor DarkGray
}
Write-Host '建议随后跑 .\.scripts\check-notes.ps1 复核断链是否归零。' -ForegroundColor DarkGray
exit 0
