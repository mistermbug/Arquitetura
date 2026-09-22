# Base inicial de Belo Horizonte

Consulta e downloads: 07/09/2026. Fontes oficiais PBH/Câmara e documentos publicados pela PBH. A pasta `fontes` guarda PDFs originais; `extratos` guarda texto extraído para pesquisa, sem garantia de preservação de tabelas/diagramas. Os manifestos registram URL, data, tamanho, hash SHA-256 e estado do download.

## Materiais e leitura aplicada

| ID no manifesto | Conteúdo e resultado da leitura | Uso proposto no aplicativo |
|---|---|---|
| representacao-r5 | Cartilha, 131 páginas. A página 2 informa natureza didática e compatibilidade com Portaria SMPU 054/2023. Há distinções entre projetos privados e públicos e regras de protocolos anteriores. | Perfil de peças gráficas e representação separado da geometria de geração. |
| niveis-terreno | Orientações ilustradas, 19 páginas. | Manter levantamento real e referência Prodabel como dados distintos; prever cortes e altimetria. |
| zoneamento | E-book, 28 páginas. | Identificar contexto territorial antes de selecionar parâmetros. |
| parametros-urbanisticos | E-book, 63 páginas. Página PDF 6 organiza os temas do Anexo XII. A apresentação menciona agosto/2023; a capa contém agosto/2020. | Mapa dos grupos de regras; não copiar números sem conferir o caso e o texto vigente. |
| procedimentos | E-book, 16 páginas. | Identificar etapas administrativas e situações condicionais. |
| plano-diretor-ebook | Compilação didática, 128 páginas. Contém sobreposição de conteúdo com os módulos individuais. | Referência contextual; não contar repetição como fonte independente. |
| lei-11181 | Cópia publicada pela PBH, 97 páginas. O nome do arquivo contém “atual”, mas a consolidação até 2026 não foi comprovada. | Ponto de partida legislativo; conferir alterações e anexos antes de ativar regras. |
| mapa-zoneamento | Anexo I publicado no portal. | Referência territorial; consulta de lote deve confirmar situação atual. |
| mapa-ade | Anexo III publicado no portal. | Identificar diretrizes especiais; conferir mudanças posteriores. |
| mapa-viario-jul2026 | Anexo V na versão de julho/2026 apontada no portal. | Verificar classificação viária aplicável ao lote. |

Fontes de distribuição: [Publicações e Cartilhas](https://prefeitura.pbh.gov.br/politica-urbana/informacoes/publicacoes-e-cartilhas), [Plano Diretor e e-books](https://prefeitura.pbh.gov.br/politica-urbana/planejamento-urbano/plano-diretor/proposta), [Mapas](https://prefeitura.pbh.gov.br/politica-urbana/planejamento-urbano/base-de-dados/mapas-legislacao-urbanistica). Os manifestos contêm os links diretos de cada PDF.

Na verificação local, pypdf conseguiu abrir os sete PDFs iniciais e extrair seus textos. Alguns documentos produziram avisos de conversão de coordenadas internas durante a extração; o texto é auxiliar e tabelas precisam ser lidas no PDF. Páginas representativas da cartilha e do módulo de parâmetros foram renderizadas para inspeção. Isso não significa revisão visual integral das centenas de páginas.

## Instrumentos legais identificados

O [índice de legislação urbanística da PBH](https://prefeitura.pbh.gov.br/politica-urbana/informacoes/legislacao-urbanistica), atualizado em 25/08/2026 na consulta, remete aos instrumentos centrais e complementares. Foram identificados:

- [Lei 11.181/2019](https://www.cmbh.mg.gov.br/atividade-legislativa/pesquisar-legislacao/lei/11181/2019): Plano Diretor.
- [Lei 9.725/2009](https://www.cmbh.mg.gov.br/atividade-legislativa/pesquisar-legislacao/lei/9725/2009): Código de Edificações.
- [Decreto 13.842/2010](https://www.cmbh.mg.gov.br/atividade-legislativa/pesquisar-legislacao/decreto/13842/2010): regulamentação do Código.
- [Decreto 17.273/2020](https://www.cmbh.mg.gov.br/atividade-legislativa/pesquisar-legislacao/decreto/17273/2020): regulamentação de temas de parcelamento, ocupação, uso e interfaces.
- [Portaria SMPU 054/2023](https://dom-web.pbh.gov.br/visualizacao/ato/428399): representação e documentação, referenciada pela cartilha e checklist oficiais.

As consultas CMBH não disponibilizaram texto consolidado legível pelo extrator web utilizado. A tentativa de arquivamento local dessas três páginas também falhou na verificação do certificado TLS; os erros estão em `manifesto-web.json`, e essas páginas não constam como baixadas. Arquivar uma página de consulta, mesmo quando possível, não equivale a revisar a lei completa. O DOM também depende de interface dinâmica. A leitura consolidada do Código, seus anexos e alterações permanece uma tarefa técnica anterior à ativação de suas regras.

O art. 158 da cópia consultada do Plano Diretor relaciona os grupos de parâmetros e remete ao zoneamento e Anexo XII. Isso exige regras condicionais. A cópia local não foi tratada como conjunto completo e atualizado de anexos.

O portal de mapas aponta atualização do sistema viário pela Lei 12.082/2026, de 21/07/2026, além de alterações de ADEs em 2024. Não presumir que o mapa original de 2019 contém todas as mudanças. [Portal oficial de mapas](https://prefeitura.pbh.gov.br/politica-urbana/planejamento-urbano/base-de-dados/mapas-legislacao-urbanistica).

## O que depende do lote

Precisamos associar localização/cadastro, polígono, testadas, situação de parcelamento, topografia e informações municipais. A [FAQ SMPU](https://prefeitura.pbh.gov.br/politica-urbana/perguntas-frequentes-smpu) explica condições de emissão da IBED e indica consultas ao cadastro de parcelamento e GeoSiurbe. Uma parte de lote não deve ser tratada automaticamente como lote regular.

Serviços de referência: [Informação Básica para Edificações](https://servicos.pbh.gov.br/servicos/i/5e68d597ea9b0e547c1a6797/), [GeoSiurbe](https://servicos.pbh.gov.br/servicos/i/5e67db26e1bf5e706b0da107/). Nenhum documento de lote específico foi solicitado ou emitido nesta pesquisa.

A proposta do produto é exigir parâmetros comprovados antes de apresentar resultado de avaliação municipal. Isso não significa que a Prefeitura exija anexação obrigatória de IBED: o [checklist oficial](https://docs.google.com/document/d/e/2PACX-1vRET6Ug0kkn6p5A6bpAhnRYECvrFIM_V_Xi3_r_x9IjKVCBnOyyvvqBQNMtd6gzb2uzJZBZ3VD0Uadn/pub) identifica esse anexo como não obrigatório. Obrigação de preencher o cadastro técnico do aplicativo é uma decisão de produto.

## Conversão para regras: grupos prioritários

| Grupo | Dados necessários | Avaliação proposta e cuidado |
|---|---|---|
| Aplicabilidade territorial | Lote, zoneamento, ADE e demais sobreposições | Selecionar perfil; mapa genérico não basta para encerrar o enquadramento. |
| Envelope de implantação | Testadas, alinhamento e afastamentos aplicáveis | Construir região edificável por borda; esquina e múltiplas frentes exigem tratamento próprio. |
| Aproveitamento | Área de terreno adotada legalmente, áreas computáveis e coeficiente aplicável | Comparar áreas segundo classificações revisadas; não usar indiscriminadamente área útil. |
| Ocupação | Projeção edificada e critérios de inclusão/exclusão | Calcular conforme definição do perfil, não apenas soma de cômodos. |
| Permeabilidade | Superfícies elegíveis, áreas e exigências do perfil | Área livre não equivale automaticamente a área permeável vegetada. |
| Altura e níveis | Referência Prodabel, terreno real, níveis e altura | Distinguir altimetria e altura na divisa; a hipótese de lote plano não elimina consulta. |
| Habitabilidade | Dimensões, áreas, pé-direito, vãos e forma de ventilação | Conferir Código/regulamento consolidado antes de estabelecer mínimos. |
| Acessos e veículos | Vagas, manobras, passeios, frente e classificação viária | Separar quantidade solicitada, exigência legal e viabilidade geométrica. |
| Interfaces | Condicionantes ambientais, culturais, viárias e outras | Encaminhar casos fora do escopo para análise; não converter pendência em aprovação. |
| Representação | Modalidade, natureza privada/pública, peças e quadro de áreas | Gerar conjunto pertinente; planta baixa isolada não é pacote completo de licenciamento. |

Essa tabela é proposta de implementação derivada da pesquisa, não transcrição de limites normativos. O catálogo `matriz-regras-bh.json` deixa valores municipais em aberto.

## Pendências explícitas

1. Obter e revisar textos consolidados e anexos do Código de Edificações e decretos, incluindo alterações aplicáveis ao caso piloto.
2. Confirmar o Anexo XII vigente para o zoneamento e eventuais regras especiais; não preencher valores apenas por exemplo didático.
3. Obter o lote piloto, seus dados cadastrais/urbanísticos e levantamento apropriado.
4. Conferir se há patrimônio, restrições ambientais, viárias, aeroportuárias ou outras interfaces no lote selecionado.
5. O [link antigo do Manual do Portal](https://prefeitura.pbh.gov.br/politica-urbana/informacoes/publicacoes-e-cartilhas/manual-portal-de-edificacoes) encaminhou a arquivo Drive com resposta 401 no acesso web. Seu conteúdo não foi baixado. Buscar a versão atual no serviço de licenciamento quando iniciarmos o fluxo administrativo. A [PBH informa que os manuais do portal são atualizados](https://prefeitura.pbh.gov.br/politica-urbana/informes-tecnicos/manual-cadastro-projeto-de-comunicacao-inicio-de-obra-portal-de-edificacoes).
6. Conferir os modelos editáveis de selo e planilha quando for implementada a emissão de pranchas.

Não houve instalação de plugin, emissão de IBED, protocolo, aprovação municipal ou criação de planta nesta etapa. Os arquivos baixados são referências de projeto, não uma confirmação de conformidade de uma residência ainda não definida.
