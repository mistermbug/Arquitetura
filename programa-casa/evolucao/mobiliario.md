# Mobiliário e qualidade de uso — especificação para a próxima versão

Data: 07/09/2026. Documento de proposta; nenhuma melhoria descrita aqui foi implementada por este relatório.

Direção confirmada durante esta rodada: equilíbrio entre custo e conforto, convivência, luz e garagem. A integração sala/cozinha deve variar entre alternativas. Isso vira parâmetro `integration_mode=explore_both`: testar solução integrada e separada, identificando a diferença na apresentação. A quantidade de vagas ainda não foi informada e deve ser configurável; qualquer vaga usada em demonstração precisa ser rotulada como hipótese.

## Diagnóstico verificável

`casa-core.lsp`, funções `cg:add-furniture` e `cg:furnish`, cadastra somente tipo, caixa retangular, altura e ambiente. Todo quarto recebe a mesma cama de 1.600 × 2.000 mm junto ao mesmo canto; o armário só aparece quando a largura chega a 3.000 mm. Estar recebe apenas sofá; jantar, mesa sem cadeiras; escritório, mesa sem cadeira; lavanderia, apenas lavadora. A cozinha nem distingue pia, preparo e cocção. A posição não consulta portas e janelas. Conter os retângulos dentro do cômodo não demonstra que alguém consiga usar os móveis.

O importador Revit extruda essas caixas como DirectShape. Sem orientação frontal, articulação, versão de produto ou identificador de família, não consegue reconstruir interiores ricos de forma confiável.

## Mudança central

Dimensionar os ambientes a partir de conjuntos de uso, testar arranjos e devolver restrições ao gerador da casa. Mobiliar somente depois de congelar todos os cômodos produz quartos que podem conter uma cama, mas não o programa do morador. Exemplo: quarto de duas crianças exige duas camas, dois lugares de guardar pertences e espaço de estudo conforme o pedido; não deve receber automaticamente uma cama de casal.

Cada conjunto deve ter itens obrigatórios, alternativas equivalentes e itens opcionais. Se nenhum arranjo acomoda o conjunto obrigatório, aumentar/redimensionar o ambiente, trocar a topologia ou informar inviabilidade. Nunca omitir silenciosamente o armário para fazer o resultado caber.

## Biblioteca inicial recomendada

As quantidades abaixo são decisões de produto propostas, editáveis pelo cliente; não são exigências legais.

| Ambiente | Conjunto funcional | Variantes que mudam de fato o projeto |
|---|---|---|
| Quarto de casal | Cama para dois, armazenamento para dois, acesso aos lados utilizados | Cama compacta/padrão/ampla; armário de correr/abrir; cabeceiras opcionais; estação de trabalho opcional |
| Quarto individual | Cama e armazenamento de uma pessoa | Estudo, brincar, leitura, hóspede eventual; previsão de crescimento |
| Quarto compartilhado | Lugares de dormir e guardar para cada usuário | Duas camas, beliche somente por opção explícita, bancada dupla ou compartilhada |
| Estar | Assentos suficientes para ocupação usual e apoio | Sofá linear + poltrona, dois sofás, sofá em L; televisão opcional; conversa ou entretenimento como prioridade |
| Jantar | Mesa e cadeiras para moradores, convidados conforme frequência | Mesa redonda/retangular/extensível, integrada ao estar ou à cozinha |
| Cozinha | Geladeira, pia, preparo, cocção e armazenamento | Linear, paralela, L, U; forno separado, lava-louças, despensa; ilha somente se restar espaço de operação |
| Banheiro completo | Bacia, lavatório e banho | Box de correr/abrir, armário, espaço para cuidador quando solicitado |
| Lavabo | Bacia e lavatório | Não confundir com banheiro com banho na contagem do programa |
| Lavanderia | Lavagem, secagem e armazenamento de limpeza | Tanque, varal, secadora empilhada/lateral, tábua de passar |
| Escritório | Mesa, cadeira e armazenamento conforme atividade | Um/dois postos; videoconferência; acessibilidade; uso eventual ou diário |
| Entrada/varanda | Conforme pedido | Apoio, sapateira, bancos, refeições, vegetação; sempre preservar acesso |
| Garagem | Veículos e vagas informados | Modelo genérico ou dimensões reais do carro, acesso de pedestres, portão e suas áreas de operação; não representar apenas retângulos de vaga |

Começar com 25–40 tipos genéricos leves, cada um com duas ou três dimensões úteis. Não confundir variedade de catálogo com qualidade: três arranjos comprovadamente utilizáveis valem mais do que centenas de blocos sem informação funcional.

## Cadastro geométrico 2D/BIM

Além dos campos atuais, incluir:

- `catalog_id`, `catalog_version`, `variant_id`, `required`, `occupancy_capacity`;
- origem de inserção e `rotation_deg`; dimensões físicas completas, incluindo estrutura da cama e puxadores;
- `footprint` como polígono local e `z_min/z_max`, permitindo verificar sobreposição em altura;
- `operation_envelopes`: porta/gaveta/cadeira puxada/manutenção, com estado e associação ao componente;
- `use_areas`: aproximação, sentar, vestir e alcançar, com ponto de acesso obrigatório;
- `dwg_block`, `revit_family`, `revit_type`, categoria BIM apropriada e parâmetros de tamanho/material;
- proveniência das dimensões: `project_default`, `manufacturer`, `recommendation` ou `applicable_requirement`, com fonte, edição e escopo;
- estilo e material como atributos independentes da geometria; licença e permissão de redistribuição dos arquivos.

Para a primeira implementação, objetos ortogonais podem usar rotações 0/90/180/270 graus e envelopes retangulares. Portas de abrir precisam de setor de giro, dobradiça e sentido. O CAD deve oferecer uma camada opcional `CASA_USO` para visualizar os envelopes; esses polígonos não são móveis físicos e não devem virar sólidos na importação Revit.

Na garagem, cadastrar carroceria, portas abertas, porta-malas, percurso de entrada e saída e operação do portão. Verificar passagem do morador com o veículo estacionado. Portão basculante, deslizante e de abrir têm envelopes diferentes, inclusive em altura. Restrições do passeio e do acesso veicular pertencem à validação municipal; dimensões de um veículo genérico não definem uma vaga legal nem comprovam manobra.

Dimensões iniciais são parâmetros de projeto, nunca mínimos legais implícitos. Manter variantes de cama/sofá/mesa configuráveis e substituir pelos dados externos reais quando houver produto escolhido. Não usar medida do colchão como dimensão automática da cama. Folga atrás de cadeira recolhida não equivale à passagem com cadeira ocupada. Espaço livre ao lado de cama não comprova acessibilidade.

## Restrições e critérios

**Rejeitar a alternativa:** móvel físico atravessa parede; itens físicos incompatíveis colidem na mesma faixa de altura; acesso obrigatório não tem rota; giro da porta principal do ambiente é bloqueado; item obrigatório não cabe; janela necessária fica completamente impedida de operar pelo móvel. A política de simultaneidade deve ser explícita: uma gaveta aberta e uma passagem temporariamente compartilhada podem receber tratamento diferente da única saída bloqueada por um móvel fixo.

**Pontuar, sem tratar como lei:** distância para tarefas relacionadas, facilidade de arrumar a cama, privacidade visual, assentos suficientes, armazenamento solicitado, espaço residual realmente utilizável, visibilidade da televisão quando pedida, reflexos potenciais na estação de trabalho, flexibilidade futura e coerência de materiais. Acesso/saída e requisitos aplicáveis não podem ser compensados por uma boa nota estética.

Móveis sob janelas exigem comparar peitoril e altura, abertura da folha e acesso de operação. Armário alto e armário baixo não são equivalentes. Uma cadeira sob a mesa pode ter interseção 2D legítima; precisa ser testada em estado recolhido, ocupado e puxado, e não pelo critério simplista de zero interseções 2D.

Para circular, inflar obstáculos pela largura do perfil de usuário adotado e procurar um caminho entre a entrada e os pontos de uso obrigatórios; amostrar apenas a largura do corredor desenhado é insuficiente. Evitar uma malha grosseira que deixe passar falsamente por cantos. Guardar a largura exigida, tolerância e método de validação no relatório.

## Método de geração

1. Transformar moradores e atividades em conjuntos obrigatórios de mobiliário.
2. Selecionar templates de ambiente compatíveis com área e proporção desejadas.
3. Reservar paredes disponíveis, portas, janelas, pontos hidráulicos e áreas de uso.
4. Gerar várias orientações e posições discretas para peças maiores; acrescentar peças menores.
5. Rejeitar colisões/inacessibilidade; pontuar funcionamento e preferências.
6. Se falhar, pedir ao gerador ajuste de dimensões/aberturas ou selecionar outro template.
7. Apresentar alternativas significativamente diferentes, com motivo de escolha e insuficiências explícitas.

Variar a posição do mesmo retângulo não deve contar como estilo diferente. Estilo altera proporções, composição, materiais e escolhas de objetos; planta aberta/fechada e formato L/U são decisões espaciais, que devem ter campos próprios. Oferecer poucos perfis inicialmente: compacto funcional, social integrado e privacidade. Separadamente, permitir linguagem contemporânea, tradicional ou outra referência fornecida pelo cliente.

## Indicadores e testes de aceitação

| Indicador | Como medir |
|---|---|
| Programa mobiliado | 100% dos itens obrigatórios e das capacidades solicitadas presentes |
| Colisão física | Nenhuma interseção incompatível acima da tolerância geométrica |
| Operação | Estados obrigatórios de portas, gavetas e equipamentos verificados |
| Acessibilidade funcional | Entrada alcança cada ponto de uso sob o perfil configurado; não chamar isso de certificação normativa |
| Assentos/armazenamento | Comparar capacidade efetiva com moradores e convidados pedidos |
| Garagem | Todas as vagas pedidas presentes; operação e acesso de pessoas/veículos verificados com os envelopes adotados |
| Diversidade | Diferenças de template, adjacências, orientação e proporção; remover rotações/espelhamentos equivalentes conforme o caso |
| BIM | Tipo, orientação, posição e dimensões coincidem entre CAD/JSON/Revit |
| Honestidade | Requisito desconhecido fica `not_evaluated`; não recebe `pass` por ausência de dados |

Casos obrigatórios de ensaio: quarto estreito com armário de abrir; duas camas; sala com duas portas; jantar com cadeiras ocupadas; cozinha com geladeira e forno abertos; janela atrás de móvel alto; mesa com cadeira parcialmente sob o tampo; nenhum arranjo viável; perfil com auxílio de mobilidade. Testes sintéticos devem ser acompanhados de revisão de plantas por arquiteto e por usuários: quantidade de verificações geométricas não mede, sozinha, qualidade arquitetônica.

## Fontes e limites

- Código local examinado: `programa-casa/casa-core.lsp` e `programa-casa/revit/importar_casa_dynamo.py`; pesquisa anterior em `pesquisa-interiores/PESQUISA.md` e `regras.json`.
- [Merrell et al., Interactive Furniture Layout Using Interior Design Guidelines, SIGGRAPH 2011](https://graphics.stanford.edu/projects/furniture/), fonte primária consultada em 07/09/2026: fundamenta converter diretrizes em critérios e gerar sugestões por amostragem. Não demonstra atendimento às normas brasileiras.
- As referências NKBA e OSHA da pesquisa anterior foram tentadas novamente, mas seus servidores retornaram 403 nesta consulta. Não se extraíram novas medidas dessas páginas.
- Este relatório não estabelece novos valores normativos. A pesquisa anterior cita NBR 9050 e outras normas; antes de transformar qualquer medida em restrição legal, confirmar edição vigente, aplicabilidade, item e unidade com a camada normativa do projeto. Preferências genéricas de mobiliário devem permanecer identificadas como escolhas de projeto.

## Perguntas que realmente mudam o resultado

1. Quantos moradores, quais dormitórios são de casal/individuais/compartilhados e existe necessidade de acessibilidade ou cuidador?
2. Cozinha e sala integradas ou separadas; refeições e recepção de convidados com qual frequência?
3. Prioridade: menor área/custo, espaços sociais amplos, armazenamento, privacidade, trabalho em casa ou adaptação futura?
4. Há móveis existentes que precisam caber, medidas máximas de orçamento e imagens de referência de estilo?

Sem resposta, o aplicativo pode usar um perfil demonstrativo explicitamente rotulado e editável; não deve inferir idade, deficiência ou hábitos pessoais como fatos.
