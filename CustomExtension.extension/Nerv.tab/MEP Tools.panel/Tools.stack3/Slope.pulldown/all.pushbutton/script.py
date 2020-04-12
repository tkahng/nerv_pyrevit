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

import clr, Selection
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import Document, FilteredElementCollector, PerformanceAdviser, FamilySymbol,BuiltInCategory, \
    MEPCurveType, RoutingPreferenceRuleGroupType, RoutingConditions, RoutingPreferenceErrorLevel, RoutingPreferenceRule,\
    PreferredJunctionType,Transaction, BuiltInParameter
from Autodesk.Revit.DB.Plumbing import PipeType, Pipe
from Autodesk.Revit.UI import TaskDialog, TaskDialogCommonButtons, TaskDialogResult
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit.framework import List
from pyrevit import revit, DB
import os
from collections import defaultdict
from pyrevit import script
from pyrevit import forms

__doc__ = 'Print all the  pipe slopes and element id in selection, please make a selection to run'

def isclose(a, b, rel_tol=1e-08, abs_tol=1e-03):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def isnotclose(a, b, rel_tol=1e-08, abs_tol=1e-03):
    return abs(a-b) >= max(rel_tol * max(abs(a), abs(b)), abs_tol)

sel_element = Selection.get_selected_elements(doc)
if len(sel_element) == 0:
    TaskDialog.Show('Warning', 'Please make selection first')
else:
    outprint = script.get_output()
    pipes = []
    for i in sel_element:
        if i.Category.Name == 'Pipes':
            pipes.append(i)
    print('Found ' + str(len(pipes)) + ' pipes')
    # pipes = FilteredElementCollector(doc).OfClass(Pipe).ToElements()
    for p in pipes:
        slope = p.LookupParameter('Slope').AsDouble()
        print(format(outprint.linkify(p.Id)) + '     SLOPE: ' + str(slope*12) + '/foot')
    print('End')
