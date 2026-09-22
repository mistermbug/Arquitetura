param([string]$DwgPath = (Join-Path $PSScriptRoot 'artifacts/cad-20260907-111541-490/casa-exemplo.dwg'))
$ErrorActionPreference='Stop'
$project = Split-Path $PSScriptRoot -Parent
$run = Join-Path $PSScriptRoot ('artifacts/reopen-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
New-Item -ItemType Directory -Path $run -Force | Out-Null
$draw = Join-Path $run 'casa-reopened.dwg'
Copy-Item -LiteralPath $DwgPath -Destination $draw
$projectL = $project.Replace('\','/')
$runL = $run.Replace('\','/')
@"
(setq previous-secureload (getvar "SECURELOAD"))
(setvar "SECURELOAD" 0)
(setq *casa-dir* "$projectL")
(load "$projectL/casa.lsp")
(load "$projectL/tests/reopen-smoke.lsp")
(setvar "SECURELOAD" previous-secureload)
(reopen:run "$runL/report.txt" "$runL/casa-reopened.dxf")
_.QUIT
_N

"@ | Set-Content (Join-Path $run 'reopen.scr') -Encoding ascii
$profile = Join-Path $run 'profile'
New-Item -ItemType Directory -Path $profile -Force | Out-Null
$proc = Start-Process 'C:\Program Files\Autodesk\AutoCAD 2027\accoreconsole.exe' -ArgumentList @('/i',('"'+$draw+'"'),'/s',('"'+(Join-Path $run 'reopen.scr')+'"'),'/l','pt-BR','/isolate','CasaReopenTests',('"'+$profile+'"')) -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $run 'stdout.txt') -RedirectStandardError (Join-Path $run 'stderr.txt')
if (!$proc.WaitForExit(180000)) {$proc.Kill(); throw 'Timeout'}
Get-Content (Join-Path $run 'report.txt')
Write-Output "Artifacts: $run"
