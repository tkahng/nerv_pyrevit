
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
views = FilteredElementCollector(doc).OfClass(View).ToElements()
selection = Selection.get_selected_elements(doc)
t = Transaction(doc, 'Change Workset')
t.Start()
fail = ""
if selection:
    data = {}
    worksets = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()
    for ele in selection:
        name = ele.Category.Name
        worksetName = ele.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM).AsValueString()
        workset = None
        for w in worksets:
            if w.Name == worksetName:
                workset = w
        data[worksetName] = workset
    sel_workSet = forms.SelectFromList.show(data.keys(), button_name='Select Item and workset', multiselect=False)
    selectedWorkset = data[str(sel_workSet)]

    for o in selection:
        try:
            o.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM).Set(selectedWorkset.Id.IntegerValue)
        except:
            fail += o.Id.ToString() + ";"
else:
    print("Please Select Item")
t.Commit()
if fail:
    print("Failed to change " + fail)
