import clr, xlsxwriter, re
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import Document,FilteredElementCollector, PerformanceAdviser, FamilySymbol
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



path = forms.pick_folder()
PurgeGuid = "e8c63650-70b7-435a-9010-ec97660c1bda"
def PerformanceCollector(doc):
    out = []
    pTypes = PerformanceAdviser.GetPerformanceAdviser().GetAllRuleIds()
    failureMessages = PerformanceAdviser.GetPerformanceAdviser().ExecuteRules(doc, pTypes)
    for i in failureMessages:
        if 'unused families and/or types' in str(i.GetDescriptionText()):
            out.append(i.GetFailingElements())
    return out
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

elementList = PerformanceCollector(doc)
names = []
cates = []
for i in elementList:
    for id in i:
        element = doc.GetElement(id)
        if element.GetType() == FamilySymbol:
            cate = str(doc.GetElement(id).Family.FamilyCategory.Name)
            # if not cate == 'Generic Annotations' and not cate == 'Error' and not 'Symbol' in cate \
                    # and not 'Tag' in cate and not 'Annotation' in cate and not 'Title' in cate and not 'Mark' in cate \
                    # and not 'Grid Heads' in cate and not 'Profile' in cate and not 'Heads' in cate:
            name = element.Family.Name
            if not name in names and not 'Clash' in name:
                print(cate)
                names.append(name)
                cates.append(cate)
print(len(cates))
print(len(names))
destinationFolder = forms.pick_folder()
rawTitle = re.split('detached', doc.Title)[0]
title = rawTitle[0:len(rawTitle) -1]
fileName = destinationFolder +'\\' + title + '.xlsx'
# Define and Open Excel File
excelFile = ExcelOpener(fileName)
lines = [['Category', 'Unused Families', 'Size']]
count = 0
for i in names:
    line = []
    print(i)
    exportName = i.replace('.', '-')
    size = os.path.getsize(path + '\\' + exportName + '.rfa') >> 10
    print(str(size) + ' KB')
    line.append(cates[count])
    line.append(i)
    line.append(str(size) + ' KB')
    lines.append(line)
    count += 1
ExcelWriter(excelFile, 'Unused Families', 0, 0, lines)
excelFile.close()





