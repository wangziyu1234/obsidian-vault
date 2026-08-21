# 给无尺寸图片引用补尺寸：宽图(宽高比>=2) |520，其余 |430
$dir = 'D:\obsidian\自动控制原理'
$jobs = @(
  @{F='00 拉普拉斯变换（数学基础）.md'; Items=@('拉氏变换-常见信号.png|430','拉氏变换-极点与响应.png|430')},
  @{F='03-1 一阶与二阶系统的时域响应.md'; Items=@('时域-性能指标.png|430','时域-二阶阻尼族.png|430')},
  @{F='04 第4章 线性系统的根轨迹法.md'; Items=@('根轨迹-三阶示例.png|430','根轨迹-常见形状.png|430','根轨迹-等zeta射线.png|430')},
  @{F='05-1 频率特性与典型环节伯德图.md'; Items=@('频域-振荡环节Bode.png|430','频域-Bode绘制示例.png|430')},
  @{F='05-2 奈氏判据与稳定裕度.md'; Items=@('频域-奈氏判稳补弧.png|520','频域-稳定裕度.png|430')},
  @{F='06-1 串联校正（超前·滞后·滞后-超前）.md'; Items=@('校正-ABCD图解.png|430','校正-超前滞后特性.png|430','校正-期望特性abcd.png|430')},
  @{F='07-1 采样与z变换.md'; Items=@('离散-采样与保持.png|520')},
  @{F='07-2 差分方程与系统稳定性.md'; Items=@('离散-z平面映射.png|520')},
  @{F='08 第8章 非线性控制系统分析.md'; Items=@('非线性-典型特性.png|430','非线性-相平面奇点.png|430','非线性-相平面例8-2.png|430','非线性-描述函数判稳.png|520')}
)
$count=0
foreach($job in $jobs){
  $p = Join-Path $dir $job.F
  if(-not (Test-Path -LiteralPath $p)){ Write-Host "!! 无此文件: $($job.F)"; continue }
  $lines = Get-Content -LiteralPath $p
  foreach($it in $job.Items){
    $parts = $it.Split('|')
    $img = $parts[0]; $size = $parts[1]
    $pattern = "!\[\[$([regex]::Escape($img))\]\]"
    $repl = "![[$img|$size]]"
    for($i=0;$i -lt $lines.Count;$i++){
      if($lines[$i] -match $pattern){
        $lines[$i] = $lines[$i] -replace $pattern, ($repl -replace '\$','$$$$')
        $count++
      }
    }
  }
  [System.IO.File]::WriteAllLines($p, $lines, (New-Object System.Text.UTF8Encoding($false)))
}
Write-Host "已补充尺寸: $count 处"