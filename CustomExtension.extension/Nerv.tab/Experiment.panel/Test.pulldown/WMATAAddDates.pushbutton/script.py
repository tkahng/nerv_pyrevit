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

t = Transaction(doc, "Add Date to Sheets")

t.Start()
# get sheets
sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).ToElements()
# categorize Drawing No.
for sheet in sheets:
    designDate = sheet.LookupParameter("Design Date")
    checkDate = sheet.LookupParameter("Checked Date")
    drawDate = sheet.LookupParameter("Drawn Date")
    submitDate = sheet.LookupParameter("Submitted Date")
    if not designDate.AsString():
        designDate.Set('05/15/2020')
    if not checkDate.AsString():
        checkDate.Set('05/15/2020')
    if not drawDate.AsString():
        drawDate.Set('05/15/2020')
    submitDate.Set('06/02/2020')

t.Commit()
# M1323-1