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
from Autodesk.Revit.DB import BuiltInParameter, WorksetTable, Element
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
import xlsxwriter
#from Autodesk.Revit.UI.Selection import Selection

__doc__ = 'Modify the Sheet Number.'

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

def ChangeSheetNumber(sheets):
    n = 1
    dic = {}
    sheetNumbers = []
    for s in sheets:
        shnumber = s.LookupParameter("Sheet Number").AsString()
        dic[shnumber] = s
        sheetNumbers.append(shnumber)
    sheetNumbers.sort()
    for i in sheetNumbers:
        d = i[0:len(i) - 4]
        if n < 10:
            dic[i].LookupParameter("Sheet Number").Set(d + "0" + str(n))
        elif n >= 10:
            dic[i].LookupParameter("Sheet Number").Set(d + str(n))
        n += 1
def PrintSheetNumber(sheets):
    n = 1
    dic = {}
    sheetNumbers = []
    for s in sheets:
        shnumber = s.LookupParameter("Sheet Number").AsString()
        dic[shnumber] = s
        sheetNumbers.append(shnumber)
    sheetNumbers.sort()
    for i in sheetNumbers:
        d = i[0:len(i) - 4]
        if n < 10:
            print(d + "0" + str(n) + "," + dic[i].LookupParameter("Sheet Number").AsString() + "," + dic[i].LookupParameter("Sheet Name").AsString())
        elif n >= 10:
            print(d + str(n) + "," + dic[i].LookupParameter("Sheet Number").AsString() + "," + dic[i].LookupParameter("Sheet Name").AsString())
        n += 1


t = Transaction(doc, "Change Drawing Number")

t.Start()
code = []
lst = []
indexNumber = []
ori = []
new = []
name = []
n = 1
sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).ToElements()

for sheet in sheets:
    SheetNumber = sheet.LookupParameter("Sheet Number").AsString()
    disCode = SheetNumber[0:-4]
    if not disCode in code:
        code.append(disCode)
disciplineSheets = []
for c in code:
    l = []
    for s in sheets:
        if c == s.LookupParameter("Sheet Number").AsString()[0: len(c)]:
            l.append(s)
    disciplineSheets.append(l)

for set in disciplineSheets:
        PrintSheetNumber(set)

'''
    lst.append(SheetNumber)
lst.sort()
for i in lst:
    if i != None:
        index = i[-5]
        splitNumber = i.split(index, 1)
        keep = splitNumber[0]
        for k in keep:
            if index in indexNumber:
                if n < 10:
                    print(k + index + "0" + str(n))
                if n >= 10:
                    print(i)
                    print(k + index + str(n))
                n += 1
            elif indexNumber == []:
                indexNumber.append(index)
            else:
                n = 1
                if n < 10:
                    print(k + index + "0" + str(n))
                if n >= 10:
                    print(i)
                    print(k + index + str(n))
                n += 1
                indexNumber.append(index)



print("done")
'''
'''

fileName = destinationFolder + '\\' + doc.Title + '.xlsx'
excelFile = ExcelOpener(fileName)
ExcelWriter(excelFile, 'Invalid', 0, 0, collectionInvalid)
ExcelWriter(excelFile, 'Model', 0, 0, collectionModel)
ExcelWriter(excelFile, 'Annotation', 0, 0, collectionAnno)


    keep = SheetNumber[0:2]
    index1 = SheetNumber[2:3]
    sector = SheetNumber[3:5]
    index2 = SheetNumber[-1]
    if index2 == "0":
        sheet.LookupParameter("Sheet Number").Set(SheetNumber[0:-1])
    elif index2 == "1":
        sheet.LookupParameter("Sheet Number").Set(SheetNumber[0:-1] + "A")
    elif index2 == "2":
        sheet.LookupParameter("Sheet Number").Set(SheetNumber[0:-1] + "B")
    else:
        print(sheet.LookupParameter("Sheet Number").AsString() + "-" + sheet.LookupParameter("Sheet Name").AsString())
'''
t.Commit()