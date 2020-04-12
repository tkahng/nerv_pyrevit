import clr
import imp
import os
import re
import sys
from pyrevit import revit, DB
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import Structure
from Autodesk.Revit.DB import ElementId, XYZ, Transform, Transaction,FamilySymbol
from pyrevit import script
from pyrevit import forms
import pyrevit
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


# Get the right point data from the right direcory
fName = doc.Title
modelRegex = re.compile(r'\w\d\d\d\d\d\d\d\d-\S\S_CENTRAL')
modelRegex2 = re.compile(r'\w\d\d\d\d\d\d\d\d-\S\S_CENTRAL_\w?\w?\w')
approvedTail = ['ENC', 'FFE', 'GEN', 'INT', 'SSM', 'C', 'CP', 'PBB', ]
noTail = modelRegex.findall(fName)
tail = modelRegex2.findall(fName)
if len(tail) == 0:
    systemExtra = '\\\\stvgroup.stvinc.com\\v3\\DGPA\\Vol3\\Projects\\3019262\\3019262_0001\\90_CAD Models and Sheets\\17017000\\_PIM\\PointData\\' + fName[0: 20]
    sys.path.append(systemExtra)
    print(systemExtra)
else:
    nameLst = re.split('_', fName)
    if nameLst[2] in approvedTail:
        systemExtra = '\\\\stvgroup.stvinc.com\\v3\\DGPA\\Vol3\\Projects\\3019262\\3019262_0001\\90_CAD Models and Sheets\\17017000\\_PIM\\PointData\\' + tail[0]
        sys.path.append(systemExtra)
        print(systemExtra)
    else:
        systemExtra = '\\\\stvgroup.stvinc.com\\v3\\DGPA\\Vol3\\Projects\\3019262\\3019262_0001\\90_CAD Models and Sheets\\17017000\\_PIM\\PointData\\' + fName[0: 20]
        sys.path.append(systemExtra)

__doc__ = 'Create a red orb on existing Clashes, have to read off a file pre-prepared by STV BIM using the Read Clash Tool'

# clash files
clashFiles = []
for file in os.listdir(systemExtra):
    if file.endswith(".py"):
        # print(os.path.join(clashpath, file))
        __import__(file[:-3], locals(), globals())
        clashFiles.append(file)
sel_clash = forms.SelectFromList.show(clashFiles, button_name='Select Item',
                                        multiselect=True)
# Be sure to import the right one as in all point data files are named the same.


# input ---------------------

ew = doc.ActiveProjectLocation.GetProjectPosition(XYZ(0,0,0)).EastWest * float(-1.0)
ns = doc.ActiveProjectLocation.GetProjectPosition(XYZ(0,0,0)).NorthSouth * float(-1.0)
elevation = doc.ActiveProjectLocation.GetProjectPosition(XYZ(0,0,0)).Elevation * float(-1.0)
angle = doc.ActiveProjectLocation.GetProjectPosition(XYZ(0,0,0)).Angle * float(-1.0)
rotationTransform = Transform.CreateRotation(XYZ.BasisZ, angle)
translationVector = XYZ(ew,ns,elevation)
translationTransform = Transform.CreateTranslation(translationVector)
finalTransform = translationTransform.Multiply(rotationTransform)
count = 0
outLst = []
# Just to be sure how many points will be created and each list are the same length

tab = '     '
outprint = script.get_output()
output = pyrevit.output.get_output()
# Transaction Start
t = Transaction(doc, 'Add CLash Points')

# Clash point Calculation
FSymbol = DB.FilteredElementCollector(doc) \
    .OfClass(clr.GetClrType(FamilySymbol)) \
    .ToElements()

selSet = []
for a in sel_clash:
    Pointdata = imp.load_source('a', systemExtra + '\\' + a)  # type: object
    print('-----------------------------------------------------------------')
    print('Here are all the clashes between ' + a[0: len(a) - 3])
    clashPoint = ()
    for i in FSymbol:
        if i.Family.Name == 'Site-Generic-Clashpoint':
            clashPoint = i
    if not clashPoint:
        print('Please Load the Clash Point Family')
    else:
        t.Start()
        print('Using Clash Point Family: ' + clashPoint.Family.Name)
        count = 0
        elements = []
        for el in Pointdata.pointX:
            x = float(Pointdata.pointX[count]) + ew
            y = float(Pointdata.pointY[count]) + ns
            z = float(Pointdata.pointZ[count]) + elevation
            pnt = XYZ(x,y,z)
            bPnt = Transform.CreateRotation(XYZ.BasisZ, angle).OfPoint(pnt)


            # Clash point creation
            boxes = doc.Create.NewFamilyInstance(bPnt, clashPoint, Structure.StructuralType.NonStructural)
            elements.append(boxes)

            boxes.LookupParameter('Clash Number').Set(str(count + 1))
            boxes.LookupParameter('Clash ID').Set(Pointdata.clashName[count])
            boxes.LookupParameter('Clash with ID').Set(Pointdata.clashwithID[count])
            boxes.LookupParameter('Clash With Model').Set(str(Pointdata.otherFile[count]))
            # boxes.LookupParameter('Clash Number').Set(str(count))
            count += 1
        t.Commit()


        secondCount = 0
        for el in elements:
            selSet.append(el.Id)
            idLen = len(Pointdata.clashName[secondCount])
            elId = Pointdata.clashName[secondCount][2: idLen - 2]
            idElement = ElementId(int(elId))
            print ('Clash No. ' + str(secondCount + 1) + tab + 'Clash Point: ' + format(outprint.linkify(el.Id)) + tab +
                   'Clash Item: ' + format(outprint.linkify(idElement)))
            secondCount += 1

revit.get_selection().set_to(selSet)

# TODO: Select clashes to view in different colors look into select workset color change.

