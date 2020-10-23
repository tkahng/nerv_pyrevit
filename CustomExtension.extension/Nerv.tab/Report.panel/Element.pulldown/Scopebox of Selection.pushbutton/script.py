from pyrevit.framework import List
from pyrevit import revit, DB
import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ
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

__doc__ = 'Select one element and print out scopebox that the element is in.'

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

if len(selection) > 0:
    el = selection[0]
else:
    print('Please select element first')
# poly = IN[0]
# pts = tolist(IN[1])

loc = el.Location.ToString
if 'Curve' in str(loc):
    Epnt = el.Location.Curve.GetEndPoint(1)
    Spnt = el.Location.Curve.GetEndPoint(0)
    x = (Epnt.X + Spnt.X)/2.0
    y = (Epnt.Y + Spnt.Y) / 2.0
    z = (Epnt.Z + Spnt.Z) / 2.0
    pnt = XYZ(x,y,z)
elif 'Point' in str(loc):
    pnt = el.Location.Point
else:
    pnt = 'Failed to get anything'
print(pnt)
'''
if 'Polygon' in poly.GetType().ToString():
    poly_pts = poly.Points
else:
    poly_pts = [c.StartPoint for c in poly.Curves()]

OUT = [containment(poly_pts, p) for p in pts]
'''


boundingBox = DB.FilteredElementCollector(doc)\
              .OfCategory(BuiltInCategory.OST_VolumeOfInterest).WherePasses(BoundingBoxContainsPointFilter(pnt))\
              .ToElements()


print ('Total Scope Box Number: ' + str(len(boundingBox)))
geoLst = []
for e in boundingBox:
    geoLst.append(e.LookupParameter('Name').AsString())
print(geoLst)

