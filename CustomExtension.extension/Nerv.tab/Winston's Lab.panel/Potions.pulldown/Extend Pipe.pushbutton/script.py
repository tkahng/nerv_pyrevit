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

class PipeSelectionFilter(UI.Selection.ISelectionFilter):
    # standard API override function
    def AllowElement(self, element):
		if element.Category.Name == "Pipes":
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

__doc__ = 'Extend pipe.'

pipFilter = PipeSelectionFilter()
choices = uidoc.Selection
pipeRef = choices.PickObject(ObjectType.Element, pipFilter, "Pick Pipe")
pipe = doc.GetElement(pipeRef.ElementId)


t = Transaction(doc, 'Extend Pipe')
t.Start()

pointOne = pipe.Location.Curve.GetEndPoint(0)
pointTwo = pipe.Location.Curve.GetEndPoint(1)


t.Commit()




