# CASA BH — AutoCAD → Revit

Cópia para transferência do trabalho desenvolvido até 22/09/2026. Inclui o gerador AutoLISP 0.4, a ponte JSON/Dynamo para Revit, móveis com medidas editáveis, catálogo de 15 espécies, exemplos, testes, pesquisas de interiores e documentos consultados de Belo Horizonte.

## Usar em outro computador

1. No GitHub, clique em **Code → Download ZIP** e extraia **toda a pasta** em um local permanente, por exemplo `C:\Projetos\casa-bh-autocad-revit`. Alternativamente, use `git clone` com a URL deste repositório. O repositório é privado: entre com a conta proprietária ou autorizada.
2. Tenha **AutoCAD 2027** e **Revit 2027 com Dynamo/PythonNet3** instalados. As licenças e os aplicativos não acompanham os arquivos.
3. No AutoCAD, use **APPLOAD** e carregue `programa-casa\entrega-0.4\CASA-BH.lsp`. É o único LISP que precisa ser carregado. Trabalhe no espaço Modelo em milímetros (`INSUNITS=4`).
4. Comandos: **CASA_GERAR**, **CASA_ALTERNATIVAS**, **CASA_MOVEL_EDITAR** e **CASA_EXPORTAR**. A edição de móveis recebe largura, profundidade e altura em metros.
5. Abra o PowerShell na pasta extraída e execute:

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File .\CONFIGURAR-NESTE-PC.ps1
   ```

   O configurador cria uma pasta `configurado` com os caminhos deste computador. Não instala programas, não altera o registro nem muda a política permanente do PowerShell. Por padrão, usa o exemplo `json\rodolfo.json`. Para outro arquivo:

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File .\CONFIGURAR-NESTE-PC.ps1 -JsonPath "C:\Projetos\minha-casa.json"
   ```

6. No Dynamo do Revit, abra o grafo apropriado:

   | Arquivo na pasta `configurado` | Uso |
   |---|---|
   | `01-IMPORTAR-CASA.dyn` | Importar a casa em um projeto Revit vazio. |
   | `02-ATUALIZAR-INTERIORES.dyn` | Atualizar móveis/vegetação da mesma casa já importada e auditar junções. |
   | `03-CORRIGIR-UNIOES.dyn` | Corrigir as junções da casa já importada. |

7. Os grafos abrem em **Manual**, com os dois Boolean em **False**. Confira o caminho do JSON no nó String. Mude o Boolean conectado a **IN[1]** para **True** e execute. Mantenha **IN[2]=False**. Ao terminar, volte IN[1] para False e salve o RVT.

Se mover a pasta posteriormente, execute novamente o configurador. Os arquivos antigos em `grafo/01.dyn` e os carregadores Python históricos mantêm caminhos da máquina original; prefira os novos arquivos da pasta `configurado`.

O ZIP `CASA-BH-AutoLISP-0.4.zip` é a entrega compacta anterior preservada. Para a transferência completa e a configuração automática, baixe **o repositório inteiro**.

## Conteúdo

- [`programa-casa/entrega-0.4`](programa-casa/entrega-0.4): LISP pronto, manuais e prévias.
- [`Guia de móveis e vegetação`](programa-casa/entrega-0.4/MOVEIS_PLANEJADOS_E_VEGETACAO.md): dimensões, critérios geométricos e limites.
- [`Catálogo de móveis`](programa-casa/entrega-0.4/exemplos/catalogo-moveis.png) e [`15 espécies`](programa-casa/entrega-0.4/exemplos/catalogo-vegetacao.png).
- [`programa-casa/revit`](programa-casa/revit): importador, atualizadores, geometria e catálogo configurável `vegetacao.json`.
- [`json/rodolfo.json`](json/rodolfo.json): modelo de exemplo exportado do AutoCAD.
- [`programa-casa/tests`](programa-casa/tests): testes e resultados relevantes; perfis temporários do AutoCAD foram excluídos desta cópia.
- [`planejamento-bh`](planejamento-bh): roadmap, matriz de regras, documentos oficiais, extratos e referências de origem.
- [`pesquisa-interiores`](pesquisa-interiores): pesquisa e regras iniciais de organização dos ambientes.
- [`MANIFESTO_TRANSFERENCIA.json`](MANIFESTO_TRANSFERENCIA.json): lista dos arquivos copiados, tamanhos e SHA-256 antes da normalização de finais de linha pelo Git.

Os documentos de terceiros permanecem com suas fontes e autoria. Não há licença de redistribuição geral adicionada ao acervo.

## Estado e limitações

A edição e persistência dos móveis foram ensaiadas no AutoCAD Core 2027. O conjunto de 20 testes Python cobre contrato de importação, geometria de móveis/vegetação, colisões e atualização. A execução da última revisão dentro do Revit ainda precisa ser validada no aplicativo; esta cópia não contém um RVT final da casa.

Os modelos são de estudo: móveis e plantas são DirectShapes estilizados. Materiais fotorrealistas, iluminação e renderização HD final ainda não foram produzidos. Os volumes dos componentes de mobiliário não são um plano de fabricação ou orçamento de materiais. A documentação de BH é uma base datada, sujeita a conferência de vigência e aplicação ao lote real.

## Desenvolvimento e testes

Para testes de contrato e geometria, instale Python 3 e execute na raiz:

```powershell
python -m unittest discover -s programa-casa/revit -p test_validate.py
python -m unittest discover -s programa-casa/revit -p test_interiores.py
```

Esses testes não exigem Autodesk ou bibliotecas externas. Renderizar as prévias locais requer Pillow e NumPy (`python -m pip install -r requirements-preview.txt`). Os scripts históricos de ensaio nativo do AutoCAD contêm caminhos da instalação original; ajuste o executável/template antes de usá-los. O teste `test_unioes_revit_dynamo.py` é destinado ao Dynamo dentro do Revit, não ao executor unittest.

Para reconstruir a entrega compacta a partir do código-fonte, execute `python programa-casa/build-release-04.py`. Use somente a entrega 0.4; scripts antigos de build são registros do desenvolvimento.
