$ErrorActionPreference='Stop'
$projectRoot=Split-Path $PSScriptRoot -Parent
$runRoot=Join-Path $PSScriptRoot ('artifacts/geometry04-'+(Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
New-Item -ItemType Directory -Path $runRoot -Force | Out-Null
$drawing=Join-Path $runRoot 'test.dwg'
Copy-Item -LiteralPath 'C:\Users\mathe\AppData\Local\Autodesk\AutoCAD 2027\R26.0\ptb\Template\acad.dwt' -Destination $drawing
$script=Join-Path $runRoot 'run.scr'
$root=$projectRoot.Replace('\','/')
$result=(Join-Path $runRoot 'results.txt').Replace('\','/')
@"
(setvar "SECURELOAD" 0)
(load "$root/casa-core.lsp")
(load "$root/casa-furniture.lsp")
(load "$root/casa-roof.lsp")
(load "$root/casa-layout.lsp")
(load "$root/tests/v03-tests.lsp")
(load "$root/tests/v04-geometry-tests.lsp")
(t4:run "$result")
_.QUIT
_N

"@ | Set-Content $script -Encoding ascii
$profile=Join-Path $runRoot 'profile'
New-Item -ItemType Directory -Path $profile -Force | Out-Null
$p=Start-Process -FilePath 'C:\Program Files\Autodesk\AutoCAD 2027\accoreconsole.exe' -ArgumentList @('/i',('"'+$drawing+'"'),'/s',('"'+$script+'"'),'/l','pt-BR','/isolate','CasaGeometry04',('"'+$profile+'"')) -WorkingDirectory $runRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $runRoot 'stdout.txt') -RedirectStandardError (Join-Path $runRoot 'stderr.txt') -PassThru
if (!$p.WaitForExit(180000)) {$p.Kill(); throw 'Timeout'}
Write-Output $runRoot
if(Test-Path $result){Get-Content $result}else{Get-Content (Join-Path $runRoot 'stdout.txt') -Encoding Unicode -Tail 35}
