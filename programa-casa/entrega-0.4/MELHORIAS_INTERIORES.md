# CASA BR — interiores e vegetação

Atualizado para `0.4-interiores-2`. A documentação vigente está em [MOVEIS_PLANEJADOS_E_VEGETACAO.md](MOVEIS_PLANEJADOS_E_VEGETACAO.md), incluindo o comando de dimensões no AutoCAD e o catálogo de 15 espécies.

## O que está preparado

- Coleção original de móveis com bases, assentos, encostos, almofadas, cabeceiras, tampos curvos, portas e puxadores. Tons de madeira, linho, caramelo, oliva, pedra e bronze.
- Louças, bancada com rebaixo de cuba, eletrodomésticos reconhecíveis e carros esquemáticos com carroceria e rodas.
- Vasos com folhagem modelada e paleta terracota/verde. Não utiliza modelos ou desenhos de fabricantes.
- Atualização da casa existente: junções de paredes, mobiliário e vegetação em uma única transação, com reversão em caso de erro.

No `rodolfo.json`: **31 peças existentes detalhadas e 6 vasos**, sendo três internos e três no quintal. Dois quartos não recebem vasos por falta de canto livre que cumpra os critérios. A prévia `exemplos/colecao-brasileira.png` usa as mesmas peças geométricas do código; não é uma captura do Revit nem uma imagem gerada por IA. A imagem `interiores-isometria.png` mostra apenas móveis e vegetação, sem paredes ou cobertura.

Os objetos são **DirectShape detalhados**, preservando os elementos existentes. Não são ainda famílias RFA editáveis pelo editor de famílias. Dimensões e formas são geradas pelo código; cores sólidas representam materiais, sem texturas fotográficas de madeira/tecido ou aparência fotorrealista. Ferragens, conforto do produto e especificações industriais ainda não foram desenvolvidos.

## Aplicar na casa já importada

1. Abra o mesmo projeto Revit da casa e use o JSON da mesma casa em IN[0], reexportado caso tenha editado dimensões no CAD.
2. Deixe o Dynamo em Manual, IN[1]=False e IN[2]=False.
3. Abra `programa-casa/revit/atualizar_interiores_dynamo.py` no Bloco de Notas e copie todo o conteúdo para substituir o código do nó PythonNet3 existente.
4. Salve o código. Passe IN[1] para True e execute uma vez.
5. O resultado esperado é `status=interiores_atualizados`. O Watch inclui `quantity_audit` das paredes e `interiors` com itens/vegetação.
6. Volte IN[1] para False, confira o modelo e salve o RVT. Na vista 3D, use **Cores consistentes** ou **Sombreado** para enxergar as cores; Linha oculta mostra essencialmente contornos.

O carregador aponta para `C:\Users\mathe\OneDrive\Desktop\Arquitetura\programa-casa\revit\importar_casa_dynamo.py`. Em outro computador/pasta, ajuste `IMPORTADOR` e mantenha `casa_interiores.py` ao lado do importador. Para editar dimensões no CAD, carregue o `CASA-BH.lsp` atualizado e reexporte o JSON após a edição. Para atualizar somente os modelos e a vegetação, o JSON existente é suficiente. Mantenha `vegetacao.json` ao lado de `casa_interiores.py`.

Novas importações pelo importador completo também aplicam esta coleção. A atualização não apaga a casa e não usa IN[2]=True. Detecta deslocamentos que alterem a caixa envolvente dos móveis e interrompe a operação; isso não é uma detecção completa de toda edição manual, especialmente mudanças que preservem os mesmos limites. Paredes alteradas manualmente e demais diferenças do projeto precisam ser conferidas: a base de posições de paisagismo continua sendo o JSON original.

## Critérios de paisagismo implementados

- Vasos internos apenas em quartos, escritório e convivência com janela identificada, até 2 m do centro da janela. Esse limite é uma heurística de projeto, **não uma medida de iluminância**.
- Envelope considera a folhagem, não apenas o vaso, com margem adicional de 20 cm para manutenção.
- Rejeição de interferência com móveis e faixas de uso, portas, reserva de operação das janelas (60 cm), circulação central e caminho de chegada.
- Faixas conservadoras de 90 cm entre portas e centro dos recintos impedem que vasos sejam acrescentados nesses percursos. Não certificam acessibilidade ou que o mobiliário existente permita todos os percursos.
- Vasos externos apenas no quintal posterior, fora da casa e de garagem/terraço existentes. Afastamento de ensaio de 60 cm da caixa da casa; apenas exemplares em vaso, sem plantio direto no solo ou sobre lajes.
- O catálogo oferece **15 espécies**, cuja escolha definitiva precisa ser confirmada após conferir luz real, clima local, manutenção e usuários da residência. Vasos requerem drenagem e recipiente interno adequado; esses detalhes não estão construtivamente modelados.

A seleção de plantas deve corresponder às condições reais de luz, conforme [University of Maryland Extension](https://www.extension.umd.edu/resource/selecting-indoor-plants). Para vasos, é necessário prever drenagem e evitar encharcamento, conforme [RHS](https://www.rhs.org.uk/container-gardening/growing-plants-in-containers). As dimensões de reserva acima são decisões deste protótipo, não prescrições dessas fontes nem regras legais de BH.

## Validação e limites

- Oito testes do contrato do importador e doze testes de interiores passaram em Python. A edição de dimensões e a reabertura do DWG também foram ensaiadas no AutoCAD Core 2027; consulte o guia atualizado.
- Modelos conferidos nas quatro rotações e nos dois estados de espelhamento para as peças do JSON Rodolfo.
- Verificados perfis não degenerados, planos e compatíveis geometricamente com extrusão nos 27 cenários CAD da bateria existente; essa checagem não executa a API Revit.
- Testes de vegetação cobrem contenção no ambiente/lote, faixas de uso dos móveis, ausência de janelas e ambientes sem espaço. Prévia renderizada e inspecionada.
- **A execução desta revisão dentro do Revit ainda precisa ser confirmada.** Não foi criado/salvo um RVT nesta entrega. Não há simulação solar, prescrição botânica definitiva ou orçamento de materiais.

Os volumes dos componentes de mobiliário incluem peças sobrepostas de representação. Não devem ser somados para orçamento de madeira, espuma ou estofamento. As plantas são representações conceituais; quantidades de compra e tamanhos comerciais dependem do projeto de paisagismo.
