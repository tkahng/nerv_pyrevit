from pyrevit.framework import List
from pyrevit import revit, DB
import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, ExternalFileReference,FamilyInstance,ElementParameterFilter
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
selection = [doc.GetElement(id)
            for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]

__doc__ = 'Select all items that are the same as one certain family instance you are going to select.'

# containment -----------------------------------
choices = uidoc.Selection
ref = choices.PickObject(ObjectType.Element, "Pick Element")
ele = doc.GetElement(ref.ElementId)
fType = ele.Symbol.Family.Name
#print(fType)
Obj = FilteredElementCollector(doc).OfClass(FamilyInstance).ToElements()
selec = []
for i in Obj:
    # WALL DOES NOT HAVE SYMBOL. MODIFY IT!!!
	if i.Symbol.Family.Name == fType:
		selec.append(i)
revit.get_selection().set_to(selec)




