# Evolução arquitetônica do CASA-BH

Data: 07/09/2026. Proposta de requisitos; não implementa nem certifica atendimento normativo.

Direção confirmada pelo usuário: equilíbrio entre conforto e custo; integração de sala/jantar/cozinha também pode variar entre alternativas; valorizar convivência e entrada de iluminação; incluir garagem no planejamento. Isso permite gerar opções integradas, parcialmente integradas e separadas com a mesma entrada, mantendo quantidades e necessidades explícitas. A garagem exige informar veículos, dimensões e acesso antes de fixar sua geometria.

## Diagnóstico do código atual

O resultado observado é consequência direta do algoritmo `corridor-0.1`: `cg:shuffle` troca a ordem de todos os ambientes, sem distinguir setores social, íntimo e serviço. Depois, o código monta pares em duas faixas de mesma largura, separados por um corredor central. A profundidade do par é a maior profundidade predefinida dos dois cômodos, acrescida apenas de 0–300 mm. Por isso um banheiro ao lado da sala herda sua profundidade; a última peça ímpar pode ocupar toda a largura. Mudar a semente muda a distribuição, mas não a concepção da casa.

`cg:furnish` insere objetos em posições fixas junto à borda superior do ambiente. Não trabalha com ocupantes, giro de portas, gavetas, cadeiras em uso ou rotas. Janelas são escolhidas por tamanho fixo e posição geométrica. A validação de conforto está corretamente marcada como não avaliada. As cotas existentes melhoram a representação, mas não demonstram habitabilidade.

Auditoria do arquivo de exemplo da versão 0.2 pela equipe identificou banheiro de 11,36 m² e quarto de 30,10 m² frente a sala de 13,49 m². São valores do arquivo de exemplo, não medidas extraídas da captura enviada. Não são automaticamente ilegais ou inviáveis, mas ilustram distribuição de área desvinculada das prioridades dos moradores.

## Mudança de princípio

Gerar alternativas a partir de relações funcionais, depois dimensionar, mobiliar e avaliar. A aleatoriedade deve explorar soluções que cumpram o programa. Não deve decidir livremente se a cozinha fica entre dormitórios nem compensar uma colisão física por uma nota alta de estilo.

Fluxo sugerido: programa dos moradores → setores e relações → família de implantação → ambientes dimensionados pelo uso → portas e janelas → conjuntos de mobiliário e áreas de operação → rejeição dos inviáveis → classificação dos viáveis → apresentação de alternativas distintas.

## Regras eliminatórias

Separar duas naturezas: consistência técnica do aplicativo e requisitos legais aplicáveis, estes somente com fonte, versão e contexto confirmados.

| Regra | Como verificar | Natureza |
|---|---|---|
| Quantidades e equipamentos indispensáveis atendidos | Comparar entrada e saída por ID e tipo | Programa do usuário |
| Ambientes e elementos dentro da área edificável | Interseção e inclusão de polígonos, espessuras reais | Geometria + parâmetros do lote |
| Acesso a todos os ambientes | Grafo de portas e rotas desde a entrada | Consistência funcional |
| Suíte sem acesso externo obrigatório ao dormitório | Banheiro exclusivo ligado ao quarto; área de passagem válida | Programa, se suíte solicitada |
| Objetos físicos sem interpenetração indevida | Colisões 2D com faixas verticais para sobreposições permitidas | Consistência geométrica |
| Portas e equipamentos operáveis | Envelope de giro/deslizamento e de uso sem bloqueios | Especificação do objeto/perfil |
| Rotas até cada ponto de uso | Caminho contínuo com largura configurada, não apenas distância em linha reta | Perfil de uso; norma se aplicável |
| Áreas, vãos, ventilação e iluminação exigidos | Regras rastreáveis conforme legislação e norma aplicável | Legal/técnica; não fixar números genéricos |
| Critérios de acessibilidade selecionados | Aproximação, alcance, transferência, circulação e manobra juntos | Perfil e aplicabilidade normativa |

Ausência de dados legais deve produzir “não avaliado”, nunca aprovação. A PBH informa que a documentação depende das especificidades do terreno e orienta consulta à Informação Básica e ao checklist de licenciamento. [PBH — perguntas frequentes](https://prefeitura.pbh.gov.br/politica-urbana/perguntas-frequentes-smpu).

## Preferências e métricas de qualidade

Estes critérios são propostas de projeto configuráveis, não transcrições de lei.

| Objetivo | Métrica verificável | Cuidados |
|---|---|---|
| Privacidade | Número de percursos de visitantes que atravessam setor íntimo; visão direta entrada→cama/bacia | Não proibir integração desejada pelo usuário |
| Boa relação social | Distância caminhável cozinha→mesa; sala→área externa; capacidade simultânea | Medir entre pontos de uso, considerando obstáculos |
| Circulação eficiente | Área exclusiva de circulação/área útil; comprimento dos principais percursos | Não minimizar até eliminar espaços necessários |
| Quarto adequado ao morador | Cama e armazenamento requeridos + uso + acesso; desvio da área alvo | Área isolada não garante funcionalidade |
| Cozinha utilizável | Sequência armazenar/lavar/preparar/cozinhar; apoio; equipamentos abertos | Configurar um ou mais cozinheiros; não exigir triângulo em toda cozinha |
| Núcleo hidráulico racional | Distância entre pontos molhados ou comprimento estimado de redes | Proxy preliminar, não projeto hidráulico |
| Separação de ruído | Adjacências de quartos com lavanderia/equipamentos/TV | Geometria não comprova isolamento acústico |
| Relação com jardim | Área exterior utilizável conectada aos ambientes previstos | Jardim residual estreito não equivale a pátio habitável |
| Potencial de luz natural | Relação abertura/ambiente, profundidade, orientação e obstruções | Proxy; não declarar desempenho lumínico sem método apropriado |
| Potencial de ventilação | Rede de aberturas efetivas e conexões internas até fachadas | Porta de dormitório aberta permanentemente não é premissa aceitável automática |
| Custo/compacidade | Área bruta, perímetro/área, recortes e extensão de paredes | Estimativa comparativa, não orçamento |
| Diversidade das alternativas | Diferenças de grafo, implantação, proporções e relação com exterior | Espelhar ou trocar etiquetas não conta como nova tipologia |

Apresentar notas por critério, falhas, dados ausentes e vantagens concretas. Inicialmente é melhor um painel multicritério do que uma nota única “qualidade 95%”. Pesos devem ser visíveis e configuráveis. Eliminar candidatos inválidos antes de pontuar os restantes.

## Tipologias a implementar

1. **Compacta setorizada:** social na frente, serviço junto à cozinha, íntimo ao fundo, pequeno distribuidor. Boa primeira alternativa ao corredor completo. Sala e jantar podem ser integrados mediante opção.
2. **Faixa lateral:** ambientes servidos por circulação curta junto a uma lateral ou sucessão de distribuidores; relação direta com jardim lateral. Precisa testar comprimento de percursos e privacidade, pois pode apenas deslocar o mesmo corredor ruim.
3. **Planta em L:** duas alas distinguem social e íntimo, associadas a jardim/pátio. Exige largura suficiente e avaliação de perímetro/custo. A posição do L deve responder ao lote e orientação.
4. **Pátio:** ambientes voltados a espaço aberto interior, com setores conectados. Para etapa posterior: pátio precisa dimensões e aberturas válidas; mais fachadas podem aumentar custo e perdas/ganhos térmicos.
5. **Compacta com núcleo molhado:** banheiros, cozinha e serviço próximos; dormitórios e sala nas fachadas. Não aceitar ambiente de permanência sem condição válida de iluminação/ventilação só para compactar redes.

A primeira entrega arquitetônica deve produzir pelo menos três famílias de organização, mantendo o corredor atual como referência. Dentro de cada uma: variar áreas alvo, posição dos setores, integração, posição/rotação dos móveis e aberturas. Não prometer que toda tipologia cabe em todo lote.

## Dimensionamento dirigido ao uso

Substituir profundidade fixa por `min_area`, `target_area`, `max_area`, dimensões livres mínimas justificadas e conjunto funcional. A primeira estimativa vem da população: casal, individual, duas pessoas, hóspede, trabalho, morador com necessidades específicas. O móvel e sua área de operação fazem parte da composição do cômodo.

Evitar perfis “econômico = apertado” e “confortável = grande” sem verificação. Um ambiente maior pode continuar ruim se a porta, a janela e o armário bloqueiam o uso. Valores numéricos iniciais de projeto devem aparecer identificados como hipóteses ajustáveis, separados dos números extraídos de normas.

## Conforto ambiental com evidência

Solicitar norte verdadeiro relativo ao desenho, frente/rua, obstruções vizinhas e preferências de ventilação. Se faltarem, declarar hipóteses de ensaio e impedir conclusão climática. Não escolher automaticamente “todos os quartos a leste”: incidência, sombreamento, ocupação e clima precisam ser considerados juntos.

O ProjetEEE reúne estratégias de sombreamento, ventilação e inércia térmica adequadas ao estudo bioclimático. A própria plataforma orienta considerar o movimento do ar entre os cômodos e a posição das divisórias; duas janelas desenhadas não demonstram ventilação cruzada. [Estratégias](https://www.mme.gov.br/projeteee/estrategias-bioclimaticas/), [Fluxo entre ambientes](https://projeteee.mme.gov.br/implementacao/ventilacao-cruzada-plantas-abertas/?cod=vn).

A relação entre forma/orientação e ventilação depende da direção dos ventos conhecida. Isso sustenta comparar implantações, sem transformar uma forma em L em garantia universal de conforto. [ProjetEEE — volumetria](https://projeteee.mme.gov.br/implementacao/ventilacao-cruzada-volumetria/?cod=vn).

O LabEEE identifica seu mapa como atualização da NBR 15220-3 de 2024. Portanto não reutilizar automaticamente classificações climáticas antigas existentes em guias. [LabEEE — zoneamento](https://labeee.ufsc.br/zoneamento/). Para avaliação térmica real, a etapa posterior precisará ainda clima, materiais, cobertura, vidros, sombreamento e ocupação.

## Estilo

Estilo deve controlar decisões observáveis: integração dos ambientes, relação com varanda/jardim, proporção das aberturas, modulação, cobertura, materiais e catálogo de mobiliário. “Contemporâneo” sozinho é ambíguo. Solicitar duas ou três referências visuais e identificar atributos, sem copiar automaticamente a planta da referência.

Começar por três escolhas funcionais: cozinha aberta/fechada; social integrado/separado; prioridade compacidade/jardim/receber visitas. Depois adicionar aparência. Renderização bonita não deve elevar a nota funcional de uma planta bloqueada.

## Perguntas de maior impacto

- Qual lote de teste (largura × profundidade) e qual limite desejado de área construída?
- Quantas pessoas morarão e como os quartos serão usados (casal, individual, compartilhado, hóspede)? Há suítes?
- Cozinha aberta ou fechada, e sala/jantar integrados ou separados?
- Garagem, varanda, escritório, despensa e área externa entram no programa?
- Quais prioridades prevalecem: economia, privacidade, receber pessoas, acessibilidade, jardim ou possibilidade de expansão?
- Há norte/posição da rua definidos ou usamos cenário hipotético claramente identificado? Quais referências de estilo agradam?

Parte já respondida: perfil equilibrado e integração variável. Essas preferências não devem ser perguntadas novamente; falta detalhar o lote, ocupantes, programa e garagem.

## Critérios de aceite da próxima etapa

- Nenhum cômodo muda de tamanho apenas porque ficou emparelhado com outro maior.
- A semente explora soluções dentro de relações funcionais válidas.
- Todo móvel obrigatório aparece ou a alternativa é rejeitada com motivo.
- Portas abertas, armários e cadeiras em uso são verificados, além de colisões de caixas.
- Alternativas exibidas têm diferenças reais de implantação ou organização, não só ordem e espelhamento.
- Áreas, métricas e hipóteses acompanham o DWG/JSON; orientação e IDs seguem para o Revit.
- Prévia compara a mesma entrada em diferentes tipologias e informa quais critérios ainda não foram avaliados.

Este relatório complementa `pesquisa-interiores/PESQUISA.md` e `planejamento-bh/BASE-BH.md`; não substitui a confirmação normativa nem a revisão do projeto por responsável técnico.
