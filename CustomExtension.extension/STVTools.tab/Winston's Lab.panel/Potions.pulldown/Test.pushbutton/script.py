from pyrevit.framework import List
from pyrevit import revit, DB
import clr, sys, re, os, imp
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
# clr.AddReference("System.Windows.Form")
import openpyxl
from Autodesk.Revit.DB import FilteredElementCollector, FilteredWorksetCollector, RevitLinkType,BuiltInParameter,\
    Workset,WorksetKind
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform, Transaction,FamilySymbol
from System.Collections.Generic import List
from pyrevit import script
from pyrevit import forms
import pyrevit
clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
from System.Windows.Forms import Application, SendKeys
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

'''
SendKeys.SendWait("%{F4}")
SendKeys.Send("{Enter}")
print('Success !')
'''
print('Get it')
worksetName = []
workset = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()
for w in workset:
    worksetName.append(w.Name[8:])

linkType = FilteredElementCollector(doc).OfClass(RevitLinkType).ToElements()
for i in linkType:
    typeWorkset = i.Parameter[BuiltInParameter.ELEM_PARTITION_PARAM].AsValueString()
    linkName = i.Parameter[BuiltInParameter.SYMBOL_NAME_PARAM].AsString()
    noTail = re.split('\.', linkName)[0]
    pieces = re.split('_', noTail)
    if len(pieces) >= 3:
        reconstruct = pieces[0] + '_' + pieces[2]
        reconstructAlt = pieces[0] + '-' + pieces[2]
    else:
        reconstruct = pieces[0]
        reconstructAlt = pieces[0]
    print(reconstruct)

    count = 0
    if not reconstruct in worksetName and reconstructAlt in worksetName:
        print(reconstruct + ' Model does not have a workset or the workset is not properly names.')
    for i in worksetName:
        if reconstruct == i or reconstructAlt == i:
           print(workset[count].Name)
        count += 1
