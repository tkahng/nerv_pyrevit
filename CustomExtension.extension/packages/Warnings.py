from Autodesk.Revit.DB import Line, Point, XYZ
import math
def CorrectLineXY(line, m):
    cS = line.GetEndPoint(0)
    cE = line.GetEndPoint(1)
    margin = m*line.Length
    dX = abs(cS.X - cE.X)
    dY = abs(cS.Y - cE.Y)
    print("dX" + str(dX))
    print('dY' + str(dY))
    if dX <= margin:
        r = Line.CreateBound(cS, XYZ(cS.X, cE.Y, cE.Z))
        print("Success")
    elif dY <= margin:
        r = Line.CreateBound(cS, XYZ(cE.X, cS.Y, cE.Z))
        print("Success")
    elif abs(dX-dY) <= m:
        r = Line.CreateBound(cS, XYZ(cE.X, cS.Y + cE.X-cS.X, cE.Z))
    else:
        r = line
        print("Fail")
    return r