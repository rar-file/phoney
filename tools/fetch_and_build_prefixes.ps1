# Downloads RIR delegated stats and builds per-country IPv4/IPv6 prefix files
# Usage (PowerShell):
#   ./tools/fetch_and_build_prefixes.ps1

param(
  [string]$PythonExe = "python"
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$tools = Join-Path $root "tools"
$dataDir = Join-Path $tools "data"
New-Item -ItemType Directory -Force -Path $dataDir | Out-Null

$files = @(
  @{ url = 'https://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-extended-latest'; out = 'delegated-apnic-extended-latest' },
  @{ url = 'https://ftp.arin.net/pub/stats/arin/delegated-arin-extended-latest'; out = 'delegated-arin-extended-latest' },
  @{ url = 'https://ftp.ripe.net/ripe/stats/delegated-ripencc-extended-latest'; out = 'delegated-ripencc-extended-latest' },
  @{ url = 'https://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-extended-latest'; out = 'delegated-lacnic-extended-latest' },
  @{ url = 'https://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-extended-latest'; out = 'delegated-afrinic-extended-latest' }
)

Write-Host "Downloading RIR delegated datasets to $dataDir ..."
foreach ($f in $files) {
  $dest = Join-Path $dataDir $f.out
  Invoke-WebRequest -Uri $f.url -OutFile $dest -UseBasicParsing
}

Write-Host "Building per-country IPv4/IPv6 prefixes ..."
& $PythonExe (Join-Path $tools 'build_prefixes.py')
Write-Host "Done. Files written under phoney/data/internet"
