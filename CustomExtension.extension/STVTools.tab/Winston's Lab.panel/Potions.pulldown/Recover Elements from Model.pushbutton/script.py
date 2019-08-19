import sys
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

import System, Selection, FileUtilities
import System.Threading
import System.Threading.Tasks
from Autodesk.Revit.DB import Document,FilteredElementCollector, PerformanceAdviser, FamilySymbol,Transaction,\
    FailureHandlingOptions, CurveElement, ElementTransformUtils, BuiltInCategory, Transform, CopyPasteOptions, ViewPlan
from Autodesk.Revit.UI import TaskDialog
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit.framework import List
from pyrevit import revit, DB
import os
from Autodesk.Revit.UI import UIApplication
from collections import defaultdict
from pyrevit import script
from pyrevit import forms

def Views_name_Id_Collector(doc):
    modelDic = {}
    viewports = FilteredElementCollector(doc).OfClass(ViewPlan).ToElements()
    for i in viewports:
        name = i.Title.decode().encode('utf-8')
        if name:
            modelDic[name] = i
        else:
            pass
    return modelDic

appDocs = {}
for d in doc.Application.Documents:
    appDocs[d.Title] = d
recoverdocName = forms.SelectFromList.show(appDocs.keys(), button_name='Source Doc ', multiselect= False)
recoverdoc = appDocs[recoverdocName]
recoverviews = Views_name_Id_Collector(recoverdoc)
recoverViewName = forms.SelectFromList.show(recoverviews.keys(), button_name='Source View ', multiselect= True)

views = Views_name_Id_Collector(doc)
# desViewName = forms.SelectFromList.show(views.keys(), button_name='Destination View',
                                        # multiselect= False)
# desview = views[desViewName]
t = Transaction(doc, 'Recover Elements')
t.Start()
for i in recoverViewName:
    recoverview = recoverviews[i]
    desview = views[i]
    # Collector all elements needed
    elementspool = FilteredElementCollector(recoverdoc, recoverview.Id).OfCategory(BuiltInCategory.OST_DoorTags).ToElementIds()
    elements = FilteredElementCollector(recoverdoc, recoverview.Id).OfCategory(BuiltInCategory.OST_DoorTags).ToElementIds()
    print(len(elementspool))
    count = 0
    for ele in elementspool:
        a = recoverdoc.GetElement(ele).IsOrphaned
        if a:
           elements.Remove(ele)
        else:
            pass
        count += 1
    if elements and desview:
        trans = None
        op = CopyPasteOptions()
        ElementTransformUtils.CopyElements(recoverview, elements, desview, trans, op)
    else:
        print(i.ToString() +' view does not have door tags or view not found')

# recoverdoc.Close(False)
t.Commit()

