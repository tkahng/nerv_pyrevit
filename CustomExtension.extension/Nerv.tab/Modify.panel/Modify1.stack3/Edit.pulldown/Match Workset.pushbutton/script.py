
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
import Selection
clr.AddReference('System')
from System.Collections.Generic import List
from Autodesk.Revit.DB import Document, FilteredElementCollector, GraphicsStyle, Transaction, BuiltInCategory, RevitLinkInstance,\
    UV, XYZ,SpatialElementBoundaryOptions, CurveArray,ElementId, View, FilteredWorksetCollector, WorksetKind, BuiltInParameter

from pyrevit import revit, DB, forms
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows.Forms

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Report the workset(s) of selected elements and change them into one workset you are going to select.'\

views = FilteredElementCollector(doc).OfClass(View).ToElements()
selection = Selection.get_selected_elements(doc)
t = Transaction(doc, 'Change Workset')
t.Start()
fail = ""
if selection:
    data = {}
    worksets = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()
    occurance = []
    for ele in selection:
        worksetName = ele.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM).AsValueString()
        occurance.append(worksetName)
        workset = None
        for w in worksets:
            if w.Name == worksetName:
                workset = w
        data[worksetName] = workset
    display = []
    for w in data.keys():
        display.append(w + ':' + str(occurance.count(w)))
    sel_workSet = forms.SelectFromList.show(display, button_name='Select Item and workset', multiselect=False)
    selectedWorkset = data[str(re.split(":", sel_workSet)[0])]


    for o in selection:
        if o.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM).AsValueString() != selectedWorkset.Name:
            try:
                o.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM).Set(selectedWorkset.Id.IntegerValue)
            except:
                fail += o.Id.ToString() + ";"

else:
    print("Please Select Item")
t.Commit()
if fail:
    print("Failed to change " + fail)
