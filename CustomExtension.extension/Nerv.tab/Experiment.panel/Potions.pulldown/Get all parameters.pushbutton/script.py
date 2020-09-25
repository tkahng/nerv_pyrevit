from pyrevit.framework import List
from pyrevit import revit, DB
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
# clr.AddReference("System.Windows.Form")

from Autodesk.Revit.DB import FilteredElementCollector, FilteredWorksetCollector, RevitLinkType,BuiltInParameter,\
    Workset,WorksetKind
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform, Transaction,FamilySymbol
from System.Collections.Generic import List
from pyrevit import script
from pyrevit import forms
import pyrevit
clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
from System.Windows.Forms import Application, SendKeys
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Get all parameters of the selected element.'

def get_selected_elements(doc):
    """API change in Revit 2016 makes old method throw an error"""
    try:
        # Revit 2016
        return [doc.GetElement(id)
                for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    except:
        # old method
        return list(__revit__.ActiveUIDocument.Selection.Elements)

selection = get_selected_elements(doc)
print(selection)
# convenience variable for first element in selection
if len(selection):
    s0 = selection[0]

def get_all_parameters(element):
    parameters = element.Parameters
    _param = []
    for param in parameters:
        if param:
            name = param.Definition.Name
            if 'String' in str(param.StorageType):
                try:
                    _param.append(name + ': ' +     str(param.AsString()))
                except:
                    _param.append(name + ': '+ str(param.AsValueString()))
            elif 'Integer' in str(param.StorageType):
                _param.append(name + ': ' + str(param.AsInteger()))
            elif 'Double' in str(param.StorageType):
                _param.append(name + ': ' + str(param.AsDouble()))
            elif 'ElementId' in str(param.StorageType):
                _param.append(name + ': '+ str(param.AsElementId().IntegerValue))
    return _param

for i in get_all_parameters(selection[0]):
    print(i)
