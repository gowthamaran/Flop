$ErrorActionPreference = 'Stop'
$Skill = Split-Path -Parent $MyInvocation.MyCommand.Path
$Repo = Split-Path -Parent $Skill
$Python = if (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { 'python' }
if ($Python -eq 'py') { & py -3 -m venv "$Skill\.venv" } else { & python -m venv "$Skill\.venv" }
$Vpy = "$Skill\.venv\Scripts\python.exe"
& $Vpy -m pip install --upgrade pip
& $Vpy -m pip install -r "$Skill\scripts\requirements.txt"
$Base = Join-Path $HOME '.agents\skills'
$Dest = Join-Path $Base 'flop-airdrop-advanced'
New-Item -ItemType Directory -Force -Path $Base | Out-Null
if (Test-Path $Dest) { Remove-Item -Recurse -Force $Dest }
Copy-Item -Recurse $Skill $Dest
Copy-Item "$Repo\technocore_agent.py" "$Base\technocore_agent.py" -Force
Write-Host "Installed at $Dest"
Write-Host "Run: $Dest\.venv\Scripts\python.exe $Dest\scripts\agent_toolkit.py doctor"
Write-Host 'No key was created. Run init interactively when ready.'
