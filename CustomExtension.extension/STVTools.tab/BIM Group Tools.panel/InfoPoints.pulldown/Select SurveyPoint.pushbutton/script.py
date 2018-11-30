from pyrevit.framework import List
from pyrevit import revit, DB
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import BuiltInCategory, ElementId
from System.Collections.Generic import List

from Autodesk.Revit.DB import *

doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Select the shared point of the model '\
          'This is helpful check project info'


elements = DB.FilteredElementCollector(doc)\
              .OfClass(BasePoint)\
              .ToElements()
selSet = []
for e in elements:
    a = e.Category.Name
    if a == "Survey Point":
        selSet.append(e)

revit.get_selection().set_to(selSet)