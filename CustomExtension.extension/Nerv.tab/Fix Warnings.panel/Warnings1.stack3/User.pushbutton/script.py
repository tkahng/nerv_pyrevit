
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
from Autodesk.Revit.ApplicationServices import Application
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


__doc__ = 'Print user names in model and Warnings based on the selection of username.'

outprint = script.get_output()
output = pyrevit.output.get_output()
tab = ' '
user = Application.Username
# input ---------------------
cate = []
path = 'C:\\Users\\loum\\Documents\\Pyscripts\\ClashScripts\\'
if revit.doc.IsWorkshared:
    warnings = doc.GetWarnings()
    count = 1
    warningRange = 0

    for i in warnings:
        id = i.GetFailingElements()
        for i in id:
            wti = DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc, i)
            owner = wti.Owner
            creator = wti.Creator
            if not owner in cate:
                cate.append(owner)
            if not creator in cate:
                cate.append(creator)
    # Select Warnings you want to print
    try:
        sel_warning = forms.SelectFromList.show(cate, button_name='Select Item',
                                                multiselect=False,
                                                name_attr='Name',)
    except:
        sel_warning = forms.SelectFromList.show(cate, title='Select Item',
                                                multiselect=False,)
    print('Below are all users in the model: ')
    print(cate)
    print('Below are selected user and warnings under his or her name: ')
    print(sel_warning)
    # Printing selected warnings
    for warning in warnings:
        elementId = warning.GetFailingElements()
        additionalId = warning.GetAdditionalElements()
        text = warning.GetDescriptionText()
        names = []
        for e in elementId:
            wti = DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc, e)
            creator = wti.Creator
            changedBy = wti.LastChangedBy
            names.append(creator)
            names.append(changedBy)
        for a in additionalId:
            awti = DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc, a)
            aCreator = awti.Creator
            aChangedBy = awti.LastChangedBy
            names.append(aCreator)
            names.append(aChangedBy)
        # print(names)
        if sel_warning[0] in names or sel_warning in names:
            output.print_md("**#** {}-----------------\n\n"
                            "- Warning Item:{}\n\n"
                            .format(count,
                                    text))
            for e in elementId:
                wti = DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc, e)
                creator = wti.Creator
                changedBy = wti.LastChangedBy
                print(tab + format(outprint.linkify(e)) + tab + 'Creator: ' + creator + tab +
                        'Last Changed by: ' + changedBy)
            for a in additionalId:
                awti = DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc, a)
                aCreator = awti.Creator
                aChangedBy = awti.LastChangedBy
                print(tab + format(outprint.linkify(a)) + tab + 'Creator: ' + aCreator + tab +
                        'Last Changed by: ' + aChangedBy)
            count += 1
        warningRange += 1
