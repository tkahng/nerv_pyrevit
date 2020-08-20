
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

def Importcsv(Filename):
    flat_list = []
    with open(Filename, 'r') as f:
        reader = csv.reader(f)
        Lst = list(reader)
        for sublist in Lst:
            for item in sublist:
                flat_list.append(item)
    return (flat_list)


import System, Selection
import System.Threading
import System.Threading.Tasks
from Autodesk.Revit.DB import Document,FilteredElementCollector, PerformanceAdviser, FamilySymbol,Transaction,\
    FailureHandlingOptions, CurveElement, BuiltInCategory, ElementCategoryFilter, ReferenceIntersector, \
    FindReferenceTarget, SpatialElementBoundaryOptions
from Autodesk.Revit.UI import TaskDialog
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit.framework import List
from pyrevit import revit, DB
import os
from collections import defaultdict
from pyrevit import script
from pyrevit import forms

__doc__ = 'Select room bounding elements of selected room'

selection = Selection.get_selected_elements(doc)

elements = []
# convenience variable for first element in selection
for i in selection:
    loops = i.GetBoundarySegments(SpatialElementBoundaryOptions())

    for l in loops:
        for s in l:
            element = s.ElementId
            print(element)
            elements.append(doc.GetElement(element))
revit.get_selection().set_to(elements)



