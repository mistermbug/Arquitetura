param([string]$ReopenDrawing)
$ErrorActionPreference='Stop'
$projectRoot=Split-Path $PSScriptRoot -Parent
$testRoot=Join-Path $PSScriptRoot ('artifacts/custom-'+(Get-Date -Format 'yyyyMMdd-HHmmss'))
New-Item -ItemType Directory -Path $testRoot -Force | Out-Null
$drawing=Join-Path $testRoot 'test.dwg'
if ($ReopenDrawing) {Copy-Item -LiteralPath $ReopenDrawing -Destination $drawing}
else {Copy-Item -LiteralPath 'C:\Users\mathe\AppData\Local\Autodesk\AutoCAD 2027\R26.0\ptb\Template\acad.dwt' -Destination $drawing}
$cadRoot=$projectRoot.Replace('\','/')
$cadTest=$testRoot.Replace('\','/')
$entry='(te:run "'+(Split-Path $projectRoot -Parent).Replace('\','/')+'/json/rodolfo.json" "'+$cadTest+'")'
$tail='(te:edit "'+$cadTest+'")'+"`n_.U`n"+'(te:finish "'+$cadTest+'")'
if ($ReopenDrawing) {$tail='(princ)';$entry='(te:reopen "'+$cadTest+'")'}
@"
(setvar "SECURELOAD" 0)
(load "$cadRoot/entrega-0.4/CASA-BH.lsp")
(load "$cadRoot/tests/custom-tests.lsp")
$entry
_.UNDO
_Control
_None
_.UNDO
_All
_.UNDO
_Auto
_Off
$tail
_.QUIT
_Y

"@ | Set-Content -LiteralPath (Join-Path $testRoot 'run.scr') -Encoding ascii
$profile=Join-Path $testRoot 'profile'
New-Item -ItemType Directory -Path $profile -Force | Out-Null
$cadProcess=Start-Process -FilePath 'C:\Program Files\Autodesk\AutoCAD 2027\accoreconsole.exe' -ArgumentList @('/i', ('"'+$drawing+'"'),'/s',('"'+$testRoot+'\run.scr"'),'/l','pt-BR','/isolate','CasaCustom',('"'+$profile+'"')) -WorkingDirectory $testRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $testRoot 'stdout.txt') -RedirectStandardError (Join-Path $testRoot 'stderr.txt') -PassThru
if (!$cadProcess.WaitForExit(150000)) {$cadProcess.Kill();throw 'Core timeout'}
Write-Output $testRoot
$report=Join-Path $testRoot 'report.txt'
if (Test-Path -LiteralPath $report) {Get-Content -LiteralPath $report}
if (!(Test-Path -LiteralPath $report) -or (Get-Content -LiteralPath $report -Raw) -notmatch 'COMPLETE failed=0') {
 Get-Content -LiteralPath (Join-Path $testRoot 'stdout.txt') -Encoding Unicode -Tail 22
 throw 'Teste incompleto ou com falhas'
}
