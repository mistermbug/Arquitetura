# Mobiliario funcional da versao 0.3

O modulo `casa-furniture.lsp` oferece `cg:furnish-model(model, params)` (chamada AutoLISP com dois argumentos). O empacotamento incorpora este modulo no LISP unico distribuido ao usuario.

- Zonas funcionais recebem conjuntos completos, com oito orientacoes candidatas (quatro rotacoes e espelhamento); salas para cinco ou seis moradores possuem ainda um segundo conjunto de assentos.
- Quartos: cama de solteiro ou casal, armario e criado. Camas de casal adicionais atendem o numero de moradores ate a capacidade de duas pessoas por quarto. A capacidade nao define um arranjo familiar adequado: revise os ocupantes de cada dormitorio.
- Sala: sofa e rack; para quatro moradores, sofa e poltrona; para cinco ou seis moradores, dois sofas com seis assentos nominais ou sofa e namoradeira, acrescentando poltrona para seis.
- Jantar: mesa com quatro ou seis cadeiras, conforme moradores.
- Cozinha: geladeira, pia, bancada e fogao.
- Banheiro: chuveiro, sanitario e lavatorio. Lavanderia: maquina e tanque. Escritorio: mesa e cadeira.
- Garagem: um volume de carro por vaga. Terraco: banco.

A verificacao geometrica rejeita sobreposicao entre volumes, pecas fora da zona, faixas de uso ocupadas por outros moveis e intersecoes com uma reserva conservadora junto a portas. As faixas de uso sao hipoteses do catalogo; nao constituem dimensionamento normativo de acessibilidade. O criado pode ocupar a faixa lateral da cama junto a cabeceira, mantendo a verificacao de colisao fisica.

Pecas com altura superior ao peitoril nao podem interceptar uma faixa de 200 mm junto ao trecho da janela. Nao se verifica caminho continuo de circulacao, abertura de folhas de janelas, iluminancia ou sombreado distante. A geometria e esquematica: os modelos Revit sao volumes, sem promessa de familia parametrica detalhada. Quando um conjunto nao cabe, o modulo devolve erro para que o gerador tente outra organizacao; nao elimina silenciosamente uma peca essencial.

O ensaio `tests/run-furniture-tests.ps1` verifica os nove grupos de catalogo, seis posicoes de portas de quarto e rejeicoes de colisao, porta bloqueada e limites, alem de dois casos de janela e contagem de dois carros. Execute com AutoCAD 2027 instalado e licenciado. Resultados so sao validos quando o arquivo de resultados contem COMPLETE e nenhuma linha FAIL.


Para cinco ou seis moradores, priorize a convivencia integrada. O ensaio ampliado usa lote 13 x 32 m, casa com 10 m de largura e semente 42: as tres organizacoes integradas passaram. Algumas combinacoes separadas foram rejeitadas por mobiliario sem encaixe; o programa deve informar essa inviabilidade. O ensaio furniture-six registra REJECTED para estas tentativas, exigindo que as tres integradas passem.

