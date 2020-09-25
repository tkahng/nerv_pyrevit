import sys
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

import System, Selection
import System.Threading
import System.Threading.Tasks
from Autodesk.Revit.DB import Document,FilteredElementCollector, PerformanceAdviser, FamilySymbol,Transaction,\
    FailureHandlingOptions, CurveElement
from Autodesk.Revit.UI import TaskDialog
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit.framework import List
from pyrevit import revit, DB
import os
from collections import defaultdict
from pyrevit import script
from pyrevit import forms

__doc__ = 'Get all parameters of the selected element'

selection = Selection.get_selected_elements(doc)

# convenience variable for first element in selection

params = Selection.get_all_parameters_as_dic(selection[0]).keys()
values = Selection.get_all_parameters_as_dic(selection[0]).values()

sel_params = forms.SelectFromList.show(params, button_name='Select Item',
                                        multiselect=True)
for i in selection:
    print(i.Id)
    for p in sel_params:
        selection
print(params)
print(values)
# TODO finish this method
# wait what this is not finished??
