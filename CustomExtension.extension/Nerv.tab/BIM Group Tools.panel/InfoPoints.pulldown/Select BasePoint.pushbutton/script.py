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


elements = DB.FilteredElementCollector(doc)\
              .OfCategory(BuiltInCategory.OST_ProjectBasePoint)\
              .ToElements()

selSet = []

for el in elements:
    selSet.append(el.Id)


revit.get_selection().set_to(selSet)