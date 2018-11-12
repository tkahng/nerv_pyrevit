from pyrevit.framework import List
from pyrevit import revit, DB
import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, ExternalFileReference, \
	BuiltInParameter, NestedFamilyTypeReference, FamilyType, Viewport,Transaction
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
def sheetidentifier(vPort):
    shId = vPort.SheetId
    veId = vPort.ViewId
    sheetN = doc.GetElement(shId).LookupParameter('Sheet Name').AsString()
    viewN = doc.GetElement(veId).Name
    if 'SECTOR' in sheetN:
        return True
    else:
        return False
# Title Block and Sheets Collector
titleBlock = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).ToElements()
sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).ToElements()
viewPorts = FilteredElementCollector(doc).OfClass(Viewport).ToElements()
sCollector = []
repeatCollector = []
usCollector = []
# print(len(viewPorts))
for viewPort in viewPorts:
    sId = viewPort.SheetId.IntegerValue
    if sId in sCollector:
        repeatCollector.append(sId)
    sCollector.append(sId)

# print(len(repeatCollector))
# Transaction Start
t = Transaction(doc, 'Align Single View Sheets')
# Get Fist View Position
# t.Start()
# Get the first View port that contains SECTOR to align to
firstViewPort = ()
for i in viewPorts:
    id = i.SheetId.IntegerValue
    eId = i.SheetId
    sheetName = doc.GetElement(eId).LookupParameter('Sheet Name').AsString()
    # print(sheetName)
    if not id in repeatCollector:
        if sheetidentifier(i):
            firstViewPort = i
            break

# Get First Viewport position to align to
firstPosition = firstViewPort.GetBoxOutline().MinimumPoint
firstPositionMax = firstViewPort.GetBoxOutline().MaximumPoint
firstsheetnumber = doc.GetElement(firstViewPort.SheetId).LookupParameter('Sheet Number').AsString()
firstsheetname = doc.GetElement(firstViewPort.SheetId).LookupParameter('Sheet Name').AsString()
firstviewName = doc.GetElement(firstViewPort.ViewId).Name
firstviewLoop = doc.GetElement(firstViewPort.ViewId).CropBox
firstviewOutline = doc.GetElement(firstViewPort.ViewId).Outline
BBox = doc.GetElement(firstViewPort.ViewId).GetCropRegionShapeManager().GetCropShape()
Plane = ()
for i in BBox:
    Plane = i.GetPlane()
    print(i.GetRectangularHeight(Plane), i.GetRectangularWidth(Plane))
Box = doc.GetElement(firstViewPort.ViewId).GetCropRegionShapeManager().GetAnnotationCropShape()

print(Box.GetRectangularHeight(Plane), Box.GetRectangularWidth(Plane))
print(firstviewLoop.Min, firstviewLoop.Max)
print(firstviewOutline.Min, firstviewOutline.Max)
firstX = firstPosition.X
firstY = firstPosition.Y
firstZ = firstPosition.Z
print(firstX, firstY, firstZ)
print(firstPositionMax.X, firstPositionMax.Y, firstPositionMax.Z)
# Get First Label Data to Align to
firstLabel = firstViewPort.GetLabelOutline().MaximumPoint
firstLabelX = firstLabel.X
firstLabelY = firstLabel.Y
firstLabelZ = firstLabel.Z
# print(firstLabelX, firstLabelY, firstLabelZ)
# print('First View to Align to', firstsheetnumber, firstsheetname, firstviewName, firstX, firstY, firstZ)