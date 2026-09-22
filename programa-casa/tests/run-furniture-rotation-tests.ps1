param(
  [string]$ConsolePath = 'C:\Program Files\Autodesk\AutoCAD 2027\accoreconsole.exe',
  [string]$TemplatePath = 'C:\Users\mathe\AppData\Local\Autodesk\AutoCAD 2027\R26.0\ptb\Template\acad.dwt'
)
$ErrorActionPreference = 'Stop'
$testRoot = $PSScriptRoot
$projectRoot = Split-Path $testRoot -Parent
if (!(Test-Path -LiteralPath $ConsolePath)) { throw "AutoCAD Core Console nao encontrado: $ConsolePath" }
if (!(Test-Path -LiteralPath $TemplatePath)) { throw "Template nao encontrado: $TemplatePath" }
$runRoot = Join-Path $testRoot ('artifacts/furniture-rotation-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
New-Item -ItemType Directory -Path $runRoot -Force | Out-Null
$copyPath = Join-Path $runRoot 'isolated.dwg'
Copy-Item -LiteralPath $TemplatePath -Destination $copyPath
$resultPath = Join-Path $runRoot 'results.txt'
$scriptPath = Join-Path $runRoot 'run.scr'
$coreLisp = (Join-Path $projectRoot 'casa-core.lsp').Replace('\','/')
$furnitureLisp = (Join-Path $projectRoot 'casa-furniture.lsp').Replace('\','/')
$testLisp = (Join-Path $testRoot 'furniture-rotation-tests.lsp').Replace('\','/')
$resultLisp = $resultPath.Replace('\','/')
@"
(setq ct:previous-secureload (getvar "SECURELOAD"))
(setvar "SECURELOAD" 0)
(load "$coreLisp")
(load "$furnitureLisp")
(load "$testLisp")
(setvar "SECURELOAD" ct:previous-secureload)
(fr:run "$resultLisp")
_.QUIT
_N

"@ | Set-Content -LiteralPath $scriptPath -Encoding ascii
$stdoutPath = Join-Path $runRoot 'console.stdout.txt'
$stderrPath = Join-Path $runRoot 'console.stderr.txt'
$profilePath = Join-Path $runRoot 'profile'
New-Item -ItemType Directory -Path $profilePath -Force | Out-Null
$process = Start-Process -FilePath $ConsolePath -ArgumentList @('/i', ('"' + $copyPath + '"'), '/s', ('"' + $scriptPath + '"'), '/l', 'pt-BR', '/isolate', 'CasaCoreTests', ('"' + $profilePath + '"')) -WorkingDirectory $runRoot -WindowStyle Hidden -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath -PassThru
if (!$process.WaitForExit(180000)) {
  $process.Kill()
  throw "Timeout dos testes AutoCAD. Consulte $runRoot"
}
if (!(Test-Path -LiteralPath $resultPath)) { throw "AutoCAD nao escreveu os resultados. Consulte $runRoot" }
$resultText = Get-Content -LiteralPath $resultPath -Raw
$resultText -split "`r?`n" | Where-Object { $_ -match '^(FAIL|COMPLETE)' } | Write-Output
Write-Output "Artefatos: $runRoot"
if (!$resultText -or $resultText -notmatch 'COMPLETE' -or $resultText -match '^FAIL' -or $resultText -match '(?m)^FAIL') {
  throw 'Testes geometricos falharam.'
}



