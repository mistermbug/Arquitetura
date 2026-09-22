"""Independent topology and dimension checks on the actual AutoCAD DXF."""
import collections
import json
from pathlib import Path
import sys

folder = Path(sys.argv[1])
lines = (folder / 'comparacao.dxf').read_text(encoding='cp1252').splitlines()
records = []
for i in range(0, len(lines)-1, 2):
    code, value = int(lines[i]), lines[i+1].strip()
    if code == 0:
        records.append([])
    if records:
        records[-1].append((code, value))

def value(record, code, default=None):
    return next((v for k, v in record if k == code), default)

def point(record, code):
    return tuple(round(float(value(record, c)), 5) for c in (code, code+10))

wall_edges = [r for r in records if value(r, 0) == 'LINE' and (1000, 'WALL-UNION') in r]
assert wall_edges, 'No union boundary drawn'
edges = [(point(r,10), point(r,11)) for r in wall_edges]
assert len(set(tuple(sorted(e)) for e in edges)) == len(edges), 'Duplicate wall edges'
degree = collections.Counter(p for e in edges for p in e)
assert all(n == 2 for n in degree.values()), 'Wall contours have open ends or crossing junctions'
for a,b in edges:
    assert a != b and (a[0] == b[0] or a[1] == b[1]), 'Degenerate/nonorthogonal edge'
horizontal = [(a,b) for a,b in edges if a[1] == b[1]]
vertical = [(a,b) for a,b in edges if a[0] == b[0]]
for a,b in horizontal:
    for c,d in vertical:
        assert not (min(a[0],b[0]) < c[0] < max(a[0],b[0]) and
                    min(c[1],d[1]) < a[1] < max(c[1],d[1])), 'Wall boundaries cross'

models = {m['project_id']:m for p in folder.glob('desenho-*.json')
          for m in [json.loads(p.read_text(encoding='utf-8-sig'))]}
checked = 0
for record in records:
    if value(record,0) != 'DIMENSION':
        continue
    app_start = next((i for i,pair in enumerate(record) if pair == (1001,'CASA_BH')), len(record))
    tags = [v for k,v in record[app_start+1:] if k == 1000]
    if len(tags) < 2 or tags[0] not in models:
        continue
    pid, tag = tags[:2]
    if not tag.startswith(('DX-CLEAR-', 'DY-CLEAR-')):
        continue
    room = next(r for r in models[pid]['rooms'] if r['id'] == tag.split('CLEAR-')[1])
    axis = 0 if tag.startswith('DX') else 1
    lo, hi = room['bounds'][axis], room['bounds'][axis+2]
    a,b = point(record,13),point(record,14)
    assert abs(a[axis]-lo) < .01 and abs(b[axis]-hi) < .01, 'Dimension not on clear faces'
    assert abs(a[1-axis]-b[1-axis]) < .01
    checked += 1
assert checked > 20, 'Missing room dimensions'
report = f'PASS: {len(edges)} wall edges; closed contours, no duplicates/crossings; {checked} clear-face dimensions.\n'
(folder / 'presentation-check.txt').write_text(report, encoding='utf-8')
print(report)
