
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
from System.Collections.Generic import List
from Autodesk.Revit.DB import Document, FilteredElementCollector, GraphicsStyle, Transaction, BuiltInCategory, \
    RevitLinkInstance, UV, XYZ,SpatialElementBoundaryOptions, CurveArray,ElementId, View, RevitLinkType
from pyrevit import script
from pyrevit import revit, DB, forms
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows.Forms
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Report the Element ID of the selected element(s).' \
          'Please select element(s) first.'

views = FilteredElementCollector(doc).OfClass(View).ToElements()

output = script.get_output()
selection = Selection.get_selected_elements(doc)
for a in selection:
    print(format(output.linkify(a.Id)))