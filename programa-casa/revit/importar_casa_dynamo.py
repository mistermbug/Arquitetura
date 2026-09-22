# -*- coding: utf-8 -*-
"""Cole inteiro em um no PythonNet3 do Dynamo para Revit 2027.
IN[0]: caminho JSON; IN[1]: executar (False); IN[2]: substituir gerados (False).
Nao executar como script externo: API Revit exige contexto do documento.
"""
import json
import math
import os


def rectangle_outline(b):
    return [[b[0], b[1]], [b[2], b[1]], [b[2], b[3]], [b[0], b[3]]]


def polygon_area(poly):
    return sum(a[0]*b[1]-b[0]*a[1] for a, b in zip(poly, poly[1:]+poly[:1]))/2


def inside_polygon(p, poly):
    x, y = p
    inside = False
    for a, b in zip(poly, poly[1:]+poly[:1]):
        if (a[1] > y) != (b[1] > y) and x < (b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:
            inside = not inside
    return inside


def rectangle_polygon_area(b, poly):
    # Exact for orthogonal polygons: each grid cell is wholly inside or outside.
    xs = sorted(set([b[0], b[2]] + [p[0] for p in poly if b[0] < p[0] < b[2]]))
    ys = sorted(set([b[1], b[3]] + [p[1] for p in poly if b[1] < p[1] < b[3]]))
    return sum((x1-x0)*(y1-y0) for x0, x1 in zip(xs, xs[1:]) for y0, y1 in zip(ys, ys[1:])
               if inside_polygon([(x0+x1)/2, (y0+y1)/2], poly))


def validate_outline(poly, label):
    if not isinstance(poly, list) or not 4 <= len(poly) <= 200:
        raise ValueError(label + ': poligono com 4 a 200 vertices obrigatorio')
    for p in poly:
        if not isinstance(p, list) or len(p) != 2 or any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or abs(v)>10000000 for v in p):
            raise ValueError(label + ': coordenadas XY invalidas')
    edges = list(zip(poly, poly[1:]+poly[:1]))
    for a, b in edges:
        if (a[0] == b[0]) == (a[1] == b[1]) or math.hypot(b[0]-a[0], b[1]-a[1]) <= 1:
            raise ValueError(label + ': arestas devem ser ortogonais e nao degeneradas')
    for i, (a, b) in enumerate(edges):
        for j, (c, d) in enumerate(edges[:i]):
            if j == i-1 or (i == len(edges)-1 and j == 0):
                continue
            if max(min(a[0],b[0]),min(c[0],d[0])) <= min(max(a[0],b[0]),max(c[0],d[0])) and max(min(a[1],b[1]),min(c[1],d[1])) <= min(max(a[1],b[1]),max(c[1],d[1])):
                raise ValueError(label + ': contorno se cruza ou se toca')
    if polygon_area(poly) <= 1:
        raise ValueError(label + ': vertices devem estar em sentido anti-horario, area positiva')
    return poly


def validate(data):
    """Validacao pura: nao importa nem altera o Revit."""
    def number(v, label, positive=False):
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
            raise ValueError(label + ': numero finito obrigatorio')
        if abs(v) > 10000000 or (positive and v <= 1):
            raise ValueError(label + ': dimensao/coordenada fora do intervalo permitido')
        return float(v)

    def point(v, label, count=2):
        if not isinstance(v, list) or len(v) != count:
            raise ValueError(label + ': vetor com {} coordenadas obrigatorio'.format(count))
        return [number(x, label) for x in v]

    def bounds(v, label):
        b = point(v, label, 4)
        if b[2] - b[0] <= 1 or b[3] - b[1] <= 1:
            raise ValueError(label + ': retangulo degenerado/invertido')
        return b

    if not isinstance(data, dict) or data.get('schema_version') != '1.0':
        raise ValueError('schema_version deve ser 1.0')
    if data.get('units') != 'mm':
        raise ValueError('units deve ser mm; nenhuma conversao implicita permitida')
    if not isinstance(data.get('project_id'), str) or not data['project_id'].strip():
        raise ValueError('project_id obrigatorio e estavel entre exportacoes')
    point(data.get('origin'), 'origin', 3)
    ids = set()
    for group in ('walls', 'openings', 'rooms', 'furniture', 'zones', 'outdoor'):
        if group in ('zones', 'outdoor') and group not in data:
            continue
        if not isinstance(data.get(group), list) or len(data[group]) > 5000:
            raise ValueError(group + ': lista obrigatoria, limite 5000')
        for item in data[group]:
            if not isinstance(item, dict) or not isinstance(item.get('id'), str) or not item['id']:
                raise ValueError(group + ': id textual obrigatorio')
            if item['id'] in ids or item['id'].startswith('__'):
                raise ValueError('id repetido ou reservado: ' + item['id'])
            ids.add(item['id'])
    if not data['walls'] or not data['rooms']:
        raise ValueError('walls e rooms nao podem estar vazios')
    walls = {}
    for w in data['walls']:
        a, b = point(w.get('start'), 'wall.start'), point(w.get('end'), 'wall.end')
        if math.hypot(b[0]-a[0], b[1]-a[1]) < 10:
            raise ValueError('Parede com menos de 10 mm: ' + w['id'])
        number(w.get('thickness'), 'wall.thickness', True)
        number(w.get('height'), 'wall.height', True)
        walls[w['id']] = w
    spans = {}
    for o in data['openings']:
        if 'door_style' in o and o['door_style'] not in ('passage', 'sliding', 'hinged'):
            raise ValueError('door_style desconhecido: ' + o['id'])
        if o.get('wall_id') not in walls or o.get('kind') not in ('door', 'window'):
            raise ValueError('Abertura com parede/tipo invalido: ' + o['id'])
        c = point(o.get('center'), 'opening.center')
        width = number(o.get('width'), 'opening.width', True)
        height = number(o.get('height'), 'opening.height', True)
        sill = number(o.get('sill'), 'opening.sill')
        w = walls[o['wall_id']]
        a, b = w['start'], w['end']
        length = math.hypot(b[0]-a[0], b[1]-a[1])
        dx, dy = (b[0]-a[0])/length, (b[1]-a[1])/length
        along = (c[0]-a[0])*dx+(c[1]-a[1])*dy
        away = abs((c[0]-a[0])*dy-(c[1]-a[1])*dx)
        if away > 1 or along-width/2 < 1 or along+width/2 > length-1:
            raise ValueError('Abertura fora do eixo/extensao da parede: ' + o['id'])
        if sill < 0 or sill+height >= w['height']:
            raise ValueError('Abertura fora da altura da parede: ' + o['id'])
        for lo, hi, bottom, top in spans.get(w['id'], []):
            if along-width/2 < hi and along+width/2 > lo and sill < top and sill+height > bottom:
                raise ValueError('Aberturas sobrepostas na parede: ' + w['id'])
        spans.setdefault(w['id'], []).append((along-width/2, along+width/2, sill, sill+height))
    for r in data['rooms']:
        bounds(r.get('bounds'), 'room.bounds')
        if not isinstance(r.get('name'), str) or not r['name'].strip() or not isinstance(r.get('kind'), str):
            raise ValueError('Ambiente sem nome/kind: ' + r['id'])
    def contains(outer, inner):
        return all((inner[0] >= outer[0]-1, inner[1] >= outer[1]-1,
                    inner[2] <= outer[2]+1, inner[3] <= outer[3]+1))

    def overlaps(a, b):
        return min(a[2], b[2])-max(a[0], b[0]) > 1 and min(a[3], b[3])-max(a[1], b[1]) > 1

    containers = {r['id']: r['bounds'] for r in data['rooms']}
    for index, room in enumerate(data['rooms']):
        if any(overlaps(room['bounds'], other['bounds']) for other in data['rooms'][:index]):
            raise ValueError('Recintos sobrepostos; use zones para funcoes integradas: ' + room['id'])
    for zone in data.get('zones', []):
        b = bounds(zone.get('bounds'), 'zone.bounds')
        if zone.get('room_id') not in containers or not contains(containers[zone['room_id']], b):
            raise ValueError('Zona fora do recinto hospedeiro: ' + zone['id'])
        if not isinstance(zone.get('kind'), str) or not zone['kind']:
            raise ValueError('Zona sem kind: ' + zone['id'])
    for area in data.get('outdoor', []):
        b = bounds(area.get('bounds'), 'outdoor.bounds')
        if area.get('kind') not in ('garage', 'terrace'):
            raise ValueError('Area externa desconhecida: ' + area['id'])
        if 'thickness' in area:
            number(area['thickness'], 'outdoor.thickness', True)
        if 'spaces' in area:
            spaces = number(area['spaces'], 'outdoor.spaces')
            if area['kind'] != 'garage' or spaces != int(spaces) or not 1 <= spaces <= 8:
                raise ValueError('Numero de vagas invalido: ' + area['id'])
        if any(overlaps(b, existing) for existing in containers.values()):
            raise ValueError('Area externa sobreposta a recinto/area externa: ' + area['id'])
        containers[area['id']] = b
    for f in data['furniture']:
        bounds(f.get('bounds'), 'furniture.bounds')
        number(f.get('height'), 'furniture.height', True)
        if not isinstance(f.get('kind'), str) or not f['kind']:
            raise ValueError('Movel sem kind: ' + f['id'])
        if 'room_id' in f and (f['room_id'] not in containers or not contains(containers[f['room_id']], f['bounds'])):
            raise ValueError('Movel fora do recinto/area externa hospedeira: ' + f['id'])
    slab = data.get('slab')
    if not isinstance(slab, dict):
        raise ValueError('slab obrigatorio')
    bounds(slab.get('bounds'), 'slab.bounds')
    number(slab.get('thickness'), 'slab.thickness', True)
    outline = validate_outline(slab.get('outline', rectangle_outline(slab['bounds'])), 'slab.outline')
    bbox = [min(p[0] for p in outline), min(p[1] for p in outline), max(p[0] for p in outline), max(p[1] for p in outline)]
    if any(abs(a-b)>1 for a,b in zip(bbox, slab['bounds'])):
        raise ValueError('slab.bounds diverge de outline')
    if 'footprint' in data and data['footprint'] != outline:
        raise ValueError('footprint deve corresponder a slab.outline')
    for room in data['rooms']:
        b = room['bounds']
        if (b[2]-b[0])*(b[3]-b[1])-rectangle_polygon_area(b, outline)>1:
            raise ValueError('Recinto fora do piso real: '+room['id'])
    for area in data.get('outdoor', []):
        if rectangle_polygon_area(area['bounds'], outline) > 1:
            raise ValueError('Piso externo sobreposto ao piso da casa: ' + area['id'])
    if 'roof' in data:
        roof = data['roof']
        if not isinstance(roof, dict) or roof.get('kind') != 'flat_slab':
            raise ValueError('roof.kind deve ser flat_slab')
        if validate_outline(roof.get('outline'), 'roof.outline') != outline:
            raise ValueError('Cobertura deve acompanhar contorno do piso')
        for key in ('base_z', 'thickness', 'parapet_thickness'):
            number(roof.get(key), 'roof.'+key, True)
        if number(roof.get('parapet_height'), 'roof.parapet_height') < 0:
            raise ValueError('Platibanda nao pode ter altura negativa')
        if abs(roof['base_z']-max(w['height'] for w in data['walls']))>1:
            raise ValueError('Base da cobertura deve coincidir com topo das paredes')
    for key in ('north', 'north_degrees'):
        if key in data:
            number(data[key], key)
    if not isinstance(data.get('validations'), list):
        raise ValueError('validations deve ser lista')
    return data


def boxes_touch(a, b, tolerance=0.0):
    """Three-dimensional broad phase; coordinates share the caller's units."""
    return all(a[i] <= b[i+3]+tolerance and b[i] <= a[i+3]+tolerance for i in range(3))


def join_and_audit_walls(doc, walls, DB):
    """Native joins plus measured solid intersections, inside caller transaction.

    Only explicitly supplied walls may change. Abort near other walls rather than
    letting Revit's automatic endpoint cleanup touch an unrelated project.
    Volumes are geometric quantities, not a bill of purchased materials.
    """
    cubic_feet_to_m3 = 0.3048**3
    tolerance_m3 = 0.000001  # One cubic centimetre per tested pair.
    allowed_ids = {int(w.Id.Value) for w in walls}

    def bounds(element):
        box = element.get_BoundingBox(None)
        if box is None:
            raise ValueError('Parede sem limites geometricos: {}'.format(element.Id))
        points = [box.Transform.OfPoint(DB.XYZ(x,y,z))
                  for x in (box.Min.X,box.Max.X) for y in (box.Min.Y,box.Max.Y)
                  for z in (box.Min.Z,box.Max.Z)]
        return [min(getattr(p,axis) for p in points) for axis in ('X','Y','Z')] + [
            max(getattr(p,axis) for p in points) for axis in ('X','Y','Z')]

    options = DB.Options()
    options.DetailLevel = DB.ViewDetailLevel.Fine
    options.IncludeNonVisibleObjects = False

    def solids(element):
        def unpack(geometry):
            result = []
            if geometry is not None:
                for obj in geometry:
                    if isinstance(obj, DB.Solid) and obj.Volume > 1e-10:
                        result.append(obj)
                    elif isinstance(obj, DB.GeometryInstance):
                        result.extend(unpack(obj.GetInstanceGeometry()))
            return result
        result = unpack(element.get_Geometry(options))
        if not result:
            raise ValueError('Parede sem solido mensuravel: {}'.format(element.Id))
        return result

    def intersection_volume(left, right):
        volume = 0.0
        try:
            for a in solids(left):
                for b in solids(right):
                    overlap = DB.BooleanOperationsUtils.ExecuteBooleanOperation(a, b, DB.BooleanOperationsType.Intersect)
                    try:
                        volume += max(0.0, overlap.Volume)*cubic_feet_to_m3
                    finally:
                        overlap.Dispose()
        except Exception as error:
            raise RuntimeError('Nao foi possivel auditar a intersecao das paredes {} / {}: {}'.format(left.Id, right.Id, error)) from error
        return volume

    def quantities():
        records = []
        for w in walls:
            parameter = w.get_Parameter(DB.BuiltInParameter.HOST_VOLUME_COMPUTED)
            records.append({'revit_id': int(w.Id.Value),
                            'solid_volume_m3': sum(s.Volume for s in solids(w))*cubic_feet_to_m3,
                            'revit_volume_m3': parameter.AsDouble()*cubic_feet_to_m3 if parameter else None})
        return records

    doc.Regenerate()
    wall_bounds = [bounds(w) for w in walls]
    for other in DB.FilteredElementCollector(doc).OfClass(DB.Wall).WhereElementIsNotElementType():
        if int(other.Id.Value) not in allowed_ids:
            if any(boxes_touch(b, bounds(other), 1000/304.8) for b in wall_bounds):
                raise ValueError('Parede externa ao projeto gerado proxima (id {}). Uniao cancelada para preservar o modelo existente.'.format(other.Id))

    before = quantities()
    for w in walls:
        DB.WallUtils.AllowWallJoinAtEnd(w, 0)
        DB.WallUtils.AllowWallJoinAtEnd(w, 1)
    doc.Regenerate()
    explicit_joins = 0
    # Native endpoint cleanup resolves L/T/collinear junctions. Any remaining
    # actual solid overlap must be cut by JoinGeometry, never hidden by graphics.
    for i, left in enumerate(walls):
        for right in walls[i+1:]:
            if boxes_touch(bounds(left), bounds(right), 1/304.8):
                if intersection_volume(left, right) > tolerance_m3:
                    if not DB.JoinGeometryUtils.AreElementsJoined(doc, left, right):
                        DB.JoinGeometryUtils.JoinGeometry(doc, left, right)
                        explicit_joins += 1
                        doc.Regenerate()

    residuals, checked = [], 0
    for i, left in enumerate(walls):
        for right in walls[i+1:]:
            if boxes_touch(bounds(left), bounds(right), 1/304.8):
                checked += 1
                volume = intersection_volume(left, right)
                if volume > tolerance_m3:
                    residuals.append({'left': int(left.Id.Value), 'right': int(right.Id.Value), 'm3': volume})
    if residuals:
        raise ValueError('Sobreposicao residual de paredes; operacao revertida: ' + json.dumps(residuals))
    # Assert that automatic joins did not include walls outside this import.
    for w in walls:
        for index in (0,1):
            for element in w.Location.get_ElementsAtJoin(index):
                if isinstance(element, DB.Wall) and int(element.Id.Value) not in allowed_ids:
                    raise ValueError('Juncao atingiu parede nao gerada; operacao revertida.')
    after = quantities()
    return {'status': 'sem_sobreposicao_detectada', 'walls_checked': len(walls),
            'candidate_pairs_checked': checked, 'explicit_geometry_joins': explicit_joins,
            'pair_tolerance_m3': tolerance_m3,
            'solid_volume_before_m3': sum(r['solid_volume_m3'] for r in before),
            'solid_volume_after_m3': sum(r['solid_volume_m3'] for r in after),
            'wall_quantities': after,
            'scope': 'Paredes e platibandas geradas, com vaos atuais. Nao valida todo o edificio nem quantitativos de compra.'}


def run(inputs, repair_existing=False, improve_interiors=False):
    if len(inputs) < 2 or inputs[1] is not True:
        return {'status': 'aguardando', 'message': 'Conecte caminho JSON e executar=True. Nenhuma alteracao.'}
    if not isinstance(inputs[0], str) or not os.path.isfile(inputs[0]):
        raise ValueError('IN[0]: arquivo JSON existente obrigatorio')
    if os.path.getsize(inputs[0]) > 10000000:
        raise ValueError('JSON excede 10 MB')
    if len(inputs) > 2 and not isinstance(inputs[2], bool):
        raise ValueError('IN[2] deve ser Boolean: autoriza recriar os elementos gerados')
    reset = len(inputs) > 2 and inputs[2] is True
    with open(inputs[0], 'r', encoding='utf-8-sig') as handle:
        data = validate(json.load(handle))

    import clr
    clr.AddReference('RevitAPI')
    clr.AddReference('RevitServices')
    from Autodesk.Revit import DB
    from Autodesk.Revit.DB.ExtensibleStorage import Schema, SchemaBuilder, Entity, AccessLevel, ExtensibleStorageFilter
    from RevitServices.Persistence import DocumentManager
    from RevitServices.Transactions import TransactionManager
    from System import Guid, String, Int64
    from System.Collections.Generic import List

    doc = DocumentManager.Instance.CurrentDBDocument
    if doc is None or doc.IsFamilyDocument or doc.IsReadOnly:
        raise ValueError('Abra um projeto Revit editavel, preferencialmente vazio')
    schema_id = Guid('1aa6e65f-fce4-40e3-a5a1-fb8fa7239a61')
    schema = Schema.Lookup(schema_id)
    project = data['project_id']

    def eid(value):
        return int(value.Value) if hasattr(value, 'Value') else int(value.IntegerValue)

    def stored(element):
        if schema is None:
            return None
        entity = element.GetEntity(schema)
        if not entity.IsValid():
            return None
        return json.loads(entity.Get[String](schema.GetField('Payload')))

    owned = []
    if schema is not None:
        # Revit exige um filtro antes de iterar o coletor. Este inclui tambem tipos.
        for e in DB.FilteredElementCollector(doc).WherePasses(ExtensibleStorageFilter(schema_id)):
            metadata = stored(e)
            if metadata and metadata.get('source') == 'casa-autolisp' and metadata.get('project_id') == project:
                owned.append(e)
    if (repair_existing or improve_interiors) and not owned:
        raise ValueError('Nao ha elementos deste JSON no documento Revit atual para corrigir.')
    if owned and not reset and not repair_existing and not improve_interiors:
        return {'status': 'bloqueado', 'message': 'Projeto ja importado. IN[2]=True autoriza recriar TODOS os elementos gerados, inclusive edicoes manuais nesses elementos. Elementos externos permanecem protegidos.', 'count': len(owned)}

    def ft(mm):
        return float(mm)/304.8

    def xyz(x, y, z=0):
        return DB.XYZ(ft(x), ft(y), ft(z))

    created = []

    def tag(element, source_id, kind, extra=None):
        payload = {'source': 'casa-autolisp', 'project_id': project, 'source_id': source_id, 'kind': kind}
        if extra:
            payload.update(extra)
        entity = Entity(schema)
        entity.Set[String](schema.GetField('Payload'), json.dumps(payload, ensure_ascii=True))
        element.SetEntity(entity)
        created[:] = [r for r in created if r['source_id'] != source_id]
        created.append({'source_id': source_id, 'kind': kind, 'revit_id': eid(element.Id)})
        return element

    def interior_collection():
        import runpy
        root = os.path.dirname(globals().get('__file__', r'C:\Users\mathe\OneDrive\Desktop\Arquitetura\programa-casa\revit\importar_casa_dynamo.py'))
        return runpy.run_path(os.path.join(root, 'casa_interiores.py'))

    def polygon_loop(outline):
        points = [xyz(*p) for p in outline]
        result = DB.CurveLoop()
        for i in range(len(points)):
            result.Append(DB.Line.CreateBound(points[i], points[(i+1)%len(points)]))
        return result

    def loop(bounds):
        return polygon_loop(rectangle_outline(bounds))

    def simple_structure(thickness, wall=False):
        # Wall structures need a vertical sample; floors must have NoEndCap.
        # EndCap.None and EndCap.NoEndCap are different Revit enum values.
        args = (DB.MaterialFunctionAssignment.Structure, ft(thickness), DB.ElementId.InvalidElementId)
        if wall:
            structure = DB.CompoundStructure.CreateSingleLayerCompoundStructure(ft(3000), *args)
            structure.EndCap = getattr(DB.EndCapCondition, 'None')
        else:
            structure = DB.CompoundStructure.CreateSingleLayerCompoundStructure(*args)
            structure.EndCap = DB.EndCapCondition.NoEndCap
        structure.StructuralMaterialIndex = 0
        return structure

    def set_structure(element_type, thickness, label, wall=False):
        try:
            element_type.SetCompoundStructure(simple_structure(thickness, wall))
        except Exception as error:
            raise RuntimeError('Camadas de {} ({} mm): {}'.format(label, thickness, error)) from error

    # Fechar a transacao de infraestrutura do Dynamo antes de transacao atomica propria.
    TransactionManager.Instance.ForceCloseTransaction()
    api_failures = []

    class RollBackOnError(DB.IFailuresPreprocessor):
        # pythonnet exige namespace ao implementar interface .NET.
        # UUID evita conflito de tipos quando o no e executado novamente.
        __namespace__ = 'CasaImporter_' + Guid.NewGuid().ToString('N')

        def PreprocessFailures(self, accessor):
            has_error = False
            for failure in accessor.GetFailureMessages():
                api_failures.append(failure.GetDescriptionText())
                if failure.GetSeverity() == DB.FailureSeverity.Error:
                    has_error = True
            if has_error:
                return DB.FailureProcessingResult.ProceedWithRollBack
            return DB.FailureProcessingResult.Continue

    tx = DB.Transaction(doc, 'CASA - importar ' + project)
    tx.Start()
    try:
        handler = RollBackOnError()
        options = tx.GetFailureHandlingOptions()
        options.SetFailuresPreprocessor(handler)
        options.SetClearAfterRollback(True)
        tx.SetFailureHandlingOptions(options)
        if improve_interiors:
            collection = interior_collection()
            furniture_ids = {stored(e)['source_id'] for e in owned if stored(e)['kind'] in ('furniture_proxy','furniture_detailed')}
            if not {f['id'] for f in data['furniture']}.issubset(furniture_ids):
                raise ValueError('Faltam moveis da geracao original. Confira o JSON/projeto antes de melhorar os interiores.')
            audit = join_and_audit_walls(doc, [e for e in owned if isinstance(e, DB.Wall)], DB)
            interior_result = collection['apply_scene'](doc, data, owned, DB, tag, stored)
            doc.Regenerate()
            for e in owned:
                if not e.IsValidObject:
                    continue  # An unchanged generated pot may have been omitted.
                if stored(e)['kind'] == 'room' and e.Area <= 0:
                    raise ValueError('Ambiente sem delimitacao apos as melhorias; operacao revertida.')
            status = tx.Commit()
            if status != DB.TransactionStatus.Committed:
                raise RuntimeError('Revit reverteu as melhorias: ' + '; '.join(api_failures))
            return {'status':'interiores_atualizados','project_id':project,'quantity_audit':audit,
                    'interiors':interior_result,'revit_warnings':api_failures}
        if repair_existing:
            generated_walls = [e for e in owned if isinstance(e, DB.Wall)]
            if not generated_walls:
                raise ValueError('Projeto sem paredes geradas para corrigir.')
            observed = {stored(e)['source_id'] for e in generated_walls}
            expected = {w['id'] for w in data['walls']}
            if not expected.issubset(observed):
                raise ValueError('Faltam paredes da geracao original; confira o JSON e o projeto aberto.')
            audit = join_and_audit_walls(doc, generated_walls, DB)
            doc.Regenerate()
            for e in owned:
                if stored(e)['kind'] == 'room' and e.Area <= 0:
                    raise ValueError('Uniao deixou ambiente sem delimitacao; operacao revertida.')
            status = tx.Commit()
            if status != DB.TransactionStatus.Committed:
                raise RuntimeError('Revit reverteu a correcao: ' + '; '.join(api_failures))
            return {'status': 'unioes_corrigidas', 'project_id': project,
                    'quantity_audit': audit, 'revit_warnings': api_failures,
                    'importer_revision': '0.4-joins-1',
                    'message': 'Paredes existentes corrigidas sem apagar e recriar a casa. Confira planta, 3D e volumes.'}
        if owned:
            allowed = {eid(e.Id) for e in owned}
            to_delete = List[DB.ElementId]()
            for e in owned:
                to_delete.Add(e.Id)
            deleted = doc.Delete(to_delete)
            unexpected = [eid(x) for x in deleted if eid(x) not in allowed]
            if unexpected:
                raise ValueError('Substituicao afetaria elementos nao gerados/dependentes: {}. Operacao revertida.'.format(unexpected))
        if schema is None:
            builder = SchemaBuilder(schema_id)
            builder.SetSchemaName('CasaAutoLispSourceV1')
            builder.SetReadAccessLevel(AccessLevel.Public)
            builder.SetWriteAccessLevel(AccessLevel.Public)
            builder.AddSimpleField('Payload', String)
            schema = builder.Finish()
        # XY no JSON e WCS global. origin e metadado: nao somar XYZ novamente.
        level = tag(DB.Level.Create(doc, 0.0), '__level', 'level')
        level.Name = 'CASA ' + project[:50] + ' ' + str(eid(level.Id))
        wall_base = next((w for w in DB.FilteredElementCollector(doc).OfClass(DB.WallType) if w.Kind == DB.WallKind.Basic), None)
        floor_base = next((f for f in DB.FilteredElementCollector(doc).OfClass(DB.FloorType) if not f.IsFoundationSlab), None)
        if wall_base is None or floor_base is None:
            raise ValueError('Template precisa de tipo basico de parede e tipo de piso')
        wall_types, revit_walls, generated_walls = {}, {}, []
        for w in data['walls']:
            key = float(w['thickness'])
            if key not in wall_types:
                wt = wall_base.Duplicate('CASA {} {}mm {}'.format(eid(level.Id), key, len(wall_types)))
                set_structure(wt, key, 'parede', wall=True)
                tag(wt, '__walltype_' + str(key), 'wall_type')
                wall_types[key] = wt
            a, b = w['start'], w['end']
            axis = DB.Line.CreateBound(xyz(*a), xyz(*b))
            wall = DB.Wall.Create(doc, axis, wall_types[key].Id, level.Id, ft(w['height']), 0.0, False, False)
            # Evita alterar paredes existentes por juncao automatica de extremidades.
            DB.WallUtils.DisallowWallJoinAtEnd(wall, 0)
            DB.WallUtils.DisallowWallJoinAtEnd(wall, 1)
            revit_walls[w['id']] = tag(wall, w['id'], 'wall')
            generated_walls.append(wall)
        floor_type = floor_base.Duplicate('CASA piso ' + str(eid(level.Id)))
        set_structure(floor_type, data['slab']['thickness'], 'piso da casa')
        tag(floor_type, '__floor_type', 'floor_type')
        loops = List[DB.CurveLoop]()
        loops.Add(polygon_loop(data['slab'].get('outline', rectangle_outline(data['slab']['bounds']))))
        tag(DB.Floor.Create(doc, loops, floor_type.Id, level.Id), '__slab', 'slab')
        if 'roof' in data:
            roof = data['roof']
            rt = floor_base.Duplicate('CASA laje cobertura ' + str(eid(level.Id)))
            set_structure(rt, roof['thickness'], 'laje de cobertura')
            tag(rt, '__roof_type', 'floor_type')
            roof_loops = List[DB.CurveLoop]()
            roof_loops.Add(polygon_loop(roof['outline']))
            roof_slab = DB.Floor.Create(doc, roof_loops, rt.Id, level.Id)
            # Revit floor elevation denotes top face; base_z denotes underside.
            roof_slab.get_Parameter(DB.BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM).Set(ft(roof['base_z']+roof['thickness']))
            tag(roof_slab, '__roof', 'roof_slab_concept')
            if roof['parapet_height'] > 1:
                pt = wall_base.Duplicate('CASA platibanda ' + str(eid(level.Id)))
                set_structure(pt, roof['parapet_thickness'], 'platibanda', wall=True)
                tag(pt, '__parapet_type', 'wall_type')
                # Offset CCW outline toward its interior, so exterior face stays on footprint.
                poly = roof['outline']
                offset = roof['parapet_thickness']/2
                inset = []
                for i, p in enumerate(poly):
                    prev, nxt = poly[i-1], poly[(i+1)%len(poly)]
                    u = [(p[0]-prev[0]), (p[1]-prev[1])]
                    v = [(nxt[0]-p[0]), (nxt[1]-p[1])]
                    lu, lv = math.hypot(*u), math.hypot(*v)
                    nu, nv = [-u[1]/lu, u[0]/lu], [-v[1]/lv, v[0]/lv]
                    # Collinear redundant vertices use just one inward normal.
                    normals = nu if abs(nu[0]-nv[0])+abs(nu[1]-nv[1])<0.001 else [nu[0]+nv[0], nu[1]+nv[1]]
                    inset.append([p[0]+offset*normals[0], p[1]+offset*normals[1]])
                for i, (a,b) in enumerate(zip(inset, inset[1:]+inset[:1])):
                    wall = DB.Wall.Create(doc, DB.Line.CreateBound(xyz(*a),xyz(*b)), pt.Id, level.Id, ft(roof['parapet_height']), ft(roof['base_z']+roof['thickness']), False, False)
                    DB.WallUtils.DisallowWallJoinAtEnd(wall, 0)
                    DB.WallUtils.DisallowWallJoinAtEnd(wall, 1)
                    tag(wall, '__parapet_'+str(i), 'parapet')
                    generated_walls.append(wall)
        exterior_types = {}
        for area in data.get('outdoor', []):
            thickness = float(area.get('thickness', 100))
            if thickness not in exterior_types:
                exterior_type = floor_base.Duplicate('CASA externo {} {}mm'.format(eid(level.Id), thickness))
                set_structure(exterior_type, thickness, 'piso externo')
                tag(exterior_type, '__exterior_type_' + str(thickness), 'floor_type')
                exterior_types[thickness] = exterior_type
            exterior_loops = List[DB.CurveLoop]()
            exterior_loops.Add(loop(area['bounds']))
            tag(DB.Floor.Create(doc, exterior_loops, exterior_types[thickness].Id, level.Id), area['id'], 'outdoor_' + area['kind'])
        doc.Regenerate()
        specs = {w['id']: w for w in data['walls']}
        for o in data['openings']:
            w = specs[o['wall_id']]
            a, b, c = w['start'], w['end'], o['center']
            length = math.hypot(b[0]-a[0], b[1]-a[1])
            dx, dy = (b[0]-a[0])/length*o['width']/2, (b[1]-a[1])/length*o['width']/2
            opening = doc.Create.NewOpening(revit_walls[o['wall_id']], xyz(c[0]-dx,c[1]-dy,o['sill']), xyz(c[0]+dx,c[1]+dy,o['sill']+o['height']))
            tag(opening, o['id'], o['kind'] + '_opening')
        quantity_audit = join_and_audit_walls(doc, generated_walls, DB)
        for f in data['furniture']:
            profiles = List[DB.CurveLoop]()
            profiles.Add(loop(f['bounds']))
            solid = DB.GeometryCreationUtilities.CreateExtrusionGeometry(profiles, DB.XYZ.BasisZ, ft(f['height']))
            shape = DB.DirectShape.CreateElement(doc, DB.ElementId(DB.BuiltInCategory.OST_Furniture))
            shape.ApplicationId = 'casa-autolisp'
            shape.ApplicationDataId = project + ':' + f['id']
            shape.Name = 'PROXY ' + f['kind']
            geom = List[DB.GeometryObject]()
            geom.Add(solid)
            shape.SetShape(geom)
            tag(shape, f['id'], 'furniture_proxy')
        collection = interior_collection()
        current_elements = [doc.GetElement(DB.ElementId(Int64(r['revit_id']))) for r in created]
        interior_result = collection['apply_scene'](doc, data, current_elements, DB, tag, stored)
        doc.Regenerate()
        room_results = []
        for r in data['rooms']:
            x0,y0,x1,y1 = r['bounds']
            room = doc.Create.NewRoom(level, DB.UV(ft((x0+x1)/2), ft((y0+y1)/2)))
            room.Name = r['name']
            room.Number = '{}-{}'.format(eid(level.Id), r['id'])
            tag(room, r['id'], 'room')
            room_results.append(room)
        doc.Regenerate()
        unbounded = [r.get_Parameter(DB.BuiltInParameter.ROOM_NAME).AsString() for r in room_results if r.Area <= 0]
        if unbounded:
            raise ValueError('Ambientes nao delimitados/redundantes no Revit: ' + ', '.join(unbounded))
        status = tx.Commit()
        if status != DB.TransactionStatus.Committed:
            raise RuntimeError('Revit nao confirmou a transacao: ' + str(status) + '; ' + '; '.join(api_failures))
        return {'status': 'importado', 'project_id': project, 'elements': created,
                'interiors': interior_result,
                'quantity_audit': quantity_audit, 'importer_revision': '0.4-joins-1',
                'warnings': ['Portas/janelas sao vaos reais SEM caixilhos, folhas ou familias.',
                             'Moveis sao modelos originais DirectShape detalhados; nao sao familias RFA parametricas.',
                             'Vegetacao e estudo com vasos e folhagens; especies, luz real e drenagem a especificar.',
                             'Cobertura, quando presente, e laje conceitual (categoria Piso) com platibanda: sem caimentos, drenagem, impermeabilizacao ou calculo estrutural.',
                             'Sem vistas de cortes/fachadas, instalacoes ou conformidade municipal certificada.',
                             'Cotas e textos do CAD nao sao transferidos ao Revit nesta versao.'],
                'revit_warnings': api_failures,
                'zones_from_cad': data.get('zones', []),
                'design_metadata': {k: data[k] for k in ('layout', 'integration', 'north', 'north_degrees', 'entry_path', 'roof') if k in data},
                'validations_from_cad': data['validations']}
    except Exception:
        if tx.GetStatus() == DB.TransactionStatus.Started:
            tx.RollBack()
        raise


if 'IN' in globals():
    try:
        OUT = run(IN)
    except Exception as error:
        import traceback
        OUT = {'status': 'erro', 'message': str(error), 'details': traceback.format_exc(),
               'importer_revision': '0.4-joins-1'}
