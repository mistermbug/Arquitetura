"""Preview only: renders simple native DXF entities, not a CAD replacement."""
from pathlib import Path
import sys, math, re
from PIL import Image, ImageDraw, ImageFont

source, target = map(Path, sys.argv[1:3])
lines = source.read_text(encoding='cp1252').splitlines()
pairs = [(int(lines[i]), lines[i+1].strip()) for i in range(0,len(lines)-1,2)]
records=[]
for code,value in pairs:
    if code==0: records.append([(code,value)])
    elif records: records[-1].append((code,value))
def val(r,c,default='0'):
    return next((v for k,v in r if k==c),default)
def num(r,c,default='0'): return float(val(r,c,default))
def point(r,c=10): return (num(r,c),num(r,c+10))
blocks={}; entities=[]; section=''; block=None
for r in records:
    kind=val(r,0)
    if kind=='SECTION': section=val(r,2)
    elif kind=='ENDSEC': section=''
    elif section=='BLOCKS':
        if kind=='BLOCK': block=val(r,2); blocks[block]=[]
        elif kind=='ENDBLK': block=None
        elif block: blocks[block].append(r)
    elif section=='ENTITIES': entities.append(r)
expanded=[]
for r in entities:
    expanded.extend(blocks.get(val(r,2),[]) if val(r,0)=='DIMENSION' else [r])
palette={'CASA_PAREDES':'#293944','CASA_MOVEIS':'#728b7a','CASA_JANELAS':'#157eac','CASA_PORTAS':'#99662c','CASA_COTAS':'#5e6670','CASA_ESTUDO':'#68717c','CASA_TERRENO':'#a4abb0'}
def render(bounds,path,width):
    x0,y0,x1,y1=bounds; scale=width/(x1-x0); height=round((y1-y0)*scale)
    im=Image.new('RGB',(width,height),'white'); d=ImageDraw.Draw(im)
    def xy(p): return ((p[0]-x0)*scale,(y1-p[1])*scale)
    for r in expanded:
        kind=val(r,0); color=palette.get(val(r,8),'#37444e')
        if kind=='LINE': d.line([xy(point(r)),xy(point(r,11))],fill=color,width=2)
        elif kind=='LWPOLYLINE':
            xs=[float(v) for k,v in r if k==10]; ys=[float(v) for k,v in r if k==20]
            pts=[xy(p) for p in zip(xs,ys)]
            if int(val(r,70)) & 1: pts.append(pts[0])
            if len(pts)>1: d.line(pts,fill=color,width=2)
        elif kind=='CIRCLE':
            cx,cy=point(r); radius=num(r,40)
            d.ellipse([xy((cx-radius,cy+radius)),xy((cx+radius,cy-radius))],outline=color,width=2)
        elif kind=='ARC':
            cx,cy=point(r); radius=num(r,40); start=num(r,50); end=num(r,51)
            if end<start: end+=360
            pts=[xy((cx+radius*math.cos(math.radians(start+(end-start)*i/60)),cy+radius*math.sin(math.radians(start+(end-start)*i/60)))) for i in range(61)]
            d.line(pts,fill=color,width=2)
        elif kind in ('TEXT','MTEXT'):
            txt=re.sub(r'\\A\d+;', '', val(r,1,'')).replace('\\P',' ').replace('%%c','Ø')
            size=max(8,round(num(r,40)*scale*1.25))
            font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',size)
            loc=xy(point(r)); angle=num(r,50)
            if abs(angle)>0.01 and kind=='TEXT':
                box=font.getbbox(txt); label=Image.new('RGBA',(max(1,box[2]+8),size*2),(255,255,255,0))
                ImageDraw.Draw(label).text((2,0),txt,font=font,fill=color)
                label=label.rotate(angle,expand=True); im.paste(label,(int(loc[0]-label.width),int(loc[1]-label.height)),label)
            else: d.text((loc[0],loc[1]-size),txt,font=font,fill=color)
    im.save(path)
target.mkdir(parents=True,exist_ok=True)
render((-1800,-1800,42500,31600),target/'previa-conjunto.png',3000)
render((-1800,3000,12700,20700),target/'previa-planta.png',1600)
print('Previews generated from native DXF; simple text placement may differ from AutoCAD.')

if len(sys.argv)>3 and sys.argv[3]=='v03':
    for n in range(3):
        render((-1800+n*41000,-4500,14700+n*41000,32000),target/f'alternativa-{n+1}.png',1300)
    render((-1800,-4500,122000,33000),target/'comparacao.png',4400)
