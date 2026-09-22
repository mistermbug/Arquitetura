# -*- coding: utf-8 -*-
"""Cole inteiro no no PythonNet3 EXISTENTE para corrigir a casa ja importada.
Conserve IN[0]=JSON, IN[1]=True, IN[2]=False. Nao apaga/recria elementos.
"""
import runpy
import traceback

IMPORTADOR = r'C:\Users\mathe\OneDrive\Desktop\Arquitetura\programa-casa\revit\importar_casa_dynamo.py'

if len(IN) < 2 or IN[1] is not True:
    OUT = {'status': 'aguardando', 'message': 'IN[1]=True executa a correcao de unioes.'}
elif len(IN) > 2 and IN[2] is not False:
    OUT = {'status': 'bloqueado', 'message': 'Mantenha IN[2]=False. Esta rotina corrige sem substituir a casa.'}
else:
    try:
        importer = runpy.run_path(IMPORTADOR)
        OUT = importer['run'](IN, repair_existing=True)
    except Exception as error:
        OUT = {'status': 'erro', 'message': str(error), 'details': traceback.format_exc(),
               'importer_revision': '0.4-joins-1'}
