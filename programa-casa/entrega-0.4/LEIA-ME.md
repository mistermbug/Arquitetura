# CASA BH 0.4

**Móveis editáveis e vegetação (11/09/2026):** use `CASA_MOVEL_EDITAR` para largura, profundidade e altura em metros. O JSON exportado leva as alterações ao Revit. Catálogo com 15 espécies em vaso e quatro palmeiras. Leia `MOVEIS_PLANEJADOS_E_VEGETACAO.md` e veja as prévias completas em `exemplos/catalogo-moveis.png` e `exemplos/catalogo-vegetacao.png`. Edição/persistência testadas no AutoCAD Core 2027; execução desta revisão no Revit ainda pendente.

**Revisada em 10/09/2026 — uniões de paredes e cotas.** Carregue novamente este LISP e gere uma planta nova para receber as correções. Desenhos já gerados não são modificados automaticamente.

As paredes em planta agora mostram o contorno da união dos trechos, sem fechamentos atravessando encontros L/T/cruzamentos. Portas e janelas mantêm seus vãos. Os eixos e dados semânticos de paredes exportados permanecem preservados. A revisão do importador Revit `0.4-joins-1` acrescenta junções nativas, correção da casa existente e auditoria de sobreposições volumétricas; leia `revit/README.md`. Sua execução real ainda precisa de confirmação no Revit.

As cotas internas medem faces livres dos ambientes e escolhem faixas menos ocupadas. Cotas externas distinguem tamanho da casa, recuo do contorno e terreno. Foram removidas as larguras de cômodos empilhadas à frente do lote. A unidade fica na legenda, com duas casas decimais e traços oblíquos nas extremidades. Texto de 140 mm no Modelo equivale a 2,8 mm ao imprimir em 1:50; confira a escala e o estilo de plotagem antes de imprimir. A cor da camada não define sozinha a espessura impressa.

Ainda é cotagem de estudo preliminar: não inclui toda a locação executiva de paredes e vãos, níveis ou compatibilização estrutural. Em espaços pequenos, desligar temporariamente `CASA_MOVEIS` facilita conferir as cotas. O posicionamento automático reduz interferências, mas não garante composição gráfica perfeita em toda combinação de entradas.

Gerador de estudos preliminares para terreno plano. O pacote contém **um único arquivo AutoLISP**, com formulário embutido, exemplos CAD e ponte JSON/Dynamo para Revit.

## Como usar

1. Extraia o ZIP e abra um desenho novo no AutoCAD 2027, espaço Modelo, com `INSUNITS = 4` (milímetros). Isso não converte a geometria de desenhos existentes.
2. Use `APPLOAD` para carregar `CASA-BH.lsp` desta versão. Não carregue os arquivos antigos depois dele.
3. Execute `CASA_GERAR` ou `CASA_ALTERNATIVAS`, preencha o formulário e indique o ponto de inserção. Use Zoom Extents para ver o conjunto.
4. Salve o DWG. Para exportar uma alternativa, execute `CASA_EXPORTAR`, selecione uma entidade dela e salve o JSON.
5. Siga `revit/README.md` para usar o importador incluído. A execução dentro do Revit ainda precisa de validação na sua instalação.

## Mudanças desta versão

- Móveis selecionados entre arranjos viáveis com rotações de 0°, 90°, 180° e 270° e espelhamento. Os símbolos internos acompanham a orientação. São verificadas colisões, faixas de uso, reservas de portas e peças altas junto às janelas.
- Entrada principal frontal, pela sala ou circulação, inclusive quando a convivência fica nos fundos. Garagem posicionada junto ao acesso de pedestres; percurso de chegada limitado a 6 m pelo critério do gerador.
- Contorno com recuo real em um canto, alterando paredes, áreas, piso e cobertura. Se os móveis não couberem, o programa tenta reduzir o recuo antes de rejeitar a alternativa. Não remove móveis essenciais para forçar o encaixe.
- Corte com teto representado pela face inferior da laje de cobertura, laje de 15 cm e platibanda de 60 cm. Fachada também recebe a cobertura. Trata-se de representação conceitual: caimentos, drenagem, impermeabilização e estrutura não foram dimensionados.
- Exportação do contorno e cobertura para Revit. A cobertura é criada como **Piso elevado**, com paredes de platibanda, não como objeto da categoria Telhado.

## Entradas e limites

O formulário recebe metros; CAD e JSON usam milímetros, com cotas exibidas em metros. Espessuras das paredes internas e externas continuam independentes. O primeiro ensaio deve ser em desenho novo para evitar valores antigos do formulário.

O perfil aceita uma sala, uma cozinha e até um jantar, além de quartos, banheiros, lavanderias e escritórios sujeitos ao encaixe. Quantidades fracionárias são rejeitadas. Moradores: 1–6; vagas descobertas: 0–2. Não inclui suítes, escadas ou garagem coberta. Camas representam capacidade de ocupação, não uma decisão sobre quem deve compartilhar quartos.

Com estacionamento, a faixa frontal efetiva é de pelo menos 6,50 m para reservar espaço de carro e passagem de pedestres. É um parâmetro de ensaio, **não um recuo legal municipal**. Vagas de 2,60 × 5,00 m não substituem análise de manobra e portão.

Mesmas entradas e semente reproduzem o resultado. As opções variam organização, integração, dimensões e mobiliário dentro de um repertório limitado. Os recuos melhoram o contorno, mas a versão ainda não resolve composições livres, casas com pátio central ou estilos detalhados. Algumas combinações não cabem; tente outra semente, organização ou dimensões. Isso não demonstra inviabilidade arquitetônica do terreno.

Norte é informação fornecida pelo usuário; não orienta automaticamente os ambientes pelo Sol. Indicadores de janela e circulação não comprovam iluminação, ventilação, conforto térmico ou acessibilidade. Regras municipais por lote e projeto executivo permanecem pendentes de desenvolvimento e revisão profissional.

## Exemplos e Revit

`exemplos/comparacao.dwg` contém três alternativas em lote de 12 × 30 m, com três quartos, quatro moradores e uma vaga. Os três arquivos `desenho-N.json` correspondem às posições dessas alternativas no DWG. As imagens PNG são prévias do DXF; fontes e detalhes podem diferir do AutoCAD.

A ponte cria paredes, pisos, ambientes, aberturas e volumes esquemáticos de mobiliário. Não fornece famílias RFA detalhadas, folhas de portas/janelas, cotas Revit ou sincronização de alterações manuais do CAD. O JSON recupera o estado gerado persistido no DWG. Leia as instruções de reimportação antes de substituir elementos no Revit.

Veja `VERIFICACAO.md` para os testes executados e suas limitações.
