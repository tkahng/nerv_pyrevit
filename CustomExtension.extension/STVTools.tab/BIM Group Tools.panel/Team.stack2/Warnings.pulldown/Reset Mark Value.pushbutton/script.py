from pyrevit.framework import List
from pyrevit import revit, DB
import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from pyrevit.framework import List
from pyrevit import revit, DB
import clr, sys, re
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Structure,BuiltInParameter
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform, Transaction,FamilySymbol
from System.Collections.Generic import List
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
from Autodesk.Revit.Creation import *
from pyrevit import script
from pyrevit import forms
import pyrevit
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import BuiltInCategory, ElementId
from System.Collections.Generic import List


doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Select the shared point of the model '\
          'This is helpful check project info'
# Find Warnings

warnings = doc.GetWarnings()
# Filter Warnings
t = Transaction(doc, 'Reset Mark Value')
selSet = []
count = 0
t.Start()
for warning in warnings:
    message = warning.GetDescriptionText()
    elements = warning.GetFailingElements()
    failingText = 'Elements have duplicate "Mark" values'
    if failingText in str(message) and count < 50:
        for element in elements:

            a = doc.GetElement(element)
            # print(a)
            try:
                a.LookupParameter('Mark').Set('')
            # doc.GetElement(element).Parameter(BuiltInParameter.ALL_MODEL_MARK).Set("")

            except:
                print('error' + str(count))

            selSet.append(element)
            count += 1
t.Commit()
print(str(len(selSet)) + ' < ' + failingText + ' >' + ' Elements Mark were reset.')
# select Room Tags
revit.get_selection().set_to(selSet)
