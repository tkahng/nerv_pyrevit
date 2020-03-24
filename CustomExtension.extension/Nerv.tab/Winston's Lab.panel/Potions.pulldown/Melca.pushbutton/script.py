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
from Autodesk.Revit.UI import TaskDialog, UIApplication

from Autodesk.Revit.UI.Selection import Selection
'''
LId = uidoc.Selection.GetElementIds()
worksetsTable = doc.GetWorksetTable()
Id = worksetsTable.GetActiveWorksetId()
t = Transaction(doc, 'Change Selected Element to active workset')
t.Start()
for e in LId:
    wsparam = doc.GetElement(e).get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
    wsparam.Set(Id.IntegerValue)
t.Commit()
'''

#2020-02-27 Change View Name from SP to SC
# Transaction Start
t = Transaction(doc, 'Change View Name from SP to SC')
t.Start()
views = FilteredElementCollector(doc).OfClass(View).ToElements()
names = []
for i in views:
    name = i.ViewName
    #if name[2:3] == "-":
        #a = name[:2]
        #b = name[3:]
        #i.ViewName = a + b
        #names.append(name)
    if name[:2] == "SP":
        a = name[2:]
        i.ViewName = "SC" + a
        names.append(name)
    else:
        pass
print(names)
print("finished")
t.Commit()


'''
    viewRegex = re.compile(r'^\w\w-\S\S-(.*)')
    viewRegex03 = re.compile(r'^\w\w-(.*)')
    for i in views:
        name = i.ViewName
        type = i.ViewType
        if viewRegex.findall(name) == [] and viewRegex03.findall(name) == []:
            try:
                if len(re.split('-', name)) <= 2 and not str(type) in excempt and not 'Revision Schedule' in str(name):
                    proposedName = UniqueName(dict[str(type)] + '-' + str(name), names)
                    names.append(proposedName)
                    i.ViewName = proposedName
                    print(name + ' Changed to ' + proposedName)
                if len(re.split('-', name)) > 2 and not str(type) in excempt and not 'Revision Schedule' in str(name):
                    first = re.split('-', name)[0]
                    proposedName = UniqueName(dict[str(type)] + str(name)[len(first):],names)
                    names.append(proposedName)
                    i.ViewName = proposedName
                    print(name + ' Changed to ' + proposedName)
            except:
                print('Failed ' + name)
'''

"""
#2020-02-10 Select Type Id
out = []
cl = FilteredElementCollector(doc)
lf = cl.OfCategory(BuiltInCategory.OST_LightingDevices).ToElements()
for x in lf:
    #i = x.Id
    #b = doc.GetElement(i)
    try:
        d = x.LookupParameter('Type').AsElementId()
    except:
        d = "N/A"
    if d in out:
        pass
    else:
        out.append(d)
revit.get_selection().set_to(out)
"""

'''
# 2020-01-23 Exporting Orphaned Elements
from Autodesk.Revit.UI.Selection import Selection
import xlsxwriter


# Create a workbook and add worksheets
#workbook = xlsxwriter.Workbook("Orphaned Elements.xlsx")
#worksheet = workbook.add_worksheet()
filelocation = forms.pick_file(file_ext='txt', multi_file=False, unc_paths=False)

out = []
LId = uidoc.Selection.GetElementIds()
for Id in LId:
    sel = doc.GetElement(Id)
    eName = sel.Category.Name
    wId = sel.WorksetId
    wSet = doc.GetWorksetTable().GetWorkset(wId)
    wName = wSet.Name
    out.append(str(eName) + "," + str(Id.IntegerValue) + "," + str(wName))

file = open(filelocation, "w")
for line in out:
    file.write(line)
    file.write("\n")

file.close()
    #row = 1
    #col = 0
    #worksheet.write(row, col, eName)
    #worksheet.write(row, col + 1, Id.IntegerValue)
    #worksheet.write(row, col + 2, wName)
    #row += 1

#workbook.close()
'''

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