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
from Autodesk.Revit.DB import Document, FilteredElementCollector, PerformanceAdviser, Family, Transaction,\
    FailureHandlingOptions, CurveElement, BuiltInCategory, ElementId, SpatialElementTag, RevitLinkInstance, \
    RevitLinkType, View, BoundingBoxXYZ, BuiltInParameter, ViewSet, ViewSheetSet, PrintRange, ViewSheet
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
from Autodesk.Revit.UI import TaskDialog, UIApplication
from Autodesk.Revit.UI.Selection import Selection


sheetPrint = []
sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).ToElements()
for sheet in sheets:
    sCategory = sheet.LookupParameter("Sheet Category").AsString()
    if sCategory == "Working Sheets":
        sheetId = sheet.Id
        sheetPrint.append(sheetId)
        print(sheet.SheetNumber)
print(len(sheetPrint))

def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


#chunks = list(divide_chunks(sheetPrint, 200))
#count = 1
t = Transaction(doc, 'Create split lists')
t.Start()
sheetSet = ViewSet()
for s in sheetPrint:
    #a = 0
    #for c in chunk:
    sheetSet.Insert(doc.GetElement(s))
    #b = doc.GetElement(s)
    #t = b.ViewType
    #r = str(b.ViewType)
    #n = b.Name
    #a += 1
    #print(r + "," + n + "," + str(s))
print(sheetSet.Size.ToString())
    #print(a)
    # Transaction Start

printManager = doc.PrintManager
printManager.PrintRange = PrintRange.Select
viewSheetSetting = printManager.ViewSheetSetting

viewSheetSetting.CurrentViewSheetSet.Views = sheetSet
viewSheetSetting.SaveAs('Working Sheets')
#count += 1

t.Commit()
