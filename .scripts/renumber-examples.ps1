<#
.SYNOPSIS
    第5章例题统一编号的重排工具（常驻）。

.DESCRIPTION
    例题编号规则见 控制理论\自动控制原理\05 第5章 线性系统的频域分析法.md §⑤：
    全章用章内连续号 例5.N，标题写 `例5.N（教材例5-x）` 或 `例5.N〔来源〕`。

    平时新增例题只需：末尾加号 / 中间用小数细分号（例5.9.1）。
    只有当同一位置插到第 4 道、小数号堆到三层时，才跑这个脚本做一次整章重排。

    用法（两步，先看再改）：
        # 1) 只检查：列出当前编号、重复、缺号
        .\renumber-examples.ps1 -Dir "控制理论\自动控制原理"

        # 2) 重排：把旧号按 -Map 映射成新号（整章一次改完）
        .\renumber-examples.ps1 -Dir "控制理论\自动控制原理" -Map "10=11,11=12,9.1=10" -Apply

    -Map 的键是旧号、值是目标号（都写 "例5." 之后的部分）；只改带 `例5.` 的标题行
    与正文里的 `例5.x` 引用，教材号 `例5-12` 不受影响。

.PARAMETER Dir
    要处理的自控笔记目录（默认 控制理论\自动控制原理）。

.PARAMETER Map
    逗号分隔的 旧号=新号 列表。

.PARAMETER Apply
    真正写回文件；不给就只报告。
#>
[CmdletBinding()]
param(
    [string]$Dir = '控制理论\自动控制原理',
    [string]$Map = '',
    [switch]$Apply
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$repo = Split-Path $PSScriptRoot -Parent
$target = Join-Path $repo $Dir
if (-not (Test-Path -LiteralPath $target)) { throw "目录不存在：$target" }

$files = Get-ChildItem -LiteralPath $target -Filter '05*.md' -File |
    Where-Object { $_.Name -ne '05 第5章 线性系统的频域分析法.md' }

$patHeading = [regex]'例\s?5\.(\d+(?:\.\d+)*)'
$rows = @()
foreach ($f in $files) {
    $lines = Get-Content -LiteralPath $f.FullName -Encoding UTF8
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        # 只认"例题标题"：`#### ✏️ 例5.x` 或 `## 图标 5.3.2.N 例5.x`、`## ✏️ 例5.x`；
        # H1 里的 `第5章（一-1·例5.2）` 只是篇名标注，不算第二个标题。
        $isExampleHeading = ($line -match '^#{3,4}\s') -or
                            ($line -match '^##\s' -and $line -match '例\s?5\.')
        if ($isExampleHeading -and $patHeading.IsMatch($line)) {
            $num = $patHeading.Match($line).Groups[1].Value
            $rows += [pscustomobject]@{ Num = $num; File = $f.Name; Line = $i + 1
                                        Text = $line.Trim() }
        }
    }
}

Write-Host "== 当前编号 ==" -ForegroundColor Cyan
$rows | Sort-Object { [double]$_.Num } | ForEach-Object {
    Write-Host ("  例5.{0,-6} {1,-42} {2}" -f $_.Num, $_.File, $_.Text.Substring(0, [Math]::Min(30, $_.Text.Length)))
}
$dupes = $rows | Group-Object Num | Where-Object Count -gt 1
Write-Host ""
Write-Host ("重复：{0}" -f $(if ($dupes) { ($dupes.Name -join ', ') } else { '无' })) -ForegroundColor $(if ($dupes) { 'Red' } else { 'Green' })

if (-not $Map) {
    Write-Host "未给 -Map，只做检查。要重排请加 -Map `"旧=新,...`" [-Apply]" -ForegroundColor DarkGray
    return
}

$pairs = @{}
foreach ($item in $Map.Split(',')) {
    $kv = $item.Trim() -split '='
    if ($kv.Count -ne 2) { throw "无法解析映射项：$item" }
    $pairs[$kv[0].Trim()] = $kv[1].Trim()
}

# 先长后短替换，避免 "5.1" 命中 "5.10" 的前缀
$ordered = $pairs.Keys | Sort-Object { $_.Length } -Descending
$changed = 0
foreach ($f in $files) {
    $text = Get-Content -LiteralPath $f.FullName -Encoding UTF8 -Raw
    $new = $text
    foreach ($old in $ordered) {
        $new = $new -replace ("例\s?5\." + [regex]::Escape($old) + "(?!\d)"), ("例5." + $pairs[$old])
    }
    if ($new -ne $text) {
        $changed++
        if ($Apply) {
            # 写回时统一无 BOM、保留原有行尾风格
            [System.IO.File]::WriteAllText($f.FullName, $new,
                (New-Object System.Text.UTF8Encoding($false)))
            Write-Host "  改写 $($f.Name)" -ForegroundColor Yellow
        } else {
            $diff = (Compare-Object ($text -split "`n") ($new -split "`n") |
                     Where-Object SideIndicator -eq '=>').Count
            Write-Host ("  待改 {0}（{1} 行）" -f $f.Name, $diff) -ForegroundColor DarkYellow
        }
    }
}
Write-Host ""
if ($Apply) {
    Write-Host "已改 $changed 个文件。别忘了同步索引页 §⑤ 的例题总表与其中的映射说明。" -ForegroundColor Green
} else {
    Write-Host "预览：$changed 个文件将被改；确认后加 -Apply。" -ForegroundColor Green
}
