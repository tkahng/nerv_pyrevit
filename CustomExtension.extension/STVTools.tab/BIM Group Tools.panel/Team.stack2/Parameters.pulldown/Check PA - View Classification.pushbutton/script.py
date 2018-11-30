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

__doc__ = 'Check if the PA - View Classification Parameter Exists'\
          'Can be modified to check other parameters too'

# View and Sheets Collector
views = DB.FilteredElementCollector(doc)\
              .OfCategory(BuiltInCategory.OST_Viewports)\
              .ToElements()
print('We found ' + str(len(views)) + ' views')
sheets = DB.FilteredElementCollector(doc)\
              .OfCategory(BuiltInCategory.OST_Sheets)\
              .ToElements()
print('We found ' + str(len(sheets)) + ' sheets')
# See if the parameter exists
print('-------------------------------------------')
for view in views:
    a = view.LookupParameter('PA - View Classification')
    if not a:
        print('PA - View Classification Parameter in views Missing')
        break
    else:
        print(a.AsString())
print('--------------------------------------------')
for sheet in sheets:
    b = sheet.LookupParameter('PA - View Classification')
    if not b:
        print('PA - View Classification Parameter in sheets Missing')
        break
    else:
        print(b.AsString())

