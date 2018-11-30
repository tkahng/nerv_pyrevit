from pyrevit.framework import List
from pyrevit import revit, DB
import clr, pprint,os

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Structure, DeleteElements
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform, Transaction,FamilySymbol
from System.Collections.Generic import List
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
from Autodesk.Revit.Creation import *
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


__doc__ = 'Select the shared point of the model '\
          'This is helpful check project info'


# input ---------------------



# Transaction Start
t = Transaction(doc, 'Delete Clash Points')
t.Start()
# Clash point Creation
elements = DB.FilteredElementCollector(doc) \
    .OfCategory(BuiltInCategory.OST_Site) \
    .ToElements()
selSet = []
setId = []
for e in elements:
    if e.Location != None:
        pp = e.GetParameters('Family')
        for p in pp:
            if p.AsValueString() == 'Site-Generic-Clashpoint':
                print(e.Id)
                selSet.append(e)
                doc.Delete(e.Id)

#revit.get_selection().set_to(selSet)

t.Commit()



