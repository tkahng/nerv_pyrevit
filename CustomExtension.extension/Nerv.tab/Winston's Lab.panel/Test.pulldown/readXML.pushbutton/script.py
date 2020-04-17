import bs4, clr, math
from bs4 import BeautifulSoup
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform, Line, Transaction, \
    GeometryCreationUtilities, CurveLoop, Arc, Plane, Line, Frame, CurveLoop, DirectShapeLibrary, DirectShape, DirectShapeType
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Plumbing import Pipe, FlexPipe
from Autodesk.Revit.DB.Mechanical import Duct, FlexDuct
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


def CreateStraightDuct(csdname, csdwidth, csdheight, csdstart, csdend, csdlength):
    print(csdname)
    print(csdlength)
    pp = Plane.CreateByNormalAndOrigin(csdend-csdstart, csdstart)
    profile1 = Arc.Create(pp, csdwidth/2, 0, math.pi)
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
    profile2 = Arc.Create(pp, csdheight/2, math.pi/2, math.pi*3/2)
    c = profile2.GetEndPoint(0)
    d = profile2.GetEndPoint(1)
    point1 = a+c - csdstart
    point2 = b+c - csdstart
    point3 = b+d - csdstart
    point4 = a+d - csdstart
    l1 = Line.CreateBound(point1, point2)
    #print(point4)
    profileorigion = CurveLoop().Create(
        [Line.CreateBound(point1, point2), Line.CreateBound(point2, point3), Line.CreateBound(point3, point4),
         Line.CreateBound(point4, point1)])
    print(l1.GetEndPoint(0))
    print(l1.GetEndPoint(1))

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
    DirectShape.CreateElement(doc, ElementId(-2000151)).SetShape([geo])
# t = Transaction(doc, 'Add CLash Points')
# t.Start()
# CreateStraightDuct(4 ,6, XYZ(0,0,0), XYZ(3, 3, 3))
# t.Commit()

def CreateCurveDuct(name, width, height, start, end, middle):
    print(name)
    print(start)
    print(end)
    print(middle)
    if start.X == end.X and start.Y == end.Y and start.Z == end.Z:
        print("Curve error, start is the same as end")
    else:
        path = Arc.Create(start, end, middle)
        print(path.Center)
        pathCurve = CurveLoop().Create([path])
        pp = Plane.CreateByNormalAndOrigin(path.ComputeDerivatives(0, True).BasisX, start)
        profile1 = Arc.Create(pp, width/2, 0, math.pi)
        a = profile1.GetEndPoint(0)

        vector1 = a-start
        vector2 = XYZ((a-start).X, (a-start).Y, 0)
        angle = vector2.AngleTo(vector1)
        print(angle)
        trans1 = Transform.CreateRotationAtPoint(path.ComputeDerivatives(0, True).BasisX, angle, start)
        trans2 = Transform.CreateRotationAtPoint(path.ComputeDerivatives(0, True).BasisX, angle * (-1), start)
        trans3 = Transform.CreateRotationAtPoint(path.ComputeDerivatives(0, True).BasisX, angle * (-1) + math.pi / 2, start)
        trans4 = Transform.CreateRotationAtPoint(path.ComputeDerivatives(0, True).BasisX, angle + math.pi / 2, start)
        b = profile1.GetEndPoint(1)
        profile2 = Arc.Create(pp, height/2, math.pi/2, math.pi*3/2)
        c = profile2.GetEndPoint(0)
        d = profile2.GetEndPoint(1)
        point1 = a+c-start
        point2 = b+c-start
        point3 = b+d-start
        point4 = a+d-start
        print(point1)
        print(point2)
        print(point3)
        print(point4)
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
        print(profile.IsOpen())
        print(profile.IsRectangular(pp))

        geo = GeometryCreationUtilities.CreateSweptGeometry(pathCurve, 0, path.GetEndParameter(0), [profile])
        DirectShape.CreateElement(doc, ElementId(-2000151)).SetShape([geo])




def CreateStraightPipe(name, diameter, start, end, length):
    print(name)
    print(length)
    pp = Plane.CreateByNormalAndOrigin(end-start, start)
    profile = CurveLoop().Create([Arc.Create(pp, diameter/2, 0 , math.pi),Arc.Create(pp, diameter/2, math.pi , math.pi*2)])
    geo = GeometryCreationUtilities.CreateExtrusionGeometry([profile], end-start, length)
    DirectShape.CreateElement(doc, ElementId(-2000151)).SetShape([geo])
    #print(Arc.Create(pp, diameter, math.pi , math.pi*2).ComputeDerivatives(0.5, True).BasisX)
    #print(Arc.Create(pp, diameter, math.pi, math.pi * 2).ComputeDerivatives(0.5, True).BasisY)
    #print(Arc.Create(pp, diameter, math.pi, math.pi * 2).ComputeDerivatives(0.5, True).BasisZ)

def CreateCurvePipe(name, diameter, start, end, middle):
    print(name)
    print(start)
    print(end)
    print(middle)
    path = Arc.Create(start, end, middle)
    pathCurve = CurveLoop().Create([path])
    pp = Plane.CreateByNormalAndOrigin(path.ComputeDerivatives(0, True).BasisX, start)
    profile = CurveLoop().Create([Arc.Create(pp, diameter/2, 0, math.pi),Arc.Create(pp, diameter/2, math.pi , math.pi*2)])
    geo = GeometryCreationUtilities.CreateSweptGeometry(pathCurve, 0, path.GetEndParameter(0), [profile])
    DirectShape.CreateElement(doc, ElementId(-2000151)).SetShape([geo])

def Number(n):
    if n[-1] == ".":
        return float(float(n[0:-1])/12)
    else:
        return float(n)


'''
t = Transaction(doc, 'Add CLash Points')
t.Start()
start = XYZ(0, 0, 0)
middle = XYZ(10, 1, 0)
end = XYZ(14, 0, 0)
CreateCurvePipe(1, start, end, middle)
# CreateStraightPipe(5, start, end)
t.Commit()
'''

# Documentation of work
points = {}
file = "C:\\Users\\mengf\\Desktop\\C1152UUMST02C19.xml"
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
            x = float(Number(s.find("center").text.split(" ")[1]))-6427300
            z = float(Number(s.find("invert").attrs['elev'] + str("0")))-300
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
        t = Transaction(doc, 'Add CLash Points')
        t.Start()
        # Straight Pipe and Duct Creation
        if not a.find("center"):
            if a.find("circpipe"):
                cirdiameter = Number(a.find("circpipe").attrs['diameter']) + float(str(a.find("circpipe").attrs['thickness']) + "0") * 2
                systemId = ElementId(607132)
                pipeTypeId = ElementId(150706)
                levelId = ElementId(30)
                cirlength = Number(a.attrs['length'])
                cirname = a.attrs['name']
                cirstartPoint = points[a.attrs['refstart']]
                cirendPoint = points[a.attrs['refend']]
                #try:
                CreateStraightPipe(cirname, cirdiameter, cirstartPoint, cirendPoint, cirlength)
                    #centerLine = Line.CreateBound(startPoint, endPoint)
                    # Pipe.Create(doc, systemId, pipeTypeId, levelId, startPoint, endPoint)
                    # print('successful')
                #except:
                 #   print("fail straight pipe")
                n += 1
            elif a.find("rectpipe"):
                recwidth = float(str(a.find("rectpipe").attrs['width']) + "0") + float(
                    str(a.find("rectpipe").attrs['thickness']) + "0") * 2
                recheight = float(str(a.find("rectpipe").attrs['height']) + "0") + float(
                    str(a.find("rectpipe").attrs['thickness']) + "0") * 2
                reclength = float(a.attrs['length'])
                systemId = ElementId(607128)
                ductTypeId = ElementId(139191)
                levelId = ElementId(30)
                recName = a.attrs['name']
                recstartPoint = points[a.attrs['refstart']]
                recendPoint = points[a.attrs['refend']]
                try:
                    CreateStraightDuct(recName, recwidth, recheight, recstartPoint, recendPoint, reclength)
                    #Duct.Create(doc, systemId, ductTypeId, levelId, startPoint, endPoint)
                    #GeometryCreationUtilities.CreateSweptGeometry.

                except:
                    print("fail straight duct")
                # flex duck and flex pipe
                n += 1


        else:
            if a.find("circpipe"):
                diameter = Number(a.find("circpipe").attrs['diameter']) + float(str(a.find("circpipe").attrs['thickness']) + "0") * 2
                midNumberY = float(a.find("center").text.split(" ")[0])-1844100
                midNumberX = float(a.find("center").text.split(" ")[1])-6427300
                startPoint = points[a.attrs['refstart']]
                endPoint = points[a.attrs['refend']]
                midNumberZ = (startPoint.Z + endPoint.Z)/2
                midPoint = XYZ(midNumberX, midNumberY, midNumberZ)
                name = a.attrs['name']
                # Pipe information
                systemId = ElementId(607132)
                typeId = ElementId(150707)
                levelId = ElementId(30)
                pipeSystemId = ElementId(607132)
                pipeTypeId = ElementId(150706)

                #try:
                    # centerLine = Line.CreateBound(startPoint, endPoint)
                CreateCurvePipe(name, diameter, startPoint, endPoint, midPoint)
                # CreateStraightPipe(diameter, startPoint, endPoint)
                #except:
                   #print("fail flex pipe")

            elif a.find("rectpipe"):
                width = float(str(a.find("rectpipe").attrs['width']) + "0") + float(str(a.find("rectpipe").attrs['thickness']) + "0") * 2
                height = float(str(a.find("rectpipe").attrs['height']) + "0") + float(str(a.find("rectpipe").attrs['thickness']) + "0") * 2
                name = a.attrs['name']
                midNumberY = float(a.find("center").text.split(" ")[0])-1844100
                midNumberX = float(a.find("center").text.split(" ")[1])-6427300
                startPoint = points[a.attrs['refstart']]
                endPoint = points[a.attrs['refend']]
                midNumberZ = (startPoint.Z + endPoint.Z)/2
                midPoint = XYZ(midNumberX, midNumberY, midNumberZ)

                systemId = ElementId(607128)
                typeId = ElementId(139193)
                levelId = ElementId(30)


                ductSystemId = ElementId(607128)
                ductTypeId = ElementId(139191)
                #try:
                CreateCurveDuct(name, width, height, startPoint, endPoint, midPoint)
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

