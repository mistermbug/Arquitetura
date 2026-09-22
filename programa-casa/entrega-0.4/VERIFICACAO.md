# Verificação da versão 0.4 — revisão de 10/09/2026

- AutoCAD Core Console 2027: 27 combinações de três organizações, três integrações e sementes 1, 42 e 91. Resultado: 25.317 verificações passaram, zero falhas, três alternativas desenhadas.
- Verificados contagem de ambientes, encaixe de mobiliário, reservas de portas, contenção geométrica, repetibilidade, contorno com recuo, espessuras externas, área, entrada frontal, percurso de chegada e correspondência entre piso e cobertura.
- A busca de encaixe utilizou uma ou três tentativas de profundidade do recuo. A bateria contém as quatro rotações de mobiliário. Os percursos de chegada mediram 2,30 m nesses cenários.
- DWG reaberto em outro processo AutoCAD: quatro verificações passaram, incluindo os três estados persistidos e presença de cotas nativas.
- Trinta JSONs finais aceitos pelo validador do importador Revit, incluindo os três exemplos nas coordenadas do DWG.
- Seis testes Python do contrato do importador passaram, incluindo compatibilidade anterior e rejeição de contornos/coberturas inválidos.
- Prévia gerada a partir do DXF nativo e inspecionada visualmente quanto a mobiliário, acesso, recuo e cobertura.

Na revisão, uma verificação independente do DXF nativo confirmou 1.136 segmentos de contornos de parede, sem duplicações, cruzamentos internos, segmentos degenerados ou pontas abertas. Também conferiu os pontos medidos de 46 cotas internas contra as faces livres dos ambientes exportados. O teste é `tests/check-cad-presentation.py`.

Evidências no código-fonte: `tests/artifacts/v04-20260910-105022-621` (geração e topologia) e `tests/artifacts/v04-20260910-105128-472` (reabertura). Esses diretórios de execução não são necessários para usar o pacote.

Esses resultados cobrem a bateria descrita, não todas as combinações possíveis. O formulário atualizado precisa de ensaio interativo. A API do Revit ainda não foi executada nesta validação. Não foram realizados dimensionamento estrutural, simulações ambientais, análise de manobra, certificação de acessibilidade ou aprovação legal pela PBH.
