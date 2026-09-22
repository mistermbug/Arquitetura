# Verificação da versão 0.1 — 07/09/2026

- Núcleo AutoLISP executado no AutoCAD Core Console 2027 instalado: 3.734 verificações aprovadas, zero falhas.
- Desenho final executado novamente após ajustes de unidades e rótulos: 141 entidades, 12 cotas DIMENSION, exportação JSON e snapshot aprovados.
- DWG final reaberto em outro processo: mesmas 141 entidades e 12 cotas; snapshot preservado com 7.663 caracteres.
- Variáveis OSMODE, CLAYER, DIMTXT, DIMLFAC e DIMPOST restauradas no ensaio.
- DXF exportado pelo AutoCAD e prévia visual inspecionada.
- Importador Python: sintaxe compilada, validação do JSON real aprovada, dois bloqueios de execução e seis rejeições de dados inválidos aprovados. Detalhes em `tests/revit-validation.txt`.

Não executados: formulário na interface gráfica do AutoCAD e importação dentro do Revit. O teste DCL no Core Console retornou -1. Não há comprovação de aprovação municipal, acessibilidade, conforto ou qualidade arquitetônica pelo fato de os testes geométricos passarem.

Logs completos ficam no workspace em `tests/artifacts/`. O pacote distribui fontes, exemplos e este resumo, sem os perfis locais Autodesk dos testes. Os caminhos dos runners precisam ser ajustados em outro computador.
