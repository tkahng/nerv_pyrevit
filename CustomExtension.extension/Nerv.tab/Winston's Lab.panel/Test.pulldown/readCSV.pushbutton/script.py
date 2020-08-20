import bs4, clr, math
from bs4 import BeautifulSoup
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform, Line, Transaction, \
    GeometryCreationUtilities, CurveLoop, Arc, Plane, Line, Frame, CurveLoop, DirectShapeLibrary, DirectShape,\
<<<<<<< HEAD
    DirectShapeType, Curve, VertexPair, SolidOptions, FilteredElementCollector, BuiltInParameter, BasePoint
=======
    DirectShapeType, Curve, VertexPair, SolidOptions
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Plumbing import Pipe, FlexPipe
from Autodesk.Revit.DB.Mechanical import Duct, FlexDuct
from pyrevit import forms, coreutils
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

def CreateCubeStrut(csdname, csdwidth, csdlength, csdheight, csdstart, csdrotation, scdthickness):
<<<<<<< HEAD
    #print(csdname)
=======
    print(csdname)
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
    vector = XYZ(0, 0, csdheight*-1)
    pp = Plane.CreateByNormalAndOrigin(vector, csdstart)

    trans = Transform.CreateRotationAtPoint(vector, csdrotation, csdstart)

    point1 = csdstart + XYZ(csdwidth/2, csdlength/2, 0)
<<<<<<< HEAD
    point2 = csdstart + XYZ(csdwidth/2 * -1, csdlength/2, 0)
    point3 = csdstart + XYZ(csdwidth/2 * -1, csdlength/2 * -1, 0)
=======
    point2 = csdstart + XYZ(csdwidth/2* -1, csdlength/2, 0)
    point3 = csdstart + XYZ(csdwidth/2* -1, csdlength/2 * -1, 0)
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
    point4 = csdstart + XYZ(csdwidth/2, csdlength/2 * -1, 0)

    profileorigion = CurveLoop().Create(
        [Line.CreateBound(point1, point2), Line.CreateBound(point2, point3), Line.CreateBound(point3, point4),
         Line.CreateBound(point4, point1)])

    finalProfile = CurveLoop.CreateViaTransform(profileorigion, trans)
    geo = GeometryCreationUtilities.CreateExtrusionGeometry([finalProfile], vector, csdheight)
    ele = DirectShape.CreateElement(doc, ElementId(-2000151))
    ele.SetShape([geo])
    ele.SetName(csdname)
    return ele.Id

def CreateRoundStrut(name, diameter, start, height, thickness):
<<<<<<< HEAD
    if height:
        vector = XYZ(0, 0, height*-1)

        #print(name)
        #print(height)

        pp = Plane.CreateByNormalAndOrigin(vector, start)
        profile = CurveLoop().Create([Arc.Create(pp, diameter/2, 0 , math.pi), Arc.Create(pp, diameter/2, math.pi , math.pi*2)])
        geo = GeometryCreationUtilities.CreateExtrusionGeometry([profile], vector, height)
        ele = DirectShape.CreateElement(doc, ElementId(-2000151))
        ele.SetShape([geo])
        ele.SetName(name)
        return ele.Id
    else:
        return None

def CreateRoundStrutwithCone(name, diameter, start, height, coneHeight, topDiameter, frameHeight):
    #print(name)
    vector = XYZ(0, 0, height*-1)
    coneVector = XYZ(0, 0, (coneHeight-frameHeight)*-1)
    frameVector = XYZ(0, 0, frameHeight * -1)

    pp = Plane.CreateByNormalAndOrigin(vector, start + coneVector + frameVector*2)
    ppCone = Plane.CreateByNormalAndOrigin(vector, start + frameVector)
    ppFrame = Plane.CreateByNormalAndOrigin(vector, start)

    frameProfile = CurveLoop().Create([Arc.Create(ppFrame, topDiameter/2, 0, math.pi), Arc.Create(ppFrame, topDiameter/2, math.pi, math.pi*2)])
    coneProfile = CurveLoop().Create([Arc.Create(ppCone, topDiameter/2 + frameHeight + 1/12, 0, math.pi), Arc.Create(ppCone, topDiameter/2 + frameHeight + 1/12, math.pi, math.pi*2)])
    profile = CurveLoop().Create([Arc.Create(pp, diameter/2, 0, math.pi), Arc.Create(pp, diameter/2, math.pi, math.pi*2)])

    frame = GeometryCreationUtilities.CreateExtrusionGeometry([frameProfile], frameVector, frameHeight)
    geo = GeometryCreationUtilities.CreateExtrusionGeometry([profile], vector, height - coneHeight-frameHeight)
    try:
        cone = GeometryCreationUtilities.CreateLoftGeometry([coneProfile, profile], SolidOptions(ElementId.InvalidElementId, ElementId.InvalidElementId))
        # Create Element
        ele = DirectShape.CreateElement(doc, ElementId(-2000151))
        ele.SetShape([geo, cone, frame])
        ele.SetName(name)
        return ele.Id
    except:
        ele = DirectShape.CreateElement(doc, ElementId(-2000151))
        ele.SetShape([geo, frame])
        ele.SetName(name)
        return ele.Id

def AngleAdjustment(csdend, csdstart, csdwidth, csdheight, thickness):
    pp = Plane.CreateByNormalAndOrigin(csdend-csdstart, csdstart)
    interVector = XYZ((csdend-csdstart).Y * -1, (csdend-csdstart).X, 0)

    profile1 = Arc.Create(pp, csdwidth/2 + thickness, 0, math.pi)
    print(pp.XVec)
    print(pp.YVec)
    a = profile1.GetEndPoint(0)
    b = profile1.GetEndPoint(1)
    profile2 = Arc.Create(pp, csdheight/2 + thickness, math.pi/2, math.pi*3/2)

=======
    vector = XYZ(0, 0, height*-1)

    print(name)
    print(height)
    pp = Plane.CreateByNormalAndOrigin(vector, start)
    profile = CurveLoop().Create([Arc.Create(pp, diameter/2, 0 , math.pi),Arc.Create(pp, diameter/2, math.pi , math.pi*2)])
    geo = GeometryCreationUtilities.CreateExtrusionGeometry([profile], vector, height)
    ele = DirectShape.CreateElement(doc, ElementId(-2000151))
    ele.SetShape([geo])
    ele.SetName(name)
    return ele.Id

def CreateRoundStrutwithCone(name, diameter, start, height, coneHeight, topDiameter):
    vector = XYZ(0, 0, height*-1)
    coneVector = XYZ(0, 0, coneHeight*-1)
    coneCurve = Line.CreateBound(start, start + coneVector)
    print(name)
    print(height)
    pp = Plane.CreateByNormalAndOrigin(vector, start + coneVector)
    ppCone = Plane.CreateByNormalAndOrigin(vector, start)

    coneProfile = CurveLoop().Create([Arc.Create(ppCone,topDiameter/2, 0 , math.pi),Arc.Create(ppCone, topDiameter/2, math.pi , math.pi*2)])
    profile = CurveLoop().Create([Arc.Create(pp, diameter/2, 0 , math.pi),Arc.Create(pp, diameter/2, math.pi , math.pi*2)])

    geo = GeometryCreationUtilities.CreateExtrusionGeometry([profile], vector, height - coneHeight)

    cone = GeometryCreationUtilities.CreateLoftGeometry([coneProfile, profile], SolidOptions(ElementId.InvalidElementId, ElementId.InvalidElementId))
    ele = DirectShape.CreateElement(doc, ElementId(-2000151))
    ele.SetShape([geo, cone])
    ele.SetName(name)
    return ele.Id

def CreateStraightDuct(csdname, csdwidth, csdheight, thickness, csdstartO, csdendO, csdlength):
    print(csdname)
    print(csdlength)
    #correction = XYZ(0, 0, csdheight / 2)
    correction = XYZ(0, 0, 0)
    csdstart = csdstartO + correction
    csdend = csdendO + correction
    pp = Plane.CreateByNormalAndOrigin(csdend-csdstart, csdstart)
    profile1 = Arc.Create(pp, csdwidth/2 + thickness, 0, math.pi)
    a = profile1.GetEndPoint(0)

    vector1 = a - csdstart
    vector2 = XYZ((a - csdstart).X, (a - csdstart).Y, 0)
    angle = vector2.AngleTo(vector1)
    print(angle)
    trans1 = Transform.CreateRotationAtPoint(csdend - csdstart, angle, csdstart)
    trans2 = Transform.CreateRotationAtPoint(csdend - csdstart, angle*(-1), csdstart)
    trans3 = Transform.CreateRotationAtPoint(csdend - csdstart, angle * (-1) + math.pi/2, csdstart)
    trans4 = Transform.CreateRotationAtPoint(csdend - csdstart, angle + math.pi / 2, csdstart)
    b = profile1.GetEndPoint(1)
    profile2 = Arc.Create(pp, csdheight/2 + thickness, math.pi/2, math.pi*3/2)
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
    c = profile2.GetEndPoint(0)
    d = profile2.GetEndPoint(1)
    point1 = a+c - csdstart
    point2 = b+c - csdstart
    point3 = b+d - csdstart
    point4 = a+d - csdstart
    l1 = Line.CreateBound(point1, point2)
<<<<<<< HEAD

    vector1 = point1 - point2
    vector2 = XYZ((point1 - point2).X, (point1 - point2).Y, 0)
    vector3 = point1 -point4
    print(vector1)
    print(vector2)
    angle = vector1.AngleOnPlaneTo(interVector, (csdend - csdstart).Normalize())
    #print(angle)
    print(point1)
    print(point2)
    trans1 = Transform.CreateRotationAtPoint(csdend - csdstart, angle, point2)
    trans2 = Transform.CreateRotationAtPoint(csdend - csdstart, angle*(-1), point2)
    trans3 = Transform.CreateRotationAtPoint(csdend - csdstart, angle * (-1) + math.pi/2, point2)
    trans4 = Transform.CreateRotationAtPoint(csdend - csdstart, angle + math.pi / 2, point2)
    print(angle)
    print(angle*(-1))
    print(angle * (-1) + math.pi/2)
    print(angle + math.pi / 2)


=======
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
    #print(point4)
    profileorigion = CurveLoop().Create(
        [Line.CreateBound(point1, point2), Line.CreateBound(point2, point3), Line.CreateBound(point3, point4),
         Line.CreateBound(point4, point1)])
<<<<<<< HEAD
    #print(l1.GetEndPoint(0))
    #print(l1.GetEndPoint(1))
=======
    print(l1.GetEndPoint(0))
    print(l1.GetEndPoint(1))
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316

    numbers = {}
    list = []
    l1Test1 = l1.CreateTransformed(trans1)
    l1Test2 = l1.CreateTransformed(trans2)
    l1Test3 = l1.CreateTransformed(trans3)
    l1Test4 = l1.CreateTransformed(trans4)
<<<<<<< HEAD
    print(l1Test1.GetEndPoint(0))
    print(l1Test1.GetEndPoint(1))
    print(l1Test2.GetEndPoint(0))
    print(l1Test2.GetEndPoint(1))
    print(l1Test3.GetEndPoint(0))
    print(l1Test3.GetEndPoint(1))
    print(l1Test4.GetEndPoint(0))
    print(l1Test4.GetEndPoint(1))
=======
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
    numbers[abs(l1Test1.GetEndPoint(0).Z - l1Test1.GetEndPoint(1).Z)] = trans1
    numbers[abs(l1Test2.GetEndPoint(0).Z - l1Test2.GetEndPoint(1).Z)] = trans2
    numbers[abs(l1Test3.GetEndPoint(0).Z - l1Test3.GetEndPoint(1).Z)] = trans3
    numbers[abs(l1Test4.GetEndPoint(0).Z - l1Test4.GetEndPoint(1).Z)] = trans4
<<<<<<< HEAD

=======
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
    list.append(abs(l1Test1.GetEndPoint(0).Z - l1Test1.GetEndPoint(1).Z))
    list.append(abs(l1Test2.GetEndPoint(0).Z - l1Test2.GetEndPoint(1).Z))
    list.append(abs(l1Test3.GetEndPoint(0).Z - l1Test3.GetEndPoint(1).Z))
    list.append(abs(l1Test4.GetEndPoint(0).Z - l1Test4.GetEndPoint(1).Z))
    list.sort()
<<<<<<< HEAD
    print(list)

def CreateStraightDuct(csdname, csdwidth, csdheight, thickness, csdstartO, csdendO, csdlength):
    #print(csdname)
    #correction = XYZ(0, 0, csdheight / 2)
    correction = XYZ(0, 0, 0)
    csdstart = csdstartO + correction
    csdend = csdendO + correction
    if (csdend-csdstart).GetLength() > 0.1:
        pp = Plane.CreateByNormalAndOrigin(csdend-csdstart, csdstart)
        profile1 = Arc.Create(pp, csdwidth/2 + thickness, 0, math.pi)
        interVector = XYZ((csdend - csdstart).Y * -1, (csdend - csdstart).X, 0)
        a = profile1.GetEndPoint(0)
        b = profile1.GetEndPoint(1)
        profile2 = Arc.Create(pp, csdheight/2 + thickness, math.pi/2, math.pi*3/2)
        c = profile2.GetEndPoint(0)
        d = profile2.GetEndPoint(1)
        point1 = a+c - csdstart
        point2 = b+c - csdstart
        point3 = b+d - csdstart
        point4 = a+d - csdstart
        l1 = Line.CreateBound(point1, point2)

        vector1 = point1 - point2
        vector2 = XYZ((point1 - point2).X, (point1 - point2).Y, 0)
        #print(vector1)
        #print(vector2)
        angle = vector1.AngleOnPlaneTo(interVector, (csdend - csdstart).Normalize())
        #angle = vector2.AngleTo(vector1)
        #print(angle)
        #print(point1)
        #print(point2)
        trans1 = Transform.CreateRotationAtPoint(csdend - csdstart, angle, csdstart)
        trans2 = Transform.CreateRotationAtPoint(csdend - csdstart, angle*(-1), csdstart)
        trans3 = Transform.CreateRotationAtPoint(csdend - csdstart, angle * (-1) + math.pi/2, csdstart)
        trans4 = Transform.CreateRotationAtPoint(csdend - csdstart, angle + math.pi / 2, csdstart)
        #print(angle)
        #print(angle*(-1))
        #print(angle * (-1) + math.pi/2)
        #print(angle + math.pi / 2)


        #print(point4)
        profileorigion = CurveLoop().Create(
            [Line.CreateBound(point1, point2), Line.CreateBound(point2, point3), Line.CreateBound(point3, point4),
             Line.CreateBound(point4, point1)])
        #print(l1.GetEndPoint(0))
        #print(l1.GetEndPoint(1))

        numbers = {}
        list = []
        l1Test1 = l1.CreateTransformed(trans1)
        l1Test2 = l1.CreateTransformed(trans2)
        l1Test3 = l1.CreateTransformed(trans3)
        l1Test4 = l1.CreateTransformed(trans4)

        numbers[abs(l1Test1.GetEndPoint(0).Z - l1Test1.GetEndPoint(1).Z)] = trans1
        numbers[abs(l1Test2.GetEndPoint(0).Z - l1Test2.GetEndPoint(1).Z)] = trans2
        numbers[abs(l1Test3.GetEndPoint(0).Z - l1Test3.GetEndPoint(1).Z)] = trans3
        numbers[abs(l1Test4.GetEndPoint(0).Z - l1Test4.GetEndPoint(1).Z)] = trans4

        list.append(abs(l1Test1.GetEndPoint(0).Z - l1Test1.GetEndPoint(1).Z))
        list.append(abs(l1Test2.GetEndPoint(0).Z - l1Test2.GetEndPoint(1).Z))
        list.append(abs(l1Test3.GetEndPoint(0).Z - l1Test3.GetEndPoint(1).Z))
        list.append(abs(l1Test4.GetEndPoint(0).Z - l1Test4.GetEndPoint(1).Z))
        list.sort()
        finalProfile = CurveLoop.CreateViaTransform(profileorigion, numbers[list[0]])
        geo = GeometryCreationUtilities.CreateExtrusionGeometry([finalProfile], csdend-csdstart, csdlength)
        ele = DirectShape.CreateElement(doc, ElementId(-2000151))
        ele.SetShape([geo])
        ele.SetName(csdname)
        return ele.Id
    else:
        print("Duct too small")
        return None
=======
    finalProfile = CurveLoop.CreateViaTransform(profileorigion, numbers[list[0]])
    geo = GeometryCreationUtilities.CreateExtrusionGeometry([finalProfile], csdend-csdstart, csdlength)
    ele = DirectShape.CreateElement(doc, ElementId(-2000151))
    ele.SetShape([geo])
    ele.SetName(csdname)
    return ele.Id
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316

def CreateCurveDuct(name, width, height, thickness, startO, endO, middleO):
    #correction = XYZ(0, 0, height / 2)
    correction = XYZ(0, 0, 0)
<<<<<<< HEAD
    #print(name)
=======
    print(name)
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
    start = startO + correction
    end = endO + correction
    middle = middleO + correction
    ele = ()
    if start.X == end.X and start.Y == end.Y and start.Z == end.Z:
        print("Curve error, start is the same as end")
        return None
    else:
        path = Arc.Create(start, end, middle)
<<<<<<< HEAD
        #print(name)
        #print(start)
        #print(end)
        #print(middle)
=======
        print(name)
        print(start)
        print(end)
        print(middle)
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
        #print(path.Center)
        pathCurve = CurveLoop().Create([path])
        pp = Plane.CreateByNormalAndOrigin(path.ComputeDerivatives(0, True).BasisX, start)
        profile1 = Arc.Create(pp, width/2 + thickness, 0, math.pi)
<<<<<<< HEAD
        normalVec = path.ComputeDerivatives(0, True).BasisX
        interVector = XYZ((normalVec).Y * -1, (normalVec).X, 0)
        a = profile1.GetEndPoint(0)
        vector1 = a-start
        vector2 = XYZ((a-start).X, (a-start).Y, 0)
        # angle = vector2.AngleTo(vector1)
        angle = vector1.AngleOnPlaneTo(interVector, (end - start).Normalize())
=======
        a = profile1.GetEndPoint(0)

        vector1 = a-start
        vector2 = XYZ((a-start).X, (a-start).Y, 0)
        angle = vector2.AngleTo(vector1)
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
        #print(angle)
        trans1 = Transform.CreateRotationAtPoint(path.ComputeDerivatives(0, True).BasisX, angle, start)
        trans2 = Transform.CreateRotationAtPoint(path.ComputeDerivatives(0, True).BasisX, angle * (-1), start)
        trans3 = Transform.CreateRotationAtPoint(path.ComputeDerivatives(0, True).BasisX, angle * (-1) + math.pi / 2, start)
        trans4 = Transform.CreateRotationAtPoint(path.ComputeDerivatives(0, True).BasisX, angle + math.pi / 2, start)
        b = profile1.GetEndPoint(1)
        profile2 = Arc.Create(pp, height/2 + thickness, math.pi/2, math.pi*3/2)
        c = profile2.GetEndPoint(0)
        d = profile2.GetEndPoint(1)
        point1 = a+c-start
        point2 = b+c-start
        point3 = b+d-start
        point4 = a+d-start

        numbers = {}
        list = []
        l1 = Line.CreateBound(point1, point2)
        l1Test1 = l1.CreateTransformed(trans1)
        l1Test2 = l1.CreateTransformed(trans2)
        l1Test3 = l1.CreateTransformed(trans3)
        l1Test4 = l1.CreateTransformed(trans4)
        numbers[abs(l1Test1.GetEndPoint(0).Z - l1Test1.GetEndPoint(1).Z)] = trans1
        numbers[abs(l1Test2.GetEndPoint(0).Z - l1Test2.GetEndPoint(1).Z)] = trans2
        numbers[abs(l1Test3.GetEndPoint(0).Z - l1Test3.GetEndPoint(1).Z)] = trans3
        numbers[abs(l1Test4.GetEndPoint(0).Z - l1Test4.GetEndPoint(1).Z)] = trans4
        list.append(abs(l1Test1.GetEndPoint(0).Z - l1Test1.GetEndPoint(1).Z))
        list.append(abs(l1Test2.GetEndPoint(0).Z - l1Test2.GetEndPoint(1).Z))
        list.append(abs(l1Test3.GetEndPoint(0).Z - l1Test3.GetEndPoint(1).Z))
        list.append(abs(l1Test4.GetEndPoint(0).Z - l1Test4.GetEndPoint(1).Z))
        list.sort()
        profileorigion = CurveLoop().Create([Line.CreateBound(point1, point2), Line.CreateBound(point2, point3), Line.CreateBound(point3, point4), Line.CreateBound(point4, point1)])
        profile = CurveLoop.CreateViaTransform(profileorigion, numbers[list[0]])


        geo = GeometryCreationUtilities.CreateSweptGeometry(pathCurve, 0, path.GetEndParameter(0), [profile])
        ele = DirectShape.CreateElement(doc, ElementId(-2000151))
        ele.SetShape([geo])
        ele.SetName(name)
        return ele.Id

def CreateStraightPipe(name, diameter, thickness, startO, endO, length):
    #correction = XYZ(0, 0, diameter/2)
<<<<<<< HEAD
    #print("Diameter" + str(diameter))
    #print(name)
    correction = XYZ(0, 0, 0)
    start = startO + correction
    end = endO + correction
    #print(name)
    #print(length)
    if (end-start).GetLength() > 0.1:
        pp = Plane.CreateByNormalAndOrigin(end-start, start)
        profile = CurveLoop().Create([Arc.Create(pp, diameter/2 + thickness, 0, math.pi), Arc.Create(pp, diameter/2 + thickness, math.pi, math.pi*2)])
        geo = GeometryCreationUtilities.CreateExtrusionGeometry([profile], end-start, length)
        ele = DirectShape.CreateElement(doc, ElementId(-2000151))
        ele.SetShape([geo])
        ele.SetName(name)
        return ele.Id
    else:
        print("Duct too small")
        return None

=======
    print("Diameter" + str(diameter))
    correction = XYZ(0, 0, 0)
    start = startO + correction
    end = endO + correction
    print(name)
    print(length)
    pp = Plane.CreateByNormalAndOrigin(end-start, start)
    profile = CurveLoop().Create([Arc.Create(pp, diameter/2 + thickness, 0, math.pi), Arc.Create(pp, diameter/2 + thickness, math.pi, math.pi*2)])
    geo = GeometryCreationUtilities.CreateExtrusionGeometry([profile], end-start, length)
    ele = DirectShape.CreateElement(doc, ElementId(-2000151))
    ele.SetShape([geo])
    ele.SetName(name)
    return ele.Id
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
    #print(Arc.Create(pp, diameter, math.pi , math.pi*2).ComputeDerivatives(0.5, True).BasisX)
    #print(Arc.Create(pp, diameter, math.pi, math.pi * 2).ComputeDerivatives(0.5, True).BasisY)
    #print(Arc.Create(pp, diameter, math.pi, math.pi * 2).ComputeDerivatives(0.5, True).BasisZ)

def CreateCurvePipe(name, diameter,thickness, startO, endO, middleO):
<<<<<<< HEAD
    #print(name)
    # print("Diameter" + str(diameter))
=======
    print("Diameter" + str(diameter))
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
    #correction = XYZ(0, 0, diameter / 2)
    correction = XYZ(0, 0, 0)
    start = startO + correction
    end = endO + correction
    middle = middleO + correction
<<<<<<< HEAD
    #print(name)
    #print(start)
    #print(end)
    #print(middle)
=======
    print(name)
    print(start)
    print(end)
    print(middle)
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
    path = Arc.Create(start, end, middle)
    pathCurve = CurveLoop().Create([path])
    pp = Plane.CreateByNormalAndOrigin(path.ComputeDerivatives(0, True).BasisX, start)
    profile = CurveLoop().Create([Arc.Create(pp, diameter/2 + thickness, 0, math.pi), Arc.Create(pp, diameter/2 + thickness, math.pi , math.pi*2)])
    geo = GeometryCreationUtilities.CreateSweptGeometry(pathCurve, 0, path.GetEndParameter(0), [profile])
    ele = DirectShape.CreateElement(doc, ElementId(-2000151))
    ele.SetShape([geo])
    ele.SetName(name)
    return ele.Id

def Number(n):
    if n[-1] == ".":
        return float(float(n[0:-1])/12)
    else:
        return float(n)

def InchOrFeet(n):
    try:
        if n[-2] == "\"":
            return float(float(n[1:-3])/12)
        elif n[-1] == "\'":
            return float(n[0:-1])
        else:
            return None
    except:
        return None

<<<<<<< HEAD

xAdjust = -6427300
yAdjust = -1844100
zAdjust = -300

xSurveyAdjust = -6426808.660
ySurveyAdjust = -1843624.760
zSurveyAdjust = 0

=======
xAdjust = -6427300
yAdjust = -1844100
zAdjust = -300
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
t = Transaction(doc, 'Add CLash Points')
t.Start()

#CreateStraightDuct("test", 48/12, 72/12, XYZ(6427332.2082 - 6427300, 1844136.7557-1844100, 306.927-300), XYZ(6427332.2082 - 6427300, 1844136.7557-1844100, 306.927-300-7), 7)
# Documentation of work\

points = {}

fileCSV = forms.pick_file(file_ext='txt', multi_file=False, unc_paths=False)


wallThicknesses = {}

with open(fileCSV, "r") as f:
    # Read each line in the file, readlines() returns a list of lines
    content = f.readlines()
    # Combine the lines in the list into a string
    for line in content:
        lineData = line.split(",")
        name = lineData[0]
<<<<<<< HEAD
        print(name)
=======
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
        dataLine = lineData[1:]
        data = {}
        for d in dataLine:
            #print(d)
            try:
                pair = str(d).split(":")
                #print(pair)
                data[pair[0].strip()] = pair[1].strip()
            except:
                print("Error 1")
        # Pressure Pipe
        if name[0:13] == 'Pressure Pipe':
            startx = float(data['StartX']) + xAdjust
            starty = float(data['StartY']) + yAdjust
            startz = float(data['StartZ']) + zAdjust
            endx = float(data['EndX']) + xAdjust
            endy = float(data['EndY']) + yAdjust
            endz = float(data['EndZ']) + zAdjust
            start = XYZ(startx, starty, startz)
            end = XYZ(endx, endy, endz)
            outDiameter = float(data['OuterDiameter'])
            innerDiameter = float(data['InnerDiameter'])
            thickness = float(data['WallThickness'])
            description = data['Style']
<<<<<<< HEAD
            eleType2 = CreateStraightPipe(name, innerDiameter, thickness, start, end, start.DistanceTo(end))
            if eleType2:
                v1 = doc.GetElement(eleType2).LookupParameter("Mark").Set(str(name))
                try:
                    v2 = doc.GetElement(eleType2).LookupParameter("Comments").Set(str(description))
                except:
                    print("Description cannot be found")


=======
            if "ductile" in description:
                eleType1 = CreateStraightDuct(name, outDiameter, innerDiameter, thickness, start, end, start.DistanceTo(end))
                if eleType1:
                    v1 = doc.GetElement(eleType1).LookupParameter("Mark").Set(str(name))
                    v2 = doc.GetElement(eleType1).LookupParameter("Comments").Set(str(description))
            else:
                eleType2 = CreateStraightPipe(name, innerDiameter, thickness, start, end, start.DistanceTo(end))
                if eleType2:
                    v1 = doc.GetElement(eleType2).LookupParameter("Mark").Set(str(name))
                    v2 = doc.GetElement(eleType2).LookupParameter("Comments").Set(str(description))
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
        # Pipes
        elif name[0:4] == 'Pipe':
            if float(data['StartX']) != 0.0 and float(data['StartY']) != 0.0 and float(data['StartZ']) != 0.0:
                startx = float(data['StartX']) + xAdjust
                starty = float(data['StartY']) + yAdjust
                startz = float(data['StartZ']) + zAdjust
                endx = float(data['EndX']) + xAdjust
                endy = float(data['EndY']) + yAdjust
                endz = float(data['EndZ']) + zAdjust
                wallThickness = float(data['Wall Thickness'])/12
                start = XYZ(startx, starty, startz)
                end = XYZ(endx, endy, endz)
                if 'Inner Pipe Diameter' in data.keys():
                    #print(float(data['Inner Pipe Diameter']))
                    pipeinnerdiameter = float(data['Inner Pipe Diameter'])
                    #print(pipeinnerdiameter)
                    pipediameter = pipeinnerdiameter/12
                    #print(pipediameter)
                    if float(data['CenterX']) != 0:
                        centerx = float(data['CenterX']) + xAdjust
                        centery = float(data['CenterY']) + yAdjust
                        centerz = (startz + endz)/2
                        middle = XYZ(centerx, centery, centerz)
                        eleType1 = CreateCurvePipe(name, pipediameter, wallThickness, start, end, middle)
                        if eleType1:
                            v1 = doc.GetElement(eleType1).LookupParameter("Mark").Set(str(name))
<<<<<<< HEAD
                            try:
                                v2 = doc.GetElement(eleType1).LookupParameter("Comments").Set(str(description))
                            except:
                                print("Description cannot be found")
=======
                            v2 = doc.GetElement(eleType1).LookupParameter("Comments").Set(str(description))
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
                    else:
                        eleType2 = CreateStraightPipe(name, pipediameter, wallThickness, start, end, start.DistanceTo(end))
                        if eleType2:
                            v1 = doc.GetElement(eleType2).LookupParameter("Mark").Set(str(name))
<<<<<<< HEAD
                            try:
                                v2 = doc.GetElement(eleType2).LookupParameter("Comments").Set(str(description))
                            except:
                                print("Description cannot be found")
=======
                            v2 = doc.GetElement(eleType2).LookupParameter("Comments").Set(str(description))
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
                elif 'Inner Pipe Width' in data.keys():
                    innerWidth = float(data['Inner Pipe Width'])/12 #+ wallThickness*2
                    innerHeight = float(data['Inner Pipe Height'])/12 #+wallThickness*2
                    #print("width" + str(innerWidth))
                    #print("height" + str(innerHeight))
                    if float(data['CenterX']) != 0.0:
                        centerx = float(data['CenterX']) + xAdjust
                        centery = float(data['CenterY']) + yAdjust
                        centerz = (startz + endz)/2
                        middle = XYZ(centerx, centery, centerz)
<<<<<<< HEAD
                        try:
                            eleType1 = CreateCurveDuct(name, innerWidth, innerHeight, wallThickness, start, end, middle)
                            if eleType1:
                                v1 = doc.GetElement(eleType1).LookupParameter("Mark").Set(str(name))
                                try:
                                    v2 = doc.GetElement(eleType1).LookupParameter("Comments").Set(str(description))
                                except:
                                    print("Description cannot be found")
                        except:
                            print("Curve Create error creating straight line")
                            eleType1 = CreateStraightDuct(name, innerWidth, innerHeight, wallThickness, start, end, start.DistanceTo(end))
                            if eleType1:
                                v1 = doc.GetElement(eleType1).LookupParameter("Mark").Set(str(name))
                                try:
                                    v2 = doc.GetElement(eleType1).LookupParameter("Comments").Set(str(description))
                                except:
                                    print("Description cannot be found")
=======
                        eleType1 = CreateCurveDuct(name, innerWidth, innerHeight, wallThickness, start, end, middle)
                        if eleType1:
                            v1 = doc.GetElement(eleType1).LookupParameter("Mark").Set(str(name))
                            v2 = doc.GetElement(eleType1).LookupParameter("Comments").Set(str(description))
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
                    else:
                        eleType2 = CreateStraightDuct(name, innerWidth, innerHeight, wallThickness, start, end, start.DistanceTo(end))
                        if eleType2:
                            v1 = doc.GetElement(eleType2).LookupParameter("Mark").Set(str(name))
<<<<<<< HEAD
                            try:
                                v2 = doc.GetElement(eleType2).LookupParameter("Comments").Set(str(description))
                            except:
                                print("Description cannot be found")
=======
                            v2 = doc.GetElement(eleType2).LookupParameter("Comments").Set(str(description))
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
            else:
                print("Please check the starting point")

        # Structures
<<<<<<< HEAD
        elif name[0:9] == 'Structure' or name[0:4] == 'SSMH':
=======
        elif name[0:9] == 'Structure':
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
            print(name)
            x = float(data['X']) + xAdjust
            y = float(data['Y']) + yAdjust
            z = float(data['Z']) + zAdjust
<<<<<<< HEAD
            struDescription = data['Description']
            position = XYZ(x, y, z)
            rotation = float(data['Rotation']) * -1
            if not "null structure" in struDescription.lower() and not "nullstructure" in struDescription.lower():
                if rotation != 0 and 'Structure Height' in data.keys() and 'Structure Width' in data.keys() and 'Structure Length' in data.keys():
                    height = float(data['Structure Height']) / 12
                    length = float(data['Structure Length']) / 12
                    width = float(data['Structure Width']) / 12

                    ele = CreateCubeStrut(name, width, length, height, position, rotation, 0)
                    if ele:
                        v1 = doc.GetElement(ele).LookupParameter("Mark").Set(str(name))
                        try:
                            v2 = doc.GetElement(ele).LookupParameter("Comments").Set(str(struDescription))
                        except:
                            print("Description cannot be found")

                elif rotation != 0 and 'Structure Height' in data.keys() and 'Structure Width' in data.keys() and 'Inner Structure Length' in data.keys():
                    height = float(data['Structure Height']) / 12
                    length = float(data['Inner Structure Length']) / 12 + float(data['Wall Thickness']) / 12 * 2
                    width = float(data['Structure Width']) / 12
                    ele = CreateCubeStrut(name, width, length, height, position, rotation, 0)
                    if ele:
                        v1 = doc.GetElement(ele).LookupParameter("Mark").Set(str(name))
                        try:
                            v2 = doc.GetElement(ele).LookupParameter("Comments").Set(str(struDescription))
                        except:
                            print("Description cannot be found")

                elif 'Cone Height' in data.keys() and 'Structure Height' in data.keys() and 'Structure Diameter' in data.keys():
                    height = float(data['Structure Height']) / 12 #+ float(data['Floor Thickness'])/12
                    diameter = float(data['Structure Diameter']) / 12 #+ float(data['Wall Thickness'])/12
                    coneHeight = float(data['Cone Height']) / 12
                    coneDiameter = float(data['Frame Diameter']) / 12
                    frameHeight = float(data['Frame Height']) / 12
                    ele = CreateRoundStrutwithCone(name, diameter, position, height, coneHeight, coneDiameter, frameHeight)
                    if ele:
                        v1 = doc.GetElement(ele).LookupParameter("Mark").Set(str(name))
                        try:
                            v2 = doc.GetElement(ele).LookupParameter("Comments").Set(str(struDescription))
                        except:
                            print("Description cannot be found")

                elif 'Rim to Sump Height' in data.keys() and 'Structure Height' in data.keys() and 'Structure Diameter' in data.keys():
                    height = float(data['Structure Height']) / 12 #+ float(data['Floor Thickness'])/12
                    diameter = float(data['Structure Diameter']) / 12 #+ float(data['Wall Thickness'])/12
                    ele = CreateRoundStrut(name, diameter, position, height, 0)
                    if ele:
                        v1 = doc.GetElement(ele).LookupParameter("Mark").Set(str(name))
                        try:
                            v2 = doc.GetElement(ele).LookupParameter("Comments").Set(str(struDescription))
                        except:
                            print("Description cannot be found")

                elif rotation == 0 and 'Structure Height' in data.keys() and 'Structure Diameter' in data.keys():
                    height = float(data['Structure Height'])/12
                    diameter = float(data['Structure Diameter'])/12
                    ele = CreateRoundStrut(name, diameter, position, height, 0)
                    if ele:
                        v1 = doc.GetElement(ele).LookupParameter("Mark").Set(str(name))
                        try:
                            v2 = doc.GetElement(ele).LookupParameter("Comments").Set(str(struDescription))
                        except:
                            print("Description cannot be found")

                elif 'Structure Height' in data.keys() and 'Structure Diameter' in data.keys():
                    height = float(data['Structure Height'])/12
                    diameter = float(data['Structure Diameter'])/12
                    ele = CreateRoundStrut(name, diameter, position, height, 0)
                    if ele:
                        v1 = doc.GetElement(ele).LookupParameter("Mark").Set(str(name))
                        try:
                            v2 = doc.GetElement(ele).LookupParameter("Comments").Set(str(struDescription))
                        except:
                            print("Description cannot be found")

                else:
                    print("Creation Error")
=======
            position = XYZ(x, y, z)
            rotation = float(data['Rotation']) * -1

            if rotation != 0 and 'Structure Height' in data.keys() and 'Structure Width' in data.keys() and 'Structure Length' in data.keys():
                height = float(data['Structure Height']) / 12
                length = float(data['Structure Length']) / 12
                width = float(data['Structure Width']) / 12
                ele = CreateCubeStrut(name, width, length, height, position, rotation, 0)
                if ele:
                    v1 = doc.GetElement(ele).LookupParameter("Mark").Set(str(name))


            elif rotation != 0 and 'Structure Height' in data.keys() and 'Structure Width' in data.keys() and 'Inner Structure Length' in data.keys():
                height = float(data['Structure Height']) / 12
                length = float(data['Inner Structure Length']) / 12 + float(data['Wall Thickness']) / 12 * 2
                width = float(data['Structure Width']) / 12
                ele = CreateCubeStrut(name, width, length, height, position, rotation, 0)
                if ele:
                    v1 = doc.GetElement(ele).LookupParameter("Mark").Set(str(name))

            elif 'Cone Height' in data.keys() and 'Structure Height' in data.keys() and 'Structure Diameter' in data.keys():
                height = float(data['Structure Height']) / 12 + int(data['Floor Thickness'])/12
                diameter = float(data['Structure Diameter']) / 12 + int(data['Wall Thickness'])/12
                coneHeight = float(data['Cone Height']) / 12
                coneDiameter = float(data['Frame Diameter']) / 12
                ele = CreateRoundStrutwithCone(name, diameter, position, height, coneHeight, coneDiameter)
                if ele:
                    v1 = doc.GetElement(ele).LookupParameter("Mark").Set(str(name))

            elif 'Rim to Sump Height' in data.keys() and 'Structure Height' in data.keys() and 'Structure Diameter' in data.keys():
                height = float(data['Structure Height']) / 12 + int(data['Floor Thickness'])/12
                diameter = float(data['Structure Diameter']) / 12 + int(data['Wall Thickness'])/12
                ele = CreateRoundStrut(name, diameter, position, height, 0)
                if ele:
                    v1 = doc.GetElement(ele).LookupParameter("Mark").Set(str(name))


            elif rotation == 0 and 'Structure Height' in data.keys() and 'Structure Diameter' in data.keys():
                height = float(data['Structure Height'])/12
                diameter = float(data['Structure Diameter'])/12
                ele = CreateRoundStrut(name, diameter, position, height, 0)
                if ele:
                    v1 = doc.GetElement(ele).LookupParameter("Mark").Set(str(name))

            else:
                print("Creation Error")
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
        # Error Message
        else:
            print(name + " not built")

<<<<<<< HEAD

    basePoint = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_ProjectBasePoint).ToElements()[0]
    basePoint.get_Parameter(BuiltInParameter.BASEPOINT_NORTHSOUTH_PARAM).Set(yAdjust*-1)
    basePoint.get_Parameter(BuiltInParameter.BASEPOINT_EASTWEST_PARAM).Set(xAdjust*-1)
    basePoint.get_Parameter(BuiltInParameter.BASEPOINT_ELEVATION_PARAM).Set(zAdjust*-1)
    '''
    surveyPoint = FilteredElementCollector(doc).OfClass(BasePoint).ToElements()[1]
    surveyPoint.get_Parameter(BuiltInParameter.BASEPOINT_NORTHSOUTH_PARAM).Set(ySurveyAdjust*-1)
    surveyPoint.get_Parameter(BuiltInParameter.BASEPOINT_EASTWEST_PARAM).Set(xSurveyAdjust*-1)
    surveyPoint.get_Parameter(BuiltInParameter.BASEPOINT_ELEVATION_PARAM).Set(zSurveyAdjust*-1)
    '''
    projectLocation = uidoc.Document.ActiveProjectLocation
    projectPosition = projectLocation.GetProjectPosition(XYZ(0, 0, 0))

    projectPosition.NorthSouth = ySurveyAdjust*-1
    projectPosition.EastWest = xSurveyAdjust*-1
    projectPosition.Elevation = zSurveyAdjust*-1
    projectLocation.SetProjectPosition(XYZ(0, 0, 0), projectPosition)

t.Commit()
=======
t.Commit()

'''
        description = lineData[1]
        diameter = ()
        width = ()
        height = ()
        thickness = ()

        startx = InchOrFeet(lineData[15])
        starty = InchOrFeet(lineData[16])
        startz = InchOrFeet(lineData[19])
        startzOut = InchOrFeet(lineData[21])

        if startzOut and startz:
            thickness = abs(startzOut - startz)
        else:
            thickness = ()
        endx = InchOrFeet(lineData[17])
        endy = InchOrFeet(lineData[18])
        endz = InchOrFeet(lineData[20])
        endOut = InchOrFeet(lineData[22])
        if "x" in lineData[4]:
            content = lineData[4].replace(" in", "")
            width = float(content.split("x")[0])/12
            height = float(content.split("x")[1])/12
        else:
            try:
                diameter = float(lineData[4]) / 12
            except:
                pass

        length = ()
        print(name)
        print(description)
        print(diameter)
        if starty and startx and startz:
            start = XYZ(startx-6427300, starty-1844100, startz-300)
            end = XYZ(endx-6427300, endy-1844100, endz-300)
            print(start)
            print(end)
            length = (end-start).GetLength()
            print(length)
        else:
            start = None
            end = None
        if diameter and start:
            eleType1 = CreateStraightPipe(name, diameter, thickness, start, end, length)
            if eleType1:
                v1 = doc.GetElement(eleType1).LookupParameter("Mark").Set(str(name))
                v2 = doc.GetElement(eleType1).LookupParameter("Comments").Set(str(description))
        elif height and width and start:
            eleType2 = CreateStraightDuct(name, width, height, thickness, start, end, length)
            if eleType2:
                v1 = doc.GetElement(eleType2).LookupParameter("Mark").Set(str(name))
                v2 = doc.GetElement(eleType2).LookupParameter("Comments").Set(str(description))
        else:
            print('invalid line')

with open(fileCSV, "r") as f:
    # Read each line in the file, readlines() returns a list of lines
    content = f.readlines()
    # Combine the lines in the list into a string
    for line in content:
        lineData = line.split(",")
        name = lineData[1]
        description = lineData[2]
        diameter = InchOrFeet(lineData[8])
        innerlength = InchOrFeet(lineData[9])
        innerwidth = InchOrFeet(lineData[10])
        innerheight = InchOrFeet(lineData[11])
        try:
            rotation = float(lineData[12][0:-3])/180 * math.pi * -1
            #rotation = 0
        except:
            rotation = None
        starty = InchOrFeet(lineData[16])
        startx = InchOrFeet(lineData[17])
        startz = InchOrFeet(lineData[18])

        print(name)
        print(description)
        print(diameter)
        print(innerlength)
        print(innerwidth)
        print(innerheight)
        print(rotation)
        print(starty)
        print(startx)
        print(startz)

        if starty and startx and startz:
            start = XYZ(startx-6427300, starty-1844100, startz-300)
        else:
            start = None
        if diameter and start and innerheight:
            eleType3 = CreateRoundStrut(name, diameter, start, innerheight)
            if eleType3:
                v1 = doc.GetElement(eleType3).LookupParameter("Mark").Set(str(name))
                v2 = doc.GetElement(eleType3).LookupParameter("Comments").Set(str(description))
        elif innerheight and innerwidth and innerlength and start:
            eleType4 = CreateCubeStrut(name, innerwidth, innerlength, innerheight, start, rotation)
            if eleType4:
                v1 = doc.GetElement(eleType4).LookupParameter("Mark").Set(str(name))
                v2 = doc.GetElement(eleType4).LookupParameter("Comments").Set(str(description))
        else:
            print('invalid line')

with open(file, "r") as f:
    # Read each line in the file, readlines() returns a list of lines
    content = f.readlines()
    # Combine the lines in the list into a string
    content = "".join(content)
    bs_content = bs4.BeautifulSoup(content, "html.parser")

    struct= bs_content.find_all("struct")

    for s in struct:
        try:
            # print(a.attrs['name'])
            y = float(s.find("center").text.split(" ")[0])-1844100
            x = float(s.find("center").text.split(" ")[1])-6427300
            z = float(s.find("invert").attrs['elev'] + str("0"))-300
            points[s.attrs['name']] = XYZ(x, y, z)
        except:
            pass
    print(str(len(points.keys())))
# find pipesurinder
    pipes = bs_content.find_all("pipe")
    print(len(pipes))
    n = 0
    for a in pipes:
        # if n < 999999:
        #t = Transaction(doc, 'Add CLash Points')
        #t.Start()
        # Straight Pipe and Duct Creation
        if not a.find("center"):
            if a.find("circpipe"):
                cirdiameter = Number(a.find("circpipe").attrs['diameter']) + float(str(a.find("circpipe").attrs['thickness']) + "0") * 2
                thickness = float(str(a.find("circpipe").attrs['thickness']) + "0")
                #systemId = ElementId(607132)
                #pipeTypeId = ElementId(150706)
                #levelId = ElementId(30)
                cirlength = Number(a.attrs['length'])
                cirname = a.attrs['name']
                cirDes = a.attrs['desc']
                cirstartPoint = points[a.attrs['refstart']]
                cirendPoint = points[a.attrs['refend']]
                #try:
                eleType1 = CreateStraightPipe(cirname, cirdiameter, thickness, cirstartPoint, cirendPoint, cirlength)
                if eleType1:
                    v1 = doc.GetElement(eleType1).LookupParameter("Mark").Set(str(cirname))
                    v2 = doc.GetElement(eleType1).LookupParameter("Comments").Set(str(cirDes))
                    #centerLine = Line.CreateBound(startPoint, endPoint)
                    # Pipe.Create(doc, systemId, pipeTypeId, levelId, startPoint, endPoint)
                    # print('successful')
                #except:
                 #   print("fail straight pipe")
                n += 1
            elif a.find("rectpipe"):
                recwidth = float(str(a.find("rectpipe").attrs['width']) + "0")
                recheight = float(str(a.find("rectpipe").attrs['height']) + "0")
                thickness = float(str(a.find("rectpipe").attrs['thickness']) + "0")
                reclength = float(a.attrs['length'])
                #systemId = ElementId(607128)
                #ductTypeId = ElementId(139191)
                #levelId = ElementId(30)
                recName = a.attrs['name']
                recDes = a.attrs['desc']
                recstartPoint = points[a.attrs['refstart']]
                recendPoint = points[a.attrs['refend']]
                try:
                    eleType2 = CreateStraightDuct(recName, recwidth, recheight, thickness, recstartPoint, recendPoint, reclength)
                    if eleType2:
                        v1 = doc.GetElement(eleType2).LookupParameter("Mark").Set(str(recName))
                        v2 = doc.GetElement(eleType2).LookupParameter("Comments").Set(str(recDes))
                    #Duct.Create(doc, systemId, ductTypeId, levelId, startPoint, endPoint)
                    #GeometryCreationUtilities.CreateSweptGeometry.

                except:
                    print("fail straight duct")
                # flex duck and flex pipe
                n += 1


        else:
            if a.find("circpipe"):
                diameter = Number(a.find("circpipe").attrs['diameter'])
                thickness = float(str(a.find("circpipe").attrs['thickness']) + "0")
                midNumberY = float(a.find("center").text.split(" ")[0])-1844100
                midNumberX = float(a.find("center").text.split(" ")[1])-6427300
                startPoint = points[a.attrs['refstart']]
                endPoint = points[a.attrs['refend']]
                midNumberZ = (startPoint.Z + endPoint.Z)/2
                midPoint = XYZ(midNumberX, midNumberY, midNumberZ)
                name = a.attrs['name']
                cirCurDes = a.attrs['desc']
                # Pipe information
                #systemId = ElementId(607132)
                #typeId = ElementId(150707)
                #levelId = ElementId(30)
                #pipeSystemId = ElementId(607132)
                pipeTypeId = ElementId(150706)

                #try:
                    #centerLine = Line.CreateBound(startPoint, endPoint)

                eleType3 = CreateCurvePipe(name, diameter, thickness, startPoint, endPoint, midPoint)
                if eleType3:
                    v1 = doc.GetElement(eleType3).LookupParameter("Mark").Set(str(name))
                    v2 = doc.GetElement(eleType3).LookupParameter("Comments").Set(str(cirCurDes))
                # CreateStraightPipe(diameter, startPoint, endPoint)
                #except:
                   #print("fail flex pipe")

            elif a.find("rectpipe"):
                width = float(str(a.find("rectpipe").attrs['width']) + "0")
                height = float(str(a.find("rectpipe").attrs['height']) + "0")
                thickness = float(str(a.find("rectpipe").attrs['thickness']) + "0") * 2
                name = a.attrs['name']
                recCurDes = a.attrs['desc']
                midNumberY = float(a.find("center").text.split(" ")[0])-1844100
                midNumberX = float(a.find("center").text.split(" ")[1])-6427300
                startPoint = points[a.attrs['refstart']]
                endPoint = points[a.attrs['refend']]
                midNumberZ = (startPoint.Z + endPoint.Z)/2
                midPoint = XYZ(midNumberX, midNumberY, midNumberZ)

                #systemId = ElementId(607128)
                #typeId = ElementId(139193)
                #levelId = ElementId(30)


                #ductSystemId = ElementId(607128)
                #ductTypeId = ElementId(139191)
                #try:

                eleType4 = CreateCurveDuct(name, width, height, thickness, startPoint, endPoint, midPoint)
                if eleType4:
                    v1 = doc.GetElement(eleType4).LookupParameter("Mark").Set(str(name))
                    v2 = doc.GetElement(eleType4).LookupParameter("Comments").Set(str(recCurDes))
                #except:
                #    print("fail flex duct")
                    #CreateCurveDuctAlt(name, width, height, startPoint, endPoint, midPoint)
                    #CreateStraightDuct(width, height, startPoint, endPoint)
                    #FlexDuct.Create(doc, systemId, typeId, levelId, [startPoint, midPoint, endPoint])
                    #Duct.Create(doc, ductSystemId, ductTypeId, levelId, startPoint, midPoint)
                    #Duct.Create(doc, ductSystemId, ductTypeId, levelId, midPoint, endPoint)

                    #print("SUCCESS flex duct")
                #except:
                    #print("fail flex duct")
                     # print(a.attrs['name'])

t.Commit()
        #n+= 1

'''
>>>>>>> f488cd7d0ca624dfa30a3056098cbce60717a316
