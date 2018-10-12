from pyrevit.framework import List
from pyrevit import revit, DB
import clr, pprint,os
import Pointdata
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Structure
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
path = 'C:\\Users\\loum\\Documents\\Pyscripts\\'
ew = doc.ActiveProjectLocation.GetProjectPosition(XYZ(0,0,0)).EastWest * float(-1.0)
ns = doc.ActiveProjectLocation.GetProjectPosition(XYZ(0,0,0)).NorthSouth * float(-1.0)
elevation = doc.ActiveProjectLocation.GetProjectPosition(XYZ(0,0,0)).Elevation * float(-1.0)
angle = doc.ActiveProjectLocation.GetProjectPosition(XYZ(0,0,0)).Angle  * float(-1.0)
rotationTransform = Transform.CreateRotation(XYZ.BasisZ, angle)
translationVector = XYZ(ew,ns,elevation)
translationTransform = Transform.CreateTranslation(translationVector)
finalTransform = translationTransform.Multiply(rotationTransform)
count = 0
outLst = []
print(len(Pointdata.pointX))
print(len(Pointdata.pointY))
print(len(Pointdata.pointZ))


# Transaction Start
t = Transaction(doc, 'Add CLash Points')
t.Start()
# Clash point Creation
FSymbol = DB.FilteredElementCollector(doc) \
    .OfClass(clr.GetClrType(FamilySymbol)) \
    .ToElements()
for i in FSymbol:
    Clashpoint = i.Family.FamilyCategory
    print(Clashpoint)
for el in Pointdata.pointX:
    x = float(Pointdata.pointX[count]) + ew
    y = float(Pointdata.pointY[count]) + ns
    z = float(Pointdata.pointZ[count]) + elevation
    pnt = XYZ(x,y,z)
    bPnt = Transform.CreateRotation(XYZ.BasisZ, angle).OfPoint(pnt)

#clashPoint = doc.Create.NewFamilyInstance(bPnt, Clashpoint[0], Structure.StructuralType.NonStructural)
t.Commit()

'''
    boundingBox = DB.FilteredElementCollector(doc)\
                  .OfCategory(BuiltInCategory.OST_VolumeOfInterest)\
                  .WherePasses(BoundingBoxContainsPointFilter(bPnt))\
                  .ToElements()

    geoLst = []
    for e in boundingBox:
        geo = e.GetParameters('Name')
        for a in geo:
            b = a.AsString()
            if 'Sector' in b:
                geoLst.append(b)

    outLst.append(geoLst)
    count = count + 1
print(outLst)

pointFile = open(path + 'Scopeboxdata.py', 'w')
pointFile.write('pointX = ' + pprint.pformat(outLst) + '\n')
'''


