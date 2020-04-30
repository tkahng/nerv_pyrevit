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

t = Transaction(doc, "Add Number to Drawing No.")

# categorize Drawing No.
withNo = []
withoutNo = []
skipNo = []
# input the added number
a = int(forms.GetValueWindow.show(None,
        value_type='string',
        default=str(0),
        prompt='Please Enter number',
        title='Add Number'))

t.Start()
# get sheets
sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).ToElements()
# categorize Drawing No.
for sheet in sheets:
    DrawingNumber = sheet.LookupParameter("Drawing No.").AsString()
    if DrawingNumber == None or DrawingNumber == "":
        withoutNo.append(sheet)
    elif DrawingNumber == "-":
        skipNo.append(sheet)
    else:
        withNo.append(sheet)
# if the Drawing No. parameter is not filled
if withoutNo:
    print("The following sheet(s) does not have Drawing No. filled:")
    for wo in withoutNo:
        SheetNumber = wo.LookupParameter("Sheet Number").AsString()
        SheetName = wo.LookupParameter("Sheet Name").AsString()
        print(SheetNumber + "-" + SheetName)
# if it is filled
else:
    for w in withNo:
        DrawingNo = w.LookupParameter("Drawing No.").AsString()
        para = w.LookupParameter("Drawing No.")
        if "-" in DrawingNo:
            x = DrawingNo.split("-")
            y = x[-1]
            number1 = int(y)
            newNumber1 = number1 + a
            para.Set("M1323-" + str(newNumber1))
        else:
            number2 = int(DrawingNo)
            newNumber2 = number2 + a
            para.Set("M1323-" + str(newNumber2))
    print("The Number " + str(a) + " has been added to Drawing No.")
t.Commit()
# M1323-1