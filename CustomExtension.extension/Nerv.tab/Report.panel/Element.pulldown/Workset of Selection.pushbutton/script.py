'''
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
'''

import System
import System.Threading
import System.Threading.Tasks
from Autodesk.Revit.DB import Document, FilteredElementCollector, PerformanceAdviser, FamilySymbol, Transaction,\
    FailureHandlingOptions, BuiltInCategory, ElementId
from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.UI.Selection import ObjectType
from pyrevit.framework import List
from pyrevit import revit, DB
from collections import defaultdict
from pyrevit import script
from pyrevit import forms

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
'''
for d in doc.Application.Documents:
    print(d.Title)
'''

__doc__ = 'Report the Category, Element ID and Workset of the selected element(s).'\
          'Click the Element ID to zoom in each element.'

filter = FilteredElementCollector(doc)
outprint = script.get_output()
def get_selected_elements(doc):
    """API change in Revit 2016 makes old method throw an error"""
    try:
        # Revit 2016
        return [doc.GetElement(id)
                for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    except:
        # old method
        return list(__revit__.ActiveUIDocument.Selection.Elements)
# get needed params
# get current selection
currentChoice = []
for i in get_selected_elements(doc):
    currentChoice.append(i)


params = []
selection = []
choices = uidoc.Selection
if not currentChoice:
    ref = choices.PickObjects(ObjectType.Element, "Pick Element")
    selection.append(doc.GetElement(ref.ElementId))
else:
    selection = currentChoice

# elementspool = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DoorTags).ToElements()
views = []
for i in selection:
    name = doc.GetWorksetTable().GetWorkset(i.WorksetId).Name
    print(i.Category.Name + '   ' + format(outprint.linkify(i.Id)) + '    ' + name)