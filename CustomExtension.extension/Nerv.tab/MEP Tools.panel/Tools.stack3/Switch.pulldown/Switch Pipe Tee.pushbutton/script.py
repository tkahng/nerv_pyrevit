import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import Document, FilteredElementCollector, PerformanceAdviser, FamilySymbol,BuiltInCategory, \
    MEPCurveType, RoutingPreferenceRuleGroupType, RoutingConditions, RoutingPreferenceErrorLevel, RoutingPreferenceRule,\
    PreferredJunctionType,Transaction, BuiltInParameter
from Autodesk.Revit.DB.Plumbing import PipeType
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit.framework import List
from pyrevit import revit, DB
import os
from collections import defaultdict
from pyrevit import script
from pyrevit import forms
__doc__ = 'Switch Tee Preference of selected Pipe'\
          'You can either select the pipe you want to switch ' \
          'or pick from list'
def CheckSelection(doc):
    selection = [doc.GetElement(id)
            for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]

    if len(selection) > 0:
        el = selection[0]
        if el.Category.Name == 'Pipes':
            sel = el.PipeType
        else:
            sel = None
    else:
        sel = None
    return sel

def PipeSelect(doc):
    namesLst = []
    pipedic = {}
    family = FilteredElementCollector(doc).OfClass(MEPCurveType).ToElements()
    for i in family:
        type = i.Category.Name
        if str(type) == 'Pipes':
            namesLst.append(i.LookupParameter('Type Name').AsString())
            pipedic[i.LookupParameter('Type Name').AsString()] = i
    sel_pipe = forms.SelectFromList.show(namesLst, button_name='Select Item',
                                            multiselect=False)
    return pipedic[sel_pipe]
'''
def ChangePreference(pipeType):
    PipeType.Elbow = None
    PipeType.Tee = None
    PipeType.Tap = None
    PipeType.Transition = None
    PipeType.Union = None
'''
def FindPipeFittings(doc, ComponentClass):
    fittings = []
    fitting = {}
    fittingNames = []
    families = FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()
    for i in families:
        if i.Family.FamilyCategory.Name == 'Pipe Fittings':
            if not i in fittings:
                fittings.append(i)
    for i in fittings:
        if str(i.get_Parameter(BuiltInParameter.RBS_COMPONENT_CLASSIFICATION_PARAM).AsValueString()) == ComponentClass:
            fitting[i.Family.Name + ' ' + i.LookupParameter('Type Name').AsString()] = i
            fittingNames.append(i.Family.Name + ' ' + i.LookupParameter('Type Name').AsString())
    sel_pipe = forms.SelectFromList.show(fittingNames, button_name='Select Item',multiselect=False)
    return fitting[sel_pipe].Id

def SetTee(pipeType, ElementId):
    pipeType.get_Parameter(BuiltInParameter.RBS_CURVETYPE_DEFAULT_TEE_PARAM).Set(ElementId)



t = Transaction(doc, 'Switching Tee')
t.Start()
if not CheckSelection(doc) is None:
    type = CheckSelection(doc)
else:
    type = PipeSelect(doc)
fitting = FindPipeFittings(doc, 'Tee')
SetTee(type, fitting)
t.Commit()
