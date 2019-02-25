import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import Document, FilteredElementCollector, PerformanceAdviser, FamilySymbol,BuiltInCategory
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


def PipeSelect(doc):
    namesLst = []
    family = FilteredElementCollector(doc).OfClass(PipeType).ToElements()
    for i in family:
        namesLst.append(i.LookupParameter('Type Name').AsString())
    sel_pipe = forms.SelectFromList.show(namesLst, button_name='Select Item',
                                            multiselect=True)
    return sel_pipe
'''
def ChangePreference(pipeType):
    PipeType.Elbow = None
    PipeType.Tee = None
    PipeType.Tap = None
    PipeType.Transition = None
    PipeType.Union = None
'''
def ChangePreferenceTee(pipeType):
    fittings = []
    families = FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()
    for i in families:
        if i.Family.FamilyCategory.Name == 'Pipe Fittings':
            if not i in fittings:
                fittings.append(i)
    for i in fittings:
        print(i.Family.Name + ' ' + i.LookupParameter('Type Name').AsString())
    # sel_pipe = forms.SelectFromList.show(fittings, button_name='Select Item',
                                                 # multiselect=True)
    # pipeType.Tee =

def ChangePreferenceElbow(pipeType):

    PipeType.Elbow = None

type = PipeSelect(doc)
ChangePreferenceTee(type)

