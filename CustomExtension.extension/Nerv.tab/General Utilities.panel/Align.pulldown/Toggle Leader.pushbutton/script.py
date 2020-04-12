
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

__doc__ = 'Switch the tag(s) leader on/off'

selection = Selection.get_selected_elements(doc)
t = Transaction(doc, 'Toggle Leader')
t.Start()
if selection:
	for i in selection:
		if i.HasLeader:
			i.HasLeader = False
		else:
			i.HasLeader = True
t.Commit()


