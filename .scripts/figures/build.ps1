<#
.SYNOPSIS
    笔记插图构建：源码 → 附件 PNG。

.DESCRIPTION
    两种源码：
      *.tex  用 xelatex 编译成 PDF，再用 pdftocairo 以指定 DPI 栅格化（透明底）。
      *.py   直接运行；脚本自己负责写 PNG（用 figures_style.py 统一风格）。

    输出统一落到 <仓库根>\附件\<同名>.png，因此文件名必须与笔记内的
    ![[...png]] 引用一致——构建脚本不改名、不猜名。

.PARAMETER File
    要构建的源文件（可多个，或管道传入）。

.PARAMETER Dir
    构建该目录下所有 .tex/.py。

.PARAMETER All
    构建本目录（.scripts\figures）下所有源码。

.PARAMETER Dpi
    tex 栅格化分辨率，默认 600（够清晰又不会过大）。

.PARAMETER NoPdf
    只想看 PDF 时用：跳过栅格化。

.EXAMPLE
    .\build.ps1 -File .\circuit-RC.tex
.EXAMPLE
    .\build.ps1 -All -Dpi 600
#>
[CmdletBinding(DefaultParameterSetName = 'File')]
param(
    [Parameter(ParameterSetName = 'File', Position = 0, ValueFromPipeline = $true)]
    [string[]]$File,

    [Parameter(ParameterSetName = 'Dir', Mandatory = $true)]
    [string]$Dir,

    [Parameter(ParameterSetName = 'All', Mandatory = $true)]
    [switch]$All,

    [int]$Dpi = 600,

    [switch]$NoPdf
)

$ErrorActionPreference = 'Stop'
# 中文路径/文件名要能正确回显（否则这里会输出乱码）
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ScriptRoot = $PSScriptRoot
$RepoRoot = Split-Path (Split-Path $ScriptRoot -Parent) -Parent
$OutDir = Join-Path $RepoRoot '附件'
if (-not (Test-Path -LiteralPath $OutDir)) { throw "找不到附件目录：$OutDir" }

function Get-Sources {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { throw "源文件不存在：$Path" }
    if ((Get-Item -LiteralPath $Path) -is [System.IO.DirectoryInfo]) {
        Get-ChildItem -LiteralPath $Path -File | Where-Object { $_.Extension -in '.tex', '.py' }
    }
    else { Get-Item -LiteralPath $Path }
}

$sources = @()
switch ($PSCmdlet.ParameterSetName) {
    'File' { if ($File) { $sources = $File | ForEach-Object { Get-Sources $_ } } }
    'Dir' { $sources = Get-Sources $Dir }
    'All' { $sources = Get-Sources $ScriptRoot }
}
$sources = $sources |
    Where-Object { $_.Extension -in '.tex', '.py' } |
    Where-Object { $_.BaseName -notlike '_*' -and $_.BaseName -ne 'figures_style' } |
    Sort-Object Name
if (-not $sources) { Write-Host '没有可构建的 .tex / .py'; exit 0 }

<#
    输出命名：源码首行的 `figure: <名字>.png` 决定附件文件名，从而沿用
    仓库的中文命名规范（自控-xxx.png / 频域-xxx.png …）而不必用中文源码名。
    没有该行时退化为源码同名 .png。
#>
function Get-FigureName {
    param([System.IO.FileInfo]$Src)
    $first = Get-Content -LiteralPath $Src.FullName -TotalCount 5 -Encoding UTF8
    foreach ($line in $first) {
        if ($line -match '^\s*(?:%|#)\s*figure:\s*(\S+\.png)\s*$') { return $Matches[1] }
    }
    return ([System.IO.Path]::GetFileNameWithoutExtension($Src.Name) + '.png')
}

$results = @()
foreach ($src in $sources) {
    $png = Join-Path $OutDir (Get-FigureName $src)
    $base = [System.IO.Path]::GetFileNameWithoutExtension($src.Name)
    Write-Host ''
    Write-Host "==> $($src.Name)  ->  附件\$([System.IO.Path]::GetFileName($png))" -ForegroundColor Cyan

    if ($src.Extension -eq '.py') {
        $env:FIGURE_OUT = $png
        $env:PYTHONIOENCODING = 'utf-8'      # 否则脚本里的中文路径打印成乱码
        & python $src.FullName
        if ($LASTEXITCODE -ne 0) { throw "python 构建失败：$($src.Name)" }
        $results += [pscustomobject]@{ Source = $src.Name; Output = $png; Ok = (Test-Path -LiteralPath $png) }
        continue
    }

    # --- .tex：先编译，再栅格化 ---
    $pdf = Join-Path $src.DirectoryName "$base.pdf"
    Push-Location $src.DirectoryName
    try {
        $texArgs = @('-interaction=nonstopmode', '-halt-on-error', '-file-line-error', $src.Name)
        $log = & xelatex @texArgs 2>&1
        if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $pdf)) {
            $log | Select-Object -Last 30 | Write-Host
            throw "xelatex 编译失败：$($src.Name)"
        }
        # 只保留值得看的字体/警告提示
        $log | Select-String -Pattern 'LaTeX Warning|Overfull|Underfull' |
            Select-Object -First 5 | ForEach-Object { Write-Host "    $($_.Line.Trim())" -ForegroundColor DarkYellow }

        if (-not $NoPdf) {
            Get-ChildItem -LiteralPath $src.DirectoryName -Filter "$base.*" -File |
                Where-Object { $_.Extension -in '.aux', '.log', '.out', '.fls', '.fdb_latexmk' } |
                Remove-Item -Force
            # pdftocairo 在 Windows 上打不开非 ASCII 输出路径，先渲到 ASCII 临时名再改名；
            # 注意它会给输出名追加 .png，所以临时前缀不能自带扩展名。
            $tmpStem = Join-Path $env:TEMP "dsh-figure-$base"
            $tmpPng  = "$tmpStem.png"
            if (Test-Path -LiteralPath $tmpPng) { Remove-Item -LiteralPath $tmpPng -Force }
            & pdftocairo -png -r $Dpi -singlefile $pdf $tmpStem
            if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $tmpPng)) {
                throw "pdftocairo 栅格化失败：$($src.Name)"
            }
            Move-Item -LiteralPath $tmpPng -Destination $png -Force
        }
    }
    finally { Pop-Location }

    if (Test-Path -LiteralPath $png) {
        $item = Get-Item -LiteralPath $png
        Write-Host ("    附件\{0}  {1:N0} KB" -f $item.Name, ($item.Length / 1KB)) -ForegroundColor DarkGray
        $results += [pscustomobject]@{ Source = $src.Name; Output = $png; Ok = $true }
    }
}

Write-Host ''
Write-Host "===== 构建完成：$($results.Count) 个 =====" -ForegroundColor Green
Write-Host ''
Write-Host '注意：生成后请在笔记里核对图片尺寸参数（正文 |430，速查/宽图 |520）。' -ForegroundColor DarkGray
