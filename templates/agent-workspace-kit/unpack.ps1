# Unpack agent-workspace-kit into a target project root.
param(
  [Parameter(Mandatory = $true)]
  [string]$Destination
)
$ErrorActionPreference = "Stop"
$kit = $PSScriptRoot
$dest = (Resolve-Path -LiteralPath $Destination -ErrorAction SilentlyContinue)
if (-not $dest) {
  New-Item -ItemType Directory -Force -Path $Destination | Out-Null
  $dest = Resolve-Path -LiteralPath $Destination
}
$dest = $dest.Path

New-Item -ItemType Directory -Force "$dest\agents" | Out-Null
New-Item -ItemType Directory -Force "$dest\.cursor\rules" | Out-Null

Copy-Item "$kit\AGENTS.md","$kit\CLAUDE.md","$kit\.claudeignore","$kit\.cursorignore" $dest -Force
Copy-Item "$kit\agents\*" "$dest\agents\" -Force
Copy-Item "$kit\.cursor\rules\*" "$dest\.cursor\rules\" -Force

Write-Host "Unpacked agent-workspace-kit -> $dest"
Write-Host "Next: edit agents/README.md, rename agents/domain.md, fill AGENTS.md paths."
