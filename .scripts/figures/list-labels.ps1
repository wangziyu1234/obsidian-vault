<#
.SYNOPSIS
    列出插图源码里的文字节点与线段坐标，供人工核对"文字是否压在线上"。

.DESCRIPTION
    纯源码级检查，不做图像识别。输出两张表：
      [文字]  节点样式、坐标、内容
      [线段]  连线命令的起止坐标
    把两张表对着看，就能定位标签是否落在某条线的路径上。

    之所以不做自动判定：中文压线的图像检测试过三种判据（pdftotext 词盒、
    连通域聚类、形态学开运算）都不稳定——`pdftotext -bbox` 对中文直接返回
    "no word list"；压线时文字与线连通，连通域法必失败；开运算在 300 dpi 下
    会把笔画一并吃掉。人工对照源码反而更快更准。

.PARAMETER File
    一个或多个 .tex 源文件；缺省则扫描本目录。
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0, ValueFromPipeline = $true)]
    [string[]]$File
)

$ErrorActionPreference = 'Stop'
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$texs = if ($File) {
    $File | ForEach-Object { Get-Item -LiteralPath $_ }
} else {
    Get-ChildItem -LiteralPath $PSScriptRoot -Filter '*.tex' -File
}

foreach ($tex in $texs) {
    $lines = Get-Content -LiteralPath $tex.FullName -Encoding UTF8
    Write-Host ''
    Write-Host "===== $($tex.Name) =====" -ForegroundColor Cyan

    Write-Host '--- 文字节点 ---' -ForegroundColor DarkGray
    $i = 0
    foreach ($ln in $lines) {
        $i++
        $m = [regex]::Matches($ln, '\\node\s*\[([^\]]*)\]\s*\(?[^)]*\)?\s*(?:\[\w+\])?\s*at\s*\(([^)]*)\)\s*\{([^}]*)\}')
        foreach ($mm in $m) {
            $style = ($mm.Groups[1].Value -split ',')[0].Trim()
            $coord = $mm.Groups[2].Value.Trim()
            $text = $mm.Groups[3].Value.Trim()
            Write-Host ("  L{0,-4} [{1,-10}] ({2,-16}) {3}" -f $i, $style, $coord, $text)
        }
    }

    Write-Host '--- 线段 ---' -ForegroundColor DarkGray
    $i = 0
    foreach ($ln in $lines) {
        $i++
        if ($ln -match '\\draw' -and $ln -match '\(') {
            $coords = [regex]::Matches($ln, '\(([-\d\.]+)\s*,\s*([-\d\.]+)\)')
            if ($coords.Count -ge 2) {
                $pts = ($coords | ForEach-Object { "($($_.Groups[1].Value),$($_.Groups[2].Value))" }) -join ' -> '
                $tag = if ($ln -match '\-\>') { '箭头' } else { '线段' }
                Write-Host ("  L{0,-4} {1} {2}" -f $i, $tag, $pts)
            }
        }
    }
}
