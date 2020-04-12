from pyrevit.framework import List
from pyrevit import revit, DB
import clr, sys, re, os, imp
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
# clr.AddReference("System.Windows.Form")

from Autodesk.Revit.DB import FilteredElementCollector, FilteredWorksetCollector, RevitLinkType,BuiltInParameter,\
    Workset,WorksetKind, RevitLinkInstance
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

__doc__ = 'Switch link workset.'

'''
SendKeys.SendWait("%{F4}")
SendKeys.Send("{Enter}")
print('Success !')
'''
def SwitchLinkWorkset(linkType, doc):
    worksetName = []
    workset = []
    all_workset = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()
    for item in all_workset:
        workset.append(item)
    for w in workset:
        worksetName.append(w.Name[8:])
    for i in linkType:
        linkTypeName = i.Parameter[BuiltInParameter.SYMBOL_NAME_PARAM].AsString()
        noTail = re.split('\.', linkTypeName)[0]
        pieces = re.split('_', noTail)
        if len(pieces) >= 3:
            reconstruct = pieces[0] + '_' + pieces[2]
            reconstructAlt = pieces[0] + '-' + pieces[2]
        else:
            reconstruct = pieces[0]
            reconstructAlt = pieces[0]
        count = 0
        if not reconstruct in worksetName and not reconstructAlt in worksetName:
            print('-------------------------------------------')
            print(reconstruct + ' Model does not have a workset or the workset is not properly named.')
            print('Creating new workset named ' + reconstruct)
            print('-------------------------------------------')
            newWorkset = Workset.Create(doc, '*LINKED '+ reconstruct)
            worksetName.append(reconstruct)
            workset.append(newWorkset)
            # TODO: if no workset created, create user Workset with proper name.
        for a in worksetName:
            if reconstruct == a or reconstructAlt == a:
                # print(workset[count].Name)
                i.Parameter[BuiltInParameter.ELEM_PARTITION_PARAM].Set(workset[count].Id.IntegerValue)
                print(reconstruct + ' changed to ' + workset[count].Name + ' Workset')
            count += 1

# Transaction Start

t = Transaction(doc, 'Reset Link Type Workset')
t.Start()
revitLinkType = FilteredElementCollector(doc).OfClass(RevitLinkType).ToElements()
revitLinkInstance = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
# SwitchLinkWorkset(revitLinkInstance)
SwitchLinkWorkset(revitLinkType, doc)
t.Commit()
