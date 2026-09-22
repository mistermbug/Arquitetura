from pathlib import Path
from urllib.request import Request, urlopen
from datetime import datetime, timezone
import hashlib, json
from html.parser import HTMLParser

class TextReader(HTMLParser):
 def __init__(self):
  super().__init__(); self.parts=[]; self.hidden=0
 def handle_starttag(self,tag,attrs):
  if tag in ('script','style'): self.hidden+=1
 def handle_endtag(self,tag):
  if tag in ('script','style'): self.hidden=max(0,self.hidden-1)
 def handle_data(self,data):
  if not self.hidden and data.strip(): self.parts.append(data.strip())

root=Path(__file__).resolve().parent
(root/'fontes-web').mkdir(exist_ok=True)
pages={
 'indice-legislacao':'https://prefeitura.pbh.gov.br/politica-urbana/informacoes/legislacao-urbanistica',
 'indice-cartilhas':'https://prefeitura.pbh.gov.br/politica-urbana/informacoes/publicacoes-e-cartilhas',
 'indice-mapas':'https://prefeitura.pbh.gov.br/politica-urbana/planejamento-urbano/base-de-dados/mapas-legislacao-urbanistica',
 'faq-smpu':'https://prefeitura.pbh.gov.br/politica-urbana/perguntas-frequentes-smpu',
 'manual-portal-indice':'https://prefeitura.pbh.gov.br/politica-urbana/informacoes/publicacoes-e-cartilhas/manual-portal-de-edificacoes',
 'checklist-documentacao':'https://docs.google.com/document/d/e/2PACX-1vRET6Ug0kkn6p5A6bpAhnRYECvrFIM_V_Xi3_r_x9IjKVCBnOyyvvqBQNMtd6gzb2uzJZBZ3VD0Uadn/pub',
 'codigo-edificacoes-consulta':'https://www.cmbh.mg.gov.br/atividade-legislativa/pesquisar-legislacao/lei/9725/2009',
 'regulamento-codigo-consulta':'https://www.cmbh.mg.gov.br/atividade-legislativa/pesquisar-legislacao/decreto/13842/2010',
 'regulamento-plano-consulta':'https://www.cmbh.mg.gov.br/atividade-legislativa/pesquisar-legislacao/decreto/17273/2020',
}
rows=[]
for key,url in pages.items():
 row=dict(id=key,url=url,checked_at=datetime.now(timezone.utc).isoformat())
 try:
  with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40) as response:
   data=response.read(); row['final_url']=response.url
  path=root/'fontes-web'/f'{key}.html'; path.write_bytes(data)
  parser=TextReader(); parser.feed(data.decode('utf-8',errors='replace'))
  txt='\n'.join(parser.parts)
  (root/'extratos'/f'{key}.txt').write_text(txt,encoding='utf-8')
  row.update(status='html_archived',sha256=hashlib.sha256(data).hexdigest(),file=str(path.relative_to(root)),bytes=len(data),text_chars=len(txt),content_verification='pagina_de_consulta_nao_comprova_texto_legal' if key.endswith('consulta') else 'conteudo_para_consulta')
  print(key,len(txt),'caracteres',flush=True)
 except Exception as exc:
  row.update(status='failed',error=str(exc)); print(key,'FALHOU',str(exc),flush=True)
 rows.append(row)
 (root/'manifesto-web.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
