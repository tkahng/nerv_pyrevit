import sys
import ConfigParser
from os.path import expanduser
# Set system path
home = expanduser("~")
cfgfile = open(home + "\\STVTools.ini", 'r')
config = ConfigParser.ConfigParser()
config.read(home + "\\STVTools.ini")
# Master Path
syspath1 = config.get('SysDir','MasterPackage')
sys.path.append(syspath1)
# Built Path
syspath2 = config.get('SysDir','SecondaryPackage')
sys.path.append(syspath2)

# -*- coding: utf-8 -*-
from pyrevit.framework import List
from pyrevit import revit, DB
import clr
from collections import defaultdict
from pyrevit import script
from pyrevit import forms
import pyrevit
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform, \
    Transaction, Line, ElementTransformUtils,JoinGeometryUtils
from System.Collections.Generic import List
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
import Warnings

__doc__ = 'Fix most of the ...joined but do not intersect warnings.'

def CloseNumber(number1, number2):
    if abs(number1-number2) < 0.005:
        return True
    else:
        return False


utprint = script.get_output()
output = pyrevit.output.get_output()
tab = ' '
# input ---------------------
cate = []
sel_warning = ()
outprint = script.get_output()
path = 'C:\\Users\\loum\\Documents\\Pyscripts\\ClashScripts\\'
# t = Transaction(doc, 'Correct Lines')
# t.Start()
if revit.doc.IsWorkshared:
    warnings = doc.GetWarnings()
# select selected warnings
    for warning in warnings:
        selection = []
        elementId = warning.GetFailingElements()
        additionalId = warning.GetAdditionalElements()
        text = warning.GetDescriptionText()
        t = Transaction(doc, 'Unjoin Elements (STVTools)')

        if 'joined but do not intersect' in text:
            print('Found Warning')
            for e in elementId:
                print(doc.GetElement(e))
                for a in additionalId:
                    print(doc.GetElement(a))
                    t.Start()
                    JoinGeometryUtils.UnjoinGeometry(doc, doc.GetElement(e), doc.GetElement(a))
                    t.Commit()
                    print('Success')

