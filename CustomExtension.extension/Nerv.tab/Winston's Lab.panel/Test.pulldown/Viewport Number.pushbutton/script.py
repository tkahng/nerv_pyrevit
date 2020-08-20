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
import System.Threading
import System.Threading.Tasks
from Autodesk.Revit.DB import Document, FilteredElementCollector, PerformanceAdviser, Family, Transaction,\
    FailureHandlingOptions, CurveElement, BuiltInCategory, ElementId, SpatialElementTag, RevitLinkInstance, \
    RevitLinkType, View, BoundingBoxXYZ, BuiltInParameter, ViewSet, ViewSheetSet, PrintRange, ViewSheet
import re
from Autodesk.Revit.DB import Level, BuiltInParameter, WorksetTable, Element
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
from Autodesk.Revit.UI.Selection import Selection

n = 0
sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).ToElements()
for sheet in sheets:
    viewports = sheet.GetAllViewports()
    n = n + len(viewports)
print(n)

'''
viewsId = []
sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).ToElements()
for sheet in sheets:
    viewId = sheet.GetAllPlacedViews()
    for v in viewId:
        viewId = v.ToString()
        if not viewId in viewsId:
            viewsId.append(viewId)

#print(viewsId)

toDelete = [3133, 3143]

n = 0
for t in toDelete:
    if str(t) in viewsId:
        print(t)
        n = 1
if n == 1:
    print("There is something wrong!!!")
elif n == 0:
    print("They can be deleted.")


# Delete all unused views beside parent views, primary views and view template

# List created to contain all views ElementIds
vElementIds = []
tempIds = []
pvElementIds = []
# Get all the views
views = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).ToElements()
# Divide the views into different groups
for view in views:
    dependency = view.LookupParameter("Dependency")
    pView = view.LookupParameter("Parent View")
    if view.IsTemplate:
        print("Template - " + view.ViewName)
    else:
        if dependency.AsString() == "Primary":
            print("Primary - " + view.ViewName)
        elif pView != None:
            parentId = pView.AsElementId()
            pvElementIds.append(parentId)
            tempIds.append(view.Id)
        else:
            tempIds.append(view.Id)
for t in tempIds:
    if t in pvElementIds:
        pass
    else:
        vElementIds.append(t)
#print(tempIds)
#print(pvElementIds)
#print(vElementIds)

#print(vElementIds)
print("-----------------------------")
#print(n)
#print("-----------------------------")

vpElementIds = []
viewports = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Viewports).ToElements()
for viewport in viewports:
    vpElementIds.append(viewport.ViewId)

delete = []
for v in vElementIds:
    if v in vpElementIds:
        pass
    else:
        delete.append(v)
        vName = doc.GetElement(v).Name
        #print(vName)
        #print("-----------------------------")

fDelete = delete[:200]
#for f in fDelete:
    #print(f)


t = Transaction(doc, 'Delete Unused Views')
t.Start()
e = 0
print("The following views are not deleted:")
for d in fDelete:
    try:
        doc.Delete(d)
        e += 1
    except:
        print(d)
print("-----------------------------")
print(str(e) + " views have been deleted.")
t.Commit()
'''
