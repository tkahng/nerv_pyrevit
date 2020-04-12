
from Autodesk.Revit.DB import Document, MEPCurveType, Reference, Options
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.UI import TaskDialog, TaskDialogCommonButtons
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit import revit, DB, UI


class PipeandFittingsSelectionFilter(UI.Selection.ISelectionFilter):
    # standard API override function
    def AllowElement(self, element):
		if element.Category.Name == "Pipes" or element.Category.Name == "Pipe Fittings":
			return True
		else:
			return False

def get_selected_elements(doc):
    """API change in Revit 2016 makes old method throw an error"""
    try:
        # Revit 2016
        return [doc.GetElement(id)
                for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    except:
        # old method
        return list(__revit__.ActiveUIDocument.Selection.Elements)


def FeettoInch(number):
    feet = int(number)
    inch = int((number - feet) * 12)

    result = str(feet) + '\' ' + str(inch) + '\"'
    return result
__doc__ = 'Measure Pip Element Length '\
          'this Ignore fitting length is estimated '

currentChoice = []
for i in get_selected_elements(doc):
    currentChoice.append(Reference(i))
result = 'Retry'
while result == 'Retry':
    pipFilter = PipeandFittingsSelectionFilter()
    choices = uidoc.Selection
    try:
        pipeRef = choices.PickObjects(ObjectType.Element, pipFilter, "Pick Pipe", currentChoice)
        currentChoice = pipeRef
        overallLength = 0.00
        for i in pipeRef:
            pipe = doc.GetElement(i.ElementId)
            # Pipe
            try:
                overallLength += pipe.Location.Curve.Length
            except:
                overallLength += pipe.GetOriginalGeometry(Options()).GetBoundingBox().Max.DistanceTo(pipe.GetOriginalGeometry(Options()).GetBoundingBox().Min)
        result = str(TaskDialog.Show("Measure", "Overall Length " + str(FeettoInch(overallLength)) + " feet", TaskDialogCommonButtons.Retry))
        uidoc.RefreshActiveView()
    except:
        result = "Cancel"




