# Evolução arquitetônica do CASA BH

Data: 07/09/2026. Estado: diagnóstico e especificação da próxima versão. As melhorias descritas aqui ainda não estão no LISP 0.2.

## Direção confirmada pelo usuário

Perfil equilibrado entre conforto e custo. Variação real de casas, cômodos e integração entre sala/jantar/cozinha. Prioridades: convivência, entrada de luz e garagem. O usuário confirmou funcionamento da inserção de cômodos e desenho no AutoCAD na versão 0.2. O programa continua começando por terreno plano e precisa preservar o caminho AutoCAD → Revit.

Norte, quantidade de moradores e vagas, área construída alvo e necessidades de acessibilidade ainda não foram definidos. Esses dados devem ser campos do aplicativo, com opção explícita de simulação quando o lote for hipotético. Não confundir hipótese com levantamento. O programa já confirmado pelo cliente deve ser preservado em todas as alternativas; preferências de integração podem variar.

## Por que o resultado atual é repetitivo

O código possui apenas duas faixas iguais e corredor central. Embaralha os nomes/funções dos ambientes, mas a profundidade do par é o maior valor dos dois, acrescido de apenas 0 a 30 cm. Quando sobra um ambiente, ele ocupa a largura inteira. Isso explica quartos enormes, banheiros acompanhando o tamanho de quartos e pouca mudança real entre alternativas.

No exemplo 0.2 salvo no workspace: banheiro 11,36 m², lavanderia 10,65 m², um quarto 30,10 m² e sala 13,49 m². São áreas desse exemplo, não medidas extraídas da imagem enviada. Não são automaticamente inadequadas em qualquer projeto; aqui resultam do empacotamento, sem demanda dos moradores que as justifique. A sala contém só um sofá; a cozinha tem geladeira e bancada, sem conjunto funcional completo.

A pesquisa de interiores existente é um catálogo de especificações. O gerador atual ainda não executa a maior parte dessas regras. A existência dos arquivos e os testes geométricos não equivalem a inteligência arquitetônica implementada.

## Fluxo proposto

**Programa dos moradores → relações entre ambientes → várias tipologias → dimensionamento com móveis → validação → seleção de alternativas diferentes → CAD → Revit.**

A aleatoriedade escolhe entre soluções admissíveis. Não deve decidir sozinha dimensões, acessos ou janelas. O programa deve descartar uma opção impossível, informar o motivo e continuar a busca dentro de um limite de tentativas.

### 1. Organizar antes de desenhar

Modelar setores social, íntimo e de serviço; relações desejadas e acessos permitidos. Exemplo: chegada à convivência; cozinha próxima do jantar; lavanderia vinculada à cozinha/serviço; quartos protegidos da circulação de visitantes. Banheiro social com acesso comum; banheiro de suíte ligado ao quarto correspondente. Não obrigar visitas a atravessarem um dormitório.

Variar integração aberta, semiaberta e fechada entre alternativas. A variante aberta ainda deve distinguir as zonas funcionais e acomodar assentos, mesa e equipamentos. No Revit, zonas de estar/jantar/cozinha não devem virar três Rooms sobrepostos: separar a função de uso do recinto delimitado por paredes. A privacidade é verificada pelo percurso e, posteriormente, por linhas de visão; vizinhança de cômodos por si só não comprova conforto acústico.

### 2. Variar a estrutura das plantas

Começar com três organizações dentro de um contorno retangular: setor social na frente e íntimo ao fundo; circulação lateral; núcleo social distribuidor com corredor reduzido. Não contar simples espelhamento ou troca de nomes como diversidade.

Depois incluir casa em L com varanda e casa com pátio. Isso exige contornos e vazios reais: o piso retangular atual preencheria indevidamente o pátio. Cotas, cortes e importador Revit também precisam dessa evolução. Cada família precisa ter limites de aplicação; se o lote não comportar uma tipologia, ela sai da busca.

### 3. Dimensionar a partir da vida cotidiana

Substituir tamanhos fixos por intervalos de área e proporção por função, ocupação e perfil. O conjunto de mobiliário, suas aberturas e a circulação precisam caber antes de aceitar o cômodo. A área alvo evita que o algoritmo desperdice terreno para resolver encaixes. Uma mesma área pode produzir um quarto confortável ou inutilizável dependendo de largura, portas e móveis.

O mobiliário deve participar da geração: quarto de casal ou solteiros; sala com assentos compatíveis com moradores e uso de visitas; jantar com cadeiras em uso; cozinha linear, em L ou em U quando couber; banheiro com louças e áreas de utilização; lavanderia com tanque, máquina e acesso; garagem com carro, abertura de portas, portão e percurso de pedestre. Ilha, mesa de centro e outros itens opcionais entram apenas se houver espaço funcional.

### 4. Luz, ventilação e áreas externas

Pedir norte e posição da rua; representar muros, vizinhos e obstáculos quando conhecidos. Priorizar aberturas voltadas a exterior ou pátio efetivo, verificar conexão dos espaços com as aberturas e testar potencial de ventilação cruzada. Uma janela desenhada não comprova iluminação suficiente; janelas grandes sem proteção podem aumentar o calor e ofuscamento.

No início, apresentar indicadores geométricos e pendências. A previsão de desempenho exige clima, materiais, cobertura, vidro, uso e entorno. O [ProjetEEE, do MME](https://www.gov.br/mme/pt-br/assuntos/secretarias/sntep/projeteee) fornece referências bioclimáticas para incorporar essa análise; não é um selo de conformidade automático do nosso gerador.

### 5. Estilo com regras próprias

Tratar estilo como escolhas coerentes de proporção, abertura, varanda, cobertura e materiais. Exemplos a oferecer futuramente: contemporânea compacta; casa avarandada; casa com pátio. Não sortear elementos decorativos incompatíveis nem apresentar uma fachada sofisticada para ocultar uma planta ruim. A prioridade desta evolução é implantação, organização e uso; detalhamento de fachadas e famílias de móveis acompanha o modelo BIM.

## Como avaliar e comparar

| Camada | Comportamento proposto |
|---|---|
| Condições obrigatórias do cliente | Preservar ambientes, vagas e demais requisitos confirmados; se não couberem, informar inviabilidade |
| Geometria e uso | Rejeitar sobreposições físicas indevidas, cômodos inacessíveis, portas bloqueadas e equipamentos essenciais sem uso |
| Regras legais | Registrar fonte, edição, aplicabilidade e resultado por regra; lacunas continuam pendentes |
| Qualidade | Comparar adequação das áreas, percurso/circulação, privacidade, convivência, potencial ambiental e compacidade |
| Diversidade | Comparar organização dos setores, acessos, integração e proporções; evitar três alternativas equivalentes |
| Custo | Usar área e perímetro/compacidade como indicadores iniciais, explicitamente sem tratá-los como orçamento |

Não permitir que uma nota alta de estética compense uma porta bloqueada. Não normalizar a pontuação de modo que a falta de dados solares vire aprovação. Mostrar vantagens e perdas de cada alternativa, em vez de uma única nota que prometa a melhor casa universal.

A meta inicial de produto é apresentar até três alternativas realmente distintas, com quadro comparativo de áreas, configuração social, garagem, mobiliário atendido e pendências. Se apenas uma passar, mostrar uma e explicar; nunca preencher a lista com cópias.

## Ordem de implementação e aceite

1. **Programa e avaliador:** novos campos, perfis de ocupação, restrições e relatório; reservar garagem e seus acessos desde o início do encaixe. Aceite: manter exigências e explicar entradas ausentes/inviabilidade.
2. **Dimensionamento e mobiliário:** intervalos, conjuntos completos, colisões e percursos. Aceite: nenhum item essencial omitido silenciosamente; móveis e portas utilizáveis segundo o perfil configurado.
3. **Três organizações e integração variável:** abandonar dependência do corredor central. Aceite: no cenário de teste viável, alternativas com organizações diferentes; reprodução pela mesma semente e configurações.
4. **Garagem e áreas externas:** acessos e convivência externa conforme programa. Aceite: carro e acesso de pedestre representados sem bloquear a casa; verificar portão e espaço de operação.
5. **L/pátio, análise ambiental e estilo:** atualizar contorno, cortes e conexão Revit; introduzir dados climáticos e de entorno. Aceite: pátio continua vazio no BIM e todos os elementos preservam posição e dimensões.

A sequência acima consolida os três pareceres: a família em L sugerida em arquitetura.md fica após a atualização de contornos; a meta inicial é até três alternativas, dentro da faixa de três a cinco sugerida em algoritmo.md.

Manter o AutoLISP como comando dentro do AutoCAD. O núcleo pode evoluir inicialmente em AutoLISP com busca limitada; motor externo passa a ser opção quando houver ganho demonstrado para otimização/simulações. Isso não deve voltar a exigir que o usuário carregue vários LISPs. A escolha técnica detalhada está em algoritmo.md.

## Referências e arquivos de trabalho

A [Portaria MCID 725, versão consolidada consultada, Anexo III](https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/habitacao/arquivos-1/Portaria_MCID_725_Especificacoes_MCMV_FAReFDS_COMPILADA3.pdf) relaciona dimensionamento habitacional a mobiliário e uso. Seu escopo é específico de linhas do Minha Casa, Minha Vida; não é uma tabela universal de conforto nem substitui legislação de BH. Usar essa abordagem como referência funcional, sem copiar seus mínimos como metas de conforto para qualquer residência.

Complementos: arquitetura.md, mobiliario.md, algoritmo.md; perfil-equilibrado.json registra as preferências e lacunas; diagnostico-exemplo.json contém a auditoria quantitativa. Todos são especificações e pesquisa, não uma nova versão executável do gerador.
