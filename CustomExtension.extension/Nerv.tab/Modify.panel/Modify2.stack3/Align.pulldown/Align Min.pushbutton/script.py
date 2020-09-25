
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

import System, Selection
from Autodesk.Revit.DB import Document, Transaction, XYZ
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Align text notes to left.'

selection = Selection.get_selected_elements(doc)
t = Transaction(doc, 'Rid Leader')
t.Start()
if selection:
	for i in selection:
		i.HasLeader = False
t.Commit()

selection = Selection.get_selected_elements(doc)
t = Transaction(doc, 'Align Min')
t.Start()
if selection:
		min = selection[0].get_BoundingBox(doc.ActiveView).Min
		location = min.X
		for i in selection:
			eleMin = i.get_BoundingBox(doc.ActiveView).Min.X
			distance = location - eleMin
			i.Location.Move(XYZ(distance, 0 , 0))
t.Commit()

selection = Selection.get_selected_elements(doc)
t = Transaction(doc, 'Enable Leader')
t.Start()
if selection:
	for i in selection:
		i.HasLeader = True
t.Commit()

