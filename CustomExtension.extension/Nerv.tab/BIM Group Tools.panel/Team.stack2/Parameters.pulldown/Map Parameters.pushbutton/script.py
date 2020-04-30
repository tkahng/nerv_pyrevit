# import packages
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
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Map the Value of one parameter to another parameter.'\
          'Please Select the element(s) you wish to map first.'\

from Autodesk.Revit.UI import TaskDialog
from pyrevit import forms
from Autodesk.Revit.DB import Transaction, StorageType
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
import Selection

def alert(msg):
    TaskDialog.Show('CHENGYING GONG', msg)

selection = Selection.get_selected_elements(doc)
# convenience variable for first element in selection
if len(selection):
    s0 = selection[0]

selection = Selection.get_selected_elements(doc)
output = []
value1 = []
value2 = []
id = []
# Input Parameter Name
parameter1 = forms.ask_for_string(default='', prompt='Please input Original Parameter', title='Parameter Mapper')
parameter2 = forms.ask_for_string(default='', prompt='Please input Destination Parameter', title='Parameter Mapper')


# Transaction Start

for x in selection:
    t = Transaction(doc, "Map Parameters")
    t.Start()
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
                try:
                    v2.Set(str(v1.AsInteger()))
                    output = "integer"
                except:
                    print(x.Id.IntegerValue)
            elif v1.StorageType == StorageType.String:
                try:
                    v2.Set(str(v1.AsString()))
                    output = "string"
                except:
                    print(x.Id.IntegerValue)
            elif v1.StorageType == StorageType.Double:
                try:
                    v2.Set(str(v1.AsDouble()))
                    output = "double"
                except:
                    print(x.Id.IntegerValue)
            else:
                output = "Error"

            value1.append(v1)
            value2.append(v2)
        else:
            output = alert("The two parameters are not the same type, try again.")
            pass
    t.Commit()


