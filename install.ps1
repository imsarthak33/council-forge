$ErrorActionPreference = "Stop"
$repoUrl = "https://github.com/imsarthak33/council-forge.git"
$targetDir = "$env:USERPROFILE\.claude\skills\council-forge"
$tempDir = Join-Path $env:TEMP "council-forge-install"

Write-Host "==> Installing Council Forge..." -ForegroundColor Cyan

if (Test-Path $targetDir) {
    $backupDir = "$targetDir.bak.$(Get-Date -Format 'yyyyMMddHHmmss')"
    Write-Host "==> Backing up existing installation to $backupDir" -ForegroundColor Yellow
    Move-Item -Path $targetDir -Destination $backupDir -Force
}

if (Test-Path $tempDir) { Remove-Item -Path $tempDir -Recurse -Force }

Write-Host "==> Fetching from $repoUrl" -ForegroundColor Cyan
git clone --quiet --depth 1 $repoUrl $tempDir

Write-Host "==> Copying files to $targetDir" -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
Copy-Item -Path "$tempDir\*" -Destination $targetDir -Recurse -Force

Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "✔ Council Forge installed to $targetDir" -ForegroundColor Green
Write-Host "Next steps:`n  Start Claude Code and try: /council-forge" -ForegroundColor Gray
