from pathlib import Path
import hashlib, json
root=Path(__file__).resolve().parent
pdfs=json.loads((root/'manifesto-fontes.json').read_text(encoding='utf-8'))
web=json.loads((root/'manifesto-web.json').read_text(encoding='utf-8'))
for row in pdfs+web:
 if row.get('status') in ('downloaded_and_parsed','html_archived'):
  path=root/row['file']
  assert path.is_file(),row['id']
  assert hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256'],row['id']
rules=json.loads((root/'matriz-regras-bh.json').read_text(encoding='utf-8'))['rules']
source_ids={r['id'] for r in pdfs+web}
assert len({r['id'] for r in rules})==len(rules)
assert all(r['source_id'] in source_ids for r in rules)
assert all(r['enabled'] is False and r['legal_parameters'] is None for r in rules)
form=json.loads((root/'campos-formulario.json').read_text(encoding='utf-8'))
assert len({f['key'] for f in form['fields']})==len(form['fields'])
summary=dict(pdf_downloads=sum(r['status']=='downloaded_and_parsed' for r in pdfs),pdf_pages=sum(r.get('pages',0) for r in pdfs),html_downloads=sum(r['status']=='html_archived' for r in web),html_failures=sum(r['status']=='failed' for r in web),rule_groups=len(rules),form_fields=len(form['fields']),integrity='passed',scope='Integridade de arquivos e catálogos; não valida legislação nem funcionamento CAD.')
(root/'verificacao'/'integridade.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
