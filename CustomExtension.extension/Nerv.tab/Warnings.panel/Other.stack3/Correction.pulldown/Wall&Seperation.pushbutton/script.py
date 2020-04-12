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
    Transaction, Line, ElementTransformUtils
from System.Collections.Generic import List
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
import Warnings

__doc__ = 'Fix most of the wall and a room separation line overlap warnings.'\

def CloseNumber(number1, number2):
    if abs(number1-number2) < 0.005:
        return True
    else:
        return False

def VectorCheck(line, wall):
    wall_start = wall.Location.Curve.GetEndPoint(0)
    wall_end = wall.Location.Curve.GetEndPoint(1)
    line_start = line.GeometryCurve.GetEndPoint(0)
    line_end = line.GeometryCurve.GetEndPoint(1)
    lineVector_X = line_start.X - line_end.X
    lineVector_Y = line_start.Y - line_end.Y
    wallVector_X = wall_start.X - wall_end.X
    wallVector_Y = wall_start.Y - wall_end.Y
    print(lineVector_X * wallVector_X)
    print(lineVector_Y * wallVector_Y)
    if lineVector_X * wallVector_X < -0.005 or lineVector_Y * wallVector_Y < -0.005:
        return False
    else:
        return True

def get_selected_elements(doc):
    """API change in Revit 2016 makes old method throw an error"""
    try:
        # Revit 2016
        return [doc.GetElement(id)
                for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    except:
        # old method
        return list(__revit__.ActiveUIDocument.Selection.Elements)

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y
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
        if 'wall and a room separation' in text:
            for e in elementId:
                selection.append(doc.GetElement(e))
            for a in additionalId:
                selection.append(doc.GetElement(a))
            # Setups
            loc = ()
            wall_start = ()
            wall_end = ()
            line_loc = ()
            line_start = ()
            line_end = ()
            line = ()
            wall = ()

            try:
                for i in selection:
                    print(i)
                    if i.Category.Name == 'Walls':
                        wall = i
                    else:
                        line = i
                # TODO: Identify the vectors
                loc = wall.Location.Curve
                wall_start = loc.GetEndPoint(0)
                wall_end = loc.GetEndPoint(1)
                print(wall_start, wall_end)
                vector_Check = VectorCheck(line,wall)
                print(vector_Check)
                if vector_Check == True:
                    line_start = line.GeometryCurve.GetEndPoint(0)
                    line_end = line.GeometryCurve.GetEndPoint(1)
                else:
                    line_end = line.GeometryCurve.GetEndPoint(0)
                    line_start = line.GeometryCurve.GetEndPoint(1)
                print(line_start, line_end)

                # Try to do the projection
                proj_start = line.GeometryCurve.Project(wall_start).XYZPoint
                proj_end = line.GeometryCurve.Project(wall_end).XYZPoint
                print(proj_start, proj_end)
# Scenario 1
                if CloseNumber(proj_start.X, line_start.X) \
                        and CloseNumber(proj_start.Y, line_start.Y)\
                        and CloseNumber(proj_end.X, line_end.X)\
                        and CloseNumber(proj_end.Y, line_end.Y):
                    print('1')
                    t = Transaction(doc, 'Correct Lines 1')
                    t.Start()
                    doc.Delete(line.Id)
                    print('Deletion of excess successful')
                    t.Commit()
# Scenario 2
                elif (CloseNumber(proj_start.X, line_start.X) \
                        and CloseNumber(proj_start.Y, line_start.Y))\
                        and (not CloseNumber(proj_end.X, line_end.X) \
                        or not CloseNumber(proj_end.Y, line_end.Y)):
                    print('2')
                    t = Transaction(doc, 'Correct Lines 2')
                    t.Start()
                    try:
                        newLine = Line.CreateBound(proj_end, line_end)
                        line.SetGeometryCurve(newLine, True)
                        print('Correction Successful')
                    except:
                        print("Wall" + format(outprint.linkify(wall.Id)))
                        print("Line" + format(outprint.linkify(line.Id)))
                    t.Commit()
# Scenario 4
                elif (CloseNumber(proj_end.X, line_end.X) \
                     and CloseNumber(proj_end.Y, line_end.Y)) \
                     and (not CloseNumber(proj_start.X, line_start.X) \
                     or not CloseNumber(proj_start.Y, line_start.Y)):
                    print('3')
                    t = Transaction(doc, 'Correct Lines 3')
                    t.Start()
                    try:
                        newLine = Line.CreateBound(proj_start, line_start)
                        line.SetGeometryCurve(newLine, True)
                        print('Correction Successful')
                    except:
                        print("Wall" + format(outprint.linkify(wall.Id)))
                        print("Line" + format(outprint.linkify(line.Id)))
                    t.Commit()
# Scenario 4
                elif (not CloseNumber(proj_start.X, line_start.X) \
                     or not CloseNumber(proj_start.Y, line_start.Y)) \
                     and (not CloseNumber(proj_end.X, line_end.X) \
                     or not CloseNumber(proj_end.Y, line_end.Y)):
                    print('4')
                    t = Transaction(doc, 'Correct Lines 4')
                    t.Start()
                    try:
                        newLine1 = Line.CreateBound(proj_start, line_start)
                        line.SetGeometryCurve(newLine1, True)
                    except:
                        print('Fail 411')

                    newLine2 = Line.CreateBound(proj_end, line_end)
                    line2 = ElementTransformUtils.CopyElement(doc, line.Id, XYZ(0.1, 0.1, 0.1))
                    doc.GetElement(line2[0]).SetGeometryCurve(newLine2, True)
                    print('Correction Successful')
                    '''
                    except:
                        print('Fail 412')
                        # print("Wall" + format(outprint.linkify(wall.Id)))
                        # print("Line" + format(outprint.linkify(line.Id)))
                    '''
                    t.Commit()
                else:
                    print('Error 5')
                print("---------------")
            except:
                print('Error 6')
# t.Commit()
