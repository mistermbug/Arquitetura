# Móveis com medidas editáveis e catálogo de vegetação

Revisão de 11/09/2026, mantida na **entrega 0.4**. A galeria anterior mostrava oito exemplos. O projeto Rodolfo tem **31 peças em 22 categorias**, incluindo mobiliário, louças, eletrodomésticos e automóveis. Veja `exemplos/catalogo-moveis.png` para a coleção presente no projeto e `exemplos/catalogo-vegetacao.png` para as 15 espécies.

## Editar um móvel no AutoCAD

1. Use **APPLOAD** e carregue o `CASA-BH.lsp` atualizado desta pasta.
2. Na sua planta existente, digite **CASA_MOVEL_EDITAR** e selecione uma linha do móvel. O programa informa seu identificador, categoria e medidas atuais.
3. Informe **largura, profundidade e altura em metros**. Exemplo: `1.80`, `0.60`, `2.20`. Enter mantém o valor indicado entre `< >`.
4. O centro e a orientação da peça são preservados. Largura/profundidade acompanham a orientação local do móvel, inclusive quando está girado a 90° ou 270°.
5. Se as novas medidas couberem, o símbolo 2D e os dados internos do DWG serão atualizados juntos. Salve o DWG. **U / Desfazer** reverte a edição e os dados associados.
6. Execute **CASA_EXPORTAR**, selecione uma entidade da mesma casa e grave o JSON que será usado no Revit.

A altura é um dado para a modelagem 3D; sua alteração isolada não muda a vista superior. A edição continua disponível depois de fechar e reabrir o DWG, carregando novamente o LISP. O comando usa o snapshot do projeto gravado no desenho, sem depender da última casa gerada na sessão.

As verificações rejeitam invasão dos limites do ambiente, sobreposição com outros móveis/faixas de uso, conflitos com abertura de portas, bloqueio de janelas pela altura e altura superior ao pé-direito. A reserva de circulação permanece com a mesma espessura: ela não encolhe junto com o móvel. São verificações geométricas do protótipo, sem certificação completa de acessibilidade ou ergonomia.

A primeira faixa de edição permite largura e profundidade a partir do maior valor entre **250 mm e 65% da dimensão original**, e altura de **100 a 3.000 mm**, respeitando também o pé-direito. Ampliar depende do espaço disponível. Limites mínimos protegem os detalhes da coleção; não são normas de fabricação. O desenho não é um bloco dinâmico: use o comando para manter CAD e JSON consistentes. MOVE, SCALE e edições diretas de linhas não atualizam o modelo; um contorno deslocado/redimensionado manualmente bloqueia o comando. Os símbolos internos da peça selecionada são regenerados, portanto intervenções manuais neles serão substituídas.

Esta é a base de móveis sob medida para estudo. Ainda não inclui módulos de marcenaria independentes, chapas, ferragens, folgas de fabricação, plano de corte ou orçamento de madeira.

## Atualizar a mesma casa no Revit

1. Abra o projeto já importado e mantenha o Dynamo em **Manual**.
2. No nó PythonNet3, use o conteúdo de `programa-casa/revit/atualizar_interiores_dynamo.py`. Ele carrega os arquivos atualizados no disco; não cole `casa_interiores.py` diretamente no nó.
3. **IN[0]**: caminho completo do JSON recém-exportado. **IN[2]**: `False`.
4. Para forçar a leitura de alterações no arquivo, coloque **IN[1] = False** e execute; depois **True** e execute novamente.
5. O resultado esperado é `status = interiores_atualizados`. Confira a casa e retorne IN[1] para False.

O carregador instalado aponta para `C:\Users\mathe\OneDrive\Desktop\Arquitetura\programa-casa\revit\importar_casa_dynamo.py`. Se mover a pasta, ajuste `IMPORTADOR` no carregador. Mantenha **importar_casa_dynamo.py**, **casa_interiores.py** e **vegetacao.json** juntos. Novas importações também usam o catálogo.

O atualizador reconhece novas dimensões pelo conteúdo, e não apenas pelo número da revisão. Atualiza o DirectShape da peça existente. Deslocamentos manuais detectáveis pela caixa envolvente no Revit interrompem a transação para evitar reposicionamento silencioso. Não detecta toda alteração que conserve a mesma caixa envolvente. Vasos gerados que deixaram de caber são removidos apenas quando pertencem ao projeto e seus limites permanecem intactos; os demais casos bloqueiam a atualização. A operação inclui a auditoria de junções já existente.

## Escolher entre 15 espécies

Abra **programa-casa/revit/vegetacao.json**. A seção `selection` permite restringir as espécies usadas na inserção automática. Por padrão, listas vazias deixam o programa tentar as opções adequadas a cada ambiente. Por exemplo:

```json
"selection": {
  "indoor": ["peperomia", "espada", "camadorea"],
  "outdoor": ["areca", "rafis", "kentia"]
}
```

Use os IDs da tabela em `CATALOGO_VEGETACAO.md`. Se uma espécie não couber, o programa tenta a próxima; se nenhuma couber, omite o vaso. Não reduz uma palmeira grande para fazê-la caber num canto pequeno. **Ter 15 opções no catálogo não significa colocar 15 plantas em toda residência.** No exemplo Rodolfo foram aceitos seis vasos: espada-de-São-Jorge, jiboia, duas zamioculcas, kentia e antúrio.

Os modelos variam entre copas de palmeiras, folhas em leque, folhagens recortadas, folhas verticais, frondes, ramos e flores. São representações geométricas estilizadas em vasos, com cores sólidas; não modelos botânicos fotorrealistas. As dimensões correspondem a exemplares de estudo em vaso, incluindo a copa e a altura do vaso. **Não representam o porte adulto garantido da espécie.**

A inserção considera projeção da folhagem, margem de manutenção de 20 cm, faixas de uso dos móveis, portas, janelas, circulação e caminho de entrada. Vasos internos exigem uma janela identificada a até 2 m e altura compatível com o pé-direito. Esse teste não mede luz. Vasos externos ficam no quintal posterior, fora da casa, garagem e terraço. A preferência por espécies, suas necessidades de luz e rega e as referências constam no catálogo; a adequação ao local/clima de BH continua pendente de conferência. Não há cálculo de insolação, raízes, drenagem construtiva ou carga de jardineiras sobre lajes.

## Verificação realizada

- **AutoCAD Core 2027:** 11 verificações aprovadas na edição inicial, incluindo leitura/gravação do JSON, atualização de altura, preservação das paredes, rejeição de ampliação conflitante e restauração pelo Desfazer. O script de teste desativa seu agrupamento automático para isolar o histórico da edição.
- **Reabertura do DWG:** 10 verificações aprovadas, incluindo persistência das dimensões, identificação das peças, quatro orientações e uma segunda edição salva no snapshot.
- **Python:** 20 testes aprovados; contrato do importador, assinaturas de atualização, bloqueio de deslocamentos manuais, todas as 15 espécies, envelopes, variação dimensional e geometria dos 27 cenários CAD existentes.
- O JSON exportado pelo ensaio nativo de redimensionamento foi aceito pelo contrato do importador e pela geração de interiores.
- As prévias são renderizações das mesmas descrições geométricas usadas pelo adaptador Revit, inspecionadas visualmente. Não são capturas do Revit.

**A execução desta revisão dentro do Revit permanece pendente de validação no aplicativo.** Não foi criado um RVT nesta atualização. Os componentes de mobiliário são representações com sobreposições; seus volumes não constituem orçamento de materiais ou plano de fabricação. As espécies ainda exigem especificação de compra e verificação de cultivo no local.
