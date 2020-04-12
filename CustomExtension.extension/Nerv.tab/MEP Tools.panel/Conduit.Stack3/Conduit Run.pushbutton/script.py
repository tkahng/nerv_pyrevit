import sys
import ConfigParser
from os.path import expanduser
# Set system path
home = expanduser("~")
cfgfile = open(home + "\\STVTools.ini", 'r')
config = ConfigParser.ConfigParser()
config.read(home + "\\STVTools.ini")
# Master Path
syspath1 = config.get('SysDir','MasterPackage')
sys.path.append(syspath1)
# Built Path
syspath2 = config.get('SysDir','SecondaryPackage')
sys.path.append(syspath2)

from Autodesk.Revit.DB import Document,FilteredElementCollector, PerformanceAdviser, \
    FamilySymbol,Transaction,FailureHandlingOptions, CurveElement
from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB.Electrical import Conduit, ConduitRun
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
__doc__ = 'Map Conduit parameters to Conduit Runs'\
          'Rely on perfect info regard conduit parameters '
from pyrevit.framework import List
from pyrevit import revit, DB, script, forms, UI
import QuestionableMath

__doc__ = 'Select the base point of the model. '\
          'This is helpful check project info'

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
def get_selected_elements(doc):
    """API change in Revit 2016 makes old method throw an error"""
    try:
        # Revit 2016
        return [doc.GetElement(id)
                for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    except:
        # old method
        return list(__revit__.ActiveUIDocument.Selection.Elements)

class ConduitSelectionFilter(UI.Selection.ISelectionFilter):
    # standard API override function
    def AllowElement(self, element):
		if element.Category.Name == "Conduits" or element.Category.Name == "Conduit Fittings":
			return True
		else:
			return False
'''
runs = FilteredElementCollector(doc).OfClass(ConduitRun).ToElements()
for i in runs:
    print(i.Id)
'''

conduitFilter = ConduitSelectionFilter()
choices = uidoc.Selection

conduitRef = choices.PickObject(ObjectType.Element, conduitFilter, "Pick Conduit")
print(conduitRef)
c = doc.GetElement(conduitRef.ElementId).Id.IntegerValue

conduits = FilteredElementCollector(doc).OfClass(Conduit).ToElements()

for conduit in conduits:
    if conduit.Id.IntegerValue == c:
        print(conduit.RunId)
        run = doc.GetElement(conduit.RunId)
        print(run.Length)
# run.LookupParameter(p).Set(conduit.LookupParameter(p).AsString())

