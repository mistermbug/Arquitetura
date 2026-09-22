"""Render the actual extrusion descriptors with Pillow, not an AI mockup."""
import sys,runpy,json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np
root=Path(__file__).resolve().parents[1]
api=runpy.run_path(str(root/'revit/casa_interiores.py'))
data=json.loads((root.parent/'json/rodolfo.json').read_text(encoding='utf-8-sig'))
design=api['scene'](data)
out=root/'entrega-0.4/exemplos'; out.mkdir(exist_ok=True)
(out/'interiores-rodolfo.json').write_text(json.dumps(design,ensure_ascii=False),encoding='utf-8')
font=lambda size:ImageFont.truetype('C:/Windows/Fonts/arial.ttf',size)

def faces(parts):
    result=[]
    for p in parts:
        low=p['vertices']; high=[[a[i]+p['direction'][i]*p['height'] for i in range(3)] for a in low]
        polygons=[low,high]+[[a,b,d,c] for a,b,c,d in zip(low,low[1:]+low[:1],high,high[1:]+high[:1])]
        for poly in polygons:
            a,b,c=poly[:3]; u=[b[i]-a[i] for i in range(3)];v=[c[i]-a[i] for i in range(3)]
            normal=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
            length=math.sqrt(sum(x*x for x in normal)) or 1
            shade=.65+.35*abs((normal[0]*.25-normal[1]*.35+normal[2]*.9)/length)
            color=tuple(min(255,round(x*shade)) for x in api['PALETTE'][p['material']])
            result.append((sum(v[0]-v[1]+v[2]*1.6 for v in poly)/len(poly),poly,color))
    return sorted(result,key=lambda v:v[0])

def render(parts,w,h):
    fs=faces(parts)
    project=lambda v:((v[0]+v[1])*.75,(v[0]-v[1])*.40-v[2])
    pts=[project(v) for _,poly,_ in fs for v in poly]
    xmin,ymin=min(x for x,y in pts),min(y for x,y in pts); xmax,ymax=max(x for x,y in pts),max(y for x,y in pts)
    scale=min((w-60)/(xmax-xmin),(h-60)/(ymax-ymin))
    ox=(w-(xmax-xmin)*scale)/2;oy=(h-(ymax-ymin)*scale)/2
    pixels=np.full((h,w,3),(247,243,235),dtype=np.uint8)
    depth=np.full((h,w),-np.inf)
    for _,poly,color in fs:
        ps=[(ox+(project(v)[0]-xmin)*scale,oy+(project(v)[1]-ymin)*scale) for v in poly]
        ds=[v[0]-v[1]+v[2]*.8 for v in poly]
        for i in range(1,len(ps)-1):
            inds=(0,i,i+1); (ax,ay),(bx,by),(cx,cy)=[ps[j] for j in inds]
            den=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
            if abs(den)<1e-8: continue
            x0=max(0,int(min(ax,bx,cx)));x1=min(w-1,int(max(ax,bx,cx))+1)
            y0=max(0,int(min(ay,by,cy)));y1=min(h-1,int(max(ay,by,cy))+1)
            xx,yy=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(y0,y1+1)+.5)
            u=((by-cy)*(xx-cx)+(cx-bx)*(yy-cy))/den
            v=((cy-ay)*(xx-cx)+(ax-cx)*(yy-cy))/den
            t=1-u-v
            z=u*ds[0]+v*ds[i]+t*ds[i+1]
            part=depth[y0:y1+1,x0:x1+1]
            mask=(u>=-1e-8)&(v>=-1e-8)&(t>=-1e-8)&(z>part)
            part[mask]=z[mask];pixels[y0:y1+1,x0:x1+1][mask]=color
    return Image.fromarray(pixels)

entries=[('sofa','Sofá com base de madeira'),('armchair','Poltrona oliva'),('dining_table','Mesa orgânica'),
         ('dining_chair','Cadeira em madeira e tecido'),('bed_double','Cama com cabeceira'),('nightstand','Mesa de cabeceira'),
         ('washer','Lavadora com porta frontal'),('plant','Vaso e folhagem')]
canvas=Image.new('RGB',(2000,1250),'#efe8dc');draw=ImageDraw.Draw(canvas)
draw.text((45,25),'CASA BR | Madeira e formas orgânicas',font=font(40),fill='#493b2d')
draw.text((45,78),'Coleção original • prévia da geometria gerada • materiais em cores sólidas',font=font(23),fill='#6c604e')
for n,(kind,label) in enumerate(entries):
    item=next(i for i in design['items'] if i['kind']==kind)
    if kind!='plant':
        f=dict(next(f for f in data['furniture'] if f['kind']==kind));f['rotation']=0;f['mirror']=0
        parts=api['furniture_parts'](f)
    else:parts=item['parts']
    x=(n%4)*500;y=135+(n//4)*540
    canvas.paste(render(parts,480,460),(x+10,y))
    draw.text((x+25,y+470),label,font=font(23),fill='#493b2d')
canvas.save(out/'colecao-brasileira.png')
render([p for i in design['items'] for p in i['parts']],2200,1600).save(out/'interiores-isometria.png')
print('Preview:',out/'colecao-brasileira.png')
print('Furniture:',len(data['furniture']),'Plants:',len(design['landscape']['plants']),'Parts:',sum(len(i['parts']) for i in design['items']))
