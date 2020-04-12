from pyrevit import revit, DB
import clr, pprint
import Pointdata
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


__doc__ = 'Read clash data off html and generate Scopebox data from a specific file'

# containment -----------------------------------
def tolist(obj1):
    if hasattr(obj1, '__iter__'):
        return obj1
    else:
        return [obj1]


def containment(poly, pt):
    def testCCW(A, B, C):
        return (B.X - A.X) * (C.Y - A.Y) > (B.Y - A.Y) * (C.X - A.X)

    wn = 0
    ln1 = len(poly)
    for i in xrange(ln1):
        j = (i + 1) % ln1
        isCCW = testCCW(poly[i], poly[j], pt)
        if poly[i].Y <= pt.Y:
            if poly[j].Y > pt.Y and isCCW: wn += 1
        else:
            if poly[j].Y <= pt.Y and not isCCW: wn -= 1

    return wn != 0


# input ---------------------
path = 'C:\\Users\\loum\\Documents\\Pyscripts\\ClashScripts\\'
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
for el in Pointdata.pointX:
    x = float(Pointdata.pointX[count]) + ew
    y = float(Pointdata.pointY[count]) + ns
    z = float(Pointdata.pointZ[count]) + elevation

    pnt = XYZ(x,y,z)

    bPnt = Transform.CreateRotation(XYZ.BasisZ, angle).OfPoint(pnt)

    boundingBox = DB.FilteredElementCollector(doc)\
                  .OfCategory(BuiltInCategory.OST_VolumeOfInterest).WherePasses(BoundingBoxContainsPointFilter(bPnt))\
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


