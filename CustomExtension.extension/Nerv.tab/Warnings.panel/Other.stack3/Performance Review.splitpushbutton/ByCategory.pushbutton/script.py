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
import pyrevit

__doc__ = 'Print the Element Id of selected performance issues category.'

text = []

def PerformanceCollector(doc):
    out = []
    pTypes = PerformanceAdviser.GetPerformanceAdviser().GetAllRuleIds()
    failureMessages = PerformanceAdviser.GetPerformanceAdviser().ExecuteRules(doc, pTypes)
    for i in failureMessages:
        if not str(i.GetDescriptionText()) in text:
            text.append(i.GetDescriptionText())

    sel_warning = forms.SelectFromList.show(text, button_name='Select Item',
                                            multiselect=True)
    output = pyrevit.output.get_output()
    outprint = script.get_output()
    count = 1
    tab = ' '
    for message in failureMessages:
        elementIds = message.GetFailingElements()
        des = message.GetDescriptionText()
        if des in str(sel_warning):
            output.print_md("**#** {}-----------------\n\n"
                            "- Warning Item:{}\n\n"
                            .format(count,
                                    des))
            for elementId in elementIds:
                wti = DB.WorksharingUtils.GetWorksharingTooltipInfo(doc, elementId)
                owner = wti.Owner
                creator = wti.Creator
                changedBy = wti.LastChangedBy
                print(tab + format(outprint.linkify(elementId)) + tab + 'Creator: ' + creator + tab +
                      'Last Changed by: ' + changedBy)
        count += 1

    return out

# TODO: INFORM USER HOW MANY INSTANCES WILL BE SHOWN AND ASK HOW MANY WANT TO BE SHOWN NEXT

PerformanceCollector(doc)




