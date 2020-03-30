import sys
import ConfigParser
from os.path import expanduser
# Set system path
home = expanduser("~")
cfgfile = open(home + "\\STVTools.ini", 'r')
config = ConfigParser.ConfigParser()
config.read(home + "\\STVTools.ini")
# Master Path
syspath1 = config.get('SysDir', 'MasterPackage')
sys.path.append(syspath1)
# Built Path
syspath2 = config.get('SysDir', 'SecondaryPackage')
sys.path.append(syspath2)

# Imports
from pyrevit import revit, DB
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
# clr.AddReference("System.Windows.Form")
from Autodesk.Revit.DB import FilteredElementCollector, FilteredWorksetCollector, Element, Transaction, \
    ElementParameterFilter, ParameterValueProvider,ElementId,BuiltInParameter ,FilterStringRule, FilterStringEquals, \
    FilterNumericEquals, FilterIntegerRule, FilterDoubleRule, FilterElementIdRule, Reference
from Autodesk.Revit.UI.Selection import ObjectType

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Select all the elements in the same workset as the workset of the selected element.'\

# import user packages
def get_selected_elements(doc):
    """API change in Revit 2016 makes old method throw an error"""
    try:
        # Revit 2016
        return [doc.GetElement(id)
                for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    except:
        # old method
        return list(__revit__.ActiveUIDocument.Selection.Elements)
# get current selection
currentChoice = []
for i in get_selected_elements(doc):
    currentChoice.append(i)

selection = []
choices = uidoc.Selection
if not currentChoice:
    ref = choices.PickObject(ObjectType.Element, "Pick One Element")
    selection.append(doc.GetElement(ref.ElementId))
else:

    # TO DO: ADD A LIST TO ALLOW USERS TO CHOOSE WHICH WORKSET THEY WANT

    selection.append(currentChoice[0])
modelLst = []
currentWorkset = selection[0].get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM).AsValueString()

allModel = FilteredElementCollector(doc) \
    .WhereElementIsNotElementType() \
    .ToElements()
allLst = []
for instance in allModel:
    cate = instance.Category
    if str(cate) != 'None':
        workset = instance.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM).AsValueString()
        if workset == currentWorkset:
            allLst.append(instance)

revit.get_selection().set_to(allLst)
