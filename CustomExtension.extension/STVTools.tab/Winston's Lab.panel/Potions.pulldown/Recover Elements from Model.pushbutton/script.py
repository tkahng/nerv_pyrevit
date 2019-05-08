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
    FailureHandlingOptions, CurveElement, ElementTransformUtils, BuiltInCategory, Transform, CopyPasteOptions, Viewport
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
    viewports = FilteredElementCollector(doc).OfClass(Viewport).ToElements()
    for i in viewports:
        name = i.LookupParameter('View Name').AsString()
        modelDic[name] = i
    return modelDic

# Open Recover doc in back ground
uiapp = UIApplication(doc.Application)
application = uiapp.Application
collectorFile = forms.pick_file(file_ext='rvt', multi_file=False, unc_paths=False)

recoverdoc = FileUtilities.OpenFileCloseWorksets(collectorFile, application, audit = False)
recoverviews = Views_name_Id_Collector(recoverdoc)
recoverViewName = forms.SelectFromList.show(recoverviews.keys(), button_name='Source View ',
                                        multiselect= True)

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
    elements = FilteredElementCollector(recoverdoc, recoverview.ViewId).OfCategory(BuiltInCategory.OST_DoorTags).ToElementIds()
    if elements:
        trans = None
        op = CopyPasteOptions()
        ElementTransformUtils.CopyElements(recoverdoc.GetElement(recoverview.ViewId), elements, doc.GetElement(desview.ViewId), trans, op)
    else:
        print(i +' view does not have door tags')
recoverdoc.Close()
t.Commit()

