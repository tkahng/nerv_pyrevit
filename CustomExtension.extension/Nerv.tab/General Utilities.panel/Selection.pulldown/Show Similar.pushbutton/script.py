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

# Imports
from pyrevit.framework import List
from pyrevit import revit, DB
import clr,re
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
# clr.AddReference("System.Windows.Form")
from Autodesk.Revit.DB import FilteredElementCollector, FilteredWorksetCollector, Element, Transaction, \
    ElementParameterFilter, ParameterValueProvider,ElementId,BuiltInParameter ,FilterStringRule, FilterStringEquals, \
    FilterNumericEquals, FilterIntegerRule, FilterDoubleRule, FilterElementIdRule
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.UI import TaskDialog, TaskDialogCommonButtons, TaskDialogResult
from System.Collections.Generic import List
from pyrevit import script
from pyrevit import forms
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

# import user packages
import Selection

def get_all_parameters(element):
    parameters = element.Parameters
    _param = []
    for param in parameters:
        if param:
            name = param.Definition.Name
            if 'String' in str(param.StorageType):
                try:
                    _param.append(name + ': ' + str(param.AsString()))
                except:
                    _param.append(name + ': ' + str(param.AsValueString()))
            elif 'Interger' in str(param.StorageType):
                _param.append(name + ': ' + str(param.AsInterger()))
            elif 'Double' in str(param.StorageType):
                _param.append(name + ': ' + str(param.AsDouble()))
            elif 'ElementId' in str(param.StorageType):
                _param.append(name + ': ' + str(param.AsElementId().IntegerValue))
    return _param

# get needed params
params = []
selection = []
choices = uidoc.Selection
ref = choices.PickObject(ObjectType.Element, "Pick Element")

selection.append(doc.GetElement(ref.ElementId))
# selection = Selection.get_selected_elements(doc)
# convenience variable for first element in selection
if len(selection):
    s0 = selection[0]
for i in Selection.get_all_parameters(selection[0]).keys():
    params.append(i)
# Select Needed parameter
sel_param_ids = []
sel_params = []
sel_param_strings = forms.SelectFromList.show(params, button_name='Select Params', multiselect=True)
for i in sel_param_strings:
    sel_param_ids.append(Selection.get_all_parameters(selection[0])[i].Id)
for i in sel_param_strings:
    sel_params.append(Selection.get_all_parameters(selection[0])[i])
# process parameters into names and string values
names = []
values = []
for i in sel_param_strings:
    a = re.split(': ', str(i))
    names.append(a[0])
    values.append(a[1])
count = 0
filter = FilteredElementCollector(doc)
outprint = script.get_output()
fRules = []
# create parameter filter by data type
for i in sel_params:
    fRule = ()
    pvp = ParameterValueProvider(sel_param_ids[count])
    if 'String' in str(i.StorageType):
        fnrv = FilterStringEquals()
        fRule = FilterStringRule(pvp, fnrv, values[count], True)
    elif 'Interger' in str(i.StorageType):
        fnrv = FilterNumericEquals()
        fRule = FilterIntegerRule(pvp, fnrv, int(values[count]))
    elif 'Double' in str(i.StorageType):
        fnrv = FilterNumericEquals()
        fRule = FilterDoubleRule(pvp, fnrv, float(values[count]), 0.001)
    elif 'ElementId' in str(i.StorageType):
        fnrv = FilterNumericEquals()
        fRule = FilterElementIdRule(pvp, fnrv, ElementId(int(values[count])))
    fRules.append(fRule)
    count += 1
# Filter all elements based on parameter values selected
paramFilters = ElementParameterFilter(fRules)
ele = filter.WherePasses(paramFilters).ToElements()
elements = []
for i in ele:
    elements.append(i)
count = 1
for i in elements:
    try:
        print(str(count) + '    ' + format(outprint.linkify(i.Id)))
        count += 1
    except:
        pass

