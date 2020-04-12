
from pyrevit import revit, DB
import clr
from pyrevit import script
import pyrevit
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


__doc__ = 'Print a warning summary including warning types and counts.'\
          ' This is helpful check model health'

outprint = script.get_output()
output = pyrevit.output.get_output()
tab = ' '
# input ---------------------
cate = []
if revit.doc.IsWorkshared:
    warnings = doc.GetWarnings()
    cateCount = 1
    cate = []
    print('Below are all warning categories: ' + str(len(warnings)))
    for i in warnings:
        categories = i.GetDescriptionText().ToString()
        if not categories in cate:
            cate.append(categories)
    for text in cate:
        count = 0
        for i in warnings:
            categories = i.GetDescriptionText().ToString()
            if categories == text:  #categories != before:
                count += 1
        print(str(cateCount) + '. ' + text)
        print('-------' + 'Error Instance: ' + str(count))
        cateCount += 1
