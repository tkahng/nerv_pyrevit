from pyrevit.framework import List
from pyrevit import revit, DB
import clr, pprint,os
from collections import defaultdict
from pyrevit import script
from pyrevit import forms
import pyrevit
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform
from System.Collections.Generic import List
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


__doc__ = 'Prints out a warnings by category.'\
          ' This is helpful to resolve warnings'

outprint = script.get_output()
output = pyrevit.output.get_output()
tab = ' '
# input ---------------------
cate = []
path = 'C:\\Users\\loum\\Documents\\Pyscripts\\ClashScripts\\'
if revit.doc.IsWorkshared:
    warnings = doc.GetWarnings()
    count = 1
    warningRange = 0

    for i in warnings:
        categories = i.GetDescriptionText()
        if not categories in cate:
            cate.append(categories)
# Select Warnings you want to print
    sel_warning = forms.SelectFromList.show(cate, button_name='Select Item',
                                            multiselect=True)

    print('Below are all warning categories: ')

    print(sel_warning)
# Printing selected warnings
    for warning in warnings:
        elementId = warning.GetFailingElements()
        additionalId = warning.GetAdditionalElements()
        text = warning.GetDescriptionText()
        if text in str(sel_warning):
            output.print_md("**#** {}-----------------\n\n"
                            "- Warning Item:{}\n\n"
                            .format(count,
                                    text))
            for e in elementId:
                wti = DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc, e)
                owner = wti.Owner
                creator = wti.Creator
                changedBy = wti.LastChangedBy
                print(tab + format(outprint.linkify(e)) + tab + 'Creator: ' + creator + tab +
                      'Last Changed by: ' + changedBy)
            for a in additionalId:
                awti = DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc, a)
                aOwner = awti.Owner
                aCreator = awti.Creator
                aChangedBy = awti.LastChangedBy
                print(tab + format(outprint.linkify(a)) + tab + 'Creator: ' + aCreator + tab +
                        'Last Changed by: ' + aChangedBy)
            count += 1
        warningRange += 1