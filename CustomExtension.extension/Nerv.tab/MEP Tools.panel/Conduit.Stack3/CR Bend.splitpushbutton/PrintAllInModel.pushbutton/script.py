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
    FamilySymbol,Transaction,FailureHandlingOptions, CurveElement, Reference, BuiltInCategory, Connector, MEPSystem
from Autodesk.Revit.UI import TaskDialog, TaskDialogCommonButtons
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB.Electrical import Conduit, ConduitRun, CableTrayConduitBase
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

from pyrevit.framework import List
from pyrevit import revit, DB, script, forms, UI
import QuestionableMath

def get_all_string_parameters(element):
    parameters = element.Parameters
    _param = []
    for param in parameters:
        if param:
            name = param.Definition.Name
            if 'String' in str(param.StorageType):
                try:
                    _param.append(name)
                except:
                    _param.append(name)
    return _param

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


outprint = script.get_output()
__doc__ = 'Get All Conduit Runs to see Conduit Run Overall Angle'

# Collect all fitting Element in the Model
conduitFittings = FilteredElementCollector(doc).\
    OfCategory(BuiltInCategory.OST_ConduitFitting).\
    WhereElementIsNotElementType().ToElements()
fittingRunIds = {}
runs = []
for i in conduitFittings:
    connectorsSet = i.MEPModel.ConnectorManager.Connectors
    for c in connectorsSet:
        ccs = c.AllRefs
        for a in ccs:
            runId = ()
            if a.Owner.Category.Name == 'Conduits' and a.Owner.RunId and a.Owner.RunId.IntegerValue > 0:
                runId = a.Owner.RunId
                fittingRunIds[i] = runId
            else:
                pass
            if not runId in runs and runId:
                runs.append(runId)

# Process Conduit Run Total Angle
for i in runs:
    degree = 0.0
    conns = 'Connctors: '
    for con in fittingRunIds.keys():
        if fittingRunIds[con] == i:
            conns += format(outprint.linkify(con.Id))
            try:
                degree += (con.LookupParameter("Angle").AsDouble()/math.pi *180.0)
            except:
                conns +=' Angle Error'

    # Check if the run is under 360 degrees
    if degree < 359.9:
        print('Run:' + format(outprint.linkify(i)) + " Bend in Total: " + str(degree) + " degrees.")
        print(conns)
    else:
        print('**Run:' + format(outprint.linkify(i)) + " Bend in Total: " + str(degree) + " degrees.")
        print(conns)
    print('----------------------------------')
    # result = str(TaskDialog.Show("Measure", "Overall degree " + str(degree) + " degree",
                                 # TaskDialogCommonButtons.Retry))
    uidoc.RefreshActiveView()


