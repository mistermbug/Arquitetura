param([string]$ReopenDrawing)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$runRoot = Join-Path $PSScriptRoot ('artifacts/v03-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
New-Item -ItemType Directory -Path $runRoot -Force | Out-Null
$drawing = Join-Path $runRoot 'comparacao.dwg'
if ($ReopenDrawing) {
 Copy-Item -LiteralPath $ReopenDrawing -Destination $drawing
} else {
 Copy-Item -LiteralPath 'C:\Users\mathe\AppData\Local\Autodesk\AutoCAD 2027\R26.0\ptb\Template\acad.dwt' -Destination $drawing
}
$rootLisp = $projectRoot.Replace('\','/')
$runLisp = $runRoot.Replace('\','/')
$script = Join-Path $runRoot 'run.scr'
$entry = '(t3:run "' + $runLisp + '")'
if ($ReopenDrawing) {
 $sourceRoot = (Split-Path -Parent (Resolve-Path -LiteralPath $ReopenDrawing).Path).Replace('\','/')
 $entry = '(t3:reopen "' + $runLisp + '" "' + $sourceRoot + '")'
}
@"
(setq oldsecure (getvar "SECURELOAD"))
(setvar "SECURELOAD" 0)
(load "$rootLisp/entrega-0.3/CASA-BH.lsp")
(load "$rootLisp/tests/v03-tests.lsp")
(setvar "SECURELOAD" oldsecure)
$entry
_.QUIT
_N

"@ | Set-Content -LiteralPath $script -Encoding ascii
$stdout = Join-Path $runRoot 'stdout.txt'
$profile = Join-Path $runRoot 'profile'
New-Item -ItemType Directory -Path $profile -Force | Out-Null
$process = Start-Process -FilePath 'C:\Program Files\Autodesk\AutoCAD 2027\accoreconsole.exe' -ArgumentList @('/i', ('"'+$drawing+'"'), '/s', ('"'+$script+'"'), '/l', 'pt-BR', '/isolate', 'CasaV03Tests', ('"'+$profile+'"')) -WorkingDirectory $runRoot -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError (Join-Path $runRoot 'stderr.txt') -PassThru
if (!$process.WaitForExit(240000)) { $process.Kill(); throw "Timeout: $runRoot" }
Write-Output "Artefatos: $runRoot"
$report = Join-Path $runRoot 'report.txt'
if (!(Test-Path -LiteralPath $report)) { Get-Content -LiteralPath $stdout -Encoding Unicode -Tail 50; throw 'Relatorio ausente' }
$text = Get-Content -LiteralPath $report -Raw
Get-Content -LiteralPath $report | Where-Object { $_ -match 'FAIL|COMPLETE' } | Select-Object -First 35
if ($text -match '(?m)^FAIL ' -or $text -notmatch 'failed=0 drawings=3') { Get-Content -LiteralPath $stdout -Encoding Unicode -Tail 35; throw 'Teste incompleto' }
