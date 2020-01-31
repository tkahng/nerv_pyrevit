
import sys, clr, re
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
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


from Autodesk.Revit.UI import TaskDialog
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit.framework import List
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

from Autodesk.Revit.DB import Transaction, StorageType

def get_selected_elements(doc):
    """API change in Revit 2016 makes old method throw an error"""
    try:
        # Revit 2016
        return [doc.GetElement(id)
                for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    except:
        # old method
        return list(__revit__.ActiveUIDocument.Selection.Elements)

def alert(msg):
    TaskDialog.Show('CHENGYING GONG', msg)

selection = get_selected_elements(doc)
# convenience variable for first element in selection
if len(selection):
    s0 = selection[0]

selection = get_selected_elements(doc)
output = []
value1 = []
value2 = []
parameter1 = forms.ask_for_string(default='', prompt='Please input Original Parameter', title='Parameter Mapper')
parameter2 = forms.ask_for_string(default='', prompt='Please input Destination Parameter', title='Parameter Mapper')
t = Transaction(doc, "Map Parameters")

# Transaction Start
t.Start()
for x in selection:
    v1 = x.LookupParameter(parameter1)
    v2 = x.LookupParameter(parameter2)
    if v1 is None:
        output = alert("The first input is not a valid parameter.")
        pass
    elif v2 is None:
        output = alert("The second input is not a valid parameter.")
        pass
    else:
        if v1.StorageType == v2.StorageType:
            if v1.StorageType == StorageType.Integer:
                v2.Set(str(v1.AsInteger()))
                output = "integer"
            elif v1.StorageType == StorageType.String:
                v2.Set(str(v1.AsString()))
                output = "string"
            elif v1.StorageType == StorageType.Double:
                v2.Set(str(v1.AsDouble()))
                output = "double"
            else:
                output = "Error"

            value1.append(v1)
            value2.append(v2)
        else:
            output = alert("The two parameters are not the same type, try again.")
            pass
t.Commit()


