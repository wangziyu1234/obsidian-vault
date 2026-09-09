<#
.SYNOPSIS
  对标 AGENTS.md 检查清单的全库笔记校验脚本。

.DESCRIPTION
  默认扫描整个 Obsidian 库（当前工作目录或其 -Root），跳过 .obsidian/、.venv/、
  .trash/、_moved_out/、copilot/、templates/、Excalidraw/ 与 AGENTS.md 自身，逐 .md 检查：

   1. 断链   ：所有 [[...]] / ![[...]] 目标必须命中（basename/短路径；表格内 \| 转义
                先拆目标；[[#锚点]] 与 [[#锚点|别名]] 为页内锚点，不查目标）
   2. LaTeX  ：$$ 成对、单 $ 成对、\begin/\end 配对、\left/\right 配对
               （剔除 \leftrightarrow）
   3. 编号   ：目录内 ## X.Y 小节号无重复；无 TODO/FIXME/待补/??；无空链接
   4. 结构   ：唯一 H1；abstract 在 H1 后（索引/入口文件用 > 定位 豁免）；
               附录 无 H3（附录 图像变换 为已知豁免）；>250 行提示拆分（完整单题豁免）

  豁免（AGENTS 已知，不误报）：
   - 05 第5章 表格内 ![[…png\|220]] 转义；\leftrightarrow
   - copilot prompts / Excalidraw 绘图 / 模板 / AGENTS.md 自身
   - 附录 图像变换 的 H3
   - frontmatter 标记 single-exercise: true 的完整单题仅豁免篇幅告警

.PARAMETER Root  扫描根目录（默认当前目录）
.PARAMETER File  只查单文件（相对/绝对路径）
.PARAMETER Dir   只查某目录（相对/绝对路径）
.EXAMPLE
  .\check-notes.ps1
  .\check-notes.ps1 -Dir 数学
  .\check-notes.ps1 -File "数学\高等数学\11 第11讲….md"
#>
param(
  [string]$Root = (Get-Location).Path,
  [string]$File,
  [string]$Dir
)

$ErrorActionPreference = 'Stop'

# --------------------------------------------------------------------------
# 输入
# --------------------------------------------------------------------------
$CheckDir = $Root
$singleFile = $null
if ($File) {
  $singleFile = [System.IO.Path]::GetFullPath($File)
  if (-not (Test-Path -LiteralPath $singleFile -PathType Leaf)) { Write-Host "文件不存在: $singleFile" -ForegroundColor Yellow; exit 1 }
  $CheckDir = Split-Path $singleFile -Parent
} elseif ($Dir) {
  $CheckDir = [System.IO.Path]::GetFullPath($Dir)
  if (-not (Test-Path -LiteralPath $CheckDir -PathType Container)) { Write-Host "目录不存在: $CheckDir" -ForegroundColor Yellow; exit 1 }
}

# 排除路径片段
$excludeSeg = @('\.obsidian\', '\.venv\', '\.trash\', '_moved_out\', '\copilot\', '\templates\', '\Excalidraw\', '\scripts\', '\教材OCR\')
function Is-Excluded([string]$p) {
  foreach ($s in $excludeSeg) { if ($p -match [regex]::Escape($s)) { return $true } }
  if ($p -match '\\AGENTS\.md$') { return $true }
  if ($p -match '\\README\.md$') { return $true }
  return $false
}

# 全库 .md basename 集合（断链解析用）；Excalidraw 绘图不计入笔记
$allMd = Get-ChildItem -Path $Root -Recurse -Filter '*.md' -File -ErrorAction SilentlyContinue |
  Where-Object { -not (Is-Excluded $_.FullName) -and -not $_.Name.EndsWith('.excalidraw.md') }
$allNames = @{}
foreach ($m in $allMd) { $allNames[$m.BaseName] = $true }
# README 免于正文审校，但仍是总目录返回链接的合法目标。
if (Test-Path -LiteralPath (Join-Path $Root 'README.md') -PathType Leaf) { $allNames['README'] = $true }

# 索引/入口文件：用 > 定位 而非 abstract，豁免 abstract 检查
$indexBase = @('高等数学公式速查', '数学', '自动控制原理', '英语')

$files = @()
if ($singleFile) {
  if (-not (Is-Excluded $singleFile)) { $files += $singleFile } else { Write-Host "跳过（豁免/排除）：$singleFile" -ForegroundColor DarkGray; exit 0 }
} else {
  $files = @(Get-ChildItem -Path $CheckDir -Recurse -Filter '*.md' -File -ErrorAction SilentlyContinue |
    Where-Object { -not (Is-Excluded $_.FullName) -and -not $_.Name.EndsWith('.excalidraw.md') } |
    ForEach-Object { $_.FullName })
}
if ($files.Count -eq 0) { Write-Host "没有可检查的 .md 文件。"; exit 0 }

# --------------------------------------------------------------------------
$errors   = New-Object System.Collections.Generic.List[string]   # 致命
$warnings = New-Object System.Collections.Generic.List[string]   # 可修复
$infos    = New-Object System.Collections.Generic.List[string]   # 提示/豁免复核

function Split-WikiTarget([string]$raw) {
  $target = ($raw -split '\|')[0]
  $target = $target -replace '\\$', ''
  if ($target.Contains('#')) { $target = ($target -split '#')[0] }
  return $target.Trim()
}

function Test-OneFile([string]$path) {
  $rel = $path.Substring($Root.Length).TrimStart('\', '/')
  $lines = Get-Content -LiteralPath $path -Encoding UTF8
  $text   = $lines -join "`n"
  $nLines = $lines.Count
  $base   = [System.IO.Path]::GetFileNameWithoutExtension($path)
  $isAppendix = $base -match '^附录'
  $secNums = New-Object System.Collections.Generic.List[string]
  $hasH1LineNo = -1

  # ---- H1 ----
  $h1s = @($lines | Where-Object { $_ -match '^# ' })
  if ($h1s.Count -ne 1) { $errors.Add("[$rel] H1 数量 = $($h1s.Count)（应为 1）") }
  for ($k=0;$k -lt $lines.Count;$k++){ if ($lines[$k] -match '^#\s'){ $hasH1LineNo=$k; break } }

  # ---- abstract ----
  if ($hasH1LineNo -ge 0 -and $base -notin $indexBase -and $rel -notmatch '\\(?!.*\\)\d+\s|\\[0-9-]') {
    $abs = $false
    for ($k=$hasH1LineNo+1;$k -lt $lines.Count;$k++){
      if ($lines[$k] -match '> \[!abstract\]'){ $abs=$true; break }
      if ($lines[$k] -match '^##\s'){ break }
    }
    if (-not $abs){ $warnings.Add("[$rel] abstract 未在 H1 后；请核对是否缺失或位于 ## 之后") }
  }

  # ---- 附录 H3 ----
  if ($isAppendix -and $base -ne '附录 图像变换') {
    if ($text -match '(?m)^### ') { $errors.Add("[$rel] 附录含 H3（附录统一不用 ## 以下）") }
  }

  # ---- 超长：完整单题只豁免篇幅，其他检查照常执行 ----
  if ($nLines -gt 250) {
    $isSingleExercise = $false
    # 逐行读取已闭合的 frontmatter；兼容 LF/CRLF，不接受正文中的同名标记。
    if ($lines[0].Trim() -eq '---') {
      $markedSingleExercise = $false
      for ($lineNo = 1; $lineNo -lt $nLines; $lineNo++) {
        $frontmatterLine = $lines[$lineNo].Trim()
        if ($frontmatterLine -eq '---') {
          $isSingleExercise = $markedSingleExercise
          break
        }
        if ($frontmatterLine -match '^single-exercise:\s*(true|false)\s*(?:#.*)?$') {
          $markedSingleExercise = $Matches[1] -eq 'true'
        }
      }
    }
    if ($isSingleExercise) {
      $infos.Add("[$rel] 共 $nLines 行（完整单题，豁免篇幅拆分）")
    } else {
      $warnings.Add("[$rel] 共 $nLines 行（>250，建议按拆分约定处理）")
    }
  }

  # ---- 占位符 ----
  if ($text -match 'TODO|FIXME|待补|待完善') { $warnings.Add("[$rel] 含 TODO/FIXME/待补 占位符") }

  # ---- LaTeX ----
  $dd = [regex]::Matches($text,'\$\$').Count
  if ($dd % 2 -ne 0){ $errors.Add("[$rel] LaTeX：\$\$ = $dd 为奇数（不成对）") }
  $sc = 0; $i=0
  while($i -lt $text.Length){
    if($text[$i] -eq '$'){
      if($i+1 -lt $text.Length -and $text[$i+1] -eq '$'){ $i+=2 } else { $sc++; $i++ }
    } else { $i++ }
  }
  if($sc % 2 -ne 0){ $errors.Add("[$rel] LaTeX：单 \$ = $sc 为奇数（\$\$ 误用或单 \$ 缺失闭合）") }
  $left  = [regex]::Matches($text,'\\left(?![A-Za-z])').Count
  $right = [regex]::Matches($text,'\\right(?![A-Za-z])').Count
  if($left -ne $right){ $errors.Add("[$rel] LaTeX：\left=$left vs \right=$right 不配对") }
  $b=[regex]::Matches($text,'\\begin\{').Count; $e=[regex]::Matches($text,'\\end\{').Count
  if($b -ne $e){ $errors.Add("[$rel] LaTeX：\begin\{=$b vs \end\{=$e 不配对") }

  # ---- 链接 ----
  for ($ln=0;$ln -lt $lines.Count;$ln++){
    foreach($m in [regex]::Matches($lines[$ln],'!?\[\[([^\]]+)\]\]')){
      $raw = $m.Groups[1].Value
      if ($raw -match '^#') { continue }            # 页内锚点 [[#...]]
      $tgt = Split-WikiTarget $raw
      if ($tgt -eq '') { $warnings.Add("[$rel] L$($ln+1)：空链接 [[]]"); continue }
      if ($tgt -match '\.\w+$') {
        $ib=[System.IO.Path]::GetFileNameWithoutExtension($tgt); $ie=[System.IO.Path]::GetExtension($tgt)
        $hit=Get-ChildItem -Path $Root -Recurse -File -Filter "*$ib$ie" -ErrorAction SilentlyContinue |
          Where-Object { -not (Is-Excluded $_.FullName) } | Select-Object -First 1
        if(-not $hit){ $errors.Add("[$rel] L$($ln+1)：图片 ${tgt} 未找到") }
      } else {
        $leaf=($tgt -split '/')[-1]
        if(-not $allNames.ContainsKey($leaf)){ $errors.Add("[$rel] L$($ln+1)：wikilink [[$tgt]] 目标未命中") }
      }
    }
  }

  # ---- ## X.Y 编号（返回给目录去重）----
  foreach($l in $lines){ if($l -match '^##\s+(?:[^\d\s]+\s+)?(\d+\.\d+)\s'){ $secNums.Add($Matches[1]) } }
  return ,$secNums
}

# --------------------------------------------------------------------------
$secByDir=@{}
foreach($f in $files){
  $secs=Test-OneFile $f
  $rel=$f.Substring($Root.Length).TrimStart('\','/')
  $d=Split-Path $rel -Parent
  if(-not $secByDir.ContainsKey($d)){ $secByDir[$d]=New-Object System.Collections.Generic.List[string] }
  foreach($s in $secs){ $secByDir[$d].Add("$rel :: $s") }
}
foreach($d in @($secByDir.Keys)){
  $seen=@{}
  foreach($en in $secByDir[$d]){
    if($en -match ':: (\d+(?:\.\d+)?)\s*$'){
      $num=$Matches[1]; $fr=($en -split ' :: ')[0]
      if($seen.ContainsKey($num)){ $errors.Add("[编号] 目录 $d 内小节号 $num 重复：$fr 与 $($seen[$num])") }
      else { $seen[$num]=$fr }
    }
  }
}

# --------------------------------------------------------------------------
Write-Host ""; Write-Host "===== 笔记检查完成 =====" -ForegroundColor Cyan
Write-Host ("扫描文件数：{0}" -f $files.Count) -ForegroundColor Cyan
$code=0
if($errors.Count -gt 0){
  $code=1; Write-Host ("【致命】{0} 处：" -f $errors.Count) -ForegroundColor Red
  foreach($x in $errors){ Write-Host "  - $x" -ForegroundColor Red }
} else { Write-Host "✔ 致命问题：0 处" -ForegroundColor Green }
if($warnings.Count -gt 0){
  Write-Host ("【待修】{0} 处：" -f $warnings.Count) -ForegroundColor Yellow
  foreach($x in $warnings){ Write-Host "  - $x" -ForegroundColor Yellow }
} else { Write-Host "✔ 待修项：0 处" -ForegroundColor Green }
if($infos.Count -gt 0){
  Write-Host ("【提示】{0} 处：" -f $infos.Count) -ForegroundColor DarkGray
  foreach($x in $infos){ Write-Host "  - $x" -ForegroundColor DarkGray }
}
Write-Host ""
if($code -eq 0){ Write-Host "✔ 全部通过。" -ForegroundColor Green }
exit $code
