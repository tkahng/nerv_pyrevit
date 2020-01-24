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
    RevitLinkType, View, BoundingBoxXYZ
import re
from Autodesk.Revit.DB import Level, BuiltInParameter, WorksetTable
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

# 2020-01-23 Exporting Orphaned Elements
from Autodesk.Revit.UI.Selection import Selection
import xlsxwriter


# Create a workbook and add worksheets
#workbook = xlsxwriter.Workbook("Orphaned Elements.xlsx")
#worksheet = workbook.add_worksheet()

LId = uidoc.Selection.GetElementIds()
for Id in LId:
    sel = doc.GetElement(Id)
    eName = sel.Name
    wId = sel.WorksetId
    wSet = doc.GetWorksetTable().GetWorkset(wId)
    wName = wSet.Name
    print(eName, Id.IntegerValue, wName)
    #row = 1
    #col = 0
    #worksheet.write(row, col, eName)
    #worksheet.write(row, col + 1, Id.IntegerValue)
    #worksheet.write(row, col + 2, wName)
    #row += 1

#workbook.close()


'''
def ExcelOpener(fileName):
    workbook = xlsxwriter.Workbook(fileName)
    return workbook

def ExcelWriter(workbook, SheetName, startRow, startCol, list):
    worksheet = workbook.add_worksheet(SheetName)
    row = startRow
    for rowItems in list:
        col = startCol
        for item in rowItems:
            worksheet.write(row, col, item)
            col += 1
        row += 1

collectorElements = ElementCheck(openedDoc)
ExcelWriter(excelFile, "ORPHANED ELEMENTS", 1, 0, collectorElements)
'''