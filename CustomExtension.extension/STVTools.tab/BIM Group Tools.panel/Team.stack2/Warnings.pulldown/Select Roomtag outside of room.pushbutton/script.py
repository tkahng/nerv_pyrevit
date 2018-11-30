from pyrevit.framework import List
from pyrevit import revit, DB
import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import BuiltInCategory, ElementId
from System.Collections.Generic import List


doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Select the shared point of the model '\
          'This is helpful check project info'
# Find Warnings

warnings = doc.GetWarnings()
# Filter Warnings

selSet = []
count = 0
for warning in warnings:
    message = warning.GetDescriptionText()
    elements = warning.GetFailingElements()
    failingText = 'Room Tag is outside of its Room'
    if failingText in str(message) and count < 200:
        for element in elements:
            selSet.append(element)
            count += 1
print(str(len(selSet)) + ' < ' + failingText + ' >' + ' Elements were selected.')
# select Room Tags
revit.get_selection().set_to(selSet)
