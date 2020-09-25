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

__doc__ = 'Prints out a warnings by category.'\
          ' This is helpful to resolve warnings'

outprint = script.get_output()
output = pyrevit.output.get_output()
tab = ' '
# input ---------------------
cate = []
sel_warning = ()
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

    selection = []
# select selected warnings
    for warning in warnings:
        elementId = warning.GetFailingElements()
        additionalId = warning.GetAdditionalElements()
        text = warning.GetDescriptionText()
        if text in str(sel_warning):
            for e in elementId:
                selection.append(doc.GetElement(e))
            for a in additionalId:
                selection.append(doc.GetElement(a))

    revit.get_selection().set_to(selection)

