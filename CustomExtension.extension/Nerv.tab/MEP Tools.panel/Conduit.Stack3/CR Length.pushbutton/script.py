import sys, math
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

from Autodesk.Revit.DB import Document,FilteredElementCollector, PerformanceAdviser, \
    FamilySymbol,Transaction,FailureHandlingOptions, CurveElement, Reference
from Autodesk.Revit.UI import TaskDialog, TaskDialogCommonButtons
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB.Electrical import Conduit, ConduitRun
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Map Conduit parameters to Conduit Runs'\
          'Rely on perfect info regard conduit parameters '

from pyrevit.framework import List
from pyrevit import revit, DB, script, forms, UI
import QuestionableMath

def get_selected_elements(doc):
    """API change in Revit 2016 makes old method throw an error"""
    try:
        # Revit 2016
        return [doc.GetElement(id)
                for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    except:
        # old method
        return list(__revit__.ActiveUIDocument.Selection.Elements)

class ConduitSelectionFilter(UI.Selection.ISelectionFilter):
    # standard API override function
    def AllowElement(self, element):
		if element.Category.Name == "Conduits" or element.Category.Name == "Conduit Fittings":
			return True
		else:
			return False

__doc__ = 'Get Conduit Run to see Conduit Run length.'

currentChoice = []
for i in get_selected_elements(doc):
    currentChoice.append(Reference(i))
result = 'Retry'
while result == 'Retry':
    conduitFilter = ConduitSelectionFilter()
    choices = uidoc.Selection
    try:
        conduitRef = choices.PickObjects(ObjectType.Element, conduitFilter, "Pick Conduit", currentChoice)
        currentChoice = conduitRef
        length = 0
        for i in conduitRef:
            conduit = doc.GetElement(i.ElementId)
            if conduit.Category.Name == 'Conduits':
                length += conduit.LookupParameter("Length").AsDouble()
            else:
                angle = conduit.LookupParameter("Angle").AsDouble()
                radius = conduit.LookupParameter("Bend Radius").AsDouble()
                length += radius * angle
                # Backup Length Parameter for fittings, mostly not correct
                # length += conduit.LookupParameter("Conduit Length").AsDouble()
        result = str(TaskDialog.Show("Measure", "Overall Length " + str(QuestionableMath.FeettoInchNotRounded(length)) + " feet", TaskDialogCommonButtons.Retry))
        uidoc.RefreshActiveView()
    except:
        result = "Cancel"
