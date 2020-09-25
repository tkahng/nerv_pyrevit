import clr, xlsxwriter, re
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import Document,FilteredElementCollector, PerformanceAdviser, FamilySymbol
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

__doc__ = 'Print performance issues, advices and instances counts.'

text = []
def PerformanceCollector(doc):
    out = []
    all = []
    pTypes = PerformanceAdviser.GetPerformanceAdviser().GetAllRuleIds()
    failureMessages = PerformanceAdviser.GetPerformanceAdviser().ExecuteRules(doc, pTypes)
    print('Below are all performance adviser categories: ' + str(len(failureMessages)))
    for i in failureMessages:
        all.append(i.GetDescriptionText())
        if not str(i.GetDescriptionText()) in text:
            text.append(i.GetDescriptionText())
    for t in text:
        print(t + '--------' + str(all.count(t)) + ' Instances in model.')
    return out

PerformanceCollector(doc)




