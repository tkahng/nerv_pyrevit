import uuid
from Autodesk.Revit.DB import Document,FilteredElementCollector, PerformanceAdviser, \
    FamilySymbol,Transaction,FailureHandlingOptions, CurveElement
from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.DB.Electrical import Conduit, ConduitRun
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

from pyrevit.framework import List
from pyrevit import revit, DB, script, forms

__doc__ = 'Map conduit parameter to conduit run parameter'

runs = FilteredElementCollector(doc).OfClass(ConduitRun).ToElements()
t = Transaction(doc, 'Map Conduit Parameter')
t.Start()
def get_all_string_parameters(element):
    parameters = element.Parameters
    _param = []
    for param in parameters:
        if param:
            name = param.Definition.Name
            if 'String' in str(param.StorageType):
                try:
                    _param.append(name)
                except:
                    _param.append(name)
    return _param
'''
dic = {}
for run in runs:
    guid = str(uuid.uuid1())
    comment = run.LookupParameter('Comments').Set(guid)
    dic[guid] = run
'''
conduits = FilteredElementCollector(doc).OfClass(Conduit).ToElements()
all_params = get_all_string_parameters(conduits[0])
params = forms.SelectFromList.show(all_params, button_name='Select parameters',
                                        multiselect=True)
for conduit in conduits:
    run = doc.GetElement(conduit.RunId)
    for p in params:
        param = conduit.LookupParameter(p).AsString()
        if param != None and run != None and not run in runs:
            # print(param)
            run.LookupParameter(p).Set(conduit.LookupParameter(p).AsString())
t.Commit()

