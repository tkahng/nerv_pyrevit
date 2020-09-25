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
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform, Transaction, JoinGeometryUtils
from System.Collections.Generic import List
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
import Warnings

__doc__ = 'Fix most of the ... is slightly off axis warnings.'

def get_selected_elements(doc):
    """API change in Revit 2016 makes old method throw an error"""
    try:
        # Revit 2016
        return [doc.GetElement(id)
                for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    except:
        # old method
        return list(__revit__.ActiveUIDocument.Selection.Elements)
# t = Transaction(doc, 'Correct Lines')
# t.Start()
allLines = []
allWalls = []
if revit.doc.IsWorkshared:
    warnings = doc.GetWarnings()
# select selected warnings

    for warning in warnings:
        lines = []
        walls = []
        elementId = warning.GetFailingElements()
        additionalId = warning.GetAdditionalElements()
        text = warning.GetDescriptionText()

        if 'lLine is slightly off axis' in text or 'lLine in Sketch is slightly off axis' in text:
            for e in elementId:
                lines.append(doc.GetElement(e))
        elif 'Wall is slightly off axis' in text or 'Curve-Based Family is slightly off axis' in text:
            for e in elementId:
                walls.append(doc.GetElement(e))
        allLines.append(lines)
        allWalls.append(walls)


i = 0
for line in allLines:
    t = Transaction(doc, 'Correct Lines')
    t.Start()
    for l in line:
        #if l.Category.Name == '<Sketch>':
        off_line = l.GeometryCurve
        joined = JoinGeometryUtils.GetJoinedElements(doc, l)
        for j in joined:
            print(j)
        sketchPlane = l.SketchPlane
        correct_line = Warnings.CorrectLineXY(off_line, 0.08)
        print(correct_line)
        try:
            try:
                l.SetSketchPlaneAndCurve(sketchPlane, correct_line)
            except:
                l.SetGeometryCurve(correct_line, True)
        except:
            print('Curve Set Error')
        '''
            if joined:
                for j in joined:
                    JoinGeometryUtils.JoinGeometry(doc, l, j)
            
        except:
            outprint = script.get_output()
            print("Exception raised" + format(outprint.linkify(l.Id)))
            '''
    t.Commit()
for wall in allWalls:
    t = Transaction(doc, 'Correct Walls')
    t.Start()
    for l in wall:
        try:
            off_line = l.Location.Curve
            correct_line = Warnings.CorrectLineXY(off_line, 0.08)
            print(correct_line)
            # l.SetSketchPlaneAndCurve(sketchPlane, correct_line)
            l.Location.Curve = correct_line
        except:
            pass

    t.Commit()
