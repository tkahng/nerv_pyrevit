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
    FailureHandlingOptions, CurveElement, ElementTransformUtils, BuiltInCategory, Transform, CopyPasteOptions, ViewPlan, ViewDrafting, ImportInstance, ElementParameterFilter, FilterNumericEquals, FilterIntegerRule
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
    viewports = FilteredElementCollector(doc).OfClass(ViewDrafting).ToElements()
    for i in viewports:
        # name = unicode(i.Title, "utf-8")
        name = i.Title.decode('utf-8', 'ignore')
        if name:
            modelDic[name] = i
        else:
            pass
    return modelDic

__doc__ = 'Copy elements from the backup model to the current model'

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
    try:
        recoverview = recoverviews[i]
        desview = views[i]
        # destination = FilteredElementCollector(doc, desview.Id).OfClass(ImportInstance).ToElementIds()
        elementspool = FilteredElementCollector(recoverdoc, recoverview.Id).OfClass(ImportInstance).ToElements()
        elements = FilteredElementCollector(recoverdoc, recoverview.Id).OfClass(ImportInstance).ToElementIds()
        # print(len(elements))
        count = 0
        for ele in elementspool:
            a = ele.IsLinked
            if a:
               elements.Remove(ele.Id)
            else:
                count += 1
        if desview:
            print("found " + str(len(elements)) + " elements")
            if elements:
                trans = None
                op = CopyPasteOptions()
                ElementTransformUtils.CopyElements(recoverview, elements, desview, trans, op)
                print("copied " + i.ToString())
            else:
                print("failed State no Elements" + i.ToString())
        else:
            print("failed State view not valid" + i.ToString())
    except:
        print("failed State final script fail " + i.ToString())


# recoverdoc.Close(False)
t.Commit()

