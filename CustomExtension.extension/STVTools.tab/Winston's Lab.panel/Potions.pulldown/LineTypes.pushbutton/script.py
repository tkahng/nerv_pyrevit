from pyrevit.framework import List
from pyrevit import revit, DB
import clr
import xlsxwriter
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, ExternalFileReference, \
	BuiltInParameter, NestedFamilyTypeReference, FamilyType, Viewport,Transaction, GraphicStyleType
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

__doc__ = 'Align sheets on model '\
          'Only works on single view sheets at the time'
# Area and Sector sheet identifier

y = []
lines = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines).SubCategories
lineStyle =[]
for i in lines:
    lineStyle.append('Line' + i.Name)
    lineStyle.append('R' + i.LineColor.Red)
    lineStyle.append('G' + i.LineColor.Green)
    lineStyle.append('B' + i.LineColor.Blue)
    lineStyle.append('Weight' + i.GetLineWeight(GraphicsStyleType.Projection))
y.append(lineStyle)
for i in y:
    print i
#Assign your output to the OUT variable
