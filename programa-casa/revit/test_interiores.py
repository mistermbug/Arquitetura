import copy
import json
import math
import unittest
from pathlib import Path
from casa_interiores import scene, landscape, hit, contains, furniture_parts, PALETTE, SPECIES, CATALOG, plant_parts, plant_options, item_signature, update_required, REVISION

ROOT=Path(__file__).resolve().parents[2]

class InteriorsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model=json.loads((ROOT/'json/rodolfo.json').read_text(encoding='utf-8-sig'))

    def test_reproducible_original_scene_and_all_categories(self):
        a=scene(self.model)
        self.assertEqual(a,scene(copy.deepcopy(self.model)))
        self.assertEqual(len(a['items']),len(self.model['furniture'])+len(a['landscape']['plants']))
        self.assertEqual(len({i['id'] for i in a['items']}),len(a['items']))
        for item in a['items']:
            self.assertGreater(len(item['parts']),1,item['kind'])

    def test_rotations_and_mirrors_have_valid_closed_profiles(self):
        for original in self.model['furniture']:
            for angle in (0,90,180,270):
                for mirror in (0,1):
                    f=dict(original,rotation=angle,mirror=mirror)
                    for part in furniture_parts(f):
                        points=part['vertices']; b=f['bounds']
                        self.assertIn(part['material'],PALETTE)
                        self.assertGreater(part['height'],.8)
                        self.assertAlmostEqual(sum(x*x for x in part['direction']),1,places=5)
                        for a,z in zip(points,points[1:]+points[:1]):
                            self.assertGreater(math.dist(a,z),.8,(f['kind'],angle,mirror))
                        for p in points:
                            q=[p[j]+part['direction'][j]*part['height'] for j in range(3)]
                            for vertex in (p,q):
                                self.assertTrue(b[0]-15<=vertex[0]<=b[2]+15,(f['kind'],vertex,b))
                                self.assertTrue(b[1]-15<=vertex[1]<=b[3]+15,(f['kind'],vertex,b))
                                self.assertTrue(-.01<=vertex[2]<=f['height']+15,(f['kind'],vertex))

    def test_garden_reserves_furniture_use_and_canopy(self):
        garden=landscape(self.model)
        self.assertGreater(len(garden['plants']),0)
        for p in garden['plants']:
            for f in self.model['furniture']:
                self.assertFalse(hit(p['maintenance_bounds'],f.get('use_bounds',f['bounds'])))
            if p['setting']=='indoor':
                room=next(r for r in self.model['rooms'] if r['id']==p['room_id'])
                self.assertTrue(contains(room['bounds'],p['maintenance_bounds']))
                self.assertLessEqual(p['window_distance_mm'],2000)
            else:
                self.assertTrue(contains(self.model['site_bounds'],p['maintenance_bounds']))
                self.assertFalse(hit(p['maintenance_bounds'],self.model['house_bounds']))
                for area in self.model['outdoor']:
                    self.assertFalse(hit(p['maintenance_bounds'],area['bounds']))
        for i,p in enumerate(garden['plants']):
            for q in garden['plants'][i+1:]: self.assertFalse(hit(p['maintenance_bounds'],q['maintenance_bounds']))

    def test_no_indoor_plants_without_windows(self):
        d=copy.deepcopy(self.model)
        d['openings']=[o for o in d['openings'] if o['kind']!='window']
        self.assertFalse(any(p['setting']=='indoor' for p in landscape(d)['plants']))

    def test_27_alternatives_have_non_degenerate_extrusion_profiles(self):
        folder=ROOT/'programa-casa/tests/artifacts/v04-20260910-105022-621'
        files=[p for p in folder.glob('*.json') if not p.name.startswith('desenho')]
        self.assertEqual(len(files),27)
        self.total_items=0
        for path in files:
            model=json.loads(path.read_text(encoding='utf-8-sig'))
            for item in scene(model)['items']:
                for part in item['parts']:
                    pts=part['vertices']
                    for a,b in zip(pts,pts[1:]+pts[:1]):
                        self.assertGreater(math.dist(a,b),.8,(path.name,item['id']))
                    a,b,c=pts[:3]
                    u=[b[i]-a[i] for i in range(3)];v=[c[i]-a[i] for i in range(3)]
                    n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
                    length=math.sqrt(sum(x*x for x in n));self.assertGreater(length,0)
                    n=[x/length for x in n]
                    self.assertGreater(abs(sum(n[i]*part['direction'][i] for i in range(3))),.1)
                    for p in pts: self.assertLess(abs(sum(n[i]*(p[i]-a[i]) for i in range(3))),.001)

    def test_crowded_rooms_skip_instead_of_forcing_plants(self):
        d=copy.deepcopy(self.model)
        for room in d['rooms']:
            d['furniture'].append({'id':'BLOCK'+room['id'],'bounds':room['bounds'],'use_bounds':room['bounds']})
        self.assertFalse(any(p['setting']=='indoor' for p in landscape(d)['plants']))

    def test_loader_is_inert_and_blocks_reset(self):
        # The adapter is not called without Revit; loaders must be inert and
        # must not allow the destructive reset flag for an interior update.
        import runpy
        loader=Path(__file__).with_name('atualizar_interiores_dynamo.py')
        self.assertEqual(runpy.run_path(str(loader),init_globals={'IN':['',False,False]})['OUT']['status'],'aguardando')
        self.assertEqual(runpy.run_path(str(loader),init_globals={'IN':['',True,True]})['OUT']['status'],'bloqueado')

    def test_catalog_15_species_geometry_envelopes(self):
        self.assertGreaterEqual(len(SPECIES),15)
        self.assertGreaterEqual(sum(s['form'].startswith('palm') for s in SPECIES.values()),4)
        signatures=set()
        for s in SPECIES.values():
            w=s['canopy_mm']; h=s['height_mm']
            plant={'bounds':[0,0,w,w],'height':h,'species_id':s['id']}
            parts=plant_parts(plant)
            signatures.add(item_signature({'parts':parts}))
            for part in parts:
                for a,b in zip(part['vertices'],part['vertices'][1:]+part['vertices'][:1]):
                    self.assertGreater(math.dist(a,b),.8,s['id'])
                for p in part['vertices']:
                    q=[p[j]+part['direction'][j]*part['height'] for j in range(3)]
                    for v in (p,q):
                        self.assertTrue(-5<=v[0]<=w+5,(s['id'],v))
                        self.assertTrue(-5<=v[1]<=w+5,(s['id'],v))
                        self.assertTrue(0<=v[2]<=h+5,(s['id'],v))
        self.assertEqual(len(signatures),len(SPECIES))

    def test_selection_filters_species_without_forcing_a_placement(self):
        before=copy.deepcopy(CATALOG['selection'])
        try:
            CATALOG['selection']['indoor']=['kentia']
            garden=landscape(self.model)
            self.assertTrue(all(p['species_id']=='kentia' for p in garden['plants'] if p['setting']=='indoor'))
            CATALOG['selection']['indoor']=['invalid']
            with self.assertRaises(ValueError): plant_options('indoor')
        finally: CATALOG['selection']=before

    def test_dimension_change_invalidates_revit_signature(self):
        f=copy.deepcopy(self.model['furniture'][0]); a=item_signature(f)
        f['height']+=100
        self.assertNotEqual(a,item_signature(f))

    def test_revit_update_accepts_cad_resize_but_blocks_manual_moves(self):
        item=scene(self.model)['items'][0]
        actual=item['bounds'][:]
        record={'render_bounds':actual,'interior_revision':REVISION,'signature':item_signature(item)}
        self.assertFalse(update_required(item,record,actual))
        changed=copy.deepcopy(item);changed['bounds'][2]-=100
        changed['source_bounds_before_edit']=actual[:]
        self.assertTrue(update_required(changed,record,actual))
        self.assertTrue(update_required(changed,{},actual))  # Legacy proxy.
        self.assertTrue(update_required(changed,{},changed['bounds']))  # New import of resized JSON.
        moved=[v+1000 for v in actual]
        with self.assertRaises(ValueError): update_required(changed,record,moved)

    def test_custom_furniture_range_has_valid_parts(self):
        for source in self.model['furniture']:
            for factor in (.65,1.5,2):
                f=copy.deepcopy(source);b=f['bounds']
                b[2]=b[0]+max(250,(b[2]-b[0])*factor)
                b[3]=b[1]+max(250,(b[3]-b[1])*factor)
                f['height']=max(100,min(3000,f['height']*factor))
                for p in furniture_parts(f):
                    for a,z in zip(p['vertices'],p['vertices'][1:]+p['vertices'][:1]):
                        self.assertGreater(math.dist(a,z),.8,(f['kind'],factor))

if __name__=='__main__': unittest.main()
