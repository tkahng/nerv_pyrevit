import clr, re
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform, Transaction,FamilySymbol, \
    ElementId, FilteredElementCollector, Structure
from System.Collections.Generic import List
from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.DB import *
from Autodesk.Revit.Creation import *
from pyrevit import script, DB, revit
from pyrevit import forms
import pyrevit
import ConfigParser
from os.path import expanduser
# Get current date

__doc__ = 'Show Latestet recorded items in Navisworks'

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

# Program Start Process Files
home = expanduser("~")
cfgfile = open(home + "\\STVTools.ini")
Config = ConfigParser.ConfigParser()
Config.read(home + "\\STVTools.ini")
filePath = ConfigSectionMap("NavisFilePath")["datapath"]
openedFile = open(filePath)
name = PAFileNameProcessor(doc)
content = openedFile.readlines()
content.reverse()
lastId = ()
selection = []

# Top Item Model Name
topItem = re.split(";", content[0])
topGrouping = topItem[6]
topModel = re.split(':', topItem[3])[2]
topModelName = topModel[0 : len(topModel) - 1]

# Selection portion
if topModelName != name:
    TaskDialog.Show('Error', 'Latest Item is not in your model')
else:
    # Split the line content
    for i in content:
        portions = re.split(";", i)
        rawId = portions[2]
        rawModel = portions[3]
        grouping = portions[6]
        id = re.split(':', rawId)[2]
        model = re.split(':', rawModel)[2]
        if name == model[0:len(model) - 1]:
            if grouping == topGrouping:
                element = doc.GetElement(ElementId(int(id[0:len(id)-1])))
                selection.append(element)
            else:
                break
        else:
            break
    revit.get_selection().set_to(selection)
