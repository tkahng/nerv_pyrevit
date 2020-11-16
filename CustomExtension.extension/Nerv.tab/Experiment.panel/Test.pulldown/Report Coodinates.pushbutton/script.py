
import sys, clr
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
import Selection
clr.AddReference('System')
from Autodesk.Revit.DB import Document, FilteredElementCollector, GraphicsStyle, Transaction, BuiltInCategory,\
    RevitLinkInstance, UV, XYZ, SpatialElementBoundaryOptions, CurveArray, ElementId, View, RevitLinkType, WorksetTable,\
    Workset, FilteredWorksetCollector, WorksetKind, RevitLinkType, RevitLinkInstance, View3D, ViewType,ElementClassFilter,\
    ViewFamilyType, ViewFamily, BuiltInParameter, IndependentTag, Reference, TagMode, TagOrientation
from System import EventHandler, Uri
from Autodesk.Revit.UI.Events import ViewActivatedEventArgs, ViewActivatingEventArgs
from pyrevit import revit, DB, forms
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows.Forms
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit import framework
from pyrevit import script
from pyrevit import DB, UI
import datetime, os
from pyrevit import HOST_APP, framework
selection = [doc.GetElement(id)
            for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]


if len(selection) > 0:
    el = selection[0]
    loc = el.Location.ToString
    if 'Curve' in str(loc):
        Epnt = el.Location.Curve.GetEndPoint(1)
        Spnt = el.Location.Curve.GetEndPoint(0)
        x = (Epnt.X + Spnt.X) / 2.0
        y = (Epnt.Y + Spnt.Y) / 2.0
        z = (Epnt.Z + Spnt.Z) / 2.0
        pnt = XYZ(x, y, z)
    elif 'Point' in str(loc):
        pnt = el.Location.Point
    else:
        pnt = 'Failed to get anything'
    print(pnt)
else:
    print('Please select element first')

