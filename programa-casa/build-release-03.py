from pathlib import Path
import json
import zipfile

root = Path(__file__).resolve().parent
out = root / 'entrega-0.3'
out.mkdir(exist_ok=True)
sources = ['casa-core.lsp', 'casa-layout.lsp', 'casa-furniture.lsp']
core = '\n'.join((root / name).read_text(encoding='ascii') for name in sources)
interface = (root / 'casa.lsp').read_text(encoding='ascii')
start = interface.index('(defun cg:ensure-core')
end = interface.index('(defun cg:accept', start)
interface = interface[:start] + '(defun cg:ensure-core () T)\n' + interface[end:]
interface = interface.replace('(setq dlg (load_dialog (strcat *casa-dir* "/casa.dcl")))',
                              '(setq dlg (load_dialog (cg:embedded-dialog)))')
embedded = '(defun cg:embedded-dialog (/ file stream)\n (setq file (vl-filename-mktemp "casa-bh-" nil ".dcl") stream (open file "w"))\n'
for line in (root / 'casa.dcl').read_text(encoding='ascii').splitlines():
    embedded += ' (write-line ' + json.dumps(line) + ' stream)\n'
embedded += ' (close stream) (setq *casa-temp-dcl* file) file)\n'
interface = interface.replace('(unload_dialog dlg)',
                              '(progn (unload_dialog dlg) (if *casa-temp-dcl* (vl-file-delete *casa-temp-dcl*)))')
display = (root / 'casa-display.lsp').read_text(encoding='ascii')
(out / 'CASA-BH.lsp').write_text(core + '\n' + embedded + '\n' + interface + '\n' + display, encoding='ascii')
with zipfile.ZipFile(root.parent / 'CASA-BH-AutoLISP-0.3.zip', 'w', zipfile.ZIP_DEFLATED) as bundle:
    for p in sorted(out.rglob('*')):
        if p.is_file():
            bundle.write(p, p.relative_to(out))
    for name in ['importar_casa_dynamo.py', 'README.md']:
        bundle.write(root / 'revit' / name, 'revit/' + name)
print(out / 'CASA-BH.lsp')
