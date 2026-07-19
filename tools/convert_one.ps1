# One-off or batch science hybrid conversion (MarkItDown + page PNGs).
# Usage:
#   .\tools\convert_one.ps1
#   .\tools\convert_one.ps1 -Force
#   .\tools\convert_one.ps1 -SkipMisc
#   .\tools\convert_one.ps1 -Limit 2
#   .\tools\convert_one.ps1 -Subjects "H2 math"

param(
    [string]$Subjects = "H2 math,H2 physics,H2 computing",
    [int]$Dpi = 150,
    [int]$Limit = 0,
    [switch]$Force,
    [switch]$SkipMisc,
    [switch]$SetupOnly
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$VenvDir = Join-Path $RepoRoot ".venv-convert"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$Req = Join-Path $PSScriptRoot "requirements-convert.txt"
$Script = Join-Path $PSScriptRoot "convert_science_package.py"

function Resolve-Python310Plus {
    # Prefer py launcher versions >= 3.10 (MarkItDown requirement)
    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($py) {
        foreach ($ver in @("3.14", "3.13", "3.12", "3.11", "3.10")) {
            try {
                $path = & py "-$ver" -c "import sys; print(sys.executable)" 2>$null
                if ($LASTEXITCODE -eq 0 -and $path) { return $path.Trim() }
            } catch { }
        }
    }
    foreach ($name in @("python3.14", "python3.13", "python3.12", "python3.11", "python3.10", "python")) {
        $cmd = Get-Command $name -ErrorAction SilentlyContinue
        if (-not $cmd) { continue }
        $verOut = & $cmd.Source -c "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')" 2>$null
        if ($LASTEXITCODE -ne 0) { continue }
        $parts = $verOut.Trim().Split(".")
        if ([int]$parts[0] -gt 3 -or ([int]$parts[0] -eq 3 -and [int]$parts[1] -ge 10)) {
            return $cmd.Source
        }
    }
    throw "Python 3.10+ is required for markitdown. Install a newer Python and re-run."
}

if (-not (Test-Path -LiteralPath $VenvPython)) {
    $BasePython = Resolve-Python310Plus
    Write-Host "Creating venv at .venv-convert with $BasePython ..."
    & $BasePython -m venv $VenvDir
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} else {
    $venvVer = & $VenvPython -c "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')"
    $parts = $venvVer.Trim().Split(".")
    if ([int]$parts[0] -lt 3 -or ([int]$parts[0] -eq 3 -and [int]$parts[1] -lt 10)) {
        Write-Host "Existing venv is Python $venvVer (<3.10). Recreating ..."
        Remove-Item -LiteralPath $VenvDir -Recurse -Force
        $BasePython = Resolve-Python310Plus
        & $BasePython -m venv $VenvDir
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
}

Write-Host "Installing / updating conversion dependencies ..."
& $VenvPython -m pip install --upgrade pip | Out-Null
& $VenvPython -m pip install -r $Req
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

if ($SetupOnly) {
    Write-Host "Setup complete."
    exit 0
}

$argsList = @(
    $Script,
    "--repo", $RepoRoot,
    "--subjects", $Subjects,
    "--dpi", "$Dpi"
)

if ($Limit -gt 0) { $argsList += @("--limit", "$Limit") }
if ($Force) { $argsList += "--force" }
if ($SkipMisc) { $argsList += @("--skip-glob", "**/misc/**") }

Write-Host "Running: $VenvPython $($argsList -join ' ')"
& $VenvPython @argsList
exit $LASTEXITCODE
