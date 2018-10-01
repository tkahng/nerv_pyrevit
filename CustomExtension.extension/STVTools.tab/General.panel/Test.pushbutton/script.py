from pyrevit.framework import List
from pyrevit import revit, DB
from pyrevit import *


__doc__ = 'Select the shared point of the model '\
          'This is helpful check project info'


textnotes = DB.FilteredElementCollector(revit.doc)\
              .OfCategory(DB.OST_Site)\
              .ToElements()

selSet = []

for el in textnotes:
    selSet.append(el.Id)


revit.get_selection().set_to(selSet)