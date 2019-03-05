import clr, re
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
import ConfigParser
from os.path import expanduser
# Get current date


clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
outprint = script.get_output()
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
home = expanduser("~")
cfgfile = open(home + "\\STVTools.ini")
Config = ConfigParser.ConfigParser()
Config.read(home + "\\STVTools.ini")
filePath = ConfigSectionMap("NavisFilePath")["datapath"]
print(filePath)

openedFile = open(filePath)

def PAFileNameProcessor(doc):
    fName = doc.Title
    fileType = ".rvt"
    modelRegex = re.compile(r'\w\d\d\d\d\d\d\d\d-\S\S_CENTRAL')
    modelRegex2 = re.compile(r'\w\d\d\d\d\d\d\d\d-\S\S_CENTRAL_\w?\w?\w')
    approvedTail = ['ENC', 'FFE', 'GEN', 'INT', 'SSM', 'C', 'CP', 'PBB', ]
    noTail = modelRegex.findall(fName)
    tail = modelRegex2.findall(fName)
    if len(tail) == 0:
        name = fName[0: 20] + fileType
    else:
        nameLst = re.split('_', fName)
        if nameLst[2] in approvedTail:
            name = tail[0] + fileType
        else:
            name = fName[0: 20] + fileType
    return name
name = PAFileNameProcessor(doc)
print(name)
content = openedFile.readlines()
content.reverse()
i = []
for c in content:
    portions = re.split(";", c)
    itemDate = portions[0]
    itemTime = portions[1]
i = content[0]
portions = re.split(";", i)
itemDate = portions[0]
itemTime = portions[1]
rawId = portions[2]
rawModel = portions[3]
comment = portions[4]
id = re.split(':', rawId)[2]
model = re.split(':',rawModel)[2]
if name == model[0:len(model) - 1]:
    element = doc.GetElement(ElementId(int(id[0:len(id)-1])))
    try:
        currentid = format(outprint.linkify(element.Id))
    except:
        currentid = id[0:len(id)-1]
    print(itemTime + '      ' + currentid + '      ' + comment)
else:
    print('Latest Item is not in your model')
# TODO: Show Latest Time Stamp
# TODO: Group based on time Stamp
# TODO:Skip print just select and zoom