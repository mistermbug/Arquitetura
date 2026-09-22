# Evolução do gerador arquitetônico — proposta baseada no código 0.2

Data: 7 de setembro de 2026. Este documento propõe mudanças; não representa funcionalidades já implementadas. A análise é do código local, não uma validação normativa ou um ensaio de desempenho de um motor novo.

Preferências já confirmadas pelo usuário: equilíbrio entre custo e conforto; comparar integração aberta, semifechada e fechada entre alternativas; casas e ambientes com organizações diferentes; prioridade para garagem, convivência e luz natural. Não voltar a perguntar essas preferências como se estivessem indefinidas.

## Por que as plantas atuais parecem iguais

Em `casa-core.lsp`, `cg:generate` constrói apenas uma tipologia: corredor central com duas faixas de ambientes de igual largura. A semente embaralha os tipos de cômodo, mas não escolhe uma organização arquitetônica diferente. Cada dupla recebe a profundidade do maior cômodo do par, somada a uma variação de apenas 0–300 mm. Um banheiro ao lado de uma sala herda praticamente a profundidade da sala. Quando sobra um ambiente, ele ocupa toda a largura no fundo. Isso explica diferenças pequenas, ambientes desproporcionais e setorização aleatória.

`cg:furnish` usa coordenadas fixas por tipo, contém poucos objetos e não busca arranjos. Verificar que um retângulo cabe no ambiente não garante que uma pessoa consiga abrir a porta, usar o armário ou circular entre os móveis. O campo `COMFORT = not_evaluated` identifica corretamente essa limitação.

Os testes existentes verificam a consistência do protótipo. Passar milhares de verificações desse contrato não demonstra qualidade arquitetônica, diversidade, conforto térmico ou aprovação legal.

## Decisão sugerida

Manter um único `CASA-BH.lsp` para o usuário carregar no AutoCAD, mas manter os módulos internos separados no desenvolvimento. O processo de empacotamento já existente pode continuar a reunir núcleo, adaptador e formulário. Um único arquivo entregue não exige uma única função de geração.

Na próxima versão, implementar um gerador de alternativas **ortogonais e térreas**, com três organizações inicialmente retangulares. Cada organização recebe dimensões variáveis, adjacências explícitas e testes de uso de mobiliário. Só depois acrescentar perímetros em L ou pátio, que exigem alterações reais no contrato geométrico.

Não começar por gerar milhares de retângulos sem estrutura e tentar corrigir os resultados. Usar estruturas arquitetônicas reconhecíveis, depois procurar dimensões e configurações de portas, janelas e móveis compatíveis com elas.

## Fluxo de geração

1. **Interpretar o programa:** criar uma instância por ambiente com identificador estável, ocupação, faixa de área, dimensões mínimas de projeto, proporção admissível e conjunto de móveis obrigatório/opcional. Texto livre precisa ser convertido para campos revisáveis antes de gerar.
2. **Montar relações:** quais espaços devem se conectar por porta, quais precisam estar próximos, quais devem ser separados e quais precisam de contato com área externa. Adjacência geométrica, acesso direto e proximidade são relações diferentes.
3. **Escolher organizações admissíveis:** eliminar previamente as incompatíveis com largura, área disponível e programa. Distribuir tentativas entre tipologias para impedir que uma única domine a busca.
4. **Dimensionar:** variar largura e profundidade de cada setor em uma malha configurável; respeitar as espessuras interna e externa. Repartir primeiro a área desejada por função, não pelo maior cômodo de cada dupla.
5. **Derivar paredes:** construir segmentos compartilhados a partir das regiões. Dividir segmentos em interseções em T, eliminar duplicações parciais e classificar parede externa/interna. `cg:add-wall` hoje só elimina segmentos inteiramente iguais; isso é insuficiente para a nova composição.
6. **Resolver acessos e aberturas:** procurar posições e sentidos de abertura válidos. Criar um grafo de acesso percorrível a partir da entrada. Reservar trechos exteriores para janelas antes de ocupar todas as paredes com armários.
7. **Mobiliar:** testar arranjos de catálogo por ambiente, orientações ortogonais e posições candidatas, considerando zonas de uso. Rejeitar ou redimensionar quando o mobiliário obrigatório não funcionar.
8. **Validar e pontuar:** eliminar violações obrigatórias, calcular os indicadores aplicáveis e conservar alternativas diversas.
9. **Apresentar:** mostrar três a cinco alternativas com área, tipologia, vantagens e pendências. Selecionar uma para desenhar e exportar. Não gravar todas automaticamente no DWG sem escolha.

Pseudocódigo sugerido:

```text
programa = normalizar(entradas)
restricoes = carregar_perfil_regras(versao, contexto)
arquivo_alternativas = []
para tipologia em tipologias_admissiveis(programa, lote):
    para tentativa em orcamento_da_tipologia:
        candidato = instanciar_setores(tipologia, programa, semente)
        candidato = dimensionar_e_conectar(candidato)
        candidato = posicionar_aberturas_e_moveis(candidato)
        verificacao = verificar_obrigatorias(candidato, restricoes)
        se verificacao.tem_falha: registrar_motivos_e_continuar
        indicadores = avaliar_preferencias(candidato, contexto)
        inserir_se_diverso(arquivo_alternativas, candidato, indicadores)
retornar alternativas_ou_diagnostico_limitado_da_busca
```

"Nenhuma solução encontrada neste conjunto de tentativas" não deve ser apresentado como prova de que é impossível construir naquele lote.

## Três primeiras organizações

| Organização | O que muda de fato | Cuidados |
|---|---|---|
| Social na frente, íntimo nos fundos | Sala/jantar podem ocupar largura maior; quartos em setor privado; cozinha próxima ao serviço | Evitar rota de visita passando por dormitórios; garantir saída e iluminação dos ambientes do fundo |
| Circulação lateral | Larguras deixam de ser duas faixas iguais; permite salas largas e quartos independentes | Controlar área de corredor, portas e fachada externa disponível |
| Núcleo de distribuição curto | Pequeno hall distribui área íntima; social e serviço ocupam setores conectados | O grafo precisa assegurar acesso sem atravessar quartos ou banheiros |

Espelhamento e giro podem ser úteis para orientação ou acesso, mas não devem contar sozinhos como tipologias diferentes no indicador de diversidade. Um lote estreito pode comportar apenas uma dessas organizações; nesse caso o sistema deve informar a limitação.

Planta em L, pátio e dois pavimentos ficam em etapas posteriores. Um vazio de pátio não pode ser representado como piso construído só porque cabe no retângulo envolvente.

## Regras obrigatórias, preferências e informação ausente

**Obrigatórias geométricas e de programa:** contagens, ambientes contidos no envelope permitido, áreas sem sobreposição, paredes de espessura correta, aberturas dentro das paredes, acesso conectado, móveis essenciais presentes, ausência de colisões e zonas de uso respeitadas segundo o perfil adotado.

**Preferências configuráveis:** corredor menor, privacidade, sala/jantar/cozinha próximos, agrupamento de instalações, áreas próximas das desejadas, ambientes menos alongados, extensão de fachada externa e oportunidades de ventilação. Uma preferência não pode compensar uma violação obrigatória através de uma nota alta.

**Legislação e normas:** manter cada requisito com fonte, versão, hipótese de aplicação e estado de verificação. Parâmetros provisórios de projeto não devem receber o rótulo de mínimo legal. Dados do lote ainda ausentes resultam em `not_evaluated`, não em aprovação implícita.

**Conforto ambiental:** contato com fachada e presença de janelas são indicadores geométricos, não comprovação de iluminação ou desempenho térmico. Sem norte, obstruções, propriedades construtivas e condições climáticas, não atribuir uma nota de conforto térmico como se houvesse simulação. Guardar os dados necessários agora permite avaliação posterior sem reconstruir o projeto.

## Pontuação explicável e diversidade

Preferir apresentação de indicadores separados a uma nota única opaca. Se houver classificação ponderada, normalizar os indicadores e guardar pesos, versão e justificativa. Exemplos de métricas computáveis:

- Área de circulação exclusiva dividida pela área útil total.
- Desvio da área de cada ambiente em relação à faixa desejada, separando insuficiência de excesso.
- Comprimento dos percursos no grafo de circulação; o teste final precisa considerar os obstáculos, não só a distância em linha reta.
- Quantidade de acessos indesejados, como entrada da casa diretamente no setor íntimo, segundo a preferência definida.
- Quantidade de itens essenciais atendidos e zonas de uso livres.
- Distância entre cozinha, lavanderia e banheiros como aproximação de concentração de instalações, sem alegar dimensionamento hidráulico.

Para diversidade, registrar assinatura da tipologia, relações de adjacência, distribuição das áreas e posição relativa dos setores. Comparar após normalização de translação; tratar espelhamentos equivalentes como similares quando norte e acesso não distinguirem as soluções. Eliminar cópias com mera troca de nome de quartos. Reservar ao menos um candidato de cada tipologia viável antes de completar a seleção pelos melhores indicadores.

Para o perfil confirmado, tratar custo e conforto como objetivos que podem competir. Mostrar um conjunto de alternativas não dominadas: uma alternativa domina outra apenas se não piora nenhum dos indicadores considerados e melhora pelo menos um. Reduzir depois esse conjunto por diversidade e legibilidade. Comprimento de paredes, área construída, perímetro e concentração de áreas molhadas podem funcionar como indicadores preliminares de complexidade/custo, mas não como orçamento em reais. Conforto deve separar uso dos ambientes, convivência e oportunidades de iluminação; luz efetiva depende de aberturas, orientação e obstruções.

Distribuir as tentativas por combinações de tipologia com integração aberta, semifechada e fechada. Na opção aberta, sala/jantar/cozinha podem ser zonas de uso de um único espaço, em vez de três recintos fechados artificiais. Isso exige representar `zones` e a relação com um recinto real; se o usuário pedir quantidades de cômodos, esclarecer na interface a diferença entre ambientes funcionais e recintos fechados. Revit deve receber um recinto coerente com seus limites e zonas identificáveis, não três Rooms sobrepostos. A opção semifechada precisa declarar quais painéis/portas/divisórias criam a separação. A opção fechada exige conexões diretas funcionais. Não basta trocar um símbolo de porta.

A garagem passa a integrar o programa prioritário e deve ser reservada junto ao acesso, considerando quantidade/dimensões de veículos, portão, desembarque e circulação a pé; ela compete com fachada iluminante e convivência, por isso deve entrar antes do encaixe dos quartos. A largura do carro sozinho não comprova usabilidade da vaga. Sem dimensões e acessos do lote definidos, registrar o pressuposto de ensaio e pedir esses dados para o caso real.

## O que reaproveitar e o que adaptar no código atual

| Componente | Reaproveitamento | Adaptação necessária |
|---|---|---|
| Entrada e entrega em um LISP | Sim | Novos campos e seleção de alternativas; preservar valores anteriores |
| JSON, IDs e armazenamento no DWG | Sim | Acrescentar versão do gerador, tipologia, métricas, parâmetros e regras aplicadas |
| `cg:draw-wall` | Parcial | Exige eixos ortogonais em direção crescente; normalizar segmentos, tratar encontros e aberturas compartilhadas |
| `cg:draw-opening` | Parcial | O sentido da porta é inferido e portas horizontais abrem sempre no mesmo sentido; inserir dobradiça, lado e direção explicitamente |
| `cg:draw-model` | Parcial | Cotas e corte assumem `CIRC` e duas faixas. Gerar cotas a partir da geometria; corte deve intersectar paredes reais |
| Móveis CAD | Parcial | Símbolos por família, orientação e zonas de operação; retângulo exterior permanece útil para detecção de colisão |
| Revit paredes | Sim para paredes retas | Preservar posição, espessura, papel e IDs; continuar verificando junções e recintos |
| Revit aberturas | Parcial | Vãos atuais não são famílias completas de portas/janelas. Adicionar catálogo e mapeamento de famílias em etapa própria |
| Revit móveis | Parcial | Volumes atuais são caixas extrudadas. Acrescentar chave de família/tipo, ponto de inserção e rotação para modelos detalhados |
| Piso, área e perímetro | Sim para retângulos | `slab.bounds` é apenas retangular. L/pátio exigem laços de contorno e vazios, cálculo de área por polígono e atualização do importador |
| Ambientes | Sim para retângulos | Centro do retângulo funciona para as primeiras tipologias. Polígonos côncavos exigem ponto interior garantido |

Compatibilidade incremental: manter o contrato 1.0 para as primeiras tipologias retangulares e acrescentar metadados opcionais. Quando a representação mudar para polígonos/pisos com vazios, criar uma nova versão explícita, validadores e conversor; o importador atual rejeita versões diferentes de `1.0` e não deve receber dados novos silenciosamente.

## AutoLISP puro ou motor externo

Para uma biblioteca pequena de tipologias, ambientes retangulares, amostragem limitada e verificações de colisão ortogonal, AutoLISP puro é uma opção coerente com o produto atual. Mantém instalação simples e permite aproveitar os testes reais em AutoCAD. Será preciso separar geração, verificação e desenho para testar tentativas sem criar entidades no DWG.

Um motor externo passa a ser atraente para geometria mais complexa, busca maior, restrições combinatórias, simulações e manutenção de catálogos. O desenho, cotas, seleção, armazenamento e exportação podem continuar no LISP; a troca seria por um contrato de dados documentado. Isso acrescenta instalação, processo externo, caminhos, mensagens de erro e versionamento, portanto não é uma melhoria gratuita. Não há ensaio neste estudo que permita afirmar uma velocidade específica ou garantir que determinada biblioteca resolve o projeto.

Recomendação: desenvolver primeiro a arquitetura de dados e o verificador independente em módulos, entregar a próxima melhoria no LISP e medir tempo de busca e taxa de soluções válidas. Se os resultados exigirem motor externo, migrar apenas a geração/verificação. O usuário continuará carregando um LISP, mas precisará instalar o motor; essa dependência deve ser declarada. Um modelo de linguagem pode estruturar o pedido e explicar alternativas, mas não substituir o verificador geométrico e normativo.

## Roadmap com critérios de aceitação

1. **Contrato arquitetônico e casos de referência.** Definir um programa de três quartos incluindo perfis distintos, conjuntos de móveis, faixas de áreas e relações. Criar também casos de lote estreito, programa incompatível e acessibilidade solicitada. Aceitação: requisitos e hipóteses reproduzíveis, sem valores legais inventados.
2. **Verificador antes de novas tipologias.** Colisões, zonas de uso, portas e grafo de acesso. Aceitação: exemplos propositalmente ruins são rejeitados com motivo; casos válidos conhecidos passam. Evitar apenas testar o que a própria função acabou de produzir.
3. **Primeira tipologia setorizada e dimensões variáveis.** Separar áreas sociais, íntimas e de serviço, sem herdar a profundidade do maior par. Aceitação: sala, banheiro e quartos atingem suas faixas individuais; acesso não cruza cômodos privados indevidamente.
4. **Mobiliário completo por perfil.** Testar mais de um arranjo para cama/armário, estar, cozinha, mesa/cadeiras, banho e serviço. Aceitação: todos os itens essenciais e suas zonas de operação cabem, portas funcionam e existe percurso contínuo até os pontos de uso.
5. **Busca de três organizações e seleção diversa.** Aceitação: no lote de referência, apresentar três soluções com organização diferente, sem contar simples espelhos; repetir entrada e semente reproduz os resultados. Se uma tipologia não couber, informar em vez de forçar.
6. **Integração CAD/Revit sem regressões.** Aceitação: cotas medem a geometria nova, corte mostra os elementos interceptados, espessuras permanecem corretas, DWG reaberto conserva os dados, JSON valida; depois ensaio no Revit instalado com volumes e posições comparados ao CAD.
7. **Contexto e estilo.** Acrescentar norte, frente, entorno e preferências; materiais e linguagem de fachada devem ter parâmetros próprios. Aceitação: explicar o efeito de cada dado e manter conforto não calculado claramente pendente. Estilo decorativo não deve determinar sozinho a planta.
8. **L/pátio, desempenho e terrenos reais.** Evoluir contrato, pisos e ambientes poligonais; adicionar dados topográficos e avaliações especializadas com fontes adequadas. Aceitação: área construída não inclui vazios e nenhum importador usa retângulo envolvente como geometria real.

## Decisões do usuário que mais influenciam a próxima versão

- Perfil dos quartos e dos moradores: casal, solteiro, duas camas, suíte, crianças, idoso ou uso acessível.
- Área construída desejada e dimensões do primeiro lote de referência.
- Quantidade de vagas e veículos de referência; garagem coberta ou descoberta, varanda, lavabo e suíte.
- Dimensões e orientação das aberturas disponíveis no lote de referência, além de possíveis obstruções do entorno, para evoluir da oportunidade geométrica de luz para uma avaliação informada.
- Possibilidade de instalar um motor auxiliar posteriormente, mantendo o LISP como comando do AutoCAD.

Essas escolhas podem ter padrões iniciais explícitos, mas não devem ser interpretadas como requisitos legais ou preferências já confirmadas.
