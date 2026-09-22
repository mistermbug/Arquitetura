> Revisão de interiores `0.4-interiores-2`: dimensões editadas por CASA_MOVEL_EDITAR são atualizadas pelo carregador de interiores com IN[2]=False. Mantenha vegetacao.json junto a casa_interiores.py. Consulte ../entrega-0.4/MOVEIS_PLANEJADOS_E_VEGETACAO.md para o fluxo atual e as 15 espécies.

# Ponte AutoCAD → Revit: primeira implementação

**Nova coleção `0.4-interiores-1`:** móveis originais detalhados e vasos com folhagem. Para atualizar a casa existente, use `atualizar_interiores_dynamo.py` no nó PythonNet3, com o mesmo JSON e IN[2]=False. A execução reúne junções das paredes, mobiliário e vegetação em uma transação. Leia `../entrega-0.4/MELHORIAS_INTERIORES.md` no projeto-fonte, ou `../MELHORIAS_INTERIORES.md` no ZIP. A API desta revisão ainda precisa de confirmação no Revit.

## Revisão 0.4-joins-1: uniões e conferência geométrica

O importador agora habilita junções nativas das paredes geradas e platibandas depois de criar seus vãos. Se ainda existir interseção volumétrica, tenta a união explícita de geometria. O resultado é auditado por interseção dos sólidos reais, não pela aparência das linhas. Sobreposição residual superior a 0,000001 m³ (1 cm³) por par, ou falha no cálculo booleano, interrompe e reverte a operação.

O campo `quantity_audit` no Watch contém volumes geométricos antes/depois, volumes por parede e o parâmetro Volume do Revit. O volume total não necessariamente diminui: junções podem completar cantos além de retirar sobreposições. A auditoria cobre paredes e platibandas do projeto importado, não todas as categorias do edifício. A tolerância é por par, e não uma garantia absoluta de erro zero.

### Corrigir a casa que já está no Revit

1. Use o mesmo projeto Revit e o mesmo JSON da casa importada.
2. Deixe `IN[1]=False` e `IN[2]=False`.
3. Substitua o código do nó Python existente pelo conteúdo de `corrigir_unioes_dynamo.py` e salve. Esse arquivo é um carregador; confira o caminho `IMPORTADOR` se usar outra pasta/computador.
4. Passe `IN[1]` para True e execute uma vez, em modo Manual. Sucesso: `status=unioes_corrigidas` e `quantity_audit.status=sem_sobreposicao_detectada`.
5. Volte `IN[1]` para False, confira planta, 3D, aberturas e volumes, e salve o RVT.

A rotina preserva os elementos e identificações existentes; não apaga nem recria a casa. Falta de paredes originais ou ambientes sem área após a correção interrompe a operação. Para proteger paredes fora do projeto gerado, a operação é recusada se houver outra parede a menos de 1 m das caixas geométricas das paredes alvo. Essa distância é uma proteção conservadora da rotina, não uma regra arquitetônica.

Novas importações usam `importar_casa_dynamo.py` completo e passam pela mesma correção. Os oito testes Python e o JSON do usuário passaram; isso não executa a API. `test_unioes_revit_dynamo.py` é um ensaio nativo separado, com encontros L/T/X/colineares e volumes de referência, para um projeto vazio descartável; ele ainda precisa ser executado no Revit. Nenhum sucesso nativo dessa revisão foi confirmado nesta entrega.

Para orçamento de materiais ainda será necessário especificar camadas, materiais, aberturas/famílias, critérios de medição, perdas e composições. As paredes atuais têm uma camada genérica; seus volumes não equivalem automaticamente a quantidades de blocos, argamassa, revestimento ou custo de obra.

Revisão `0.4-endcap-1`: corrigido o erro `Input compound structure has wrong EndCap condition for this element type`. Pisos da casa, cobertura e pisos externos recebem explicitamente `EndCapCondition.NoEndCap`; paredes e platibandas usam estrutura vertical de uma camada. A mensagem de erro agora identifica a etapa e inclui o traceback Python. Reabra o arquivo Python e substitua todo o código no nó já existente; atualizar o arquivo no disco não altera o código colado no Dynamo. A correção ainda precisa de nova execução no documento Revit.

`importar_casa_dynamo.py` usa a API real do Revit dentro do Dynamo. Não precisa de pyRevit, pacotes externos, ChatGPT conectado ou importação DWG. Não é uma sincronização bidirecional.

## Executar

1. Exporte o JSON do programa AutoLISP. Trabalhe primeiro em uma cópia ou projeto Revit vazio baseado em template arquitetônico.
2. No Revit, abra **Gerenciar → Dynamo**, crie um grafo e selecione execução **Manual**.
3. Insira um nó **Python Script**, escolha o mecanismo **PythonNet3** no Revit 2027 e cole todo o conteúdo de `importar_casa_dynamo.py`. Não use IronPython. Adicione entradas até aparecerem IN[0], IN[1] e IN[2].
4. Conecte um nó **String** com o caminho absoluto do JSON em IN[0]. Conecte Boolean **False** em IN[1] e **False** em IN[2].
5. Passe IN[1] para **True** e execute uma vez. Inspecione OUT em um nó Watch. `status=importado` confirma a transação. Salve o RVT após conferir planta e vista 3D.
6. Volte IN[1] a False para evitar execuções acidentais.

Entradas ausentes/execução desativada não alteram o documento. JSON inválido é rejeitado antes de abrir uma transação. O script foi escrito para a API disponível no Revit 2024–2027; a instalação e versão do Revit do usuário ainda precisam de teste real. A sintaxe Python foi verificada fora do Revit; isso não comprova execução da API.

## Elementos e limites

- Paredes nativas, em eixos do JSON, com tipos novos de camada única na espessura solicitada. Junções habilitadas e geometria auditada na revisão 0.4-joins-1, conforme o escopo acima. O tratamento de camadas e materiais para orçamento ainda precisa de desenvolvimento.
- Piso nativo com contorno real de `slab.outline`, inclusive recortes, com espessura solicitada e topo no nível zero. JSONs antigos sem outline continuam usando retângulo. Sem estrutura calculada.
- Na versão 0.4, `roof` gera uma **laje de cobertura nativa na categoria Piso**, com face inferior na altura das paredes, espessura de 150 mm e platibanda nativa de 600 mm de altura e 100 mm de espessura. São valores de representação, não dimensionamento. O contorno acompanha os recortes do piso; não preenche o pátio. Caimentos, drenagem, impermeabilização, estrutura e acabamento térmico ainda precisam de projeto. Não há telhado inclinado nem objeto Roof.
- Na versão 0.3, `outdoor` produz pisos nativos separados para garagem descoberta e terraço, sem cobertura nem ambientes Revit. A espessura padrão desses pisos é 100 mm, parâmetro de representação e não dimensionamento estrutural. Veículos são volumes 3D esquemáticos, assim como os móveis.
- Um nível próprio em elevação zero, sem vistas novas automáticas.
- Ambientes nativos colocados no centro do retângulo informado; importação revertida se o Revit detectar ambientes sem área ou redundantes. Áreas reais dependem das paredes e das configurações de cálculo do Revit.
- Sala/jantar/cozinha integrados formam um único recinto Revit. As funções em `zones` são preservadas na saída `zones_from_cad`; não criam ambientes sobrepostos nem separadores artificiais. Norte e opções de organização são devolvidos em `design_metadata`; o importador não gira o projeto, ajusta o Norte Verdadeiro ou realiza simulação ambiental.
- Portas e janelas viram **aberturas retangulares reais nas paredes**, sem folhas, caixilhos, ferragens ou famílias de portas/janelas. Portanto não entram como portas/janelas nativas em tabelas dessas categorias.
- Móveis recebem **modelos DirectShape detalhados na categoria Mobiliário**, com rotação/espelhamento e proporções baseadas no JSON. São peças originais de estudo com cores de materiais. Ainda não são famílias RFA paramétricas nem produtos especificados de fabricantes. Vegetação em vasos recebe categoria Plantio, quando aceita pela API.
- Sem cotas Revit, pranchas, vistas de cortes/fachadas, materiais especificados ou instalações. As cotas/textos produzidos pelo AutoLISP permanecem no CAD. O resultado é estudo preliminar, não projeto executivo ou aprovado.

## Reimportação e proteção

Cada elemento e tipo criado recebe Extensible Storage com namespace `casa-autolisp`, `project_id`, `source_id` e `kind`. O UUID do esquema é fixo. Mantenha o mesmo `project_id` para atualizar uma alternativa; use outro projeto para manter duas alternativas.

Por padrão, importar novamente o mesmo projeto é **bloqueado**, inclusive quando o JSON não mudou. Não há detecção automática de mudanças manuais nem atualização elemento a elemento nesta versão.

**IN[2]=True é autorização explícita para apagar e recriar todos os elementos/tipos gerados desse projeto, inclusive alterações manuais feitas neles.** Essa política evita sobrescrever silenciosamente edições. Não use True para preservar essas alterações. Elementos sem a identificação do importador não são alvo da substituição. Se apagar os gerados também apagaria dependentes não gerados (por exemplo uma dimensão, vista vinculada ao nível ou família manual hospedada na parede), a operação inteira é revertida. Um erro na criação também reverte a exclusão anterior. A operação é uma única transação do Revit.

## Contrato 1.0

Todas as medidas são **milímetros**. `start`, `end`, `center` e `bounds` já são coordenadas globais WCS. `origin` é metadado e **não é somado**. Esta versão admite apenas terreno plano e um pavimento em Z=0. IDs precisam ser únicos entre todas as coleções (inclusive opcionais `zones` e `outdoor`) e não podem começar com `__`. O schema permanece 1.0; JSONs das versões 0.1 e 0.2 continuam aceitos.

Extensões opcionais da versão 0.3:

- `zones`: lista de `{id, room_id, kind, bounds}`, com retângulo contido no recinto indicado.
- `outdoor`: lista de `{id, kind, bounds, thickness?}`, em que `kind` é `garage` ou `terrace`. Retângulos externos não podem sobrepor o piso da casa nem uns aos outros.
- `furniture.room_id`: pode referenciar recinto ou área externa; o móvel precisa estar contido nesse retângulo. O campo ausente continua aceito por compatibilidade.
- `openings.door_style`: `hinged`, `sliding` ou `passage`. Todos continuam gerando somente abertura retangular no Revit.
- `north` (graus, nome emitido pelo gerador), `north_degrees` (alias), `layout` e `integration`: metadados informativos devolvidos em `design_metadata`, sem rotação ou atribuição automática a parâmetros Revit.

Execute `python test_validate.py` para verificar compatibilidade antiga, extensões e rejeição de geometrias/referências inválidas. Esses testes são de contrato de dados; a aceitação da API exige o ensaio abaixo no Revit.

Extensões opcionais da versão 0.4:

- `footprint` e `slab.outline`: mesmos vértices XY externos em sentido anti-horário, sem repetir o primeiro vértice. Polígono ortogonal simples, área positiva. `slab.bounds` permanece a caixa delimitadora. A validação verifica área real, inclusive recortes, para conter os recintos e rejeitar sobreposição com pisos externos.
- `roof`: `{kind: "flat_slab", outline, base_z, thickness, parapet_height, parapet_thickness}`. A face inferior é `base_z` e a superior é `base_z + thickness`. A platibanda começa nesta face superior. O contorno deve ser igual ao do piso. Campos em milímetros.
- `entry_path`: metadado do percurso de acesso, devolvido em `design_metadata`; não cria um novo piso automaticamente.
- Os limites de mobiliário são coordenadas globais já transformadas. O importador não gira novamente os volumes; continua usando o retângulo envolvente que recebeu.

```json
{
  "schema_version": "1.0",
  "project_id": "exemplo-estavel",
  "units": "mm",
  "origin": [0, 0, 0],
  "walls": [{"id":"w1","start":[0,0],"end":[5000,0],"thickness":150,"height":2800}],
  "openings": [{"id":"o1","wall_id":"w1","kind":"door","center":[1000,0],"width":800,"height":2100,"sill":0}],
  "rooms": [{"id":"r1","name":"Quarto","kind":"bedroom","bounds":[75,75,4925,3925]}],
  "furniture": [{"id":"f1","kind":"bed","bounds":[200,200,1580,2080],"height":550}],
  "slab": {"bounds":[-75,-75,5075,4075],"thickness":150},
  "validations": []
}
```

O exemplo acima explica os campos; tem apenas uma parede e **não é um cômodo fechado importável**. Use o JSON completo gerado pelo AutoLISP para o ensaio de ponta a ponta. `kind` de abertura aceita `door` ou `window`. Aberturas devem estar no eixo, dentro do comprimento e abaixo do topo da parede, sem sobreposição.

## Teste de aceitação no Revit

1. Importar uma casa, conferir espessuras, alturas, cotas de referência no CAD e posição dos móveis.
2. Verificar que aberturas atravessam paredes e que os ambientes têm áreas positivas.
3. Reexecutar com IN[2]=False: conferir bloqueio e ausência de duplicatas.
4. Alterar JSON e executar com IN[2]=True: conferir substituição e contagens, sem duplicatas.
5. Hospedar uma família manual numa parede gerada e tentar substituir: conferir bloqueio/reversão e preservação do modelo anterior.
6. Forçar um ambiente não fechado: conferir reversão completa.

## Referências oficiais consultadas

- [Autodesk: DirectShape e categoria/SetShape](https://help.autodesk.com/cloudhelp/2024/ENU/Revit-API/files/Revit_API_Developers_Guide/Revit_Geometric_Elements/Revit_API_Revit_API_Developers_Guide_Revit_Geometric_Elements_DirectShape_html.html).
- [Autodesk: aberturas nas paredes](https://help.autodesk.com/cloudhelp/2024/PTB/Revit-API/files/Revit_API_Developers_Guide/Revit_Geometric_Elements/Walls_Floors_Ceilings_Roofs_and_Openings/Revit_API_Revit_API_Developers_Guide_Revit_Geometric_Elements_Walls_Floors_Ceilings_Roofs_and_Openings_Opening_html.html).
- [Autodesk: CompoundStructure](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API-MainReference/files/html/dc1a081e-8dab-565f-145d-a429098d353c.htm).
- [Autodesk: pisos e Floor.Create](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API/files/Revit_API_Developers_Guide/Revit_Geometric_Elements/Walls_Floors_Ceilings_Roofs_and_Openings/Revit_API_Revit_API_Developers_Guide_Revit_Geometric_Elements_Walls_Floors_Ceilings_Roofs_and_Openings_Floors_Ceilings_and_Foundations_html.html).
- [Autodesk: Extensible Storage](https://help.autodesk.com/cloudhelp/2017/DEU/Revit-API/files/GUID-113B09CA-DBBB-41A7-8021-005663B267AE.htm).
