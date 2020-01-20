from pyrevit.framework import List
from pyrevit import revit, DB
import clr, sys, re, os, imp
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
# clr.AddReference("System.Windows.Form")

from Autodesk.Revit.DB import FilteredElementCollector, FilteredWorksetCollector, RevitLinkType,BuiltInParameter,\
    Workset,WorksetKind
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform, Transaction,FamilySymbol
from System.Collections.Generic import List
from pyrevit import script
from pyrevit import forms
import pyrevit
clr. AddReferenceByPartialName('PresentationCore')
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

# TODO Create a 3D View
# TODO: Graphic Override based on elementID
# TODO: Cancel all Graphic Overide
