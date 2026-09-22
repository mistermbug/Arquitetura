# Testes em AutoLISP nativo

Execute no PowerShell, a partir da pasta programa-casa:

```powershell
.\tests\run-core-tests.ps1
```

O script usa o AutoCAD Core Console 2027 instalado neste computador. Os parametros
`-ConsolePath` e `-TemplatePath` permitem usar outra instalacao e template. Ele
copia o template para uma pasta nova em `tests/artifacts`, carrega o nucleo e os
testes e fecha o processo sem salvar alteracoes no desenho de entrada. O valor de
SECURELOAD e restaurado logo apos carregar os arquivos. Nenhuma sessao interativa
do AutoCAD e controlada pelo teste.

Cada execucao preserva `results.txt` e os logs do console. Sucesso exige o marcador
`COMPLETE` e nenhuma linha `FAIL`. Falha ao iniciar, erro AutoLISP ou timeout nao
contam como sucesso.

As verificacoes usam o nucleo real `casa-core.lsp`, sem reproduzir seu algoritmo em
outra linguagem. Cobrem repetibilidade da semente, 25 sementes diferentes,
retangulos de ambientes e moveis com area positiva e dentro da laje, paredes
nao degeneradas, existencia de parede hospedeira para cada vao e posicionamento
do vao no eixo e dentro da extensao da parede. Tambem verificam os moveis dentro
do ambiente atribuido, quantidades exatas dos tipos solicitados, um programa com
quantidade impar de ambientes, opcao de desligar mobiliario e rejeicao de lote
inviavel, quantidade fracionaria e espessura negativa.

Execucao verificada em 07/09/2026: AutoCAD Core Console 2027, **3734 assertions
aprovadas, 0 falhas**. Relatorio: `artifacts/run-20260907-111203-664/results.txt`.
O processo precisou de acesso ao perfil Autodesk fora do sandbox do agente; o
runner utiliza `/isolate` e mantem os arquivos de perfil na pasta de artefatos.

Isso verifica propriedades geometricas do prototipo. Nao comprova aprovacao
municipal, desempenho ambiental, habitabilidade, renderizacao grafica, interface
interativa nem execucao do importador dentro do Revit. Esses itens exigem revisoes
e testes especificos adicionais.
