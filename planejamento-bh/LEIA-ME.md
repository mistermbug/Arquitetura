# Comece aqui

Este pacote prepara a construção do gerador de plantas residenciais no AutoCAD 2027, com base inicial em Belo Horizonte.

- [Roadmap e especificação do aplicativo](ROADMAP.md).
- [Síntese dos documentos de BH e pendências](BASE-BH.md).
- [Campos obrigatórios propostos](campos-formulario.json).
- [Matriz de 18 grupos de regras municipais](matriz-regras-bh.json).
- [Manifesto dos PDFs baixados](manifesto-fontes.json).
- [Manifesto das páginas arquivadas](manifesto-web.json).

Os PDFs originais estão em `fontes`, páginas públicas em `fontes-web` e textos auxiliares em `extratos`. O manifesto é a referência para confirmar o que foi efetivamente baixado. A data de download não é a data de edição nem prova vigência legal.

## PDFs do acervo

| Documento | Arquivo |
|---|---|
| Cartilha de representação gráfica, R5 | [Abrir PDF](fontes/representacao-r5.pdf) |
| Representação de níveis do terreno | [Abrir PDF](fontes/niveis-terreno.pdf) |
| Zoneamento, e-book | [Abrir PDF](fontes/zoneamento.pdf) |
| Parâmetros urbanísticos, e-book | [Abrir PDF](fontes/parametros-urbanisticos.pdf) |
| Procedimentos, e-book | [Abrir PDF](fontes/procedimentos.pdf) |
| E-book completo de ocupação do solo | [Abrir PDF](fontes/plano-diretor-ebook.pdf) |
| Lei 11.181, cópia com consolidação a conferir | [Abrir PDF](fontes/lei-11181.pdf) |
| Mapa de zoneamento | [Abrir PDF](fontes/mapa-zoneamento.pdf) |
| Mapa de áreas de diretrizes especiais | [Abrir PDF](fontes/mapa-ade.pdf) |
| Mapa viário, versão julho/2026 | [Abrir PDF](fontes/mapa-viario-jul2026.pdf) |

O núcleo gerador, o formulário no CAD e a integração Revit ainda serão implementados. As regras municipais estão desativadas até revisão da base consolidada e do lote. A biblioteca anterior de interiores continua em `../pesquisa-interiores` e será incorporada na etapa correspondente.

## Reproduzir a coleta

`baixar_fontes.py` requer Python com pypdf e acesso à internet. Reutiliza arquivos cujo hash corresponde ao manifesto; para conferir mudanças remotas será necessária atualização explícita da coleta. `arquivar_paginas.py` usa a biblioteca padrão do Python e arquiva as páginas públicas indicadas. Nenhum script usa login, protocola pedido ou modifica dados na Prefeitura.
