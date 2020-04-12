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
from Autodesk.Revit.DB import Document, FilteredElementCollector, PerformanceAdviser, FamilySymbol,BuiltInCategory, \
    MEPCurveType, RoutingPreferenceRuleGroupType, RoutingConditions, RoutingPreferenceErrorLevel, RoutingPreferenceRule,\
    PreferredJunctionType,Transaction, BuiltInParameter, XYZ, Line, Connector
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB.Plumbing import PipeType
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit.framework import List
from pyrevit import revit, DB, UI
from pyrevit import forms
import MEPUtilities

class PipeandPipeFittingSelectionFilter(UI.Selection.ISelectionFilter):
	# standard API override function
	def AllowElement(self, element):
		if element.Category.Name == "Pipe Fittings" or element.Category.Name == 'Pipes':
			return True
		else:
			return False

__doc__ = 'Connect Pipes and fittings'

pipeandfittingFilter = PipeandPipeFittingSelectionFilter()

choices = uidoc.Selection

connectorRef = choices.PickObjects(ObjectType.Element, pipeandfittingFilter, "Pick Pipe Fitting")
rotateobjs = []


for i in connectorRef:
    connectors = doc.GetElement(i.ElementId)
    rotateobjs.append(connectors)

rPipes = []
rConnectors = []

for connector in rotateobjs:
    # See if it is a pipe or fitting
    if connector.Category.Name == "Pipe Fittings":
        rConnectors.append(connector)
    else:
        rPipes.append(connector)

# Transaction Start
t = Transaction(doc, 'Connect Pipes and fittings')
t.Start()
MEPUtilities.reconnect(rPipes,rConnectors, 0.1)
t.Commit()


