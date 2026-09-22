# -*- coding: utf-8 -*-
"""Cole este arquivo no no PythonNet3 existente. Mesmos tres conectores.
IN[0]=JSON da casa, IN[1]=True para executar, IN[2]=False (sem recriar casa).
Reune correcao de paredes, moveis detalhados e vegetacao em uma transacao.
"""
import runpy
import traceback
IMPORTADOR = r'C:\Users\mathe\OneDrive\Desktop\Arquitetura\programa-casa\revit\importar_casa_dynamo.py'
if len(IN)<2 or IN[1] is not True:
    OUT={'status':'aguardando','message':'IN[1]=True aplica as melhorias.'}
elif len(IN)>2 and IN[2] is not False:
    OUT={'status':'bloqueado','message':'Mantenha IN[2]=False. Nao e necessario recriar a casa.'}
else:
    try:
        api=runpy.run_path(IMPORTADOR)
        OUT=api['run'](IN,improve_interiors=True)
    except Exception as error:
        OUT={'status':'erro','message':str(error),'details':traceback.format_exc(),'revision':'0.4-interiores-1'}
