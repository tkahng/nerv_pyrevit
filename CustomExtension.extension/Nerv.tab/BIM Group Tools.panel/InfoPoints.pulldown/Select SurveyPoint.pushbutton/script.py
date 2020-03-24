from pyrevit import revit, DB
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import BasePoint
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Select the survey point of the model '\
          ' This is helpful check project info'


elements = DB.FilteredElementCollector(doc)\
              .OfClass(BasePoint)\
              .ToElements()
selSet = []
for e in elements:
    a = e.Category.Name
    if a == "Survey Point":
        selSet.append(e)

revit.get_selection().set_to(selSet)