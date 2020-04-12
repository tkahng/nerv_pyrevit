import uuid
from Autodesk.Revit.DB import Document,FilteredElementCollector, PerformanceAdviser, \
    FamilySymbol,Transaction,FailureHandlingOptions, CurveElement
from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.DB.Electrical import Conduit, ConduitRun
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Map Conduit parameters to Conduit Runs'\
          'Rely on perfect info regard conduit parameters '

from pyrevit.framework import List
from pyrevit import revit, DB, script, forms

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

runs = FilteredElementCollector(doc).OfClass(ConduitRun).ToElements()
t = Transaction(doc, 'Map Conduit Param to Conduit Runs')

t.Start()
conduits = FilteredElementCollector(doc).OfClass(Conduit).ToElements()
all_params = get_all_string_parameters(conduits[0])
params = forms.SelectFromList.show(all_params, button_name='Select parameters',
                                        multiselect=True)
for conduit in conduits:
    run = doc.GetElement(conduit.RunId)
    for p in params:
        param = conduit.LookupParameter(p).AsString()
        if param != None and run != None:
            # print(param)
            run.LookupParameter(p).Set(conduit.LookupParameter(p).AsString())
t.Commit()

