from pyrevit.framework import List
from pyrevit import revit, DB
import clr, pprint,os
from collections import defaultdict
from pyrevit import script
from pyrevit import forms
import pyrevit
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform
from System.Collections.Generic import List
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


__doc__ = 'Select the shared point of the model '\
          'This is helpful check project info'

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
