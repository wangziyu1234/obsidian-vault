$ErrorActionPreference='Stop'
$taskRoot=[IO.Path]::GetFullPath('D:\obsidian')
$controlRoot=[IO.Path]::GetFullPath((Join-Path $taskRoot '控制理论'))
$destination=[IO.Path]::GetFullPath((Join-Path $controlRoot '附录'))
$sourceRoots=@('自动控制原理','现代控制理论') | ForEach-Object { [IO.Path]::GetFullPath((Join-Path $controlRoot $_)) }
$files=@($sourceRoots | ForEach-Object { Get-ChildItem -LiteralPath $_ -File -Filter '附录*.md' })
if($files.Count -ne 14){throw "Expected 14 appendix files, found $($files.Count)"}
$manifest=@()
foreach($file in $files){
    $source=[IO.Path]::GetFullPath($file.FullName)
    $target=[IO.Path]::GetFullPath((Join-Path $destination $file.Name))
    if($sourceRoots -notcontains [IO.Path]::GetDirectoryName($source)){throw "Unexpected source: $source"}
    if(-not $target.StartsWith($destination+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw "Out-of-scope target: $target"}
    if(Test-Path -LiteralPath $target){throw "Destination already exists: $target"}
    $manifest += [pscustomobject]@{source=$source;target=$target;sha256=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash}
}
if(@($manifest.target | Select-Object -Unique).Count -ne $files.Count){throw 'Duplicate destination names'}
[IO.File]::WriteAllText((Join-Path $taskRoot '.workbuddy\appendix-move-manifest-20261006.json'),($manifest | ConvertTo-Json -Depth 3),[Text.UTF8Encoding]::new($false))
if(-not(Test-Path -LiteralPath $destination)){New-Item -ItemType Directory -Path $destination | Out-Null}
foreach($entry in $manifest){
    Move-Item -LiteralPath $entry.source -Destination $entry.target
    if((Get-FileHash -LiteralPath $entry.target -Algorithm SHA256).Hash -ne $entry.sha256){throw "Hash mismatch: $($entry.target)"}
}
Write-Output "Moved $($manifest.Count) appendices into $destination; all content hashes preserved."
