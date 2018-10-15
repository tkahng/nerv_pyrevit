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
              .OfCategory(BuiltInCategory.OST_Site)\
              .ToElements()
selSet = []
for e in elements:
    if e.Location != None:

        pp = e.GetParameters('Family')
        for p in pp:
            if p.AsValueString() == 'Shared Point':
                selSet.append(e)
                #print(p.Location.Point)
                #print(str(p.IsValidObject))
                #print(p.Parameters)
revit.get_selection().set_to(selSet)
