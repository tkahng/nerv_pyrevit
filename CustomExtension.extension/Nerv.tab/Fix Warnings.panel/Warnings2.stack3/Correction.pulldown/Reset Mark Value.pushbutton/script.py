
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from pyrevit import revit, DB
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import BuiltInCategory, ElementId, Transaction, FamilySymbol

doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Reset the Mark Value of Duplicate '\
          'Mark Value Warning Items.'
# Find Warnings

warnings = doc.GetWarnings()
# Filter Warnings
t = Transaction(doc, 'Reset Mark Value')
selSet = []
count = 0
t.Start()
failingText = ""
for warning in warnings:
    message = warning.GetDescriptionText()
    elements = warning.GetFailingElements()
    failingText = 'Elements have duplicate "Mark" values'
    if failingText in str(message) and count < 50:
        for element in elements:
            a = doc.GetElement(element)
            try:
                a.LookupParameter('Mark').Set('')
            except:
                print('error' + str(count))

            selSet.append(element)
            count += 1
t.Commit()
print(str(len(selSet)) + ' < ' + failingText + ' >' + ' Elements Mark were reset.')
# select Elements
revit.get_selection().set_to(selSet)
