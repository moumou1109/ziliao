[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Stop"
$dir = "E:\资料\论文抓取\_ref"
New-Item -ItemType Directory -Force -Path $dir | Out-Null
$url = "https://hz.xidian.edu.cn/info/1277/25374.htm"
$r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 30
$bytes = $r.RawContentStream.ToArray()
[System.IO.File]::WriteAllBytes("$dir\homepage.html", $bytes)
Write-Output ("bytes=" + $bytes.Length)
