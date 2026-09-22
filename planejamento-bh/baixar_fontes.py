"""Baixa fontes públicas indicadas pela PBH, valida PDFs e registra procedência.
Executar com Python com pypdf instalado. Não autentica nem protocola projetos.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from datetime import datetime, timezone
import hashlib
import json
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
BASE = 'https://prefeitura.pbh.gov.br/sites/default/files/estrutura-de-governo/'
SOURCES = [
    ('representacao-r5', 'Cartilha de Representação Gráfica R5', BASE+'politica-urbana/2025/cartilharepresentacaopbh_smpu_r5.pdf', 'manual'),
    ('niveis-terreno', 'Representação de níveis de terreno', BASE+'politica-urbana/representacao-de-niveis-de-terreno-1_0.pdf', 'orientacao'),
    ('zoneamento', 'E-book Plano Diretor: zoneamento', BASE+'politica-urbana/2023/001_zoneamento_0.pdf', 'didatico'),
    ('parametros-urbanisticos', 'E-book Plano Diretor: parâmetros urbanísticos', BASE+'politica-urbana/2023/002_parametros-urbanisticos_0.pdf', 'didatico'),
    ('procedimentos', 'E-book Plano Diretor: procedimentos', BASE+'politica-urbana/2023/005_procedimentos_0.pdf', 'didatico'),
    ('plano-diretor-ebook', 'E-book Plano Diretor: versão completa atualizada no link PBH', BASE+'politica-urbana/2023/versao-completa-atualizada_1.pdf', 'didatico'),
    ('lei-11181', 'Lei 11.181: PDF publicado pela PBH; consolidação a conferir', BASE+'meio-ambiente/lei11181-atual.pdf', 'legislacao_consolidacao_a_conferir'),
    ('mapa-zoneamento', 'Anexo I: mapa de zoneamento publicado pela PBH', BASE+'politica-urbana/2020/lei11181-01-anexo-i-mapa-de-estrutura-urbana-zoneamento.pdf', 'mapa_referencia_conferir_sobreposicoes'),
    ('mapa-ade', 'Anexo III: áreas de diretrizes especiais', BASE+'politica-urbana/2020/lei11181-03-anexo-iii-mapa-de-areas-de-diretrizes-especiais.pdf', 'mapa_referencia_conferir_alteracoes'),
    ('mapa-viario-jul2026', 'Anexo V: hierarquização viária, julho de 2026', BASE+'politica-urbana/2026/anexo-v_mp_hierar_sist_viar_a0_jul_26.pdf', 'mapa'),
]

def main():
    (ROOT/'fontes').mkdir(exist_ok=True)
    (ROOT/'extratos').mkdir(exist_ok=True)
    manifest=ROOT/'manifesto-fontes.json'
    existing={r['id']:r for r in json.loads(manifest.read_text(encoding='utf-8'))} if manifest.exists() else {}
    entries=[]
    for key,title,url,kind in SOURCES:
        old=existing.get(key,{})
        old_path=ROOT/old.get('file','missing')
        if old.get('status')=='downloaded_and_parsed' and old_path.is_file() and hashlib.sha256(old_path.read_bytes()).hexdigest()==old.get('sha256'):
            entries.append(old)
            continue
        row=dict(id=key,title=title,url=url,kind=kind,checked_at=datetime.now(timezone.utc).isoformat(),legal_status='vigencia_e_alteracoes_nao_certificadas')
        try:
            req=Request(url, headers={'User-Agent':'Mozilla/5.0 (local architectural research)'})
            with urlopen(req, timeout=45) as response:
                data=response.read()
                row.update(final_url=response.url,content_type=response.headers.get('Content-Type'))
            if not data.startswith(b'%PDF-'):
                raise ValueError('Resposta não é PDF')
            path=ROOT/'fontes'/f'{key}.pdf'
            path.write_bytes(data)
            reader=PdfReader(path)
            texts=[f'\n\n--- Página PDF {i+1} ---\n'+(page.extract_text() or '') for i,page in enumerate(reader.pages)]
            (ROOT/'extratos'/f'{key}.txt').write_text(''.join(texts),encoding='utf-8')
            row.update(status='downloaded_and_parsed',file=str(path.relative_to(ROOT)),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),pages=len(reader.pages))
            print(key, row['pages'], 'páginas',flush=True)
        except Exception as exc:
            row.update(status='failed',error=str(exc))
            print(key,'FALHOU',str(exc),flush=True)
        entries.append(row)
        (ROOT/'manifesto-fontes.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':
    main()
