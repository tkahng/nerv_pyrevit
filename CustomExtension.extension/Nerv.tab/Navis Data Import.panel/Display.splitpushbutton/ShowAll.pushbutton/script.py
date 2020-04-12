import clr, re, datetime
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")

from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform, Transaction,FamilySymbol,ElementId
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
from Autodesk.Revit.Creation import *
from pyrevit import script, DB, revit
from pyrevit import coreutils
from pyrevit.output import linkmaker
import ConfigParser
from os.path import expanduser

__doc__ = 'Show All recorded items in Navisworks'

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

# Open File
home = expanduser("~")
cfgfile = open(home + "\\STVTools.ini")
Config = ConfigParser.ConfigParser()
Config.read(home + "\\STVTools.ini")
filePath = ConfigSectionMap("NavisFilePath")["datapath"]
print(filePath)
openedFile = open(filePath)

# Program Start
name = PAFileNameProcessor(doc)
print(name)
content = openedFile.readlines()
content.reverse()
groupIndi = []
for i in content:
    portions = re.split(";", i)
    grouping = portions[6]
    groupIndi.append(grouping)

lastId = ()
num = 1
allId = []
# print group separation line
print('---------------------------------------')
for i in content:
    portions = re.split(";", i)
    date = portions[0]
    time = portions[1]
    rawId = portions[2]
    rawModel = portions[3]
    comment = portions[4]
    username = portions[5]
    grouping = portions[6]
    id = re.split(':', rawId)[2]
    model = re.split(':', rawModel)[2]
    # print line info
    if name == model[0:len(model) - 1]:
        if grouping != lastId:
            if len(allId) > 1:
                good = coreutils.prepare_html_str(linkmaker.make_link(allId, contents='GROUP SELECT'))
                print('Select all ' + str(len(allId)) + ' elements   ' + good + ' Group ID: ' + str(grouping))
                print('---------------------------------------')
                # print ('GROUP ' + str(num) + '---------------------------------------')
                num += 1
                allId = []
            else:
                print('---------------------------------------')
                allId = []
        element = doc.GetElement(ElementId(int(id[0:len(id)-1])))
        try:
            currentid = format(outprint.linkify(element.Id))
        except:
            currentid = id[0:len(id)-1]
        print(date + '  ' + time + '    ' + 'User: ' + username + '      ' + currentid  +'      ' + comment)
        allId.append(element.Id)
        lastId = grouping
    else:
        pass

if len(allId) > 1:

    good = coreutils.prepare_html_str(linkmaker.make_link(allId, contents='GROUP SELECT'))
    print('Select all ' + str(len(allId)) + ' elements   ' + good + ' Group ID: ' + str(lastId))
    print('---------------------------------------')
    num += 1
    allId = []
else:
    print('---------------------------------------')
    allId = []