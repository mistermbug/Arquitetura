"""Native acceptance test, not executed by Python-only contract tests.
Run in PythonNet3 in an EMPTY disposable Revit project, IN[0]=True.
All temporary elements are rolled back. No JSON or existing house is needed.
"""
import runpy
import traceback

if not IN or IN[0] is not True:
    OUT = {'status':'aguardando'}
else:
    import clr
    clr.AddReference('RevitAPI')
    clr.AddReference('RevitServices')
    from Autodesk.Revit import DB
    from RevitServices.Persistence import DocumentManager
    from RevitServices.Transactions import TransactionManager
    doc = DocumentManager.Instance.CurrentDBDocument
    module = runpy.run_path(r'C:\Users\mathe\OneDrive\Desktop\Arquitetura\programa-casa\revit\importar_casa_dynamo.py')
    TransactionManager.Instance.ForceCloseTransaction()
    tx = DB.Transaction(doc, 'CASA - teste temporario de unioes')
    tx.Start()
    try:
        level = DB.Level.Create(doc,0)
        base = next(w for w in DB.FilteredElementCollector(doc).OfClass(DB.WallType) if w.Kind == DB.WallKind.Basic)
        types = {}
        for thickness in (150,200):
            wt = base.Duplicate('TESTE CASA {} {}'.format(level.Id, thickness))
            cs = DB.CompoundStructure.CreateSingleLayerCompoundStructure(3000/304.8,DB.MaterialFunctionAssignment.Structure,thickness/304.8,DB.ElementId.InvalidElementId)
            cs.EndCap = getattr(DB.EndCapCondition,'None')
            wt.SetCompoundStructure(cs)
            types[thickness] = wt
        cases = [
            ('L', [((0,0),(4000,0),200),((0,0),(0,3000),200)], None),
            ('T', [((-2000,0),(2000,0),200),((0,0),(0,3000),150)], 1.235*2.8),
            ('X', [((-2000,0),(2000,0),200),((0,-1500),(0,1500),150)], 1.22*2.8),
            ('CONTINUA', [((0,0),(4000,0),200),((4000,0),(8000,0),200)], 1.6*2.8),
        ]
        results = []
        for i,(name,specs,expected) in enumerate(cases):
            walls = []
            for a,b,thickness in specs:
                line = DB.Line.CreateBound(DB.XYZ((a[0]+i*20000)/304.8,a[1]/304.8,0),DB.XYZ((b[0]+i*20000)/304.8,b[1]/304.8,0))
                w = DB.Wall.Create(doc,line,types[thickness].Id,level.Id,2800/304.8,0,False,False)
                DB.WallUtils.DisallowWallJoinAtEnd(w,0)
                DB.WallUtils.DisallowWallJoinAtEnd(w,1)
                walls.append(w)
            report = module['join_and_audit_walls'](doc,walls,DB)
            assert expected is None or abs(report['solid_volume_after_m3']-expected)<0.00001, name+' volume inesperado'
            results.append({'case':name,'audit':report})
        OUT = {'status':'testes_passaram','results':results,'temporary_elements':'rolled_back'}
    except Exception as error:
        OUT = {'status':'erro','message':str(error),'details':traceback.format_exc()}
    finally:
        if tx.GetStatus() == DB.TransactionStatus.Started:
            tx.RollBack()
