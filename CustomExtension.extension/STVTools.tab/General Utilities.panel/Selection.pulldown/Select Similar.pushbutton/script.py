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

# Imports
from pyrevit.framework import List
from pyrevit import revit, DB
import clr
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
clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
from System.Windows.Forms import Application, SendKeys
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

# import user packages
import Selection

Selection.


