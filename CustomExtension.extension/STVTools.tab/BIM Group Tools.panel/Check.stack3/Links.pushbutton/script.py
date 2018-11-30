from pyrevit.framework import List
from pyrevit import revit, DB
import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, ExternalFileReference
from System.Collections.Generic import List
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
selection = [doc.GetElement(id)
            for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]

__doc__ = 'Select the shared point of the model '\
          'This is helpful check project info'

# containment -----------------------------------

LinkObj = FilteredElementCollector(doc).OfClass(clr.GetClrType(RevitLinkType)).ToElements()
rvt = []
for i in LinkObj:
	if i.IsExternalFileReference() == True:
		rvt.append(i)
for a in rvt:
	name = a.GetExternalFileReference()
	b = a.AttachmentType
	pp = name.GetAbsolutePath()
	print(b)
	print(pp)



