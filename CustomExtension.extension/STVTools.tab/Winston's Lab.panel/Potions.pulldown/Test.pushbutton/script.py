
import sys, clr
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


import System
import System.Threading
import System.Threading.Tasks
from Autodesk.Revit.DB import Document,FilteredElementCollector, PerformanceAdviser, FamilySymbol,Transaction,\
    FailureHandlingOptions, CurveElement, BuiltInCategory, ElementId, ObjectType
from Autodesk.Revit.UI import TaskDialog
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows.Forms
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit.framework import List
from pyrevit import revit, DB
import os
from collections import defaultdict
from pyrevit import script
from pyrevit import forms
'''
for d in doc.Application.Documents:
    print(d.Title)
'''
selection = []
currentChoice = []
choices = uidoc.Selection
if not currentChoice:
    ref = choices.PickObject(ObjectType.Element, "Pick Element")
    selection.append(doc.GetElement(ref.ElementId))
else:
    selection.append(currentChoice[0])
# selection = Selection.get_selected_elements(doc)
# convenience variable for first element in selection
if selection:
    views = []
    for i in selection:
        name = doc.GetWorksetTable().GetWorkset(i.WorksetId).Name
        if not name in views:
            views.append(name)
    for v in views:
        print(v)



