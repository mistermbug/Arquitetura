from pathlib import Path
import json, zipfile
root=Path(__file__).resolve().parent
out=root/'entrega-0.2'
out.mkdir(exist_ok=True)
core=(root/'casa-core.lsp').read_text()
interface=(root/'casa.lsp').read_text()
start=interface.index('(defun cg:ensure-core')
end=interface.index('(defun cg:accept',start)
interface=interface[:start]+'(defun cg:ensure-core () T)\n'+interface[end:]
interface=interface.replace('(setq dlg (load_dialog (strcat *casa-dir* "/casa.dcl")))','(setq dlg (load_dialog (cg:embedded-dialog)))')
lines=(root/'casa.dcl').read_text().splitlines()
embedded='(defun cg:embedded-dialog (/ file stream)\n (setq file (vl-filename-mktemp "casa-bh-" nil ".dcl") stream (open file "w"))\n'
embedded+=''.join(' (write-line '+json.dumps(line)+' stream)\n' for line in lines)
embedded+=' (close stream) (setq *casa-temp-dcl* file) file)\n'
interface=interface.replace('(unload_dialog dlg)', '(progn (unload_dialog dlg) (if *casa-temp-dcl* (vl-file-delete *casa-temp-dcl*)))')
(out/'CASA-BH.lsp').write_text(core+'\n'+embedded+'\n'+interface,encoding='ascii')
(out/'LEIA-ME.md').write_text("""# CASA BH 0.2 â€” um Ãºnico AutoLISP

1. Abra um desenho novo no espaÃ§o Modelo. Use milÃ­metros (INSUNITS = 4).
2. Execute APPLOAD e carregue **CASA-BH.lsp** desta pasta. Ele contÃ©m o gerador, o desenho, a exportaÃ§Ã£o e o formulÃ¡rio. NÃ£o carregue os LISPs antigos.
3. Execute CASA_GERAR. Preencha as quantidades e **Parede interna** / **Parede externa**, em metros (por exemplo 0,15 e 0,20).
4. Confirme e indique o ponto de inserÃ§Ã£o. Use ZOOM Extents para ver o conjunto.
5. CASA_EXPORTAR salva o JSON para o importador em revit/. As espessuras individuais seguem em cada parede.

CorreÃ§Ãµes: quantidades inteiras lidas como 3.0 agora funcionam; quantidades fracionÃ¡rias continuam rejeitadas. As paredes internas e externas tÃªm espessuras independentes, com ajuste dos eixos, Ã¡reas Ãºteis e profundidade da casa.

O formulÃ¡rio DCL estÃ¡ embutido no LISP e Ã© extraÃ­do temporariamente ao abrir. NÃ£o Ã© preciso selecionar outro LISP ou copiar um DCL separado. Os arquivos modulares antigos sÃ£o fontes de desenvolvimento, nÃ£o dependÃªncias desta entrega.

Estudo preliminar: legislaÃ§Ã£o municipal, conforto e acessibilidade ainda nÃ£o sÃ£o validados. A exportaÃ§Ã£o contÃ©m o estado gerado; ediÃ§Ãµes manuais no CAD nÃ£o sÃ£o sincronizadas. O importador Revit ainda requer ensaio na sua instalaÃ§Ã£o; mÃ³veis sÃ£o volumes esquemÃ¡ticos. Consulte revit/README.md.
""",encoding='utf-8')
with zipfile.ZipFile(root.parent/'CASA-BH-AutoLISP-0.2.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in out.iterdir():
  if p.is_file(): z.write(p,p.name)
 for p in (root/'revit').iterdir():
  if p.is_file(): z.write(p,'revit/'+p.name)
print(out/'CASA-BH.lsp')
