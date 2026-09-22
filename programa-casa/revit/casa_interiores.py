"""Original Brazilian contemporary collection. Units: mm; no manufacturer assets.
Pure scene generation is separate from the Revit adapter for reproducible QA.
Detailed DirectShape models, not parametric RFA families or construction specs.
"""
import math
import json
import hashlib
from pathlib import Path

REVISION = '0.4-interiores-2'
CATALOG = json.loads(Path(__file__).with_name('vegetacao.json').read_text(encoding='utf-8-sig'))
SPECIES = {s['id']:s for s in CATALOG['species']}
PALETTE = {'wood': (113,73,45), 'wood_light': (173,124,76), 'linen': (226,214,188),
           'olive': (114,128,89), 'leather': (158,99,56), 'stone': (200,189,163),
           'bronze': (126,99,65), 'white': (242,240,232), 'dark': (43,48,45),
           'glass': (109,150,153), 'clay': (174,104,73), 'soil': (67,48,34),
           'leaf': (65,113,62), 'leaf_light': (112,150,73), 'flower_red': (166,42,46), 'flower_cream': (241,230,186)}

def plant_options(setting, offset=0):
    chosen=CATALOG['selection'].get(setting,[])
    if not isinstance(chosen,list) or any(k not in SPECIES or setting not in SPECIES[k]['settings'] for k in chosen):
        raise ValueError('Selecao de vegetacao invalida: '+setting)
    options=[SPECIES[k] for k in chosen] if chosen else [s for s in SPECIES.values() if setting in s['settings']]
    return options[offset%len(options):]+options[:offset%len(options)] if options else []

def item_signature(item):
    # Source dimensions and the generated geometry both participate. A style
    # revision alone cannot detect a changed CAD dimension or species choice.
    return hashlib.sha256(json.dumps(item,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()

def update_required(item,record,actual):
    previous=record.get('render_bounds')
    candidates=[previous] if previous else [item['bounds'],item.get('source_bounds_before_edit') or item['bounds']]
    if not any(max(abs(a-b) for a,b in zip(actual,expected))<=2 for expected in candidates):
        raise ValueError('Elemento deslocado/editado no Revit: '+item['id']+'. Atualizacao cancelada.')
    return not (previous and record.get('interior_revision')==REVISION and record.get('signature')==item_signature(item))

def hit(a,b):
    return a[0]<b[2]-.01 and a[2]>b[0]+.01 and a[1]<b[3]-.01 and a[3]>b[1]+.01

def expand(b,d):
    return [b[0]-d,b[1]-d,b[2]+d,b[3]+d]

def contains(outer,b):
    return all((b[0]>=outer[0],b[1]>=outer[1],b[2]<=outer[2],b[3]<=outer[3]))

def rounded(x,y,w,d,r):
    r=max(.1,min(r,w*.40,d*.40))
    points=[]
    for cx,cy,start in [(x+w-r,y+r,-90),(x+w-r,y+d-r,0),(x+r,y+d-r,90),(x+r,y+r,180)]:
        for j in range(5):
            t=math.radians(start+j*22.5)
            points.append([cx+r*math.cos(t),cy+r*math.sin(t)])
    return points

def ellipse(x,y,w,d,n=32):
    return [[x+w/2+w/2*math.cos(2*math.pi*i/n),y+d/2+d/2*math.sin(2*math.pi*i/n)] for i in range(n)]

def furniture_parts(item):
    b=item['bounds']; angle=int(round(item.get('rotation',0)))%360
    if angle not in (0,90,180,270):
        raise ValueError('Rotacao de movel nao ortogonal: '+item['id'])
    w,d=b[2]-b[0],b[3]-b[1]
    if angle in (90,270): w,d=d,w
    h=item['height']; k=item['kind']; parts=[]
    def block(x,y,z,ww,dd,hh,mat='wood',r=0,plane='xy'):
        if min(ww,dd,hh)<=.1: return
        outline=rounded(x,y,ww,dd,r) if r else [[x,y],[x+ww,y],[x+ww,y+dd],[x,y+dd]]
        parts.append({'profile':outline,'z':z,'height':hh,'material':mat,'plane':plane})
    def oval(x,y,z,ww,dd,hh,mat):
        parts.append({'profile':ellipse(x,y,ww,dd),'z':z,'height':hh,'material':mat,'plane':'xy'})
    def legs(top,mat='wood',radius=24):
        for x in (w*.12,w*.88):
            for y in (d*.14,d*.86): oval(x-radius,y-radius,0,radius*2,radius*2,top,mat)
    seed=sum(ord(c) for c in item['id'])
    cloth='olive' if k=='armchair' else 'linen'
    if k in ('sofa','armchair','loveseat'):
        legs(h*.18,'wood',min(w,d)*.033)
        block(0,0,h*.16,w,d,h*.14,'wood',70)
        n=max(1,round(w/750)); arm=min(w*.13,140)
        for i in range(n):
            block(arm+i*(w-2*arm)/n+4,20,h*.30,(w-2*arm)/n-8,d*.70,h*.24,cloth,70)
            block(arm+i*(w-2*arm)/n+4,d*.74,h*.35,(w-2*arm)/n-8,d*.26,h*.65,cloth,60)
        for x in (0,w-arm): block(x,0,h*.30,arm,d*.94,h*.43,cloth,arm*.45)
        block(arm+20,d*.53,h*.52,min(w*.2,340),d*.19,h*.25,'leather' if seed%2 else 'olive',40)
    elif k in ('dining_chair','office_chair','chair'):
        legs(h*.48,'wood',18)
        block(0,0,h*.45,w,d*.90,h*.10,'wood',w*.2)
        block(15,12,h*.55,w-30,d*.78,h*.08,'linen',w*.2)
        for x in (w*.09,w*.85): block(x,d*.85,h*.44,w*.06,d*.10,h*.50,'wood',12)
        block(0,d*.80,h*.72,w,d*.20,h*.28,'leather' if seed%2 else 'linen',45)
    elif k in ('dining_table','desk'):
        if k=='dining_table':
            for x in (w*.27,w*.73): oval(x-w*.10,d*.2,0,w*.2,d*.6,h*.91,'wood')
            oval(0,0,h*.91,w,d,h*.09,'wood_light' if seed%2 else 'stone')
        else:
            legs(h*.94)
            block(0,0,h*.92,w,d,h*.08,'wood_light',60)
    elif k in ('bed_double','bed_single','bed','double_bed','single_bed'):
        legs(h*.13)
        block(0,0,h*.10,w,d,h*.22,'wood',45)
        block(10,20,h*.32,w-20,d-50,h*.52,'linen',90)
        block(0,d-75,h*.1,w,75,h*.9,'olive' if seed%2 else 'linen',30)
        count=2 if w>1100 else 1
        for i in range(count): block(w*.06+i*w*.47,d*.73,h*.84,w*(.42 if count==2 else .88),d*.20,h*.16,'white',70)
        block(10,d*.13,h*.84,w-20,d*.21,h*.035,'leather',30)
    elif k in ('wardrobe','tv_rack','rack','nightstand','counter'):
        # Some CAD rack templates have their long axis along local Y.
        sideways=k in ('tv_rack','rack') and d>w
        ww,dd=(d,w) if sideways else (w,d)
        block(0,0,h*.10,w,d,h*.83,'wood',min(w,d)*.08)
        legs(h*.12,'bronze',15)
        count=max(2,round(ww/500))
        for i in range(count):
            if sideways:
                block(w-16,8+i*ww/count,h*.17,18,ww/count-16,h*.69,'wood_light',3)
            else:
                block(8+i*ww/count,-2,h*.17,ww/count-16,18,h*.69,'wood_light',3)
                block(ww*(i+.80)/count,0,h*.40,10,25,h*.19,'bronze',3)
        block(0,0,h*.93,w,d,h*.07,'stone' if k in ('counter','nightstand') else 'wood',25)
    elif k in ('sink','basin','laundry_sink','tank'):
        legs(h*.12)
        block(0,0,h*.10,w,d,h*.78,'wood',20)
        # Four countertop strips leave a visible bowl recess.
        block(0,0,h*.88,w,d*.16,h*.10,'stone',10)
        block(0,d*.82,h*.88,w,d*.18,h*.10,'stone',10)
        for x in (0,w*.85): block(x,d*.16,h*.88,w*.15,d*.66,h*.10,'stone',10)
        oval(w*.17,d*.20,h*.80,w*.66,d*.57,h*.03,'white')
        oval(w*.47,d*.83,h*.89,w*.04,d*.06,h*.11,'bronze')
    elif k=='toilet':
        oval(w*.24,d*.12,0,w*.52,d*.59,h*.48,'white')
        oval(w*.05,d*.02,h*.48,w*.90,d*.69,h*.15,'white')
        oval(w*.21,d*.13,h*.63,w*.58,d*.43,4,'dark')
        block(w*.07,d*.73,0,w*.86,d*.27,h,'white',35)
        oval(w*.45,d*.81,h,w*.10,d*.09,3,'bronze')
    elif k in ('washer','fridge','stove'):
        block(0,0,0,w,d,h,'white' if k=='washer' else 'dark',22)
        if k=='washer':
            # Front round hatch, profile drawn in XZ and extruded along +Y.
            block(w*.12,h*.12,-2,w*.76,h*.62,9,'bronze',min(w,h)*.28,'xz')
            block(w*.19,h*.19,-3,w*.62,h*.48,9,'glass',min(w,h)*.22,'xz')
            block(w*.07,h*.82,-2,w*.40,h*.08,8,'dark',5,'xz')
        elif k=='fridge':
            block(w*.04,-2,h*.03,w*.92,8,h*.63,'stone',12)
            block(w*.04,-2,h*.69,w*.92,8,h*.28,'stone',12)
            for z in (h*.53,h*.72): block(w*.83,-8,z,w*.03,12,h*.15,'bronze',4)
        else:
            block(w*.1,h*.13,-3,w*.8,h*.49,8,'glass',18,'xz')
            for x in (w*.28,w*.72):
                for y in (d*.28,d*.72): oval(x-w*.12,y-d*.12,h,w*.24,d*.24,4,'bronze')
    elif k=='shower':
        block(0,0,0,w,d,45,'stone',12)
        oval(w*.46,d*.46,45,w*.08,d*.08,3,'dark')
        # No enclosure/fixture fabricated beyond the original height envelope.
    elif k=='bench':
        legs(h*.78)
        for i in range(5): block(0,d*i/5,h*.78,w,d/5-8,h*.22,'wood_light',12)
    elif k=='car':
        block(w*.02,d*.03,h*.15,w*.96,d*.94,h*.42,'stone',120)
        block(w*.12,d*.25,h*.57,w*.76,d*.46,h*.43,'glass',100)
        for x in (0,w*.9):
            for y in (d*.18,d*.75): block(x,y,h*.10,w*.1,d*.12,h*.22,'dark',25)
    else:
        raise ValueError('Categoria sem modelo detalhado: '+k)
    # Normalize the extrusion descriptor to world space without rotating an
    # already global bounding box a second time.
    def transform(x,y):
        if item.get('mirror',0): x=w-x
        if angle==0: return [b[0]+x,b[1]+y]
        if angle==90: return [b[0]+d-y,b[1]+x]
        if angle==180: return [b[0]+w-x,b[1]+d-y]
        return [b[0]+y,b[1]+w-x]
    for p in parts:
        p['vertices']=[]
        for x,y in p['profile']:
            xx,yy,zz=(x,y,p['z']) if p['plane']=='xy' else (x,p['z'],y)
            a=transform(xx,yy); p['vertices'].append([a[0],a[1],zz])
        if p['plane']=='xy': p['direction']=[0,0,1]
        else:
            a=transform(0,0); z=transform(0,1); p['direction']=[z[0]-a[0],z[1]-a[1],0]
    return parts

def landscape(data):
    """Conservative concept placement; no species/sunlight certification."""
    plants=[]; rejected=[]; obstacles=[]
    for f in data['furniture']: obstacles.append(expand(f.get('use_bounds',f['bounds']),100))
    walls={w['id']:w for w in data['walls']}
    openings=[]
    for o in data['openings']:
        c=o['center']; w=walls[o['wall_id']]; horizontal=abs(w['start'][1]-w['end'][1])<1
        half=o['width']/2+100
        depth=o['width']+300 if o['kind']=='door' else 600
        box=[c[0]-half,c[1]-depth,c[0]+half,c[1]+depth] if horizontal else [c[0]-depth,c[1]-half,c[0]+depth,c[1]+half]
        openings.append(box)
    obstacles+=openings
    path=data.get('entry_path',{})
    for a,b in zip(path.get('points',[]),path.get('points',[])[1:]):
        radius=path.get('width',1200)/2+200
        obstacles.append([min(a[0],b[0])-radius,min(a[1],b[1])-radius,max(a[0],b[0])+radius,max(a[1],b[1])+radius])
    # Conservative orthogonal strips connect doors to each room center. These
    # protect a route from added vegetation; existing furniture is not certified.
    for room in data['rooms']:
        b=room['bounds']
        if room['kind']=='corridor': obstacles.append(b)
        center=[(b[0]+b[2])/2,(b[1]+b[3])/2]
        for o in data['openings']:
            if o['kind']!='door': continue
            c=o['center']
            if b[0]-350<=c[0]<=b[2]+350 and b[1]-350<=c[1]<=b[3]+350:
                horizontal=abs(walls[o['wall_id']]['start'][1]-walls[o['wall_id']]['end'][1])<1
                bend=[c[0],center[1]] if horizontal else [center[0],c[1]]
                for a,z in ((c,bend),(bend,center)):
                    obstacles.append([max(b[0],min(a[0],z[0])-450),max(b[1],min(a[1],z[1])-450),
                                      min(b[2],max(a[0],z[0])+450),min(b[3],max(a[1],z[1])+450)])
    def add(b,room_id,setting,species,nearest=None):
        maintenance=expand(b,200)
        if any(hit(maintenance,o) for o in obstacles): return False
        plants.append({'id':'__plant_'+str(len(plants)+1),'bounds':b,'maintenance_bounds':maintenance,
                       'height':species['height_mm'],'room_id':room_id,
                       'setting':setting,'window_distance_mm':nearest,'species':species['name'],
                       'species_id':species['id'],'scientific':species['scientific'],
                       'light_required':species['light'],'light_verified':False,'water':species['water'],
                       'growth':species['growth'],'source':species['source'],
                       'drainage':'vaso drenante com recipiente estanque removivel; evitar agua acumulada',
                       'canopy_diameter_mm':b[2]-b[0],'concept_only':True})
        obstacles.append(maintenance); return True
    for r in data['rooms']:
        if r['kind'] not in ('social','living','bedroom','office'): continue
        b=r['bounds']; win=[]
        for o in data['openings']:
            if o['kind']=='window':
                c=o['center']
                if b[0]-350<=c[0]<=b[2]+350 and b[1]-350<=c[1]<=b[3]+350: win.append(c)
        if not win: rejected.append({'room':r['id'],'reason':'sem janela identificada'}); continue
        placed=False
        for species in plant_options('indoor',len(plants)*3):
            if species['height_mm']+100>min(w['height'] for w in data['walls']): continue
            candidates=[]; size=species['canopy_mm']; margin=225
            for x in (b[0]+margin,b[2]-margin-size):
                for y in (b[1]+margin,b[3]-margin-size):
                    distance=min(math.hypot(x+size/2-c[0],y+size/2-c[1]) for c in win)
                    candidates.append((distance,[x,y,x+size,y+size]))
            for distance,box in sorted(candidates):
                if distance<=2000 and contains(b,expand(box,200)) and add(box,r['id'],'indoor',species,distance):
                    placed=True; break
            if placed: break
        if not placed: rejected.append({'room':r['id'],'reason':'sem canto livre proximo da janela; nao forcar vaso'})
    # External pots only in the rear yard, outside the house AND existing patios.
    site=data['site_bounds']; house=data['house_bounds']
    obstacles.extend([expand(house,600)]+[expand(o['bounds'],300) for o in data.get('outdoor',[])])
    if site[3]-house[3]>1800:
        for corner in range(4):
            for species in plant_options('outdoor',corner*3):
                size=species['canopy_mm']
                x=site[0]+1000 if corner<2 else site[2]-1000-size
                y=house[3]+1400 if corner%2==0 else site[3]-1000-size
                box=[x,y,x+size,y+size]
                if contains(site,expand(box,300)) and add(box,'SITE','outdoor',species): break
    return {'plants':plants,'omitted':rejected,'criteria':{
        'indoor_window_distance_max_mm':2000,'maintenance_margin_mm':200,
        'window_operation_reserve_mm':600,'outdoor_house_offset_mm':600,
        'note':'Distancia a janela e triagem geometrica, nao medicao de luz. Especies em vaso; medidas de exemplares de estudo, nao porte adulto. Cultivo a confirmar no local, sem plantio em solo/laje.'}}

def plant_parts(plant):
    b=plant['bounds']; w=b[2]-b[0]; h=plant['height']; cx=(b[0]+b[2])/2; cy=(b[1]+b[3])/2
    parts=[]
    def extrude(poly,z,height,material):
        parts.append({'vertices':[[x,y,z] for x,y in poly],'direction':[0,0,1],'height':height,'material':material})
    base=min(h*.32,440)
    extrude(ellipse(cx-w*.23,cy-w*.23,w*.46,w*.46),0,base,'clay')
    extrude(ellipse(cx-w*.20,cy-w*.20,w*.40,w*.40),base,5,'soil')
    form=SPECIES[plant.get('species_id','peperomia')]['form']
    def stem(x,y,z,top,radius=7):
        if top>z+1: extrude(ellipse(x-radius,y-radius,radius*2,radius*2,16),z,top-z,'wood')
    def leaf(x,y,z,t,length,side,rise=0,mat='leaf',lobes=False,curve=0):
        vx,vy=math.cos(t),math.sin(t); poly=[]
        if curve:
            # Eight planar strips describe an arch while remaining valid closed
            # extrusion profiles. Avoid nonplanar polygons in Revit CurveLoops.
            for j in range(8):
                a=j/8; b=(j+1)/8
                za=z+rise*a+curve*math.sin(math.pi*a)
                zb=z+rise*b+curve*math.sin(math.pi*b)
                vertices=[]
                for u,sign,zz in ((a,1,za),(b,1,zb),(b,-1,zb),(a,-1,za)):
                    lateral=sign*side*math.sin(math.pi*u)
                    point=[x+length*u*vx-lateral*vy,y+length*u*vy+lateral*vx,zz]
                    if not any(math.dist(point,q)<.01 for q in vertices): vertices.append(point)
                delta=zb-za; span=length/8;norm=math.hypot(delta,span)
                parts.append({'vertices':vertices,'direction':[-delta*vx/norm,-delta*vy/norm,span/norm],'height':4,'material':mat})
            return
        for sign,steps in ((1,range(9)),(-1,range(7,0,-1))):
            for j in steps:
                u=j/8; lateral=sign*side*math.sin(math.pi*u)
                if lobes: lateral*=1 if j%2 else .48
                poly.append([x+length*u*vx-lateral*vy,y+length*u*vy+lateral*vx,z+rise*u])
        norm=math.hypot(rise,length)
        parts.append({'vertices':poly,'direction':[-rise*vx/norm,-rise*vy/norm,length/norm],'height':4,'material':mat})
    if form.startswith('palm') or form=='fern':
        count=9 if form=='fern' else (7 if form=='palm_arch' else 8)
        for i in range(count):
            t=i*2.399; top=base+(h-base)*(.12 if form=='fern' else .55+.05*(i%3))
            sx=cx+math.cos(t)*w*.035;sy=cy+math.sin(t)*w*.035
            stem(sx,sy,base,top)
            length=w*.35;rise=(h-top)*(.55 if form!='fern' else .40)
            arch=0
            if form in ('palm_arch','fern'):
                rise=-(h-base)*.10;arch=(h-base)*.17
            if form=='palm_fan':
                for j in range(7): leaf(sx,sy,top,t+(j-3)*.19,w*.38,w*.025,rise,'leaf' if i%2 else 'leaf_light')
            else:
                leaf(sx,sy,top,t,length,w*.015,rise,'leaf_light',curve=arch)
                for j in range(1,6):
                    u=j/6; xx=sx+length*u*math.cos(t);yy=sy+length*u*math.sin(t)
                    for sign in (-1,1): leaf(xx,yy,top+rise*u+arch*math.sin(math.pi*u),t+sign*.95,w*.13*(1-u*.45),w*.024,rise*.1)
    elif form in ('sword','strap'):
        for i in range(13):
            t=i*2.399;radius=w*.12;xx=cx+radius*math.cos(t);yy=cy+radius*math.sin(t)
            leaf(xx,yy,base+8,t,w*(.10 if form=='sword' else .31),w*.038,
                 (h-base)*(.5+.035*i) if form=='sword' else (h-base)*.10,
                 'leaf_light' if i%3==0 else 'leaf',curve=0 if form=='sword' else (h-base)*(.48+.02*i))
    elif form in ('paired','succulent'):
        for i in range(6):
            t=i*2.399;radius=w*.12;sx=cx+radius*math.cos(t);sy=cy+radius*math.sin(t)
            top=base+(h-base)*(.65+.04*i);stem(sx,sy,base,top,10)
            for j in range(4):
                for sign in (-1,1): leaf(sx,sy,base+(top-base)*(.3+j*.2),t+sign*1.2,w*.19,w*(.065 if form=='succulent' else .045),20,'leaf' if j%2 else 'leaf_light')
    else:
        count=8 if form in ('lobed','tree_broad') else 11
        for i in range(count):
            t=i*2.399;top=base+(h-base)*(.20+.055*i)
            if form=='tree_broad':top=base+(h-base)*(.48+.054*i)
            stem(cx,cy,base,top,12 if form=='tree_broad' else 7)
            side=w*(.16 if form in ('lobed','tree_broad','round') else .11)
            leaf(cx,cy,top,t,w*(.32+.015*(i%3)),side,(h-top)*.20,'leaf' if i%2 else 'leaf_light',form=='lobed')
        if form in ('flower_white','flower_red'):
            for i in range(3):
                t=i*2.1;xx=cx+math.cos(t)*w*.13;yy=cy+math.sin(t)*w*.13;top=h*.80+i*h*.035
                stem(xx,yy,base,top)
                leaf(xx,yy,top,t,w*.19,w*.06,h*.06,'white' if form=='flower_white' else 'flower_red')
                extrude(ellipse(xx-8,yy-8,16,16,16),top,35,'flower_cream')
        if form=='trailing':
            for i in range(8):
                t=i*.7;xx=cx+w*.25*math.cos(t);yy=cy+w*.25*math.sin(t)
                leaf(xx,yy,base*(.6+.03*i),t+.6,w*.16,w*.07,30)
    return parts

def scene(data):
    items=[{'id':f['id'],'kind':f['kind'],'parts':furniture_parts(f),'bounds':f['bounds'],
            'source_bounds_before_edit':f.get('source_bounds_before_edit')} for f in data['furniture']]
    garden=landscape(data)
    items += [{'id':p['id'],'kind':'plant','species_id':p['species_id'],'label':p['species'],
               'parts':plant_parts(p),'bounds':p['bounds']} for p in garden['plants']]
    return {'revision':REVISION,'style':'Luxo brasileiro: madeira e formas organicas','items':items,'landscape':garden,'palette':PALETTE}

def apply_scene(doc,data,owned,DB,tag,stored):
    """Update existing DirectShape in place; never deletes walls or furniture."""
    from System.Collections.Generic import List
    doc.Regenerate()
    design=scene(data); by_id={stored(e)['source_id']:e for e in owned}
    mats={}
    for key,rgb in PALETTE.items():
        source='__interior_material_'+key
        material=by_id.get(source)
        if material is None:
            mid=DB.Material.Create(doc,'CASA '+str(data['project_id'])[:35]+' '+key+' '+str(doc.Application.VersionNumber)+' '+str(len(owned)))
            material=doc.GetElement(mid); tag(material,source,'interior_material')
            material.Color=DB.Color(*rgb)
            material.Shininess=5 if key not in ('bronze','glass') else 45
            material.Transparency=35 if key=='glass' else 0
        mats[key]=material.Id
    def solid(part):
        loop=DB.CurveLoop(); vertices=part['vertices']
        for a,b in zip(vertices,vertices[1:]+vertices[:1]):
            loop.Append(DB.Line.CreateBound(DB.XYZ(*[v/304.8 for v in a]),DB.XYZ(*[v/304.8 for v in b])))
        loops=List[DB.CurveLoop](); loops.Add(loop)
        options=DB.SolidOptions(mats[part['material']],DB.ElementId.InvalidElementId)
        return DB.GeometryCreationUtilities.CreateExtrusionGeometry(loops,DB.XYZ(*part['direction']),part['height']/304.8,options)
    results=[]
    for item in design['items']:
        element=by_id.get(item['id'])
        if element is not None and not isinstance(element,DB.DirectShape):
            raise ValueError('Elemento foi substituido por familia/manual: '+item['id'])
        # Do not silently move proxies that the user already relocated in Revit.
        if element is not None:
            bb=element.get_BoundingBox(None)
            actual=[bb.Min.X*304.8,bb.Min.Y*304.8,bb.Max.X*304.8,bb.Max.Y*304.8]
            if not update_required(item,stored(element),actual):
                results.append({'source_id':item['id'],'revit_id':int(element.Id.Value),'parts':len(item['parts']),'status':'ja_atualizado'})
                continue
        geometry=List[DB.GeometryObject]()
        for part in item['parts']: geometry.Add(solid(part))
        if element is None:
            cat=DB.BuiltInCategory.OST_Planting if item['kind']=='plant' else DB.BuiltInCategory.OST_Furniture
            element=DB.DirectShape.CreateElement(doc,DB.ElementId(cat))
            element.ApplicationId='casa-autolisp'; element.ApplicationDataId=data['project_id']+':'+item['id']
        element.SetShape(geometry); element.Name='CASA BR | '+item.get('label',item['kind'])
        comments=element.get_Parameter(DB.BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
        if comments and not comments.IsReadOnly:
            comments.Set('CASA BR | '+item['label']+' | Exemplar em vaso. Confirmar luz, crescimento e cultivo no local.' if item['kind']=='plant'
                         else 'CASA BR | Colecao original em madeira, tecido e pedra. Modelo de estudo, sem fabricante/material executivo definido.')
        doc.Regenerate()
        bb=element.get_BoundingBox(None)
        render_bounds=[bb.Min.X*304.8,bb.Min.Y*304.8,bb.Max.X*304.8,bb.Max.Y*304.8]
        tag(element,item['id'],'plant_concept' if item['kind']=='plant' else 'furniture_detailed',
            extra={'render_bounds':render_bounds,'interior_revision':REVISION,'signature':item_signature(item)})
        results.append({'source_id':item['id'],'revit_id':int(element.Id.Value),'parts':len(item['parts'])})
    # A changed layout/catalog may omit old generated pots. Remove only owned,
    # unchanged plant DirectShapes; manual edits block the atomic transaction.
    active={i['id'] for i in design['items']}
    for key,element in by_id.items():
        record=stored(element)
        if record.get('kind')!='plant_concept' or key in active: continue
        if not isinstance(element,DB.DirectShape) or not record.get('render_bounds'):
            raise ValueError('Vegetacao anterior sem assinatura segura: '+key)
        bb=element.get_BoundingBox(None)
        actual=[bb.Min.X*304.8,bb.Min.Y*304.8,bb.Max.X*304.8,bb.Max.Y*304.8]
        if max(abs(a-b) for a,b in zip(actual,record['render_bounds']))>2:
            raise ValueError('Vaso antigo movido manualmente: '+key)
        doc.Delete(element.Id)
        results.append({'source_id':key,'status':'vaso_omitido_por_falta_de_espaco'})
    doc.Regenerate()
    return {'revision':REVISION,'updated':results,'landscape':design['landscape'],
            'note':'Modelos originais DirectShape detalhados, nao familias RFA. Materiais de estudo; especies, insolacao, drenagem e quantitativos a especificar.'}
