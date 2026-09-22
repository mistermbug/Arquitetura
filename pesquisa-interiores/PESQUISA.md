# Pesquisa aplicada: interiores residenciais e automação AutoCAD–Revit

Data: 07/09/2026. Interpretação adotada: “conforto de denominação” significa conforto de iluminação. Brasil é a referência territorial inicial.

**Recomendação:** construir uma base própria de regras rastreáveis, um catálogo de móveis com áreas de uso e um gerador geométrico conectado a famílias Revit. Ferramentas existentes podem acelerar partes desse processo. Na documentação examinada, não foi demonstrada uma solução única que entregue todo esse fluxo com validação normativa brasileira, térmica, lumínica e acústica.

## 1. Ferramentas e plugins encontrados

| Ferramenta | Evidência e utilidade | Limitação para este projeto |
|---|---|---|
| [Finch](https://docs.finch3d.com/readme/new-features) | Documenta exportação de mobiliário para famílias Revit, biblioteca de plantas adaptáveis e regras de dimensão de espaços. Candidato prioritário para demonstração de geração de plantas. | Não foi comprovado atendimento automático às normas brasileiras nem disponibilidade de API adequada ao nosso aplicativo. |
| [Dynamo + Generative Design](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-GDiR/files/GUID-016FB82B-6F34-4290-B00C-5A043E8C8144.htm) | Permite codificar entradas, restrições, objetivos e criação de elementos a partir de alternativas. Bom caminho para um protótipo controlável. | É necessário escrever a lógica residencial. Exemplos de escritórios não resolvem quartos e cozinhas automaticamente. |
| [Spazio — Extract and Regenerate Rooms](https://marketplace.autodesk.com/apps/81708ba0-12b9-4668-91e0-82a05c009fa6) | A listagem descreve extração e recriação de ambientes com paredes, móveis e equipamentos. Útil para reaproveitar soluções aprovadas. | Reutilização de um ambiente não demonstra adaptação correta a qualquer geometria. |
| [Hypar](https://docs.hypar.io/c13c5ab1655a45d499c1f6e68a8fc209) | Planejamento de espaços com tipos de ambientes oriundos do Revit. Referência para bibliotecas de ambientes e estudos de encaixe. | A documentação consultada enfatiza também escritórios, saúde e comércio; validar o escopo residencial antes de adotar. |
| [BIMobject](https://www.bimobject.com/en-us/categories/furniture?software=revit) | Biblioteca de produtos de fabricantes, filtrável por famílias Revit. Fonte de geometria e dimensões reais. | Não é um mecanismo de decisão de layout. Conferir licença de redistribuição, qualidade e versão de cada família. |
| [Honeybee / Ladybug Tools](https://www.ladybug.tools/honeybee.html) | Integra simulação de luz com Radiance e de energia com EnergyPlus/OpenStudio. | Exige modelo analítico, materiais, clima e configuração; a interface descrita usa Rhino/Grasshopper. Não é uma conexão AutoCAD–Revit pronta. |
| [CBE Thermal Comfort Tool](https://cbe.berkeley.edu/research/cbe-thermal-comfort-tool/) | Ferramenta acadêmica para conforto térmico, com modelos PMV e adaptativo. | Avalia condições térmicas; não distribui móveis nem substitui a avaliação de desempenho da edificação. |
| [Veras](https://apps.autodesk.com/en/Detail/HelpDoc?appId=1053074555136920532&appLang=en&os=Win64) | Visualização por IA a partir de vistas, inclusive Revit. Útil para explorar aparência. | A documentação consultada descreve renderização, não geração validada de famílias e áreas de circulação. |

Nenhum plugin foi instalado ou comprado. Não havia ferramenta de busca de diretório de plugins disponível nesta sessão; a verificação de produtos Autodesk e serviços externos foi feita na web. A lista de plugins sugeridos na conversa não comprova integração específica com AutoCAD/Revit.

Para testar fornecedores, usar o mesmo conjunto de plantas: quarto estreito, sala irregular com duas portas, cozinha com eletrodomésticos abertos e dormitório acessível. Exigir demonstração de famílias editáveis, coordenadas, atualização sem duplicação, controle de dimensões e registro das regras violadas. Confirmar versões, licenciamento, operação local/nuvem e exportação de dados antes da escolha.

## 2. Conhecimento de referência

| Referência | Papel na base | Tratamento |
|---|---|---|
| [ABNT NBR 9050:2020, cópia disponibilizada pela Prefeitura de Macaé](https://www.macae.rj.gov.br/midia/uploads/NBR%209050_2020.pdf) | Acessibilidade, aproximação, alcance e manobra. | Conferir versão corrigida, atualizações e aplicação ao caso; não transformar uma medida isolada em aprovação geral. |
| [NBR 15575 — materiais técnicos do LabEEE](https://labeee.ufsc.br/pt-br/NBR15575-2020) | Desempenho habitacional e método térmico. | A página explica a revisão térmica de 2021 e distingue propostas posteriores. Confirmar a edição de cada parte e emenda adotada. |
| [NBR 15220 — LabEEE](https://labeee.ufsc.br/pt-br/node/1149) | Propriedades térmicas e zoneamento bioclimático atualizado em dezembro de 2024. | Guardar edição e arquivo climático; não fixar o antigo zoneamento no código. |
| [NBR 10152 — comunicação do CAU/BR](https://caubr.gov.br/norma-de-acustica-abnt-publica-versao-atualizada-de-parametros-para-edificacoes-2/) | Referências acústicas para ambientes internos. | A notícia de 2018 trata da edição 2017; não comprova, sozinha, sua vigência em 2026. Confirmar no catálogo. |
| [NKBA — diretrizes de planejamento](https://kb.nkba.org/guidelines/?dontautodisplay=1) | Planejamento de cozinhas e banheiros. | Recomendações estrangeiras; não equivalem a requisitos legais brasileiros. |
| [Panero e Zelnik — Human Dimension and Interior Space](https://www.penguinrandomhouse.com/books/126412/human-dimension-and-interior-space-by-julius-panero-and-martin-zelnick/) | Antropometria e relação entre usuário, mobiliário e espaço. | Referência bibliográfica identificada pela editora; o livro completo não foi consultado. Considerar população, idade e diversidade corporal. |
| [Neufert — Architects’ Data, 6ª edição](https://uat.store.wiley.com/en-us/architects%27-data-6th-edition-p-9781119873945) | Dimensões e organização funcional na fase inicial de projeto. | Referência bibliográfica; tabelas completas não foram extraídas nem incorporadas. |
| [Merrell et al., SIGGRAPH 2011](https://graphics.stanford.edu/projects/furniture/) | Formula diretrizes de interiores como critérios para geração computacional de arranjos. | Referência de método, não norma nem evidência de software comercial pronto. |
| [OSHA — estações de trabalho](https://www.osha.gov/etools/computer-workstations/) | Ajustabilidade e organização ergonômica do home office. | Orientação técnica estrangeira, sem importar automaticamente obrigações trabalhistas. |

Completar a camada normativa com Código de Obras municipal, requisitos locais de ventilação e iluminação, regras aplicáveis ao empreendimento e manuais de instalação. Verificar também as partes pertinentes da NBR 15575 para funcionalidade, iluminação e acústica. Uma proposta em consulta ou um guia antigo não deve entrar no sistema como norma vigente.

## 3. Como representar um móvel

Proposta de modelagem para o aplicativo:

1. **Volume físico:** geometria real, altura, projeção, saliências e posição de instalação.
2. **Envelope de operação:** portas, gavetas, reclinação, extensão de mesa e manutenção.
3. **Área de uso humano:** sentar, levantar, vestir-se, cozinhar e aproximar-se.
4. **Rota de circulação:** caminho contínuo entre acessos e pontos de uso, com largura compatível com o perfil.

Essas regiões não são intercambiáveis. A cadeira recolhida e a cadeira ocupada produzem layouts diferentes. Sobreposições verticais legítimas, como cadeira sob a mesa ou armário superior sobre bancada, precisam de validação em altura. Duas áreas de uso podem compartilhar espaço somente quando a simultaneidade e as regras aplicáveis permitirem.

Cada item deve registrar ID estável, categoria, dimensões externas, geometria, orientação frontal, ponto de inserção, posições permitidas, áreas funcionais, fabricante/modelo, custo estimado quando conhecido e vínculo bloco DWG ↔ família/tipo RFA. Não usar apenas largura × profundidade ou o centro da caixa envolvente para posicionar tudo.

## 4. Organização por ambiente

As orientações abaixo são síntese de projeto proposta para o protótipo. Não representam transcrição de norma. A seleção final vem do programa dos moradores; televisão, mesa de jantar e mesa de cabeceira não são universais.

| Ambiente | Conjunto funcional inicial | Como organizar e avaliar |
|---|---|---|
| Entrada | Acesso e apoio/armazenamento, se desejado | Preservar abertura da porta, percurso de entrada e apoio sem estrangular a passagem. |
| Estar | Assentos conforme ocupação; apoios; TV/estante opcionais | Formar grupo de conversa; avaliar visibilidade; manter acesso aos outros cômodos sem exigir atravessar o espaço entre pessoa e mesa de apoio. |
| Jantar | Mesa e assentos compatíveis com os moradores | Avaliar cadeiras puxadas e ocupadas, alcance da mesa e passagem atrás dos usuários. Priorizar proximidade funcional à cozinha. |
| Quarto de casal | Cama e armazenamento; apoios e trabalho opcionais | Preservar acesso aos lados conforme os usuários; abrir armários; verificar luz, ruído e conflito entre trabalho e descanso. |
| Quarto individual/infantil | Cama, armazenamento e estudo/brincar conforme idade | Considerar crescimento, alcance e estabilidade dos móveis; avaliar riscos de escalada junto às janelas. Não otimizar apenas densidade. |
| Cozinha | Armazenar, lavar, preparar e cozinhar; equipamentos conforme programa | Fixar pontos de instalação; organizar sequência de tarefas; verificar portas de eletrodomésticos e uso por uma ou mais pessoas. |
| Banheiro | Bacia, lavatório e banho quando previsto | Modelar uso, abertura do box, aproximação e limpeza; o perfil acessível precisa de regras próprias de transferência, alcance e manobra. |
| Lavanderia | Lavagem e secagem; tanque/armazenamento conforme programa | Verificar abertura frontal ou superior, manutenção, pontos hidráulicos, ventilação e separação de materiais de limpeza. |
| Home office | Mesa, cadeira e equipamentos necessários | Permitir ajustes, acomodação das pernas, distância visual e acesso; evitar que circulação passe pela cadeira em uso. |
| Varanda | Assentos/refeições opcionais | Preservar portas, drenagem e acesso; conferir exposição dos materiais e relação com guarda-corpos. |

Na cozinha, usar proximidade entre tarefas como objetivo. O tradicional triângulo de trabalho pode orientar algumas configurações, mas cozinhas lineares e múltiplos cozinheiros pedem outras relações. Modelar apoios e afastamentos conforme os equipamentos selecionados.

## 5. Medidas iniciais e sua procedência

| Situação | Valor inicial | Natureza e condição |
|---|---|---|
| Corredor de trabalho de cozinha, um cozinheiro | 1.067 mm | Recomendação NKBA; entre frentes de bancadas, armários altos e/ou equipamentos. |
| Corredor de trabalho de cozinha, vários cozinheiros | 1.219 mm | Recomendação NKBA; conferir também equipamentos abertos e circulação simultânea. |
| Espaço ao redor da cama | A IKEA cita aproximadamente 500–600 mm | Referência comercial de uso cotidiano; não é rota acessível nem garantia de abertura de armário. |
| Módulo de referência de cadeira de rodas | 800 × 1.200 mm | NBR 9050:2020, item 4.2.2; representa ocupação, não toda a área de manobra. |
| Porta em contexto acessível | Vão livre de pelo menos 800 × 2.100 mm | NBR 9050:2020, item 6.11.2.4; dimensão livre, não largura nominal da folha. Verificar aproximação e demais requisitos. |
| Distância de visualização do monitor | Pelo menos cerca de 500 mm | Orientação OSHA para acomodação na mesa; ajustar ao equipamento e usuário. |

Fontes das recomendações: [NKBA, diretriz 6](https://kb.nkba.org/uploads/2022/05/Kitchen-Planning-Guidelines.pdf), [IKEA, guia de escolha de cama](https://www.ikea.com/pl/pl/rooms/bedroom/how-to/wiec-kupujesz-lozko-pub30c7ac50/), [OSHA, mesas](https://www.osha.gov/etools/computer-workstations/components/desks). Os valores normativos vêm da [NBR 9050 consultada](https://www.macae.rj.gov.br/midia/uploads/NBR%209050_2020.pdf).

Não aplicar 600 mm como circulação universal. Não atribuir automaticamente medidas de colchão à cama completa. Não estabelecer distância única de TV, altura única de bancada ou afastamento universal de fogão: dependem de produto, usuários e atividade. O cadastro deve distinguir valor observado em fonte, parâmetro adotado pelo projeto e resultado calculado.

## 6. Conforto ambiental

### Térmico e ventilação

O layout deve ser avaliado junto com clima, orientação, envoltória, aberturas, ocupação e equipamentos. O LabEEE descreve avaliação térmica com indicadores como horas em faixa de temperatura operativa e cargas térmicas; posicionar móveis não basta para demonstrar desempenho. A revisão do zoneamento de 2024 precisa ser tratada explicitamente na configuração. [Método térmico](https://labeee.ufsc.br/pt-br/NBR15575-2020), [zoneamento](https://labeee.ufsc.br/pt-br/node/1149).

Propostas para o motor: impedir obstrução de aberturas e grelhas; testar incidência solar nas posições de longa permanência; permitir sombreamento; penalizar jatos diretos desconfortáveis sobre ocupantes quando houver dados do equipamento. Duas janelas não comprovam ventilação cruzada: é preciso considerar conexão dos espaços, áreas efetivas, vento e diferenças de pressão. O desempenho dos vidros depende também de orientação, clima e características do edifício. [DOE, janelas](https://www.energy.gov/energysaver/window-types-and-technologies).

Usar CBE para checagens de conforto compatíveis com o modelo escolhido. Não aplicar PMV/adaptativo indiscriminadamente: a própria ferramenta informa limitações, incluindo condições de sono e uso de roupa de cama. [Condições de aplicação](https://comfort.cbe.berkeley.edu/).

### Iluminação e conforto visual

Separar luz ambiente, tarefa e destaque. Avaliar sombras nas bancadas, reflexos em telas, contraste, controle de entrada de sol e acionamento acessível. Posições de trabalho devem considerar a janela, o usuário e o plano da tela, não apenas a orientação da mesa. São verificações propostas para o gerador.

A iluminação depende de orientação e refletâncias de superfícies, inclusive móveis. [DOE, envoltória e luz](https://www.energy.gov/cmei/buildings/zeb-technologies-building-envelope-architectural-considerations). Simular luz natural com Radiance/Honeybee quando houver geometria, materiais e condições de céu; para luz artificial, cadastrar fotometria, plano de avaliação e critérios da atividade. [Honeybee](https://www.ladybug.tools/honeybee.html).

Não foi fixado um valor universal de lux residencial. As metas devem ser justificadas por atividade e norma aplicável. A NBR 5413 aparece como cancelada em registros oficiais; não usar suas tabelas como requisito atual. [Registro do Ministério do Trabalho](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/arquivos/atas-ctpp/91_reuniao_ordinaria_21_e_22_11_2017.pdf).

### Acústico, ar e manutenção

Propostas de organização: afastar atividades ruidosas das áreas de descanso quando possível; evitar equipamentos vibratórios adjacentes às cabeceiras; prever soluções de separação e vedação. Estofados, tapetes e cortinas podem alterar a absorção interna, mas não comprovam isolamento entre cômodos. A avaliação precisa distinguir nível de ruído, reverberação e transmissão por sistemas construtivos. A [referência divulgada pelo CAU para NBR 10152](https://caubr.gov.br/norma-de-acustica-abnt-publica-versao-atualizada-de-parametros-para-edificacoes-2/) é um ponto de partida, sujeito à conferência de edição.

Incluir acesso para limpeza e manutenção, controle de umidade e ventilação compatível com cozinha e banheiro. Ventilação integra a qualidade do ambiente e o controle de umidade. [DOE, melhorias residenciais](https://www.energy.gov/save/home-upgrades). Não assumir que uma coifa recirculante oferece renovação de ar exterior.

## 7. Design e composição visual

Proposta de critérios flexíveis: escala dos móveis em relação ao cômodo, agrupamento por atividade, equilíbrio de volumes, relação com vistas, continuidade de materiais e quantidade de armazenamento. Estilo deve ser configurável: não impor simetria, televisão como foco ou uma paleta específica a toda residência.

A pesquisa de Merrell e colaboradores mostra como diretrizes podem orientar amostragem de arranjos e avaliação de alternativas. Para nosso aplicativo, a adaptação recomendada é usar critérios estéticos somente depois da viabilidade física e funcional. [Projeto de pesquisa](https://graphics.stanford.edu/projects/furniture/).

## 8. Arquitetura proposta para o aplicativo

Fluxo: **planta e programa → modelo geométrico comum → seleção de móveis → geração de alternativas → validação → comparação → blocos AutoCAD e famílias Revit**.

Separar três classes de regras:

- Obrigatórias: colisões indevidas, contenção no ambiente, conexões de acesso, requisitos normativos confirmados e exigências dos equipamentos.
- Recomendadas: distâncias de trabalho, conveniência, relação entre atividades e qualidade visual.
- Dependentes de cálculo: conforto térmico, iluminação e acústica. Sem dados ou simulação, devolver “não avaliado”.

Proposta de algoritmo: posicionar equipamentos fixos; enumerar posições candidatas dos móveis principais; acrescentar apoios; validar geometria e estados de uso; calcular rotas no espaço livre; ordenar somente soluções viáveis. Retornar de três a cinco alternativas distintas com justificativas. Um ótimo estético não pode compensar porta bloqueada.

A geometria deve considerar polígonos irregulares, pilares, vãos, recuos e altura. Uma grade pode acelerar busca preliminar, mas o resultado precisa de verificação geométrica precisa e tolerância explícita. Guardar estado do móvel e simultaneidade das atividades. Se não houver solução, informar o conjunto de conflitos, sem reduzir silenciosamente dimensões ou retirar móveis obrigatórios.

No AutoCAD, associar identidade e classificação a blocos e atributos; a API permite armazenar informações nos atributos. [Documentação Autodesk](https://help.autodesk.com/cloudhelp/2017/ENU/AutoCAD-NET/files/GUID-36DB5C5C-1706-4E8B-9431-AF8D1B5319E7.htm).

No Revit, mapear cada item para família/tipo e criar instâncias respeitando nível, hospedeiro e modo de colocação. Carregar a família e ativar o símbolo quando necessário. O método de criação varia conforme a família; não existe uma única sobrecarga adequada a todos os móveis. [FamilyInstances](https://help.autodesk.com/cloudhelp/2024/ENU/Revit-API/files/Revit_API_Developers_Guide/Revit_Geometric_Elements/Family_Instances/Revit_API_Revit_API_Developers_Guide_Revit_Geometric_Elements_Family_Instances_FamilyInstances_html.html).

Proposta de intercâmbio: JSON em milímetros com ID, geometria, posição, rotação, nível e referência de catálogo. Converter unidades pela API; comprimentos internos do Revit usam pés. [Unidades](https://help.autodesk.com/view/RVT/2021/ENU/?guid=Revit_API_Revit_API_Developers_Guide_Introduction_Application_and_Document_Units_html), [UnitUtils](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API-MainReference/files/html/128dd879-fea8-5d7b-1eb2-d64f87753990.htm).

Projetar atualização por ID para evitar duplicação; preservar ajustes manuais bloqueados; definir quem prevalece em conflitos AutoCAD/Revit; registrar exclusões, versões e transformações de coordenadas. Importar um desenho 2D, por si só, não estabelece esse mapeamento semântico de mobiliário.

## 9. Próxima etapa e validação

Começar com um quarto e uma sala, catálogo pequeno de famílias genéricas e verificação de portas, armários e assentos. Em seguida, incluir cozinha, banheiro e perfil acessível; integrar simulações ambientais depois que a geometria estiver consistente.

Critérios de aceitação propostos: ausência de colisões indevidas; equipamentos operáveis; pontos de uso alcançáveis; móveis do programa presentes; alternativas reproduzíveis; correspondência 2D/3D de quantidade, dimensão, posição e orientação; reimportação sem duplicação; resultados desconhecidos explicitamente sinalizados. Executar casos com corredor estreito, parede inclinada, gaveta aberta, janela baixa, família hospedada e mudança manual no Revit.

Para transformar esta pesquisa em produto, faltam: município/estado, perfil dos moradores e acessibilidade, tipologias, faixa de área, orçamento/estilo, versões dos programas, famílias disponíveis e definição do alcance da geração arquitetônica. Essas lacunas não impedem a base de conhecimento, mas impedem declarar uma planta adequada a um empreendimento específico.

As normas completas e os livros não foram reproduzidos. Antes de incorporar conteúdo protegido ou redistribuir famílias em um aplicativo, conferir os direitos de uso. Nesta entrega foram criadas sínteses, referências e propostas de regras, não uma cópia de tabelas integrais.
