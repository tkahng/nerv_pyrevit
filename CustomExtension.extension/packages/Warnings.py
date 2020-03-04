from Autodesk.Revit.DB import Line, Point, XYZ
import math
def CorrectLineXY(line, m):
    cS = line.GetEndPoint(0)
    cE = line.GetEndPoint(1)
    margin = m*line.Length
    dX = abs(cS.X - cE.X)
    dY = abs(cS.Y - cE.Y)
    dZ = abs(cS.Z - cE.Z)
    r = Line.CreateBound(cS, cE)
    print("dX" + str(dX))
    print('dY' + str(dY))
    print('dZ' + str(dZ))
    if dX <= margin and dX != 0.0:
        r = Line.CreateBound(r.GetEndPoint(0), XYZ(r.GetEndPoint(0).X, r.GetEndPoint(1).Y, r.GetEndPoint(1).Z))
        print("Success 1")
    if dY <= margin and dY != 0.0:
        r = Line.CreateBound(r.GetEndPoint(0), XYZ(r.GetEndPoint(1).X, r.GetEndPoint(0).Y, r.GetEndPoint(1).Z))
        print("Success 2")
    if dZ <= margin and dZ != 0.0:
        r = Line.CreateBound(r.GetEndPoint(0), XYZ(r.GetEndPoint(1).X, r.GetEndPoint(1).Y, r.GetEndPoint(0).Z))
        print("Success 3")

    if abs(dX-dY) <= m and abs(dX-dY) != 0.0 and dX != 0.0 and dY != 0.0:
        r = Line.CreateBound(r.GetEndPoint(0), XYZ(r.GetEndPoint(1).X, r.GetEndPoint(0).Y + r.GetEndPoint(1).X-r.GetEndPoint(0).X, r.GetEndPoint(1).Z))
        print("Success 4")

    if abs(dX-dZ) <= m and abs(dX-dZ) != 0.0 and dX != 0.0 and dZ != 0.0:
        r = Line.CreateBound(r.GetEndPoint(0), XYZ(r.GetEndPoint(1).X, r.GetEndPoint(1).Y, r.GetEndPoint(0).Z + r.GetEndPoint(1).X-r.GetEndPoint(0).X))
        print("Success 5")

    if abs(dY-dZ) <= m and abs(dY-dZ) != 0.0 and dY != 0.0 and dZ != 0.0:
        r = Line.CreateBound(cS, XYZ(r.GetEndPoint(1).X, r.GetEndPoint(0).Y + r.GetEndPoint(1).Z-r.GetEndPoint(0).Z, r.GetEndPoint(1).Z))
        print("Success 6")

    return r