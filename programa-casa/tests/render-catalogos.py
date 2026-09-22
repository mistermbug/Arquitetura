"""Contact sheets rendered from the same extrusion geometry sent to Revit."""
import runpy, json, math
from pathlib import Path
from PIL import Image, ImageDraw

env=runpy.run_path(str(Path(__file__).with_name('render-interiores.py')))
api=env['api']; render=env['render']; font=env['font']; out=env['out']; data=env['data']
species=list(api['SPECIES'].values())
sheet=Image.new('RGB',(2000,1640),'#efe8dc'); draw=ImageDraw.Draw(sheet)
draw.text((35,20),'CASA BR | 15 espécies em vaso',font=font(40),fill='#493b2d')
draw.text((35,72),'Geometria real da coleção • escalas individuais • medidas incluem vaso e copa',font=font(23),fill='#6c604e')
for i,s in enumerate(species):
    w=s['canopy_mm'];h=s['height_mm']
    parts=api['plant_parts']({'bounds':[0,0,w,w],'height':h,'species_id':s['id']})
    x=(i%5)*400;y=115+(i//5)*500
    sheet.paste(render(parts,385,395),(x+7,y))
    draw.text((x+18,y+399),s['name'],font=font(22),fill='#493b2d')
    draw.text((x+18,y+432),f"{s['id']} | copa {w/1000:g} m · h {h/1000:g} m",font=font(18),fill='#6c604e')
sheet.save(out/'catalogo-vegetacao.png')
labels={'desk':'Escrivaninha','office_chair':'Cadeira de escritório','sofa':'Sofá','armchair':'Poltrona','dining_table':'Mesa de jantar','dining_chair':'Cadeira',
        'bed_double':'Cama de casal','bed_single':'Cama de solteiro','nightstand':'Mesa de cabeceira',
        'wardrobe':'Armário','tv_rack':'Rack','counter':'Bancada','washer':'Lavadora','fridge':'Geladeira',
        'sink':'Pia de cozinha','basin':'Lavatório','stove':'Fogão','shower':'Base de chuveiro',
        'toilet':'Vaso sanitário','laundry_sink':'Tanque','bench':'Banco','car':'Automóvel'}
unique={f['kind']:f for f in data['furniture']}
rows=math.ceil(len(unique)/5)
sheet=Image.new('RGB',(2000,130+rows*380),'#efe8dc');draw=ImageDraw.Draw(sheet)
draw.text((35,20),'CASA BR | Peças presentes no projeto',font=font(40),fill='#493b2d')
draw.text((35,72),f"{len(data['furniture'])} peças · {len(unique)} categorias · originais, sem modelos de fabricantes",font=font(23),fill='#6c604e')
for i,(kind,item) in enumerate(unique.items()):
    f=dict(item,rotation=0,mirror=0);parts=api['furniture_parts'](f)
    x=(i%5)*400;y=115+(i//5)*380
    sheet.paste(render(parts,385,325),(x+7,y))
    draw.text((x+18,y+330),labels.get(kind,kind),font=font(23),fill='#493b2d')
sheet.save(out/'catalogo-moveis.png')
print('Catalogos:',len(species),'especies;',len(unique),'categorias de moveis')
print('Especies no exemplo:',[p['species_id'] for p in api['landscape'](data)['plants']])
