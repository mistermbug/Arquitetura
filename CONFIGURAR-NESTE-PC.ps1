param([string]$JsonPath)
$ErrorActionPreference = 'Stop'
$projectPath = $PSScriptRoot
if (!$JsonPath) { $JsonPath = Join-Path $projectPath 'json\rodolfo.json' }
$JsonPath = (Resolve-Path -LiteralPath $JsonPath).Path
$importerPath = (Resolve-Path -LiteralPath (Join-Path $projectPath 'programa-casa\revit\importar_casa_dynamo.py')).Path
$templatePath = Join-Path $projectPath 'grafo\01.dyn'
$destination = Join-Path $projectPath 'configurado'
New-Item -ItemType Directory -Path $destination -Force | Out-Null
# JSON string quoting also produces a valid Python string literal, including
# backslashes, apostrophes and non-ASCII Windows usernames.
$importerLiteral = ConvertTo-Json -InputObject $importerPath -Compress
$operations = @(
    @{ Name='01-IMPORTAR-CASA'; Arguments=''; Description='Importar em um projeto Revit vazio' },
    @{ Name='02-ATUALIZAR-INTERIORES'; Arguments=', improve_interiors=True'; Description='Atualizar moveis e vegetacao da casa existente' },
    @{ Name='03-CORRIGIR-UNIOES'; Arguments=', repair_existing=True'; Description='Corrigir unioes da casa existente' }
)
foreach ($operation in $operations) {
    $code = @"
# Gerado para este computador. PythonNet3; IN[0]=JSON, IN[1]=executar, IN[2]=False.
import runpy
import traceback
IMPORTADOR = $importerLiteral
if len(IN) < 2 or IN[1] is not True:
    OUT = {'status': 'aguardando', 'message': 'IN[1]=True para executar.'}
elif len(IN) > 2 and IN[2] is not False:
    OUT = {'status': 'bloqueado', 'message': 'Mantenha IN[2]=False neste carregador.'}
else:
    try:
        api = runpy.run_path(IMPORTADOR)
        OUT = api['run'](IN$($operation.Arguments))
    except Exception as error:
        OUT = {'status': 'erro', 'message': str(error), 'details': traceback.format_exc()}
"@
    $graph = Get-Content -LiteralPath $templatePath -Raw -Encoding UTF8 | ConvertFrom-Json
    $graph.Name = $operation.Name
    $graph.Description = $operation.Description
    $graph.View.Dynamo.RunType = 'Manual'
    foreach ($node in $graph.Nodes) {
        if ($node.ConcreteType -like 'PythonNodeModels.PythonNode,*') {
            $node.Code = $code
            $node.Engine = 'PythonNet3'
        } elseif ($node.NodeType -eq 'StringInputNode') {
            $node.InputValue = $JsonPath
        } elseif ($node.NodeType -eq 'BooleanInputNode') {
            $node.InputValue = $false
        }
    }
    $utf8 = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText((Join-Path $destination ($operation.Name+'.py')), $code, $utf8)
    [System.IO.File]::WriteAllText((Join-Path $destination ($operation.Name+'.dyn')), ($graph | ConvertTo-Json -Depth 100), $utf8)
}
Write-Output "Configuracao pronta: $destination"
Write-Output 'Abra 01-IMPORTAR-CASA.dyn em um projeto vazio ou 02-ATUALIZAR-INTERIORES.dyn na casa ja importada.'
Write-Output 'Confira o JSON no no String, mantenha IN[2]=False e mude somente IN[1] para True quando for executar.'
Write-Output 'No AutoCAD, use APPLOAD: programa-casa\entrega-0.4\CASA-BH.lsp'
