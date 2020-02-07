
import sys, clr
import ConfigParser
from os.path import expanduser
# Set system path
home = expanduser("~")
cfgfile = open(home + "\\STVTools.ini", 'r')
config = ConfigParser.ConfigParser()
config.read(home + "\\STVTools.ini")
# Master Path
syspath1 = config.get('SysDir','MasterPackage')
sys.path.append(syspath1)
# Built Path
syspath2 = config.get('SysDir','SecondaryPackage')
sys.path.append(syspath2)

import System, Selection
import System.Threading, System.Threading.Tasks
from Autodesk.Revit.DB import Document, FilteredElementCollector, GraphicsStyle
from Autodesk.Revit.DB import Level, BuiltInParameter
from Autodesk.Revit.UI import TaskDialog
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows.Forms
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit.framework import List
from pyrevit import revit, DB
import os
from collections import defaultdict
from pyrevit import script
from pyrevit import forms
from Autodesk.Revit.UI import TaskDialog, UIApplication
'''
LinkObj = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
LinkTyp = FilteredElementCollector(doc).OfClass(RevitLinkType).ToElements()
modelLst = []
count = 0
for a in LinkObj:
    line = []
    print(a.Name)
    '''
'''
from os.path import expanduser
home = expanduser("~")
print(home)
print(doc.Title)

uiapp = UIApplication(doc.Application)
application = uiapp.Application
versionName = application.VersionName
print(versionName)
viewports = FilteredElementCollector(doc).OfClass(View).ToElements()
for v in viewports:
    print v.Name
'''

gStyle = FilteredElementCollector(doc).OfClass(GraphicsStyle).ToElements()
collection = []
for g in gStyle:
    list = []
    workSet = g.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM).AsValueString()
    if workSet == "Object Styles":
        if g.GraphicsStyleCategory.Parent:
            print(g.GraphicsStyleCategory.Parent.Name.ToString())
        else:
            print("None")
        # print(workSet + " " + g.Name + " " + g.GraphicsStyleType.ToString() + " " +
        #      g.GraphicsStyleCategory.Parent.Name.ToString() + " " + g.GraphicsStyleCategory.GetLineWeight(g.GraphicsStyleType).ToString() + " " + g.GraphicsStyleCategory.GetLinePatternId(g.GraphicsStyleType).ToString()
         #     )

    '''
    params = Selection.get_all_parameters_as_dic(g).keys()
    values = Selection.get_all_parameters_as_dic(g).values()
    count = 0
    for i in params:
        list.append(i)# + ' : ' + values[count])
        count += 1
    collection.append(list)
for i in collection:
    print('----------------------')
    for a in i:
        print(a)
        '''

