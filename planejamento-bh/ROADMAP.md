# Roadmap: gerador residencial no AutoCAD 2027 para Belo Horizonte

Data: 07/09/2026. Estado: pesquisa inicial e desenho do produto. O usuário confirmou AutoCAD 2027; edição completo/LT ainda não confirmada. Três subagentes auxiliaram a pesquisa de manuais, legislação e integração Autodesk. Nenhum gerador CAD foi implementado nesta etapa.

## Objetivo acordado

O cliente informa os ambientes desejados em campos obrigatórios. O aplicativo gera alternativas de planta dentro do AutoCAD. Nesta etapa, a variedade da distribuição importa mais que o refinamento decorativo. A geração deve preservar o programa e testar restrições geométricas e urbanísticas implementadas. Depois virão interiores e criação de elementos BIM no Revit.

O primeiro trabalho solicitado foi encontrar, baixar e assimilar os materiais de BH. O pacote local contém documentos oficiais, extratos pesquisáveis, registros de procedência e uma lista explícita das lacunas. Essa base não é uma revisão jurídica integral e não habilita aprovação automática pela Prefeitura.

## Decisões e perguntas em aberto

| Item | Situação |
|---|---|
| AutoCAD | 2027, confirmado pelo usuário. |
| Sistema operacional | Ambiente desta tarefa é Windows. |
| Completo ou LT | Pendente. Recomendação C# depende da edição completa. |
| Versão do Revit | Pendente; não fixar SDK do adaptador Revit antes disso. |
| Primeiro tipo de casa | Proposta provisória: unifamiliar térrea, sem subsolo. Pergunta enviada. |
| Primeiro lote | Terreno hipotético plano, confirmado pelo usuário. Dimensões ainda não definidas; formato retangular e uma frente são propostas do MVP. |
| Evolução dos terrenos | Suporte a terrenos reais confirmado como objetivo posterior; incorporar levantamento e condicionantes próprios. |
| Município | Belo Horizonte/MG, confirmado no pedido. |
| Precisão municipal | Por regras e dados comprovados do lote, com cobertura declarada. |
| Linguagem natural | Pode preencher um rascunho do formulário; campos obrigatórios continuam sendo conferidos. |

As hipóteses simples servem ao planejamento do MVP; não foram apresentadas como respostas do usuário. Lote de esquina, declive, patrimônio, múltiplas unidades, reforma e regularização exigem ramificações específicas.

Atualização de escopo: o usuário confirmou começar com terreno considerado plano e trabalhar com terrenos reais posteriormente. No protótipo, a superfície pode ser representada por um plano horizontal com cota local zero, convenção de modelagem que não corresponde a uma altitude levantada. Preservar no contrato os campos de origem dos dados, sistema de coordenadas e referência vertical para a evolução. A escolha de terreno plano não confirma, por si só, casa térrea, formato retangular ou dimensões do lote.

## Etapas e critérios para avançar

| Etapa | Trabalho | Entrega e critério de conclusão | Estado |
|---|---|---|---|
| 0. Base BH | Baixar guias; identificar legislação, versões e condicionantes; relacionar documentos às regras | Acervo local com origem, hash e limites de validade; plano de fechamento de lacunas | Acervo inicial realizado; consolidação normativa pendente |
| 1. Programa e lote | Definir formulário, contagens, unidades, geometria do terreno e perfil municipal | Exemplo de entrada sem ambiguidades; campos ausentes geram pendência | Especificado nesta entrega |
| 2. Núcleo gerador | Produzir configurações com aleatoriedade controlada, topologia de acesso e geometria | Alternativas reproduzíveis com todos os ambientes; resultados de validação e limite de tentativas | A implementar |
| 3. AutoCAD | Criar comando, formulário e adaptador de desenho | Gerar planta editável, cotada e identificada no AutoCAD 2027; desfazer sem resíduos | A implementar |
| 4. Piloto de integração | Passar um ambiente simples e seus elementos ao Revit | Escala, posição, paredes e aberturas corretas; repetição sem duplicatas | Antecipar antes de ampliar o gerador |
| 5. Regras BH executáveis | Implementar subconjunto revisado e testar seus limites | Relatório por regra com fonte, valor e resultado; cobertura explícita | Depende do lote e da consolidação |
| 6. Qualidade arquitetônica e interiores | Incorporar mobiliário funcional, relações espaciais e conforto | Verificações de uso, circulação e geometria; avaliações ambientais quando configuradas | Usará a base pesquisa-interiores |
| 7. Revit completo | Criar e atualizar famílias e elementos nativos a partir do modelo comum | Planta e 3D coerentes, IDs persistentes e política de conflitos | Futuro |
| 8. Documentação de projeto | Automatizar as peças pertinentes e revisão técnica | Pranchas e documentos conforme a modalidade e exigências verificadas | Futuro; não confundir com planta baixa isolada |

Não há estimativa de prazo fechada: a confirmação das versões, do lote e do escopo de legislação altera o esforço. Cada etapa terá demonstração verificável antes de ampliar a seguinte.

## Tecnologia proposta

Para **AutoCAD 2027 completo no Windows**, usar C# com a versão de .NET compatível com o SDK do produto; a tabela oficial consultada informa .NET 10.0 para 2027. Formulário WPF é uma escolha de implementação proposta. [Compatibilidade Autodesk](https://help.autodesk.com/cloudhelp/2027/ENU/AutoCAD-Customization/files/GUID-A6C680F2-DE2E-418A-A182-E4884073338A.htm).

AutoLISP com DCL é uma alternativa para demonstração menor e para avaliar suporte em LT. A matriz Autodesk diferencia suporte a AutoLISP e a Managed .NET por produto/plataforma; LT Windows não dispõe de Managed .NET. Confirmar edição antes de implementar. [Matriz de interfaces](https://help.autodesk.com/cloudhelp/2027/ENU/AutoCAD-Customization/files/GUID-E6429154-36DF-4D84-8ABC-9FCA15B66158.htm).

Arquitetura proposta:

- `Domain`: lote, pavimentos, programa, ambientes, paredes, vãos e identidade dos objetos.
- `Generator`: lógica de distribuição, independente das APIs Autodesk.
- `Validation`: geometria, programa e perfis normativos revisados.
- `AutoCADAdapter`: formulário, leitura do lote e desenho no CAD.
- `RevitAdapter`: futuro consumidor do mesmo modelo de dados.
- `AIAdapter`: futuro intérprete de pedidos do cliente e explicações.

O núcleo inicial pode funcionar sem serviço de IA. Assim, “gerar outra alternativa” não depende de uma chamada de modelo. O código e o perfil técnico calculam a geometria; uma futura interpretação de texto só propõe valores para o formulário.

## Formulário obrigatório

“Obrigatório” é requisito do aplicativo, salvo quando identificado expressamente como exigência municipal. Não pedir que o cliente adivinhe recuos ou índices urbanísticos.

| Bloco | Campos | Regras do formulário |
|---|---|---|
| Projeto | Nome, modo conceitual/lote real, uso e pavimentos | No MVP simples, uso unifamiliar e um pavimento podem vir fixos e visíveis. |
| Moradores | Quantidade de moradores; necessidades de acessibilidade: sim, não ou a definir | “A definir” gera pendência correspondente. |
| Dormir | Total de quartos e quantos são suítes | Inteiros; suítes não podem exceder quartos. |
| Banheiros | Banheiros sociais completos e lavabos | Contar separadamente dos banheiros das suítes. |
| Social | Quantidade de salas; jantar integrado ou separado | Não contar sala integrada duas vezes na área. |
| Serviço | Cozinhas, lavanderias e armazenamento adicional | Campo respondido, incluindo zero se admitido pelo programa. |
| Veículos | Vagas desejadas | Desejo do cliente não define eventual mínimo legal. |
| Outros | Lista explícita de ambientes adicionais, ou “nenhum” | Quantidade, função e prioridade; não descartar silenciosamente. |
| Tamanho | Intervalo desejado de área construída ou escolha de perfil de tamanho documentado | Distinguir área útil, construída e área computável urbanística. |
| Lote | Polígono fechado ou largura/profundidade; unidade; frente/acesso | Sem lote não há encaixe verificável. Lote hipotético deve estar identificado. |
| Preferências | Cozinha integrada/separada/indiferente; outras relações opcionais | Preferências flexibilizáveis, diferente de ambientes obrigatórios. |

Campos técnicos para lote real: identificação cadastral, CP quando pertinente, levantamento, norte, testadas, topografia, zoneamento/sobreposições e perfil de condicionantes com fonte e data. A consulta desses dados cabe ao fluxo técnico. Dados desconhecidos ficam nulos, nunca zero.

Exemplo de interpretação: “3 quartos, sendo 1 suíte, cozinha e sala” corresponde a três dormitórios, dos quais um possui banheiro privativo. Banheiro social, lavanderia, vagas, área e lote ainda precisam de resposta ou de um perfil explicitamente escolhido. A frase isolada não encerra o programa.

## Como gerar plantas aleatórias úteis

1. Conferir o programa, o perfil construtivo e o modo de uso.
2. Construir o envelope de implantação com os parâmetros disponíveis. Em modo fictício, usar perfil de ensaio identificado, sem atribuí-lo à legislação de BH.
3. Criar relações entre ambientes e acessos. Exemplo de preferência: cozinha próxima à sala; exemplo de restrição: cada ambiente precisa ser alcançável por portas e circulação.
4. Sortear uma organização espacial entre alternativas previstas, incluindo posições e dimensões dentro de intervalos configurados.
5. Resolver o encaixe considerando espessura das paredes, áreas úteis e posições possíveis de aberturas.
6. Criar paredes compartilhadas uma única vez e associar portas/janelas a hospedeiros.
7. Rejeitar colisões, ambientes fora do envelope, contagens incorretas e demais violações obrigatórias implementadas.
8. Retornar até três alternativas viáveis distintas e explicar pendências. Se menos alternativas forem encontradas, mostrar a quantidade real.

Salvar seed, versão do algoritmo, perfil de regras, dados completos e geometria escolhida. A seed sozinha não garante reprodução após mudança do código. Limitar tempo/tentativas; “não foi encontrada solução” não prova impossibilidade matemática do programa.

Inicialmente não é necessário otimizar decoração. Continuam necessários acesso, paredes coerentes, aberturas e um conjunto mínimo de verificações para a planta ser útil. A lógica deve permitir futuramente reservar envelopes de móveis desde a geração arquitetônica.

## Saída do primeiro protótipo CAD

Comandos propostos: `CASA_GERAR`, `CASA_ALTERNATIVA`, `CASA_VALIDAR`, `CASA_EXPORTAR`. São nomes de projeto, ainda não disponíveis.

Desenhar lote, envelope, paredes, vãos, identificação dos ambientes, áreas e cotas em layers próprios. Cada geração deve permitir desfazer, manter entidades externas ao projeto e salvar seus dados em JSON. Registrar ID estável do domínio; handles CAD e identificadores Revit são mapeamentos por documento.

Separar resultados `atende`, `nao_atende`, `nao_verificado`, `nao_aplicavel`. Uma planta pode atender às contagens e ainda não ter avaliação municipal. A interface deve mostrar a cobertura das verificações, sem transformar ausência de falha em “aprovado pela PBH”.

## Testes que demonstram funcionamento

- Mesmo conjunto de entradas e versões gera a mesma geometria.
- Três quartos com uma suíte produz exatamente três dormitórios e um banheiro privativo.
- Campos vazios, negativos, suítes excedentes e lote inválido são rejeitados antes de desenhar.
- Todos os ambientes são alcançáveis; portas têm paredes hospedeiras válidas.
- Polígonos fechados, áreas positivas, paredes coerentes e ausência de sobreposição indevida.
- Restrições implementadas testadas abaixo, no limite e acima do valor adotado.
- Parâmetro municipal desconhecido gera `nao_verificado`.
- Amostra de sementes registra taxa de sucesso, diversidade e tempo de processamento.
- Erro/cancelamento desfaz alterações da operação; desenho pré-existente permanece íntegro.
- Piloto Revit verifica escala, orientação e reimportação sem duplicação.

## Próxima execução concreta

Confirmar as respostas pendentes; escolher um caso de teste; completar o perfil técnico desse caso; implementar o núcleo geométrico e o formulário. O primeiro demonstrador deve resolver uma tipologia limitada e declarar suas restrições. A presente entrega prepara esse trabalho e registra o que ainda não foi comprovado.
