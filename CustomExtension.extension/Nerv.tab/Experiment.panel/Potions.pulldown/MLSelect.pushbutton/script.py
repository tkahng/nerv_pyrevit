
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


import System, Selection
import System.Threading
import System.Threading.Tasks
from Autodesk.Revit.DB import Document,FilteredElementCollector, PerformanceAdviser, Family,Transaction,\
    FailureHandlingOptions, CurveElement, BuiltInCategory, ElementId, SpatialElementTag, BuiltInParameter
import time
from Autodesk.Revit.DB.Architecture import RoomTag
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
e = str(forms.GetValueWindow.show(None,
        value_type='string',
    default=str(),
        prompt='Please Enter Element ID',
        title='Element ID'))
explodeElement = doc.GetElement(ElementId(int(e)))
viewId = explodeElement.OwnerViewId
view = doc.GetElement(viewId)
uidoc.ActiveView = view
revit.get_selection().set_to(explodeElement)
'''

__doc__ = 'Select DWG for BIM Group'

f = open("U:\\B52\\ids.txt", "r")
ele = f.readline().split(",")
e = ele[0]
f.close()
if e:
    line = ""
    explodeElement = doc.GetElement(ElementId(int(e)))
    # Activate View
    if explodeElement:
        viewId = explodeElement.OwnerViewId
        view = doc.GetElement(viewId)
        uidoc.ActiveView = view
        revit.get_selection().set_to(explodeElement)
    else:
        for k in ele[1:]:
            line += k + ","
        updateLine = line[0: len(line) - 1]
        w = open("U:\\B52\\ids.txt", "w")
        w.write(updateLine)
        w.close()
