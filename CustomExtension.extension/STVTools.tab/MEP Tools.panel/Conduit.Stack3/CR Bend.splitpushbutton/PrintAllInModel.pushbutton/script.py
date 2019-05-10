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
    FamilySymbol,Transaction,FailureHandlingOptions, CurveElement, Reference, BuiltInCategory
from Autodesk.Revit.UI import TaskDialog, TaskDialogCommonButtons
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB.Electrical import Conduit, ConduitRun, CableTrayConduitBase
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
__doc__ = 'Map Conduit parameters to Conduit Runs'\
          'Rely on perfect info regard conduit parameters '
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


def nextElements(elem):
    listout = []
    if elem.GetType() == Connector:
        conn = elem
        for c in conn.AllRefs:
            if c.Owner.Id.Equals(elem.Owner.Id):
                continue
            elif isinstance(c.Owner, MEPSystem):
                continue
            else:
                newelem = c.Owner
            listout.append(newelem)
        return listout
    try:
        connectors = elem.ConnectorManager.Connectors
    except:
        connectors = elem.MEPModel.ConnectorManager.Connectors
    for conn in connectors:
        for c in conn.AllRefs:
            if c.Owner.Id.Equals(elem.Id):
                continue
            elif isinstance(c.Owner, MEPSystem):
                continue
            elif c.Owner.Id.Equals(ownerId):
                continue
            else:
                newelem = c.Owner
            listout.append(newelem)
    return listout


def collector(elem):
    cont = 0
    elements = nextElements(elem)
    for x in elements:
        if x.Id in lookup:
            cont += 1
        else:
            item = doc.GetElement(x.Id)

            lookup[x.Id] = item
            collector(x)
    if cont == len(elements):
        return elem


listout = []
for x in connector:
    lookup = collections.OrderedDict()
    if x.GetType() == Connector:
        ownerId = x.Owner.Id
    else:
        ownerId = x.Id
    collector(x)
    listout.append(lookup.Values)

# Assign your output to the OUT variable.
if toggle:
    OUT = lookup.Values
else:
    OUT = listout


'''
runs = FilteredElementCollector(doc).OfClass(ConduitRun).ToElements()
for i in runs:
    print(i.Id)
'''
__doc__ = 'Get Conduit Run to see Conduit Run Overall Angle'
currentChoice = []
conduits = FilteredElementCollector(doc).OfClass(CableTrayConduitBase).WhereElementIsNotElementType().ToElements()
for i in conduits:
    print(i)
runs = []
outprint = script.get_output()
for conduit in conduits:
    run = doc.GetElement(conduit.MEPModel.ElectricalSystems.RunId)
    if not run in runs:
        runs.append(run)
for i in runs:
    degree = 0.0
    for con in conduits:

        if doc.GetElement(con.MEPModel.RunId) == i:
            print(con)
            if con.Category.Name == 'Conduit Fittings':
                degree += (con.LookupParameter("Angle").AsDouble()/math.pi *180.0)
            else:
                degree += 0.0
    print(format(outprint.linkify(i.Id)) + " Bend in Total: " + str(degree) + " degrees.")
    # result = str(TaskDialog.Show("Measure", "Overall degree " + str(degree) + " degree",
                                 # TaskDialogCommonButtons.Retry))
    uidoc.RefreshActiveView()


