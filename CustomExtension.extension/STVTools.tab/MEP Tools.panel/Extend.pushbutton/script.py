import math
from Autodesk.Revit.DB import Document, FilteredElementCollector, PerformanceAdviser, FamilySymbol,BuiltInCategory, \
    MEPCurveType, RoutingPreferenceRuleGroupType, RoutingConditions, RoutingPreferenceErrorLevel, RoutingPreferenceRule,\
    PreferredJunctionType,Transaction, BuiltInParameter, XYZ, Line, Connector, Plane
from Autodesk.Revit.UI.Selection import ObjectType, ObjectSnapTypes
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

__doc__ = 'Rotate Pipe Fittings connected to pipe'\
          'Click the tool, select the pipe and then the fitting ' \
          'Type in a number you want to rotate and you are good to go,'\
          'Can Take negative Values'
pipFilter = PipeSelectionFilter()
fittingFilter = PipeFittingSelectionFilter()
choices = uidoc.Selection
pipeRef = choices.PickObject(ObjectType.Element, pipFilter, "Pick Pipe")
pointRef = choices.PickPoint(ObjectSnapTypes.Endpoints, "Pick End Point")
# extendRef = choices.PickObjects(ObjectType.Element, fittingFilter, "Pick Pipe Fitting")
pipe = doc.GetElement(pipeRef.ElementId)
# extend = doc.GetElement(extendRef.ElementId)

pointOne = pipe.Location.Curve.GetEndPoint(0)
pointTwo = pipe.Location.Curve.GetEndPoint(1)

line1 = pointRef.DistanceTo(pointOne)
line2 = pointRef.DistanceTo(pointTwo)
if line1 >= line2:
    pointEnd = pointTwo
    normal = pointTwo.Subtract(pointOne)
else:
    pointEnd = pointOne
    normal = pointTwo.Subtract(pointTwo)
plane = Plane.CreateByNormalAndOrigion(normal, pointEnd)

t = Transaction(doc, 'Extend Pipes')
t.Start()


t.Commit()


