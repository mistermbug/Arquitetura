param()
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$runRoot = Join-Path $PSScriptRoot ('artifacts/cad-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
New-Item -ItemType Directory -Path $runRoot -Force | Out-Null
$drawing = Join-Path $runRoot 'casa-exemplo.dwg'
Copy-Item -LiteralPath 'C:\Users\mathe\AppData\Local\Autodesk\AutoCAD 2027\R26.0\ptb\Template\acad.dwt' -Destination $drawing
$rootLisp = $projectRoot.Replace('\','/')
$runLisp = $runRoot.Replace('\','/')
$script = Join-Path $runRoot 'smoke.scr'
@"
(setq smoke:sec (getvar "SECURELOAD"))
(setvar "SECURELOAD" 0)
(load "$rootLisp/entrega-0.2/CASA-BH.lsp")
(load "$rootLisp/tests/core-tests.lsp")
(load "$rootLisp/tests/cad-smoke.lsp")
(setvar "SECURELOAD" smoke:sec)
(setq *casa-dir* "$rootLisp")
(smoke:run "$runLisp/casa-exemplo.json" "$runLisp/report.txt" "$runLisp/casa-exemplo.dwg")
_.QUIT
_N

"@ | Set-Content -LiteralPath $script -Encoding ascii
$stdout = Join-Path $runRoot 'stdout.txt'
$stderr = Join-Path $runRoot 'stderr.txt'
$profile = Join-Path $runRoot 'profile'
New-Item -ItemType Directory -Path $profile -Force | Out-Null
$process = Start-Process -FilePath 'C:\Program Files\Autodesk\AutoCAD 2027\accoreconsole.exe' -ArgumentList @('/i', ('"'+$drawing+'"'), '/s', ('"'+$script+'"'), '/l', 'pt-BR', '/isolate', 'CasaSmokeTests', ('"'+$profile+'"')) -WorkingDirectory $runRoot -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru
if (!$process.WaitForExit(180000)) { $process.Kill(); throw "Timeout: $runRoot" }
Write-Output "Artefatos: $runRoot"
$report = Join-Path $runRoot 'report.txt'
if (!(Test-Path -LiteralPath $report)) { Get-Content -LiteralPath $stdout -Encoding Unicode -Tail 40; throw 'Relatorio ausente' }
Get-Content -LiteralPath $report
$text = Get-Content -LiteralPath $report -Raw
if ($text -match 'FAIL' -or $text -notmatch 'EXPORT=PASS') { Get-Content -LiteralPath $stdout -Encoding Unicode -Tail 50; throw 'Teste CAD incompleto' }
