import clr, sys, re, os, imp
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Structure
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform, Transaction,FamilySymbol,ElementId
from System.Collections.Generic import List
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
from Autodesk.Revit.Creation import *
from pyrevit import script, DB, revit
from pyrevit import forms
import pyrevit
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
outprint = script.get_output()
path = r'\\stvgroup.stvinc.com\v3\DGPA\Vol3\Projects\3019262\3019262_0001\90_CAD Models and Sheets\17017000\_PIM\Data\NavisData'
filePath = forms.pick_file(file_ext='txt', multi_file=False, init_dir=path, unc_paths=False)

openedFile = open(filePath)
content = openedFile.readlines()
for i in content:
    portions = re.split(";", i)
    rawId = portions[0]
    rawModel = portions[1]
    comment = portions[2]
    id = re.split(':', rawId)[2]
    model = re.split(':',rawModel)[2]

    element = doc.GetElement(ElementId(int(id[0:len(id)-1])))

    try:
        currentid = format(outprint.linkify(element.Id))
    except:
        currentid = id[0:len(id)-1]
    print(currentid + '      ' + model[0:len(model)-1] + '       ' + comment)
