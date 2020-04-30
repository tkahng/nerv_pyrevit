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
    FailureHandlingOptions, CurveElement, BuiltInCategory, ElementId, SpatialElementTag, RevitLinkInstance, \
    RevitLinkType, View, BoundingBoxXYZ, BuiltInParameter
import re
from Autodesk.Revit.DB import Level, BuiltInParameter, WorksetTable, Element
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
from Autodesk.Revit.UI import RevitCommandId
from Autodesk.Revit.UI.Events import CommandEventArgs
#from Autodesk.Revit.UI.Selection import Selection

__doc__ = 'Add number to the Drawing No. according to other disciplines.'



# categorize Drawing No.
withNo = []
withoutNo = []
skipNo = []
# input the added number


# get sheets
sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).ToElements()
# categorize Drawing No.
for sheet in sheets:
    DrawingNumber = sheet.LookupParameter("Drawing No.").AsString()
    if DrawingNumber == "-":
        skipNo.append(sheet)
    else:
        withNo.append(sheet)

for w in withNo:
    t = Transaction(doc, "Change drawing no. to 'M1323-'")
    t.Start()
    para = w.LookupParameter("Drawing No.")
    para.Set("M1323-")
    t.Commit()


# M1323-1