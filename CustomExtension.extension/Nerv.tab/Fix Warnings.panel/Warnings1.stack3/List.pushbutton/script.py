# -*- coding: utf-8 -*-

from pyrevit import revit, DB
import clr
from pyrevit import script
from pyrevit import forms
import pyrevit
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


__doc__ = 'Prints out warnings by category with Element Id.'\
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
        # decode utf-8 to ascii
        text = i.GetDescriptionText()# .decode().encode('utf-8')
        udata = text# .decode("utf-8")
        categories = udata.encode("ascii", "ignore")
        if not categories in cate:
            cate.append(categories)
# Select Warnings you want to print
    sel_warning = forms.SelectFromList.show(cate,
                                            multiselect=True,
                                            button_name='Select Item')


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