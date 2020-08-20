import bs4, clr, math
from bs4 import BeautifulSoup
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform, Line, Transaction, \
    GeometryCreationUtilities, CurveLoop, Arc, Plane, Line, Frame, CurveLoop, DirectShapeLibrary, DirectShape, DirectShapeType
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

def CreateCubeStrut(csdname, csdwidth, csdlength, csdheight, csdstart, csdrotation):
    print(csdname)
    vector = XYZ(0, 0, csdheight*-1)
    pp = Plane.CreateByNormalAndOrigin(vector, csdstart)

    trans = Transform.CreateRotationAtPoint(vector, csdrotation, csdstart)

    point1 = csdstart + XYZ(csdwidth/2, csdlength/2, 0)
    point2 = csdstart + XYZ(csdwidth/2* -1, csdlength/2, 0)
    point3 = csdstart + XYZ(csdwidth/2* -1, csdlength/2 * -1, 0)
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

def CreateRoundStrut(name, diameter, start, height):
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

def CreateStraightDuct(csdname, csdwidth, csdheight, thickness, csdstartO, csdendO, csdlength):
    print(csdname)
    print(csdlength)
    correction = XYZ(0, 0, csdheight / 2)
    csdstart = csdstartO + correction
    csdend = csdendO + correction
    pp = Plane.CreateByNormalAndOrigin(csdend-csdstart, csdstart)
    profile1 = Arc.Create(pp, csdwidth/2 + thickness, 0, math.pi)
    a = profile1.GetEndPoint(0)

    vector1 = a - csdstart
    vector2 = XYZ((a - csdstart).X, (a - csdstart).Y, 0)
    angle = vector2.AngleTo(vector1)
    #print(angle)
    trans1 = Transform.CreateRotationAtPoint(csdend - csdstart, angle, csdstart)
    trans2 = Transform.CreateRotationAtPoint(csdend - csdstart, angle*(-1), csdstart)
    trans3 = Transform.CreateRotationAtPoint(csdend - csdstart, angle * (-1) + math.pi/2, csdstart)
    trans4 = Transform.CreateRotationAtPoint(csdend - csdstart, angle + math.pi / 2, csdstart)
    b = profile1.GetEndPoint(1)
    profile2 = Arc.Create(pp, csdheight/2 + thickness, math.pi/2, math.pi*3/2)
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

def CreateCurveDuct(name, width, height, thickness, startO, endO, middleO):
    correction = XYZ(0, 0, height / 2)
    print(name)
    start = startO + correction
    end = endO + correction
    middle = middleO + correction
    ele = ()
    if start.X == end.X and start.Y == end.Y and start.Z == end.Z:
        print("Curve error, start is the same as end")
        return None
    else:
        path = Arc.Create(start, end, middle)
        print(name)
        print(start)
        print(end)
        print(middle)
        pathCurve = CurveLoop().Create([path])
        pp = Plane.CreateByNormalAndOrigin(path.ComputeDerivatives(0, True).BasisX, start)
        profile1 = Arc.Create(pp, width/2 + thickness, 0, math.pi)
        a = profile1.GetEndPoint(0)

        vector1 = a-start
        vector2 = XYZ((a-start).X, (a-start).Y, 0)
        angle = vector2.AngleTo(vector1)

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
    correction = XYZ(0, 0, diameter/2)
    start = startO + correction
    end = endO + correction
    print(name)
    print(length)
    pp = Plane.CreateByNormalAndOrigin(end-start, start)
    profile = CurveLoop().Create([Arc.Create(pp, diameter/2 + thickness, 0 , math.pi), Arc.Create(pp, diameter/2 + thickness, math.pi , math.pi*2)])
    geo = GeometryCreationUtilities.CreateExtrusionGeometry([profile], end-start, length)
    ele = DirectShape.CreateElement(doc, ElementId(-2000151))
    ele.SetShape([geo])
    ele.SetName(name)
    return ele.Id
    #print(Arc.Create(pp, diameter, math.pi , math.pi*2).ComputeDerivatives(0.5, True).BasisX)
    #print(Arc.Create(pp, diameter, math.pi, math.pi * 2).ComputeDerivatives(0.5, True).BasisY)
    #print(Arc.Create(pp, diameter, math.pi, math.pi * 2).ComputeDerivatives(0.5, True).BasisZ)

def CreateCurvePipe(name, diameter,thickness, startO, endO, middleO):
    correction = XYZ(0, 0, diameter / 2)
    start = startO + correction
    end = endO + correction
    middle = middleO + correction
    print(name)
    print(start)
    print(end)
    print(middle)
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

t = Transaction(doc, 'Add CLash Points')
t.Start()

#CreateStraightDuct("test", 48/12, 72/12, XYZ(6427332.2082 - 6427300, 1844136.7557-1844100, 306.927-300), XYZ(6427332.2082 - 6427300, 1844136.7557-1844100, 306.927-300-7), 7)
# Documentation of work\

points = {}
file = forms.pick_file(file_ext='xml', multi_file=False, unc_paths=False)
fileCSV = forms.pick_file(file_ext='csv', multi_file=False, unc_paths=False)
pressureCSV = forms.pick_file(file_ext='csv', multi_file=False, unc_paths=False)

wallThicknesses = {}

with open(pressureCSV, "r") as f:
    # Read each line in the file, readlines() returns a list of lines
    content = f.readlines()
    # Combine the lines in the list into a string
    for line in content:
        lineData = line.split(",")
        name = lineData[0]
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