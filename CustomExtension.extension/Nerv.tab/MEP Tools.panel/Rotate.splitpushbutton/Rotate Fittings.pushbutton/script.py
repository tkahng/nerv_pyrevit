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

import math
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

def disconnect(curve):
	connectors = curve.ConnectorManager.Connectors
	for conn in connectors:
		if conn.IsConnected:
			for c in conn.AllRefs:
				if conn.IsConnectedTo(c):
					# conns[0] = conn
					# conns[1] = c
					conn.DisconnectFrom(c)

class PipeSelectionFilter(UI.Selection.ISelectionFilter):
    # standard API override function
    def AllowElement(self, element):
		if element.Category.Name == "Pipes":
			return True
		else:
			return False

class PipeandPipeFittingSelectionFilter(UI.Selection.ISelectionFilter):
	# standard API override function
	def AllowElement(self, element):
		if element.Category.Name == "Pipe Fittings" or element.Category.Name == 'Pipes':
			return True
		else:
			return False

class PipeFittingSelectionFilter(UI.Selection.ISelectionFilter):
	# standard API override function
	def AllowElement(self, element):
		if element.Category.Name == "Pipe Fittings":
			return True
		else:
			return False

__doc__ = 'Rotate Pipe Fittings connected to pipe'\
          'Click the tool, select the pipe and then the fitting ' \
          'Type in a number you want to rotate and you are good to go,'\
          'Can Take negative Values'

pipFilter = PipeSelectionFilter()
# fittingFilter = PipeFittingSelectionFilter()
pipeandfittingFilter = PipeandPipeFittingSelectionFilter()

choices = uidoc.Selection
pipeRef = choices.PickObject(ObjectType.Element, pipFilter, "Pick Pipe")
connectorRef = choices.PickObjects(ObjectType.Element, pipeandfittingFilter, "Pick Pipe Fitting")
rotateobjs = []
pipe = doc.GetElement(pipeRef.ElementId)

for i in connectorRef:
    connectors = doc.GetElement(i.ElementId)
    rotateobjs.append(connectors)

angleInput = str(forms.GetValueWindow.show(None,
        value_type='string',
        default=str(0.00),
        prompt='Please Enter angle',
        title='Angle'))
angle = (float(angleInput)*math.pi)/180

rPipes = []
rConnectors = []
line = ()
for connector in rotateobjs:
    # Create a center line for rotation
    pointOne = pipe.Location.Curve.GetEndPoint(0)
    pointTwo = pipe.Location.Curve.GetEndPoint(1)
    line = DB.Line.CreateBound(pointOne, pointTwo)
    # See if it is a pipe or fitting
    if connector.Category.Name == "Pipe Fittings":
        rConnectors.append(connector)
    else:
        rPipes.append(connector)

# Transaction Start
t = Transaction(doc, 'Rotate Fittings')
t.Start()
for connector in rPipes:
    disconnect(connector)
    pointStart = connector.Location.Curve.GetEndPoint(0)
    pointFinish = connector.Location.Curve.GetEndPoint(1)
    ductloc = connector.Location
    ductloc.Rotate(line, angle)

for connector in rConnectors:
    primary = ()
    inn = [connector,pipe]
    connectors = inn[0].MEPModel.ConnectorManager.Connectors
    for c in connectors:
        if c.GetMEPConnectorInfo().IsPrimary:
            primary = c
            break
        primary = c
    loc = inn[0].Location
    ductloc = inn[1].Location
    center = primary.Origin
    disconnect(inn[1])
    try:
        disconnect(inn[0])
    except:
        pass
    ductloc.Rotate(line, angle)
    success = loc.Rotate(line, angle)

# Get and sort Connector Onjs
pipeConnectors = []
connectorC = []
rPipes.append(pipe)
for i in rPipes:
    ppConnectors = i.ConnectorManager.Connectors
    for pp in ppConnectors:
        pipeConnectors.append(pp)
        #print(pp)
for connectorSets in rConnectors:
    cs = connectorSets.MEPModel.ConnectorManager.Connectors
    for a in cs:
        connectorC.append(a)
        #print(a)
for ca in pipeConnectors:
    pipeLoc = ca.Origin
    for cc in connectorC:
        connectorLoc = cc.Origin
        if pipeLoc.DistanceTo(connectorLoc) < 0.1:
            try:
                ca.ConnectTo(cc)

            except:
                pass
t.Commit()


