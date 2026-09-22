# Exemplo gerado no AutoCAD 2027

Abra `casa-exemplo.dwg` no AutoCAD. O DXF contém a mesma geometria para intercâmbio. `casa-exemplo.json` alimenta o importador Dynamo/Revit.

Lote hipotético plano de 12 × 30 m, três quartos, banheiro, sala, cozinha, lavanderia e circulação. Semente 42. São 15 paredes lógicas, 15 aberturas, oito ambientes incluindo circulação e 13 móveis esquemáticos.

As imagens PNG foram renderizadas a partir das entidades do DXF gerado pelo AutoCAD, com um renderizador simples incluído em `tests/render-dxf-preview.py`. São prévias de conferência: fonte, posição de textos e setas de cota podem diferir do AutoCAD. Use o DWG como referência de desenho.

A distribuição foi gerada para testar o algoritmo aleatório. Ainda não foi otimizada arquitetonicamente: por exemplo, o último quarto ocupa toda a largura disponível. Não é uma proposta de projeto aprovada.
