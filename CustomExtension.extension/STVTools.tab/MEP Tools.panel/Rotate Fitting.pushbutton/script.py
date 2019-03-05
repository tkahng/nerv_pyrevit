import clr, math
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import Document, FilteredElementCollector, PerformanceAdviser, FamilySymbol,BuiltInCategory, \
    MEPCurveType, RoutingPreferenceRuleGroupType, RoutingConditions, RoutingPreferenceErrorLevel, RoutingPreferenceRule,\
    PreferredJunctionType,Transaction, BuiltInParameter, XYZ, Line
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB.Plumbing import PipeType
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit.framework import List
from pyrevit import revit, DB
import os
from collections import defaultdict
from pyrevit import script
from pyrevit import forms
__doc__ = 'Switch Elbow Preference of selected Pipe'\
          'You can either select the pipe you want to switch ' \
          'or pick from list'
choices = uidoc.Selection
pipeRef = choices.PickObject(ObjectType.Element, "Pick Pipe")
connectorRef = choices.PickObject(ObjectType.Element, "Pick Pipe Fitting")
pipe = doc.GetElement(pipeRef.ElementId)
connector = doc.GetElement(pipeRef.ElementId)
print(pipeRef.ElementId)
print(connectorRef.ElementId)
conns = []
def disconnect(curve, list):

	connectors = curve.ConnectorManager.Connectors
	for conn in connectors:
		if conn.IsConnected:
			for c in conn.AllRefs:
				if conn.IsConnectedTo(c):
					list.append(conn)
					list.append(c)
					conn.DisconnectFrom(c)

angleInput = str(forms.GetValueWindow.show(None,
        value_type='string',
        default=str(0.00),
        prompt='Please Enter angle',
        title='Angle'))
angle = float(angleInput)
t = Transaction(doc, 'Rotate Fitting')
t.Start()
primary = ()
connectors = connector.ConnectorManager.Connectors
print(connectors)
for c in connectors:
	if c.GetMEPConnectorInfo().IsPrimary:
		primary = c
		break
	primary = c
print(primary)
loc = connector.Location
ductloc = pipe.Location
center = primary.CoordinateSystem.BasisZ
centerrot = XYZ(center.X,center.Y,center.Z)
line = Line.CreateUnbound(primary.Origin,center)
disconnect(connector, conns)
ductloc.Rotate(line,angle)
loc.Rotate(line,angle)
print(conns[0])
print(conns[1])
conns[0].ConnectTo(conns[1])

t.Commit()


