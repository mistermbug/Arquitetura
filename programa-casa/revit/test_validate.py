"""Execute com Python normal; valida contrato, sem afirmar teste da API Revit."""
import copy
import json
from pathlib import Path
import unittest

from importar_casa_dynamo import validate, run, validate_outline, polygon_area, rectangle_polygon_area, boxes_touch


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.old = json.loads((Path(__file__).resolve().parents[1] / 'examples' / 'casa-exemplo.json').read_text(encoding='utf-8-sig'))
        self.new = copy.deepcopy(self.old)
        room = self.new['rooms'][0]
        self.new['zones'] = [{'id': 'Z1', 'kind': 'living', 'room_id': room['id'], 'bounds': list(room['bounds'])}]
        self.new['outdoor'] = [{'id': 'G1', 'kind': 'garage', 'bounds': [1500, 0, 4500, 4900]}]
        self.new['furniture'].append({'id': 'CAR1', 'kind': 'car', 'room_id': 'G1', 'bounds': [2000, 200, 4000, 4700], 'height': 1500})
        self.new['openings'][0]['door_style'] = 'sliding'
        self.new['north_degrees'] = 45

    def test_legacy(self):
        self.assertIs(validate(self.old), self.old)

    def test_optional_metadata_and_exterior(self):
        self.assertIs(validate(self.new), self.new)

    def test_inactive_no_revit(self):
        self.assertEqual(run(['invalid.json', False])['status'], 'aguardando')
        self.assertEqual(run(['invalid.json', False], repair_existing=True)['status'], 'aguardando')

    def test_join_candidates_include_contacts_but_not_separate_storeys(self):
        wall = [0, 0, 0, 4000, 200, 2800]
        self.assertTrue(boxes_touch(wall, [3900, 100, 0, 4100, 3000, 2800]))  # L
        self.assertTrue(boxes_touch(wall, [1900, 100, 0, 2050, 3000, 2800]))  # T, mixed widths
        self.assertTrue(boxes_touch(wall, [1900, -1000, 0, 2050, 3000, 2800]))  # X
        self.assertTrue(boxes_touch(wall, [4000, 0, 0, 8000, 200, 2800]))  # continuous
        self.assertFalse(boxes_touch(wall, [0, 0, 2950, 4000, 200, 3550]))  # parapet above
        self.assertFalse(boxes_touch(wall, [4100, 0, 0, 8000, 200, 2800]))  # gap

    def test_repair_loader_inactive_does_not_access_revit(self):
        import runpy
        path = Path(__file__).with_name('corrigir_unioes_dynamo.py')
        self.assertEqual(runpy.run_path(str(path), init_globals={'IN':['invalid',False,False]})['OUT']['status'], 'aguardando')
        self.assertEqual(runpy.run_path(str(path), init_globals={'IN':['invalid',True,True]})['OUT']['status'], 'bloqueado')

    def test_notched_slab_and_roof(self):
        p = [[0,0],[8000,0],[8000,6000],[3000,6000],[3000,3000],[0,3000]]
        self.assertEqual(polygon_area(validate_outline(p,'test')), 39000000)
        self.assertEqual(rectangle_polygon_area([0,3000,3000,6000],p), 0)
        self.assertEqual(rectangle_polygon_area([1000,2000,4000,4000],p), 4000000)
        data = copy.deepcopy(self.old)
        data.update(walls=[{'id':'w','start':[0,0],'end':[8000,0],'thickness':200,'height':2800}],
                    rooms=[{'id':'r','name':'Sala','kind':'living','bounds':[200,200,7800,2800]}],
                    openings=[], furniture=[], slab={'bounds':[0,0,8000,6000],'outline':p,'thickness':150},
                    footprint=p, outdoor=[{'id':'patio','kind':'terrace','bounds':[0,3000,3000,6000]}],
                    roof={'kind':'flat_slab','outline':p,'base_z':2800,'thickness':150,'parapet_height':600,'parapet_thickness':100})
        self.assertIs(validate(data),data)
        for edit in [lambda d:d['rooms'][0].update(bounds=[1000,1000,7000,5000]),
                     lambda d:d['roof'].update(base_z=2600),
                     lambda d:d['roof'].update(parapet_height=-100),
                     lambda d:d['outdoor'][0].update(bounds=[0,2900,3000,6000])]:
            bad = copy.deepcopy(data)
            edit(bad)
            with self.assertRaises(ValueError): validate(bad)

    def test_invalid_outlines(self):
        bad = [ [[0,0],[4000,0],[4000,4000],[2000,4000],[2000,-1000],[0,-1000]],
                [[0,0],[0,4000],[4000,4000],[4000,0]],
                [[0,0],[4000,0],[3500,4000],[0,4000]],
                [[0,0],[4000,0],[4000,4000],[0,4000],[0,0]] ]
        for p in bad:
            with self.assertRaises(ValueError): validate_outline(p,'test')

    def test_reject_invalid_variants(self):
        edits = [
            lambda d: d['zones'][0].update(room_id='missing'),
            lambda d: d['zones'][0].update(bounds=[-100, -100, 50000, 50000]),
            lambda d: d['zones'][0].update(id=d['rooms'][0]['id']),
            lambda d: d['zones'][0].update(bounds=[0, 0, float('nan'), 500]),
            lambda d: d['outdoor'][0].update(kind='unknown'),
            lambda d: d['outdoor'][0].update(bounds=list(d['slab']['bounds'])),
            lambda d: d['outdoor'][0].update(thickness=-1),
            lambda d: d['furniture'][-1].update(room_id='missing'),
            lambda d: d['furniture'][-1].update(bounds=[0, 0, 9000, 9000]),
            lambda d: d['openings'][0].update(door_style='unknown'),
            lambda d: d.update(north_degrees=float('inf')),
            lambda d: d['rooms'][1].update(bounds=list(d['rooms'][0]['bounds'])),
        ]
        for edit in edits:
            with self.subTest(edit=edit):
                data = copy.deepcopy(self.new)
                edit(data)
                with self.assertRaises(ValueError):
                    validate(data)


if __name__ == '__main__':
    unittest.main()
